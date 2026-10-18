import {
  ARCHETYPES,
  type ArchetypeId,
  type Classification,
  type FeatureKey,
  type FeatureVector,
  type SessionSignals,
} from './types';

const clamp01 = (v: number) => Math.max(0, Math.min(1, v));

/** raw observation → 0..1 normalised signal */
export function normalise(raw: FeatureVector): Record<FeatureKey, number> {
  return {
    linearity: clamp01(raw.linearity),
    breadth: clamp01(raw.breadth),
    revisit: clamp01(raw.revisit / 0.6),
    volume: clamp01(raw.volume),
    cadence: clamp01(raw.cadence),
    scan: clamp01(raw.scan / 1500),
    dwell: clamp01(raw.dwell / 6000),
    command: clamp01(raw.command / 0.5),
    spatial: clamp01(raw.spatial / 0.5),
    query: clamp01(raw.query / 0.6),
    edge: clamp01(raw.edge / 0.5),
  };
}

/**
 * Turn a raw session trace into a feature vector.
 * `isNeighbour` tells us whether two consecutively opened nodes are related.
 */
export function computeFeatures(
  s: SessionSignals,
  isNeighbour: (a: string, b: string) => boolean,
): FeatureVector {
  const transitions = s.steps + s.jumps;
  const totalActions = Object.values(s.actions).reduce((a, b) => a + b, 0) || 1;

  // neighbours-in-path sanity: if a caller did not report adjacency, infer it
  let steps = s.steps;
  let jumps = s.jumps;
  if (transitions === 0 && s.path.length > 1) {
    for (let i = 1; i < s.path.length; i++) {
      if (isNeighbour(s.path[i - 1], s.path[i])) steps++;
      else jumps++;
    }
  }

  return {
    linearity: transitions ? steps / transitions : 0.35,
    breadth: s.opens ? new Set(s.path).size / s.opens : 0,
    revisit: s.opens ? s.revisits / s.opens : 0,
    volume: clamp01(s.opens / 8),
    cadence: cadenceOf(s),
    scan: Math.max(
      s.scrollSeconds ? s.scrollPixels / s.scrollSeconds : 0,
      s.pointerMs > 400 ? (s.pointerPx / (s.pointerMs / 1000)) : 0,
    ),
    dwell: s.opens ? s.focusMs / s.opens : 0,
    command: s.actions.command / totalActions,
    spatial: s.actions.pan / totalActions,
    query: (s.actions.search + s.actions.filter) / totalActions,
    edge: s.actions.edge / totalActions,
  };
}

/**
 * Impatience: the mean gap between two consecutive objects, mapped so that
 * ~0.4 s reads as frantic and ~4 s reads as patient.
 */
export function cadenceOf(s: SessionSignals): number {
  if (s.path.length < 3) return 0;
  const gaps: number[] = [];
  for (let i = 1; i < s.path.length; i++) {
    const d = s.openTimes[i] - s.openTimes[i - 1];
    if (d > 0) gaps.push(d);
  }
  if (!gaps.length) return 0;
  const mean = gaps.reduce((a, b) => a + b, 0) / gaps.length;
  return clamp01(1 - (mean - 400) / 3600);
}

/** the concrete numbers behind a read, used to phrase the reasons honestly */
export interface ReadContext {
  opens: number;
  unique: number;
  steps: number;
  jumps: number;
  focusMs: number;
  elapsedMs: number;
  fastScrolls: number;
  queries: number;
  filters: number;
  commands: number;
  spatial: number;
}

export function contextFrom(s: SessionSignals): ReadContext {
  return {
    opens: s.opens,
    unique: new Set(s.path).size,
    steps: s.steps,
    jumps: s.jumps,
    focusMs: s.focusMs,
    elapsedMs: s.elapsedMs,
    fastScrolls: s.fastScrolls,
    queries: s.queries.length,
    filters: s.filters.length,
    commands: s.commands.length,
    spatial: s.actions.pan,
  };
}

const REASON_TEMPLATES: Record<
  ArchetypeId,
  (n: Record<FeatureKey, number>, c: ReadContext) => string[]
> = {
  reader: (n, c) => [
    `you spend ${(c.focusMs / Math.max(1, c.opens) / 1000).toFixed(1)}s on each object before moving on`,
    `${Math.round(n.linearity * 100)}% of your moves follow a stated relation (${c.steps} of ${c.steps + c.jumps})`,
    `depth, not breadth — ${c.unique} objects, opened ${Math.round((1 - n.cadence) * 100)}% at your own pace`,
  ],
  contemplative: (_n, c) => [
    `single-object attention: ${(c.focusMs / 1000).toFixed(0)}s on ${c.opens} object${c.opens === 1 ? '' : 's'}`,
    `only ${c.unique} object${c.unique === 1 ? '' : 's'} opened — you are not collecting`,
    `no queries, no filters, no commands — ${c.queries + c.filters + c.commands} interventions`,
  ],
  scout: (n, c) => [
    `you reach ${Math.round(n.breadth * 100)}% distinct objects — wide, not deep`,
    c.spatial > 0
      ? `${c.spatial} spatial actions (drag / zoom) — you think in positions`
      : `${c.jumps} cross-field jumps — you think in positions`,
    `you travel by relation ${Math.round(n.edge * 100)}% of the time`,
  ],
  skimmer: (n, c) => [
    `motion sits at ${Math.round(n.scan * 100)}% of the fast band (${c.fastScrolls} fast scroll bursts)`,
    `you open objects ${Math.round(n.cadence * 100)}% as fast as a hurried visitor`,
    `${c.opens} objects opened, ${(c.focusMs / 1000).toFixed(0)}s of attention spread across them`,
  ],
  analyst: (n, c) => [
    `${c.queries} searches and ${c.filters} filters — you interrogate the corpus`,
    `you revisit ${Math.round(n.revisit * 100)}% of what you open`,
    `you hold several objects in mind at once`,
  ],
  commander: (_n, c) => [
    `${c.commands} typed commands — you use verbs instead of targets`,
    `you reach for the keyboard before the pointer`,
    `${c.queries + c.filters} queries issued from the prompt`,
  ],
};

/**
 * Some archetypes are defined by the *absence* of behaviour and can be
 * triggered by a single careless click. Each read must therefore clear a
 * minimum evidentiary bar before it is allowed to become the headline.
 */
export function viable(a: ArchetypeId, f: FeatureVector, c: ReadContext): boolean {
  switch (a) {
    case 'contemplative':
      return c.focusMs >= 5000 && f.dwell >= 6000 && c.opens <= 4;
    case 'reader':
      return f.dwell >= 1200 || c.steps >= 2;
    case 'scout':
      return c.opens >= 2;
    case 'skimmer':
      return c.fastScrolls >= 2 || f.scan > 700 || f.cadence > 0.72;
    case 'analyst':
      return c.queries + c.filters >= 2;
    case 'commander':
      return c.commands >= 2;
    default:
      return true;
  }
}

/**
 * Score every archetype by *affinity to its ideal signature* rather than by
 * raw feature mass.
 *
 * For each feature we ask "how close is this visitor to the behaviour this
 * archetype describes?" and weight that by how much the archetype cares
 * about the feature. A visitor who behaves like the archetype scores near 1;
 * a visitor who behaves like its opposite scores near 0.
 */
export function classify(features: FeatureVector, ctx: ReadContext): Classification {
  const n = normalise(features);
  const scores = {} as Record<ArchetypeId, number>;
  const rank: ArchetypeId[] = [];

  for (const a of ARCHETYPES) {
    let total = 0;
    let weight = 0;
    for (const [key, w] of Object.entries(a.weights) as [FeatureKey, number][]) {
      const ideal = a.ideal[key] ?? 0;
      const spread = Math.max(ideal, 1 - ideal);
      const affinity = 1 - Math.min(1, Math.abs(n[key] - ideal) / spread);
      total += w * affinity;
      weight += w;
    }
    scores[a.id] = weight ? total / weight : 0;
  }

  const sorted = [...ARCHETYPES].sort((x, y) => scores[y.id] - scores[x.id]);

  /* the headline read is the best *credible* one — a single click must never
     be enough to convince the engine that you are a contemplator */
  const credible = sorted.filter((a) => viable(a.id, features, ctx));
  const blank = credible.length === 0;
  const pool = blank ? sorted : credible;
  const top = blank ? 'reader' : pool[0].id;
  const second = (pool[1] ?? sorted.find((a) => a.id !== top) ?? sorted[0]).id;

  const ordered = [...pool, ...sorted.filter((a) => !pool.includes(a))];
  ordered.forEach((a) => rank.push(a.id));

  const confidence = blank ? 0 : scores[top];
  const margin = blank ? 0 : scores[top] - scores[second];

  const reasons = blank
    ? ['no observations yet — the engine is waiting for you to move']
    : REASON_TEMPLATES[top](n, ctx).filter(Boolean).slice(0, 3);

  return {
    features,
    ctx,
    scores,
    rank,
    top,
    confidence,
    margin,
    reasons,
    evidence: 0,
    blank,
  };
}

/** Human label for a 0..1 confidence */
export function confidenceLabel(c: number): string {
  if (c > 0.62) return 'certain';
  if (c > 0.48) return 'confident';
  if (c > 0.36) return 'tentative';
  return 'ambiguous';
}
