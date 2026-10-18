import { NODES } from '../content/graph';
import {
  emptyActions,
  type ArchetypeId,
  type FeatureId,
  type Genome,
  type LogEntry,
  type ParadigmId,
} from './types';

const STORAGE_KEY = 'deepfield.genome.v2';

/** deterministic PRNG so a given generation always produces the same ordering */
export function mulberry32(seed: number) {
  let a = seed >>> 0;
  return function rng() {
    a |= 0;
    a = (a + 0x6d2b79f5) | 0;
    let t = Math.imul(a ^ (a >>> 15), 1 | a);
    t = (t + Math.imul(t ^ (t >>> 7), 61 | t)) ^ t;
    return ((t ^ (t >>> 14)) >>> 0) / 4294967296;
  };
}

const FEATURE_UNLOCKS: { gen: number; feature: FeatureId; label: string }[] = [
  { gen: 2, feature: 'trail', label: 'TRAIL — a personalised route through the graph' },
  { gen: 3, feature: 'compare', label: 'COMPARE — hold two objects side by side' },
  { gen: 3, feature: 'memory', label: 'MEMORY — the site remembers where you left off' },
  { gen: 4, feature: 'chapters', label: 'CHAPTERS — a syllabus synthesised from your trail' },
];

export function newGenome(now = Date.now()): Genome {
  return {
    version: 2,
    generation: 0,
    visits: 0,
    archetype: 'reader',
    archetypeLog: [],
    actions: emptyActions(),
    interest: {},
    nodeInterest: {},
    visited: [],
    paradigm: 'codex',
    pinned: false,
    used: ['codex'],
    features: { trail: false, compare: false, memory: false, chapters: false },
    log: [],
    seed: Math.floor(Math.random() * 0xffffffff),
    totalMs: 0,
    firstSeen: now,
  };
}

export function loadGenome(): Genome {
  if (typeof localStorage === 'undefined') return newGenome();
  try {
    const raw = localStorage.getItem(STORAGE_KEY);
    if (!raw) return newGenome();
    const parsed = JSON.parse(raw) as Genome;
    if (!parsed || parsed.version !== 2 || !Array.isArray(parsed.visited)) {
      return newGenome();
    }
    return {
      ...newGenome(),
      ...parsed,
      actions: { ...emptyActions(), ...parsed.actions },
      features: { ...newGenome().features, ...parsed.features },
      interest: parsed.interest ?? {},
      nodeInterest: parsed.nodeInterest ?? {},
      log: parsed.log ?? [],
      archetypeLog: parsed.archetypeLog ?? [],
      used: parsed.used?.length ? parsed.used : ['codex'],
    };
  } catch {
    return newGenome();
  }
}

export function saveGenome(g: Genome) {
  if (typeof localStorage === 'undefined') return;
  try {
    localStorage.setItem(STORAGE_KEY, JSON.stringify(g));
  } catch {
    /* storage may be unavailable — the site still works, it just forgets */
  }
}

export function clearGenome() {
  if (typeof localStorage === 'undefined') return;
  try {
    localStorage.removeItem(STORAGE_KEY);
  } catch {
    /* ignore */
  }
}

function pushLog(g: Genome, kind: LogEntry['kind'], text: string) {
  g.log = [{ gen: g.generation, ts: Date.now(), kind, text }, ...g.log].slice(0, 60);
}

export function registerVisit(g: Genome, archetype: ArchetypeId, confidence: number): Genome {
  const next: Genome = {
    ...g,
    visits: g.visits + 1,
    generation: g.generation + 1,
    archetype,
    archetypeLog: [
      { gen: Math.max(1, g.generation + 1), archetype, confidence },
      ...g.archetypeLog,
    ].slice(0, 20),
    features: { ...g.features },
    interest: { ...g.interest },
    nodeInterest: { ...g.nodeInterest },
    actions: { ...g.actions },
    visited: [...g.visited],
    used: [...g.used],
    log: [...g.log],
  };
  next.seed = (g.seed * 1664525 + 1013904223) >>> 0;
  pushLog(
    next,
    'session',
    `Visit ${next.visits} · generation ${next.generation} · read as ${archetype} (${Math.round(confidence * 100)}%)`,
  );
  return next;
}

/** Force the next generation: unlock behaviour and re-seed the arrangement. */
export function mutateGenome(g: Genome, reason = 'manual'): Genome {
  const next: Genome = {
    ...g,
    generation: g.generation + 1,
    seed: (g.seed * 1103515245 + 12345) >>> 0,
    features: { ...g.features },
    interest: { ...g.interest },
    nodeInterest: { ...g.nodeInterest },
    actions: { ...g.actions },
    visited: [...g.visited],
    used: [...g.used],
    log: [...g.log],
  };

  const unlocked: string[] = [];
  for (const u of FEATURE_UNLOCKS) {
    if (next.generation >= u.gen && !next.features[u.feature]) {
      next.features[u.feature] = true;
      unlocked.push(u.label);
    }
  }

  if (unlocked.length) {
    pushLog(next, 'unlock', `Generation ${next.generation} unlocked ${unlocked.join(' · ')}`);
  } else {
    pushLog(
      next,
      'mutation',
      `Generation ${next.generation} · arrangement re-seeded and relations re-weighted (${reason})`,
    );
  }
  return next;
}

/** Fold one interaction into the cumulative interest model. */
export function registerInterest(
  g: Genome,
  nodeId: string,
  tags: string[],
  dwellMs: number,
): Genome {
  const interest = { ...g.interest };
  const nodeInterest = { ...g.nodeInterest };
  const weight = 1 + Math.min(2.5, dwellMs / 6000);

  for (const t of tags) interest[t] = (interest[t] ?? 0) + weight;
  nodeInterest[nodeId] = (nodeInterest[nodeId] ?? 0) + weight;

  const total = Object.values(interest).reduce((a, b) => a + b, 0) || 1;
  const normalised: Record<string, number> = {};
  for (const [k, v] of Object.entries(interest)) normalised[k] = v / total;

  return { ...g, interest: normalised, nodeInterest };
}

export function registerAction(g: Genome, action: keyof Genome['actions'], amount = 1): Genome {
  const actions = { ...g.actions };
  actions[action] = (actions[action] ?? 0) + amount;
  return { ...g, actions };
}

export function registerVisitNode(g: Genome, id: string): Genome {
  const visited = g.visited.includes(id) ? g.visited : [...g.visited, id];
  return { ...g, visited };
}

export function registerParadigm(g: Genome, p: ParadigmId): Genome {
  const used = g.used.includes(p) ? g.used : [...g.used, p];
  return { ...g, used };
}

export function logVerdict(g: Genome, text: string): Genome {
  const next = { ...g, log: [...g.log] };
  pushLog(next, 'verdict', text);
  return next;
}

/**
 * Order the corpus for a generation.
 * The engine re-weights by cumulative interest, then by novelty (never seen),
 * then by a seeded shuffle so two different visitors get different orders.
 */
export function orderFor(
  g: Genome,
  opts: { only?: string[]; weights?: Record<string, number> } = {},
): string[] {
  const rng = mulberry32(g.seed);
  const pool = (opts.only ?? NODES.map((n) => n.id)).slice();
  const w = opts.weights ?? g.nodeInterest;
  const scored = pool.map((id) => {
    const jitter = rng() * 0.35;
    const seen = g.visited.includes(id) ? 0 : 0.25;
    return { id, score: (w[id] ?? 0) * 0.6 + seen + jitter };
  });
  scored.sort((a, b) => b.score - a.score);
  return scored.map((s) => s.id);
}
