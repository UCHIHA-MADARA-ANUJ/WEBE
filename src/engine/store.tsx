import React, {
  createContext,
  useCallback,
  useContext,
  useEffect,
  useMemo,
  useRef,
  useState,
} from 'react';
import { NODES, NODE_BY_ID, neighboursOf } from '../content/graph';
import { classify, computeFeatures, contextFrom } from './classify';
import {
  buildChapters,
  buildManifest,
  buildTrail,
  decideParadigm,
  relatedTo,
} from './decide';
import {
  clearGenome,
  loadGenome,
  logVerdict,
  mutateGenome,
  orderFor,
  registerAction,
  registerInterest,
  registerVisit,
  registerVisitNode,
  saveGenome,
} from './genome';
import {
  emptySignals,
  type ActionId,
  type Classification,
  type FeatureId,
  type Genome,
  type LogEntry,
  type Manifest,
  type ParadigmId,
  type SessionSignals,
} from './types';

export interface PrimaryAction {
  label: string;
  nodeId: string | null;
  kind: 'trail' | 'related' | 'compare' | 'explore' | 'resume';
}

export interface EngineApi {
  genome: Genome;
  signals: SessionSignals;
  classification: Classification;
  paradigm: ParadigmId;
  pinned: boolean;
  manifest: Manifest | null;
  log: LogEntry[];
  features: Record<FeatureId, boolean>;
  trail: string[];
  chapters: { family: string; node: string }[];
  promoted: string[];
  primary: PrimaryAction;
  order: string[];
  cold: boolean;

  openNode: (id: string) => void;
  closeNode: () => void;
  followEdge: (id: string) => void;
  noteScroll: (pixels: number, velocity: number, dtMs: number) => void;
  notePointer: (pixels: number, dtMs: number) => void;
  noteSearch: (q: string) => void;
  noteFilter: (tag: string) => void;
  noteCommand: (cmd: string) => void;
  note: (action: ActionId) => void;
  setParadigm: (p: ParadigmId, pinned?: boolean) => void;
  mutate: () => void;
  reset: () => void;
  related: (id: string) => { id: string; kind: string }[];
}

const EngineContext = createContext<EngineApi | null>(null);

/** Test bus — lets the headless harness drive the real engine. */
export const testBus: { api: EngineApi | null } = { api: null };

const isNeighbour = (a: string, b: string) => neighboursOf(a).includes(b);

/** how many observations before the engine is allowed to restructure */
const MIN_EVIDENCE = 6;
/** minimum seconds between two automatic restructurings */
const MIN_SWITCH_GAP = 9;

export function EngineProvider({ children }: { children: React.ReactNode }) {
  const [genome, setGenome] = useState<Genome>(() => loadGenome());
  const [paradigm, setParadigmState] = useState<ParadigmId>('constellation');
  const [pinned, setPinned] = useState(false);
  const [manifest, setManifest] = useState<Manifest | null>(null);
  const [tick, setTick] = useState(0);
  const [cold, setCold] = useState(true);

  const signalsRef = useRef<SessionSignals>(emptySignals());
  const lastSwitchRef = useRef(0);
  const firstOpenRef = useRef(false);
  const bootedRef = useRef(false);

  const persist = useCallback((g: Genome) => {
    saveGenome(g);
    return g;
  }, []);

  /* ---------------------------------------------------------------- */
  /* boot: register the visit, restore procedural state                 */
  /* ---------------------------------------------------------------- */
  useEffect(() => {
    const loaded = loadGenome();
    const isReturning = loaded.visits > 0;
    const restoredParadigm: ParadigmId = isReturning ? loaded.paradigm : 'constellation';
    const next = registerVisit(loaded, loaded.archetype, 0.5);
    next.paradigm = restoredParadigm;
    next.pinned = false;
    persist(next);
    setGenome(next);
    setParadigmState(restoredParadigm);
    bootedRef.current = true;
    // eslint-disable-next-line react-hooks/exhaustive-deps
  }, []);

  /* ---------------------------------------------------------------- */
  /* heartbeat: age the session, accumulate focus time                  */
  /* ---------------------------------------------------------------- */
  useEffect(() => {
    const id = window.setInterval(() => {
      const s = signalsRef.current;
      s.elapsedMs = Date.now() - s.startedAt;
      if (s.focusOpen && s.lastNode) s.focusMs += 500;
    }, 500);
    return () => window.clearInterval(id);
  }, []);

  /* ---------------------------------------------------------------- */
  /* classification (derived, cheap)                                   */
  /* ---------------------------------------------------------------- */
  const classification = useMemo(() => {
    const s = signalsRef.current;
    const features = computeFeatures(s, isNeighbour);
    const c = classify(features, contextFrom(s));
    c.evidence =
      s.opens +
      Object.values(s.actions).reduce((a, b) => a + b, 0) +
      Math.floor(s.scrollPixels / 800);
    return c;
    // eslint-disable-next-line react-hooks/exhaustive-deps
  }, [tick]);

  /* ---------------------------------------------------------------- */
  /* the decision loop                                                 */
  /* ---------------------------------------------------------------- */
  useEffect(() => {
    if (!bootedRef.current) return;
    const s = signalsRef.current;
    if (s.opens === 0 && s.scrollPixels < 200) return;
    if (classification.evidence < MIN_EVIDENCE) return;
    if (pinned) return;

    // never restructure on the strength of one or two gestures
    const gestures = s.actions.search + s.actions.filter + s.actions.command;
    if (s.opens < 3 && gestures < 3) return;
    if (s.elapsedMs < 2500) return;
    if (!firstOpenRef.current) {
      // the first interaction always leaves the cold state
      firstOpenRef.current = true;
      setCold(false);
    }

    const decision = decideParadigm(classification, paradigm, pinned);
    if (!decision.changed) return;

    const now = Date.now();
    if (now - lastSwitchRef.current < MIN_SWITCH_GAP * 1000) return;
    lastSwitchRef.current = now;

    const previous = paradigm;

    setParadigmState(decision.paradigm);
    setManifest(
      buildManifest(previous, decision.paradigm, classification, genome),
    );

    setGenome((g) => {
      const next = logVerdict(
        { ...g, paradigm: decision.paradigm },
        `Restructured: ${previous} → ${decision.paradigm} — ${decision.reason}`,
      );
      return persist(next);
    });
    // eslint-disable-next-line react-hooks/exhaustive-deps
  }, [tick]);

  /* ---------------------------------------------------------------- */
  /* actions                                                           */
  /* ---------------------------------------------------------------- */
  const bump = useCallback(() => setTick((t) => t + 1), []);

  const openNode = useCallback(
    (id: string) => {
      if (!NODE_BY_ID[id]) return;
      const s = signalsRef.current;

      // close out the previous focal point and fold its dwell into interest
      if (s.focusOpen && s.lastNode && s.lastNode !== id) {
        const dwell = Date.now() - s.focusStart;
        s.focusMs += Math.max(0, dwell);
        setGenome((g) =>
          persist(
            registerInterest(
              g,
              s.lastNode as string,
              NODE_BY_ID[s.lastNode as string].tags,
              dwell,
            ),
          ),
        );
      } else if (s.focusOpen && s.lastNode === id) {
        const dwell = Date.now() - s.focusStart;
        s.focusMs += Math.max(0, dwell);
      }

      if (s.path.length) {
        const prev = s.path[s.path.length - 1];
        if (isNeighbour(prev, id)) s.steps++;
        else s.jumps++;
      }

      s.path.push(id);
      s.openTimes.push(Date.now());
      s.opens++;
      if (s.seen.includes(id)) s.revisits++;
      else s.seen.push(id);
      s.lastNode = id;
      s.focusStart = Date.now();
      s.focusOpen = true;
      s.actions.open++;
      if (s.opens === 1) {
        firstOpenRef.current = true;
        setCold(false);
      }

      setGenome((g) => {
        const next = registerVisitNode(registerAction(g, 'open'), id);
        return persist(next);
      });
      bump();
    },
    [bump, persist],
  );

  const closeNode = useCallback(() => {
    const s = signalsRef.current;
    const last = s.lastNode;
    if (s.focusOpen && last) {
      const dwell = Date.now() - s.focusStart;
      s.focusMs += Math.max(0, dwell);
      setGenome((g) =>
        persist(
          registerInterest(g, last, NODE_BY_ID[last]?.tags ?? [], dwell),
        ),
      );
    }
    s.focusOpen = false;
    bump();
  }, [bump, persist]);

  const followEdge = useCallback(
    (id: string) => {
      const s = signalsRef.current;
      s.actions.edge++;
      if (s.path.length) {
        const prev = s.path[s.path.length - 1];
        if (isNeighbour(prev, id)) {
          s.steps++;
          s.actions.edge++;
        } else s.jumps++;
      }
      s.path.push(id);
      s.openTimes.push(Date.now());
      s.opens++;
      if (s.seen.includes(id)) s.revisits++;
      else s.seen.push(id);
      s.lastNode = id;
      s.focusStart = Date.now();
      s.focusOpen = true;
      setGenome((g) => persist(registerVisitNode(registerAction(g, 'edge'), id)));
      bump();
    },
    [bump, persist],
  );

  const noteScroll = useCallback(
    (pixels: number, velocity: number, dtMs: number) => {
      const s = signalsRef.current;
      s.scrollPixels += pixels;
      s.scrollSeconds += dtMs / 1000;
      s.peakVelocity = Math.max(s.peakVelocity, velocity);
      if (velocity > 900) s.fastScrolls++;
      else if (velocity < 120) s.slowScrolls++;
      bump();
    },
    [bump],
  );

  const lastPointerBump = useRef(0);
  const notePointer = useCallback(
    (pixels: number, dtMs: number) => {
      const s = signalsRef.current;
      // a cursor teleport is not a swipe — ignore sub-frame jumps
      if (dtMs < 8) return;
      const capped = Math.min(pixels, 60);
      s.pointerPx += capped;
      s.pointerMs += Math.min(120, dtMs);
      const v = s.pointerPx / (s.pointerMs / 1000);
      s.peakPointer = Math.max(s.peakPointer, v);
      const now = Date.now();
      if (now - lastPointerBump.current > 120) {
        lastPointerBump.current = now;
        bump();
      }
    },
    [bump],
  );

  const noteSearch = useCallback(
    (q: string) => {
      const s = signalsRef.current;
      s.actions.search++;
      if (q) s.queries.push(q);
      bump();
    },
    [bump],
  );

  const noteFilter = useCallback(
    (tag: string) => {
      const s = signalsRef.current;
      s.actions.filter++;
      if (tag) s.filters.push(tag);
      bump();
    },
    [bump],
  );

  const noteCommand = useCallback(
    (cmd: string) => {
      const s = signalsRef.current;
      s.actions.command++;
      if (cmd) s.commands.push(cmd);
      bump();
    },
    [bump],
  );

  const note = useCallback(
    (action: ActionId) => {
      const s = signalsRef.current;
      s.actions[action]++;
      bump();
    },
    [bump],
  );

  const setParadigm = useCallback(
    (p: ParadigmId, pin = false) => {
      const previous = paradigm;
      setParadigmState(p);
      setPinned(pin);
      if (previous !== p) {
        setManifest(buildManifest(previous, p, classification, genome, true));
      }
      setGenome((g) => {
        const next = logVerdict(
          { ...g, paradigm: p, pinned: pin, used: g.used.includes(p) ? g.used : [...g.used, p] },
          pin
            ? `You pinned the structure to ${p} — the engine will now observe only.`
            : `You chose ${p} manually.`,
        );
        return persist(next);
      });
    },
    [classification, genome, paradigm, persist],
  );

  const mutate = useCallback(() => {
    setGenome((g) => {
      const next = mutateGenome(g, 'you asked');
      next.paradigm = g.paradigm;
      persist(next);
      return next;
    });
    bump();
  }, [bump, persist]);

  const reset = useCallback(() => {
    clearGenome();
    const fresh = loadGenome();
    setGenome(fresh);
    setPinned(false);
    setParadigm('constellation');
    setManifest(null);
    signalsRef.current = emptySignals();
    setCold(true);
    bump();
  }, [bump]);

  /* ---------------------------------------------------------------- */
  /* derived views                                                     */
  /* ---------------------------------------------------------------- */
  const trail = useMemo(() => buildTrail(genome, 5), [genome]);
  const chapters = useMemo(() => buildChapters(genome, 6), [genome]);
  const promoted = useMemo(
    () => orderFor(genome, { weights: genome.nodeInterest }).slice(0, 5),
    [genome],
  );
  const order = useMemo(() => orderFor(genome), [genome]);

  const primary = useMemo<PrimaryAction>(() => {
    const s = signalsRef.current;
    if (genome.features.memory && genome.visited.length) {
      return {
        label: `Resume · ${NODE_BY_ID[genome.visited[genome.visited.length - 1]]?.title ?? ''}`,
        nodeId: genome.visited[genome.visited.length - 1] ?? null,
        kind: 'resume',
      };
    }
    if (genome.features.trail && trail.length) {
      return { label: 'Follow your trail', nodeId: trail[0] ?? null, kind: 'trail' };
    }
    if (s.lastNode) {
      const rel = relatedTo(s.lastNode, genome, 1)[0];
      if (rel) return { label: `Next: ${NODE_BY_ID[rel.id]?.title ?? rel.id}`, nodeId: rel.id, kind: 'related' };
    }
    if (promoted.length) {
      return { label: `Enter · ${NODE_BY_ID[promoted[0]]?.title ?? ''}`, nodeId: promoted[0], kind: 'explore' };
    }
    return { label: 'Enter the field', nodeId: NODES[0].id, kind: 'explore' };
  }, [genome, promoted, trail]);

  const related = useCallback((id: string) => relatedTo(id, genome, 6), [genome]);

  const value: EngineApi = {
    genome,
    signals: signalsRef.current,
    classification,
    paradigm,
    pinned,
    manifest,
    log: genome.log,
    features: genome.features,
    trail,
    chapters,
    promoted,
    primary,
    order,
    cold,
    openNode,
    closeNode,
    followEdge,
    noteScroll,
    notePointer,
    noteSearch,
    noteFilter,
    noteCommand,
    note,
    setParadigm,
    mutate,
    reset,
    related,
  };

  testBus.api = value;

  return <EngineContext.Provider value={value}>{children}</EngineContext.Provider>;
}

export function useEngine(): EngineApi {
  const ctx = useContext(EngineContext);
  if (!ctx) throw new Error('useEngine must be used inside <EngineProvider>');
  return ctx;
}
