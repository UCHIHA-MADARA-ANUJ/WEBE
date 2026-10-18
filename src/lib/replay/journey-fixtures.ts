/**
 * STRATA — Journey Fixtures
 *
 * Three reproducible demonstration sequences, each run through the *real*
 * production event-recording → profile-update → composition-scoring → adaptation
 * pipeline. They must produce meaningfully different final compositions from the
 * same starting state.
 *
 * Each journey is a sequence of typed interaction events that exercise the
 * actual engine (classify.ts + decide.ts + genome.ts), not a hardcoded layout.
 */

export interface JourneyEvent {
  kind: 'open' | 'edge' | 'search' | 'filter' | 'command' | 'scroll' | 'dwell' | 'pointer';
  target?: string;
  query?: string;
  tag?: string;
  cmd?: string;
  pixels?: number;
  velocity?: number;
  dtMs?: number;
  dwellMs?: number;
  note?: string;
}

export interface Journey {
  id: string;
  label: string;
  glyph: string;
  blurb: string;
  color: string;
  events: JourneyEvent[];
}

export const JOURNEYS: Journey[] = [
  {
    id: 'explorer',
    label: 'The Explorer',
    glyph: '✧',
    blurb: 'Follows relationships, branches into new areas, revisits connections — wants the map.',
    color: '#1E40AF',
    events: [
      { kind: 'open', target: 'q-launch', note: 'Starts at the central question' },
      { kind: 'edge', target: 'alt-lean', note: 'Follows related-to into Lean Launch' },
      { kind: 'edge', target: 'claim-speed-wins', note: 'From Lean → claim that supports it' },
      { kind: 'edge', target: 'ev-team-capacity', note: 'Claim → evidence that contradicts it — contradiction is interesting' },
      { kind: 'edge', target: 'note-constraint', note: 'Capacity evidence → calendar constraint' },
      { kind: 'open', target: 'alt-community', note: 'Jumps to compare: Community alternative' },
      { kind: 'edge', target: 'claim-community-compounds', note: 'Community → its supporting claim' },
      { kind: 'edge', target: 'ev-waitlist-signals', note: 'Claim → waitlist evidence' },
      { kind: 'open', target: 'alt-stealth', note: 'Checks the third alternative for comparison' },
      { kind: 'edge', target: 'risk-visibility', note: 'Stealth → visibility risk that blocks Lean' },
      { kind: 'open', target: 'ev-competitor-pricing', note: 'Digs into pricing context' },
      { kind: 'pointer', pixels: 420, dtMs: 900, note: 'Drags the map around, exploring spatially' },
      { kind: 'pointer', pixels: 380, dtMs: 800, note: 'More spatial exploration' },
      { kind: 'open', target: 'task-public-assets', note: 'Looks at what public launch would require' },
      { kind: 'dwell', dwellMs: 8000, note: 'Lingers — reading the task dependencies' },
    ],
  },
  {
    id: 'executor',
    label: 'The Executor',
    glyph: '▸',
    blurb: 'Completes tasks, follows dependency chains, resolves blockers — wants the sequence.',
    color: '#D97706',
    events: [
      { kind: 'open', target: 'task-message', note: 'Goes straight to the first task' },
      { kind: 'dwell', dwellMs: 4500, note: 'Reads the task, then marks it mentally' },
      { kind: 'open', target: 'task-waitlist-triage', note: 'Follows dependency: message → triage' },
      { kind: 'edge', target: 'ev-waitlist-signals', note: 'Triage → the evidence it acts on' },
      { kind: 'open', target: 'task-onboarding-flow', note: 'Next in sequence: onboarding' },
      { kind: 'open', target: 'task-pricing-page', note: 'Then pricing page' },
      { kind: 'open', target: 'task-pilot-ops', note: 'Then pilot ops — following the dependency chain' },
      { kind: 'open', target: 'task-public-assets', note: 'Final task in the critical path' },
      { kind: 'dwell', dwellMs: 3000, note: 'Reviews the full sequence' },
      { kind: 'search', query: 'pricing', note: 'Searches to confirm pricing task status' },
      { kind: 'filter', tag: 'tasks', note: 'Filters to the task family — focusing on execution' },
      { kind: 'open', target: 'note-constraint', note: 'Checks the hard constraint that affects timing' },
      { kind: 'open', target: 'decision-draft', note: 'Checks what the decision currently says' },
      { kind: 'open', target: 'outcome-brief', note: 'Then the brief it produces' },
    ],
  },
  {
    id: 'analyst',
    label: 'The Analyst',
    glyph: '⊞',
    blurb: 'Compares alternatives, applies criteria, weighs evidence — wants the matrix.',
    color: '#065F46',
    events: [
      { kind: 'open', target: 'alt-lean', note: 'Opens Lean — first alternative' },
      { kind: 'open', target: 'alt-community', note: 'Immediately compares with Community' },
      { kind: 'open', target: 'alt-stealth', note: 'Then Stealth — holds all three in mind' },
      { kind: 'search', query: 'pricing', note: 'Searches for pricing-related evidence' },
      { kind: 'open', target: 'ev-competitor-pricing', note: 'Finds competitor pricing scan' },
      { kind: 'open', target: 'crit-speed', note: 'Checks Speed criterion scoring' },
      { kind: 'open', target: 'crit-risk', note: 'Then Risk criterion — opposite end' },
      { kind: 'open', target: 'crit-cost', note: 'Then Cost' },
      { kind: 'open', target: 'crit-distribution', note: 'All four criteria examined' },
      { kind: 'filter', tag: 'evidence', note: 'Filters to evidence family to cross-reference' },
      { kind: 'open', target: 'ev-interviews', note: 'Interviews — the strongest evidence' },
      { kind: 'open', target: 'ev-landing-test', note: 'Landing test — complementary evidence' },
      { kind: 'search', query: 'risk', note: 'Searches risks to complete the comparison' },
      { kind: 'open', target: 'risk-capacity-breach', note: 'Capacity risk — tests Lean weakness' },
      { kind: 'filter', tag: 'risks', note: 'Filters risks — systematic comparison' },
      { kind: 'dwell', dwellMs: 6000, note: 'Weighs the trade-offs' },
    ],
  },
];

/** Commander variant — drives by keyboard (for testing the console paradigm) */
export const COMMANDER_JOURNEY: Journey = {
  id: 'commander',
  label: 'The Commander',
  glyph: '❯',
  blurb: 'Drives the workspace by keyboard verbs — prefers commands to clicks.',
  color: '#7C3AED',
  events: [
    { kind: 'command', cmd: 'open q-launch' },
    { kind: 'command', cmd: 'related q-launch' },
    { kind: 'command', cmd: 'open alt-lean' },
    { kind: 'command', cmd: 'compare alt-lean alt-community' },
    { kind: 'command', cmd: 'filter evidence' },
    { kind: 'command', cmd: 'search pricing' },
    { kind: 'open', target: 'crit-risk' },
    { kind: 'command', cmd: 'trail' },
    { kind: 'command', cmd: 'help' },
  ],
};
