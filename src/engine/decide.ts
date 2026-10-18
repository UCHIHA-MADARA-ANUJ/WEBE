import {
  EDGES,
  NODES,
  NODE_BY_ID,
  neighboursOf,
  type FieldNode,
} from '../content/graph';
import { mulberry32, orderFor } from './genome';
import {
  ARCHETYPES,
  PARADIGMS,
  type ArchetypeId,
  type Classification,
  type Genome,
  type Manifest,
  type ParadigmId,
} from './types';

export interface Decision {
  paradigm: ParadigmId;
  changed: boolean;
  reason: string;
  confidence: number;
}



/**
 * The single most important decision the engine makes: *what shape the
 * interface should be right now*.
 *
 * It is deliberately conservative — a wrong switch is far more damaging than
 * a late one — so it requires a confident read and a clear margin before it
 * restructures anything.
 */
export function decideParadigm(
  classification: Classification,
  current: ParadigmId,
  pinned: boolean,
): Decision {
  const spec = PARADIGMS[current];
  if (pinned) {
    return {
      paradigm: current,
      changed: false,
      reason: `pinned by you — the engine is observing but not restructuring`,
      confidence: classification.confidence,
    };
  }

  const top = classification.top;
  const desired = ARCHETYPES.find((a) => a.id === top)?.prefers;

  if (!desired) {
    return {
      paradigm: current,
      changed: false,
      reason: 'no preference could be derived',
      confidence: classification.confidence,
    };
  }

  if (desired === current) {
    return {
      paradigm: current,
      changed: false,
      reason: `your reading matches ${spec.name.toLowerCase()} — holding the structure`,
      confidence: classification.confidence,
    };
  }

  const CONFIDENT = 0.42;
  const MARGIN = 0.05;

  if (classification.confidence < CONFIDENT) {
    return {
      paradigm: current,
      changed: false,
      reason: `the read is too ambiguous (${Math.round(classification.confidence * 100)}%) to justify tearing the layout down`,
      confidence: classification.confidence,
    };
  }

  if (classification.margin < MARGIN) {
    return {
      paradigm: current,
      changed: false,
      reason: `two readings are competing — no clear winner yet`,
      confidence: classification.confidence,
    };
  }

  return {
    paradigm: desired,
    changed: true,
    reason: `read as ${top} (${Math.round(classification.confidence * 100)}%) — restructuring into ${PARADIGMS[desired].name}`,
    confidence: classification.confidence,
  };
}

/** Headline for the reconfiguration overlay. */
export function headlineFor(from: ParadigmId, to: ParadigmId, archetype: ArchetypeId): string {
  const verbs: Record<ArchetypeId, string> = {
    reader: 'settles',
    contemplative: 'stillens',
    scout: 'wanders',
    skimmer: 'sweeps',
    analyst: 'compares',
    commander: 'directs',
  };
  return `You ${verbs[archetype]} — the interface unfolded out of ${PARADIGMS[from].name} and into ${PARADIGMS[to].name}.`;
}

/**
 * Which entries move forward, and which recede, when the structure changes.
 * Promotion is a function of cumulative interest, novelty and the relation
 * between the previous focal point and the new one.
 */
export function buildManifest(
  from: ParadigmId,
  to: ParadigmId,
  classification: Classification,
  genome: Genome,
  manual = false,
): Manifest {
  const ranked = orderFor(genome, { weights: genome.nodeInterest });
  const promoted = ranked.slice(0, 3);
  const demoted = ranked.slice(-3).reverse();
  return {
    ts: Date.now(),
    manual,
    from,
    to,
    fromLabel: PARADIGMS[from].name,
    toLabel: PARADIGMS[to].name,
    archetype: classification.top,
    confidence: classification.confidence,
    reasons: classification.reasons,
    promoted,
    demoted,
    verbs: PARADIGMS[to].verbs,
    headline: headlineFor(from, to, classification.top),
  };
}

/**
 * TRAIL — a personalised route through the graph.
 * Greedy: from the most interesting node you already touched, walk to the
 * neighbour that maximises interest + novelty + a mild preference for
 * relations that explain rather than merely relate.
 */
export function buildTrail(genome: Genome, length = 5): string[] {
  const visited = new Set(genome.visited);
  const weights = genome.nodeInterest;
  const rng = mulberry32(genome.seed ^ 0x9e37);

  const scored = NODES.map((n) => ({
    n,
    score: (weights[n.id] ?? 0) + (visited.has(n.id) ? 0.6 : 0.15) + rng() * 0.2,
  })).sort((a, b) => b.score - a.score);

  const start = scored[0]?.n.id ?? NODES[0].id;
  const trail: string[] = [start];
  const used = new Set(trail);

  while (trail.length < length) {
    const current = trail[trail.length - 1];
    const candidates = neighboursOf(current)
      .filter((id) => !used.has(id))
      .map((id) => {
        const w = weights[id] ?? 0;
        const novelty = visited.has(id) ? 0.1 : 0.45;
        const structural = degreeOf(id) / 6;
        return { id, score: w * 0.8 + novelty + structural * 0.2 + rng() * 0.25 };
      })
      .sort((a, b) => b.score - a.score);

    if (!candidates.length) break;
    trail.push(candidates[0].id);
    used.add(candidates[0].id);
  }
  return trail;
}

/**
 * CHAPTERS — a syllabus synthesised from the visitor's accumulated interest.
 * One entry per family, ordered by how much attention that family has earned.
 */
export function buildChapters(genome: Genome, max = 6): { family: string; node: string }[] {
  const byFamily = new Map<string, FieldNode[]>();
  for (const n of NODES) {
    const arr = byFamily.get(n.family) ?? [];
    arr.push(n);
    byFamily.set(n.family, arr);
  }

  const scored = [...byFamily.entries()].map(([family, nodes]) => {
    const familyScore = nodes.reduce(
      (acc, n) =>
        acc +
        (genome.interest[n.tags[0]] ?? 0) +
        (genome.nodeInterest[n.id] ?? 0) * 0.5,
      0,
    );
    const best = nodes
      .slice()
      .sort(
        (a, b) =>
          (genome.nodeInterest[b.id] ?? 0) + (genome.visited.includes(b.id) ? 0.2 : 0) -
          ((genome.nodeInterest[a.id] ?? 0) + (genome.visited.includes(a.id) ? 0.2 : 0)),
      )[0];
    return { family, node: best.id, score: familyScore };
  });

  scored.sort((a, b) => b.score - a.score);
  return scored.slice(0, max).map((s) => ({ family: s.family, node: s.node }));
}

function degreeOf(id: string): number {
  let d = 0;
  for (const e of EDGES) if (e.from === id || e.to === id) d++;
  return d;
}

/** Related entries, ranked by shared relation strength and interest. */
export function relatedTo(id: string, genome: Genome, limit = 5): { id: string; kind: string }[] {
  const out: { id: string; kind: string }[] = [];
  for (const e of EDGES) {
    if (e.from === id) out.push({ id: e.to, kind: e.kind });
    else if (e.to === id) out.push({ id: e.from, kind: e.kind });
  }
  return out
    .map((r) => ({
      ...r,
      score: (genome.nodeInterest[r.id] ?? 0) + (genome.visited.includes(r.id) ? 0.15 : 0.35),
    }))
    .sort((a, b) => b.score - a.score)
    .slice(0, limit);
}

export function nodeTitle(id: string): string {
  return NODE_BY_ID[id]?.title ?? id;
}
