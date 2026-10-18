/**
 * The Evolution Engine — type vocabulary.
 *
 * Everything the engine observes is a *signal*. Everything it produces is a
 * *decision*. Decisions are structural: they change the shape of the
 * interface, the set of available actions, and the hierarchy of the content.
 */

export type ParadigmId =
  | 'codex'
  | 'constellation'
  | 'mosaic'
  | 'lattice'
  | 'console'
  | 'zen';

export type ArchetypeId =
  | 'reader'
  | 'contemplative'
  | 'scout'
  | 'skimmer'
  | 'analyst'
  | 'commander';

export type ActionId =
  | 'open'
  | 'edge'
  | 'search'
  | 'filter'
  | 'command'
  | 'compare'
  | 'shuffle'
  | 'trail'
  | 'pan'
  | 'back'
  | 'expand';

export const ACTION_IDS: ActionId[] = [
  'open',
  'edge',
  'search',
  'filter',
  'command',
  'compare',
  'shuffle',
  'trail',
  'pan',
  'back',
  'expand',
];

export type ActionCounts = Record<ActionId, number>;

export function emptyActions(): ActionCounts {
  return ACTION_IDS.reduce((a, k) => {
    a[k] = 0;
    return a;
  }, {} as ActionCounts);
}

/* ------------------------------------------------------------------ */
/* Signals                                                             */
/* ------------------------------------------------------------------ */

export interface SessionSignals {
  startedAt: number;
  /** every node opened, in order — the raw trajectory */
  path: string[];
  /** tags the user filtered on */
  filters: string[];
  /** free-text queries issued */
  queries: string[];
  /** commands typed in the console paradigm */
  commands: string[];
  actions: ActionCounts;
  scrollPixels: number;
  /** seconds during which the user was actively scrolling */
  scrollSeconds: number;
  /** number of scroll bursts faster than 900 px/s */
  fastScrolls: number;
  /** number of scroll bursts slower than 120 px/s */
  slowScrolls: number;
  /** ms spent with a node focused/open */
  focusMs: number;
  /** ms of total session life */
  elapsedMs: number;
  /** how many times a node was re-opened after already being seen */
  revisits: number;
  /** transitions between nodes that are *not* graph neighbours */
  jumps: number;
  /** transitions between nodes that *are* graph neighbours */
  steps: number;
  /** raw count of node opens */
  opens: number;
  /** last node opened */
  lastNode: string | null;
  /** true while a node is actually open on screen */
  focusOpen: boolean;
  /** timestamp of the moment the current node was opened */
  focusStart: number;
  /** ids of nodes opened in this session */
  seen: string[];
  /** max scroll velocity observed, px/s */
  peakVelocity: number;
  /** count of pointer-driven drags */
  drags: number;
}

export function emptySignals(now = Date.now()): SessionSignals {
  return {
    startedAt: now,
    path: [],
    filters: [],
    queries: [],
    commands: [],
    actions: emptyActions(),
    scrollPixels: 0,
    scrollSeconds: 0,
    fastScrolls: 0,
    slowScrolls: 0,
    focusMs: 0,
    elapsedMs: 0,
    revisits: 0,
    jumps: 0,
    steps: 0,
    opens: 0,
    lastNode: null,
    focusOpen: false,
    focusStart: 0,
    seen: [],
    peakVelocity: 0,
    drags: 0,
  };
}

/* ------------------------------------------------------------------ */
/* Features & classification                                            */
/* ------------------------------------------------------------------ */

export interface FeatureVector {
  /** fraction of transitions that follow a relation in the graph */
  linearity: number;
  /** unique nodes opened / total opens */
  breadth: number;
  /** share of opens that were re-opens */
  revisit: number;
  /** how much of the corpus has been touched (0..1) */
  volume: number;
  /** scroll velocity, px/s */
  scan: number;
  /** mean ms spent per opened node */
  dwell: number;
  /** share of actions that were typed commands */
  command: number;
  /** share of actions that were spatial drags/zooms */
  spatial: number;
  /** share of actions that were search or filter */
  query: number;
  /** share of actions that opened a relation link */
  edge: number;
}

export type FeatureKey = keyof FeatureVector;

export interface Classification {
  features: FeatureVector;
  /** the concrete counts behind the read */
  ctx: {
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
  };
  scores: Record<ArchetypeId, number>;
  rank: ArchetypeId[];
  top: ArchetypeId;
  confidence: number;
  margin: number;
  /** human readable reasons for the current read */
  reasons: string[];
  /** how many observations back this read */
  evidence: number;
  /** true when there is not enough signal to read anything at all */
  blank: boolean;
}

export interface ArchetypeSpec {
  id: ArchetypeId;
  label: string;
  glyph: string;
  blurb: string;
  prefers: ParadigmId;
  /** weight of each feature for this archetype */
  weights: Partial<Record<FeatureKey, number>>;
  /** feature values at which the archetype "peaks" (for normalisation) */
  ideal: Partial<Record<FeatureKey, number>>;
}

export const ARCHETYPES: ArchetypeSpec[] = [
  {
    id: 'reader',
    label: 'Reader',
    glyph: '\u00b6',
    blurb: 'Settles into a text, lingers, follows one thread deep.',
    prefers: 'codex',
    weights: { dwell: 1.2, linearity: 0.9, volume: 0.6, scan: 0.7, breadth: 0.4 },
    ideal: { dwell: 1, linearity: 1, volume: 0.55, scan: 0, breadth: 0.35 },
  },
  {
    id: 'contemplative',
    label: 'Contemplative',
    glyph: '\u25d0',
    blurb: 'Rarely acts. Wants one thing, large, unhurried.',
    prefers: 'zen',
    weights: { dwell: 1.3, volume: 1, scan: 0.4, query: 0.3, command: 0.3, linearity: 0.3 },
    ideal: { dwell: 1, volume: 0.12, scan: 0, query: 0, command: 0, linearity: 0.6 },
  },
  {
    id: 'scout',
    label: 'Scout',
    glyph: '\u2726',
    blurb: 'Hops widely, jumps between distant relatives, wants the map.',
    prefers: 'constellation',
    weights: { breadth: 1, edge: 0.6, volume: 0.7, spatial: 0.8, dwell: 0.4, linearity: 0.3 },
    ideal: { breadth: 1, edge: 0.7, volume: 0.75, spatial: 0.8, dwell: 0.1, linearity: 0.2 },
  },
  {
    id: 'skimmer',
    label: 'Skimmer',
    glyph: '\u2248',
    blurb: 'Scrolls fast, skims surfaces, collects rather than reads.',
    prefers: 'mosaic',
    weights: { scan: 1.2, volume: 0.6, dwell: 0.9, breadth: 0.5, linearity: 0.3 },
    ideal: { scan: 1, volume: 0.6, dwell: 0.05, breadth: 0.6, linearity: 0.2 },
  },
  {
    id: 'analyst',
    label: 'Analyst',
    glyph: '\u229e',
    blurb: 'Filters, compares, re-reads. Wants two things at once.',
    prefers: 'lattice',
    weights: { query: 1.1, revisit: 0.7, edge: 0.5, command: 0.4, volume: 0.4, dwell: 0.3 },
    ideal: { query: 1, revisit: 0.6, edge: 0.5, command: 0.4, volume: 0.4, dwell: 0.5 },
  },
  {
    id: 'commander',
    label: 'Commander',
    glyph: '\u276f',
    blurb: 'Drives the site by keyboard. Prefers verbs to buttons.',
    prefers: 'console',
    weights: { command: 1.3, edge: 0.4, query: 0.4, spatial: 0.3, volume: 0.3, dwell: 0.3 },
    ideal: { command: 1, edge: 0.4, query: 0.4, spatial: 0.1, volume: 0.35, dwell: 0.2 },
  },
];

/* ------------------------------------------------------------------ */
/* Paradigms                                                           */
/* ------------------------------------------------------------------ */

export interface ParadigmSpec {
  id: ParadigmId;
  name: string;
  glyph: string;
  /** one line: what this structure *is* */
  tagline: string;
  /** the interaction contract — what is possible here and nowhere else */
  contract: string;
  /** primary action verbs this paradigm makes available */
  verbs: string[];
  archetype: ArchetypeId;
  /** which engine feature it needs; null = always available */
  requires: FeatureId | null;
}

export type FeatureId = 'trail' | 'compare' | 'memory' | 'chapters';

export const PARADIGMS: Record<ParadigmId, ParadigmSpec> = {
  codex: {
    id: 'codex',
    name: 'Codex',
    glyph: '§',
    tagline: 'One column, one entry at a time.',
    contract:
      'A reading column. Only one object is present at any moment; the rest of the universe is folded into a thin rail on the left. Navigation is sequential and irreversible-ish: you move forward through a path, and the page itself is the index.',
    verbs: ['continue', 'back', 'branch', 'open'],
    archetype: 'reader',
    requires: null,
  },
  constellation: {
    id: 'constellation',
    name: 'Constellation',
    glyph: '✧',
    tagline: 'A map you fly through.',
    contract:
      'A spatial graph. Nothing is a list; everything is a position. You pan, zoom, and trace relations by hovering. Depth is replaced by geometry, and the only way to read is to fly to it.',
    verbs: ['trace', 'fly to', 'zoom', 'isolate'],
    archetype: 'scout',
    requires: null,
  },
  mosaic: {
    id: 'mosaic',
    name: 'Mosaic',
    glyph: '▦',
    tagline: 'A dense board that re-tiles itself.',
    contract:
      'A packed grid of tiles. Information density is the point: you scan, hover for a quick read, and the board silently re-sorts itself as your interests change. Nothing is committed until you open it.',
    verbs: ['scan', 'peek', 'filter', 'shuffle'],
    archetype: 'skimmer',
    requires: null,
  },
  lattice: {
    id: 'lattice',
    name: 'Lattice',
    glyph: '⊟',
    tagline: 'Index on the left, evidence on the right.',
    contract:
      'A two-pane instrument. A flat, sortable index on one side, the working detail on the other, and a comparison strip along the bottom. Built for holding several objects in mind at once.',
    verbs: ['select', 'compare', 'filter', 'sort'],
    archetype: 'analyst',
    requires: null,
  },
  console: {
    id: 'console',
    name: 'Console',
    glyph: '❯',
    tagline: 'A text interface that talks back.',
    contract:
      'No chrome at all — a prompt. The site is a verb environment: you type commands, the site answers, and the set of valid commands changes as the engine learns what you are trying to do.',
    verbs: ['type', 'run', 'help', 'undo'],
    archetype: 'commander',
    requires: null,
  },
  zen: {
    id: 'zen',
    name: 'Zen',
    glyph: '◍',
    tagline: 'One object, full bleed, no chrome.',
    contract:
      'A single object fills the screen. There is no index, no rail, no alternative. The only decisions are to go deeper, to go back, or to let the site choose the next one for you.',
    verbs: ['deeper', 'return', 'let it choose'],
    archetype: 'contemplative',
    requires: null,
  },
};

export const PARADIGM_ORDER: ParadigmId[] = [
  'codex',
  'constellation',
  'mosaic',
  'lattice',
  'console',
  'zen',
];

/* ------------------------------------------------------------------ */
/* Genome (cross-visit procedural state)                               */
/* ------------------------------------------------------------------ */

export interface LogEntry {
  gen: number;
  ts: number;
  kind: 'session' | 'switch' | 'mutation' | 'unlock' | 'verdict';
  text: string;
}

export interface Genome {
  version: number;
  /** procedural generation — increments each visit and each forced mutation */
  generation: number;
  visits: number;
  archetype: ArchetypeId;
  archetypeLog: { gen: number; archetype: ArchetypeId; confidence: number }[];
  actions: ActionCounts;
  /** cumulative tag interest, 0..1 normalised */
  interest: Record<string, number>;
  /** cumulative per-node interest */
  nodeInterest: Record<string, number>;
  /** every node ever opened */
  visited: string[];
  paradigm: ParadigmId;
  pinned: boolean;
  /** paradigms the visitor has personally used */
  used: ParadigmId[];
  features: Record<FeatureId, boolean>;
  log: LogEntry[];
  seed: number;
  totalMs: number;
  firstSeen: number;
}

/* ------------------------------------------------------------------ */
/* Reconfiguration manifest                                            */
/* ------------------------------------------------------------------ */

export interface Manifest {
  ts: number;
  /** true when a human asked for this structure, false when the engine chose it */
  manual: boolean;
  from: ParadigmId;
  to: ParadigmId;
  fromLabel: string;
  toLabel: string;
  archetype: ArchetypeId;
  confidence: number;
  reasons: string[];
  promoted: string[];
  demoted: string[];
  verbs: string[];
  headline: string;
}
