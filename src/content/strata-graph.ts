/**
 * STRATA — The Demonstration Scenario
 *
 * Mission: "Determine the best way to launch a small digital product in the next 14 days."
 *
 * This is a FICTIONAL product-launch decision, seeded with interconnected entities
 * so the Evolution Engine has real structure to learn from. All numbers are
 * illustrative, not market research.
 */

export type EntityType =
  | 'question'
  | 'alternative'
  | 'claim'
  | 'evidence'
  | 'source'
  | 'criterion'
  | 'risk'
  | 'task'
  | 'decision'
  | 'note'
  | 'outcome';

export type RelationKind =
  | 'supports'
  | 'contradicts'
  | 'depends-on'
  | 'related-to'
  | 'evaluates'
  | 'blocks'
  | 'produces';

export const RELATION_LABEL: Record<RelationKind, string> = {
  'supports': 'supports',
  'contradicts': 'contradicts',
  'depends-on': 'depends on',
  'related-to': 'related to',
  'evaluates': 'evaluates',
  'blocks': 'blocks',
  'produces': 'produces',
};

export interface StrataEntity {
  id: string;
  type: EntityType;
  title: string;
  catalog: string;
  family: FamilyId;
  summary: string;
  body: string[];
  readings: { label: string; value: string }[];
  tags: string[];
  weight: number;
  // Task-specific
  status?: 'todo' | 'in-progress' | 'done' | 'blocked';
  dependsOn?: string[];
}

export interface StrataRelation {
  from: string;
  to: string;
  kind: RelationKind;
  note: string;
}

export type FamilyId =
  | 'question'
  | 'alternatives'
  | 'evidence'
  | 'criteria'
  | 'risks'
  | 'tasks'
  | 'synthesis';

export interface Family {
  id: FamilyId;
  label: string;
  hue: number;
  blurb: string;
}

export const FAMILIES: Record<FamilyId, Family> = {
  question:     { id: 'question',     label: 'Question',     hue: 28,  blurb: 'The decisions that need making.' },
  alternatives: { id: 'alternatives', label: 'Alternatives', hue: 168, blurb: 'Different ways to do the launch.' },
  evidence:     { id: 'evidence',     label: 'Evidence',     hue: 196, blurb: 'Research, signals, and what we know.' },
  criteria:     { id: 'criteria',     label: 'Criteria',     hue: 268, blurb: 'How we judge what good looks like.' },
  risks:        { id: 'risks',        label: 'Risks',        hue: 8,   blurb: 'What could go wrong, and how likely.' },
  tasks:        { id: 'tasks',        label: 'Tasks',        hue: 48,  blurb: 'Work that needs doing, in order.' },
  synthesis:    { id: 'synthesis',    label: 'Synthesis',    hue: 210, blurb: 'Conclusions pulled from everything else.' },
};

export const FAMILY_ORDER: FamilyId[] = ['question','alternatives','evidence','criteria','risks','tasks','synthesis'];

// ─── ENTITIES ──────────────────────────────────────────────────────────────

export const ENTITIES: StrataEntity[] = [
  // ── QUESTION ──
  {
    id: 'q-launch',
    type: 'question',
    title: 'How do we launch in 14 days?',
    catalog: 'ST-001 · QUESTION',
    family: 'question',
    summary: 'A small, focused digital product needs to find its first users — with almost no budget and a hard 14-day window.',
    body: [
      'The team has a working product, a list of about 200 warm contacts, and a runway that makes a long runway impossible. The question is not whether to launch, but how to sequence the work so the launch compounds rather than dissipates.',
      'Three paths have emerged from weeks of informal research: a lean public launch, a community-first rollout, and a stealth premium approach. Each has real evidence behind it, each carries different risks, and each implies a different set of tasks. The job now is to weigh them, commit, and execute.',
    ],
    readings: [
      { label: 'window', value: '14 days' },
      { label: 'warm contacts', value: '~200' },
      { label: 'budget', value: 'illustrative: < $2k' },
      { label: 'team size', value: '2–3 people' },
    ],
    tags: ['strategy','timeline','decision'],
    weight: 1,
  },
  {
    id: 'q-audience',
    type: 'question',
    title: 'Who are we actually building for?',
    catalog: 'ST-002 · QUESTION',
    family: 'question',
    summary: 'The product serves two adjacent audiences with overlapping needs but very different acquisition channels.',
    body: [
      'Early interviews split roughly 60/40 between independent creators who want simplicity and small teams who want control. The messaging that excites one group bores the other. Picking a primary audience for the launch changes the copy, the pricing, the channels, and the proof you lead with.',
      'This is not a positioning exercise for the next year. It is a decision about the first 100 users — who they are, and what promise you make them on day one.',
    ],
    readings: [
      { label: 'split', value: '60% solo / 40% small team' },
      { label: 'interviews', value: '18 conducted' },
      { label: 'open question', value: 'primary persona' },
    ],
    tags: ['audience','research','positioning'],
    weight: 0.88,
  },

  // ── ALTERNATIVES ──
  {
    id: 'alt-lean',
    type: 'alternative',
    title: 'Lean Public Launch',
    catalog: 'ST-010 · ALTERNATIVE A',
    family: 'alternatives',
    summary: 'Ship publicly on day 3, learn in the open, iterate daily. Maximum learning speed, maximum exposure.',
    body: [
      'The argument for Lean is tempo. You announce early, publish a short manifesto, open the product to anyone with a link, and treat the first week as a public beta. Every conversation becomes user research. The team at Linear and the early days of Figma both followed recognisable variants of this — loud, fast, and honest about rough edges.',
      'The cost is polish. First impressions form fast, and a public launch that feels half-baked can close doors that a slower approach would keep open. Support load also spikes immediately, which is hard to manage with a two-person team.',
    ],
    readings: [
      { label: 'ship date', value: 'day 3' },
      { label: 'public from', value: 'day 3 · open link' },
      { label: 'learning speed', value: 'high — daily iterations' },
      { label: 'team load', value: 'high support + build' },
    ],
    tags: ['speed','openness','learning'],
    weight: 0.92,
  },
  {
    id: 'alt-community',
    type: 'alternative',
    title: 'Community-First Rollout',
    catalog: 'ST-011 · ALTERNATIVE B',
    family: 'alternatives',
    summary: 'Seed with 30 hand-picked users, run a tight feedback loop, then expand in waves. Slower start, warmer reception.',
    body: [
      'This path treats distribution as a community craft. You invite a small, specific group — people who already feel the pain, who you can talk to directly — and give them disproportionate attention. Notion’s early ambassadors and the invite mechanics of Superhuman both built durable advocacy this way.',
      'It trades speed for depth. The launch feels intentional rather than loud, which earns trust, but it also means no public momentum until week two. If the private cohort does not convert into advocates, the timeline slips with no external signal to course-correct on.',
    ],
    readings: [
      { label: 'seed cohort', value: '30 hand-picked' },
      { label: 'public from', value: 'day 10 · wave 2' },
      { label: 'learning speed', value: 'medium — cohort depth' },
      { label: 'team load', value: 'medium — concierge' },
    ],
    tags: ['community','trust','advocacy'],
    weight: 0.9,
  },
  {
    id: 'alt-stealth',
    type: 'alternative',
    title: 'Stealth Premium',
    catalog: 'ST-012 · ALTERNATIVE C',
    family: 'alternatives',
    summary: 'Launch quietly to 10 design partners at a premium price. Prove willingness to pay first, scale later.',
    body: [
      'The thesis here is that price is a filter, not just revenue. A small number of customers paying meaningfully is stronger validation than a large number paying nothing — and it funds the next iteration. The team at Linear, Descript, and a handful of B2B tools launched this way, deliberately pricing high to find the customers who hurt most.',
      'The risk is silence. Without public energy the product can feel invisible, which makes hiring, press, and second-wave distribution harder. It also demands confidence in the pricing, which the team has not yet validated at this level.',
    ],
    readings: [
      { label: 'design partners', value: '10 at premium' },
      { label: 'public from', value: 'day 14+ · waitlist' },
      { label: 'learning speed', value: 'low — depth over breadth' },
      { label: 'team load', value: 'low — focused' },
    ],
    tags: ['premium','validation','pricing'],
    weight: 0.86,
  },

  // ── CLAIMS ──
  {
    id: 'claim-speed-wins',
    type: 'claim',
    title: 'Speed of learning beats polish at this stage',
    catalog: 'ST-020 · CLAIM',
    family: 'evidence',
    summary: 'For products with <1k users, the team that ships daily learns an order of magnitude faster than the team that polishes.',
    body: [
      'This claim shows up consistently across post-mortems of successful launches. The mechanism is straightforward: each day in the wild produces conversations that no amount of internal debate can simulate. The faster the loop, the fewer assumptions survive untested.',
      'It is not universally true. In categories where trust is paramount — finance, health, education — polish signals safety and early roughness actively damages adoption. Whether this product falls into that category is contested.',
    ],
    readings: [
      { label: 'claim type', value: 'learning advantage' },
      { label: 'confidence', value: 'strong — pattern across cases' },
      { label: 'contested', value: 'does trust category apply?' },
    ],
    tags: ['learning','speed','trust'],
    weight: 0.84,
  },
  {
    id: 'claim-community-compounds',
    type: 'claim',
    title: 'A cared-for cohort compounds into distribution',
    catalog: 'ST-021 · CLAIM',
    family: 'evidence',
    summary: '30 enthusiastic users create more distribution than 3,000 indifferent sign-ups — if the loop is designed for advocacy.',
    body: [
      'The compounding argument is that distribution is not a funnel but a network. One user who feels deeply understood and visibly influences the product tells ten people with credibility that advertising cannot buy. This is the logic behind Notion’s campus ambassadors and Figma’s early community program.',
      'It only works when the product is ready to be co-shaped. If the team cannot respond quickly to the cohort’s input, the advantage collapses and the exclusivity becomes frustration.',
    ],
    readings: [
      { label: 'claim type', value: 'network effect' },
      { label: 'requires', value: 'ready to co-shape' },
      { label: 'risk if slow', value: 'exclusivity → frustration' },
    ],
    tags: ['advocacy','network','community'],
    weight: 0.81,
  },
  {
    id: 'claim-price-signals',
    type: 'claim',
    title: 'Premium pricing filters for real pain',
    catalog: 'ST-022 · CLAIM',
    family: 'evidence',
    summary: 'Asking for real money immediately separates curiosity from commitment — and the conversations are higher quality.',
    body: [
      'Free users and paying users behave differently. Free users request features; paying users report problems they will churn over. The signal quality is so different that some teams consider free feedback actively misleading — it optimises for breadth of appeal rather than depth of utility.',
      'The counter-claim is that premature pricing filters too aggressively. If the product is not yet delivering its core promise reliably, charging early can feel extractive and damage the very trust a small team needs most.',
    ],
    readings: [
      { label: 'signal gap', value: 'paid ≫ free quality' },
      { label: 'filter', value: 'curiosity vs commitment' },
      { label: 'danger', value: 'feels extractive if early' },
    ],
    tags: ['pricing','validation','signal'],
    weight: 0.79,
  },

  // ── EVIDENCE ──
  {
    id: 'ev-interviews',
    type: 'evidence',
    title: '18 user interviews — pain patterns',
    catalog: 'ST-030 · EVIDENCE',
    family: 'evidence',
    summary: 'Semi-structured interviews with solo creators and small teams, focused on current workflow and willingness to switch.',
    body: [
      'The interviews were coded for pain frequency. The most common theme (12/18) was not missing features but scattered context — people manage their work across 4–7 tools and lose time to re-assembly rather than to any single tool’s limitation. The second theme (9/18) was decision fatigue: choosing between tools takes longer than doing the work.',
      'Willingness to try something new was high (14/18) but willingness to pay immediately was lower (5/18) — and those five clustered among the small-team segment, not the solo creators. The product’s promise of “one place that adapts to how you work” resonated most with the small-team group (7/8) and least with those already heavily systemised (2/6).',
    ],
    readings: [
      { label: 'sample', value: '18 · semi-structured' },
      { label: 'top pain', value: 'scattered context (12/18)' },
      { label: 'willing to try', value: '14/18' },
      { label: 'willing to pay now', value: '5/18 · clustered small-team' },
    ],
    tags: ['research','pain','audience'],
    weight: 0.88,
  },
  {
    id: 'ev-landing-test',
    type: 'evidence',
    title: 'Landing page test — 3 message variants',
    catalog: 'ST-031 · EVIDENCE',
    family: 'evidence',
    summary: 'A 4-day test with ~$180 spend, comparing three value propositions to measure click-through and waitlist conversion.',
    body: [
      'Three landing pages were tested with identical design and different headlines: (A) “The workspace that learns how you work”, (B) “Stop rebuilding your workspace”, (C) “One place for every decision”. Variant A had the highest click-through (3.1% vs 1.8% and 1.4%) but the lowest conversion to waitlist (8% vs 14% and 11%).',
      'The interpretation is that A attracts curiosity but sets an expectation the current product cannot fully meet — it promises adaptation, which the product delivers gradually. Variants B and C attracted fewer but more committed visitors. The team has not yet tested pricing on the landing page.',
    ],
    readings: [
      { label: 'spend', value: '~$180 · 4 days' },
      { label: 'winner CTR', value: 'A: 3.1%' },
      { label: 'winner conversion', value: 'B: 14%' },
      { label: 'learning', value: 'curiosity ≠ commitment' },
    ],
    tags: ['messaging','acquisition','testing'],
    weight: 0.82,
  },
  {
    id: 'ev-competitor-pricing',
    type: 'evidence',
    title: 'Competitor pricing scan — 12 tools',
    catalog: 'ST-032 · EVIDENCE',
    family: 'evidence',
    summary: 'Desk research on direct and adjacent tools: free tiers, entry pricing, and the narrative they use to justify paid plans.',
    body: [
      'Of 12 tools in the consideration set, 9 offer a free tier and 5 charge $10–$20/mo at entry. Only 2 charge more than $30 at the low end — both positioned as “professional” tools with explicit team features. The narrative common to higher-priced tools is not “more features” but “less work”: they promise to remove meetings, reduce context-switching, or eliminate a category of admin.',
      'No direct competitor claims to adapt its interface to the user. This is either a meaningful differentiation or a message that will require significant education — there is no existing mental model for buyers to map it to.',
    ],
    readings: [
      { label: 'tools scanned', value: '12' },
      { label: 'free tier', value: '9/12 offer one' },
      { label: 'entry price', value: '$10–20/mo typical' },
      { label: 'unique claim', value: 'no competitor does adaptive UI' },
    ],
    tags: ['pricing','competition','differentiation'],
    weight: 0.8,
  },
  {
    id: 'ev-waitlist-signals',
    type: 'evidence',
    title: 'Waitlist — 47 sign-ups, qualitative notes',
    catalog: 'ST-033 · EVIDENCE',
    family: 'evidence',
    summary: 'An organic waitlist built over 3 weeks via personal outreach and a small Twitter thread. 11 people wrote more than one sentence about why.',
    body: [
      'The waitlist grew without paid acquisition — mostly through the founder’s personal network and a single thread that reached ~3k impressions. Of 47 sign-ups, 11 left detailed notes, and 7 of those used language like “exactly what I need” or described a specific workflow they currently do manually.',
      'However, 3 of those 7 also described workflows the product handles only partially. The gap between expectation and current capability is real, and the enthusiastic segment is not cleanly predictive of retention. Two sign-ups asked about enterprise features that are explicitly out of scope.',
    ],
    readings: [
      { label: 'sign-ups', value: '47 · 3 weeks organic' },
      { label: 'detailed notes', value: '11/47' },
      { label: 'strong fit', value: '7/11 detailed' },
      { label: 'misalignment', value: '3/7 strong-fit · partial coverage' },
    ],
    tags: ['distribution','fit','expectation'],
    weight: 0.78,
  },
  {
    id: 'ev-team-capacity',
    type: 'evidence',
    title: 'Team capacity audit — honest accounting',
    catalog: 'ST-034 · EVIDENCE',
    family: 'evidence',
    summary: 'A realistic assessment of what 2–3 people can ship and support in 14 days without burning out or breaking promises.',
    body: [
      'The team estimated they can handle ~15 meaningful conversations per day alongside building, or ~40 per day if they pause building. Public launch load is estimated at 50–80 inbound per day for the first 3 days based on comparable launches. This suggests a lean public launch would require either pre-written support material that does not yet exist, or accepting slow replies that risk first-impression damage.',
      'Community-first and stealth paths both fit within the 15-conversation/day capacity. Both were rated as “sustainable with current energy” in a direct team question; lean public was rated “possible but anxious” by two of three team members.',
    ],
    readings: [
      { label: 'daily capacity', value: '~15 deep convos + build' },
      { label: 'public estimate', value: '50–80/day · first 3 days' },
      { label: 'team sentiment', value: '2/3 anxious on lean' },
      { label: 'sustainable', value: 'community + stealth only' },
    ],
    tags: ['capacity','load','team'],
    weight: 0.85,
  },

  // ── CRITERIA ──
  {
    id: 'crit-speed',
    type: 'criterion',
    title: 'Speed to learning',
    catalog: 'ST-040 · CRITERION',
    family: 'criteria',
    summary: 'How quickly we generate real signal about what to build next — measured in meaningful user conversations per day.',
    body: [
      'If the product’s thesis is uncertain — and it is, particularly around the audience split and pricing tolerance — then the speed at which we learn outweighs polish. This criterion favours the alternative that creates the most feedback surface area, fastest.',
      'It does not mean speed at any cost. Support debt and first-impression damage can slow learning by contaminating the signal with complaints about experience rather than the core value proposition.',
    ],
    readings: [
      { label: 'scoring', value: 'lean 9 · community 6 · stealth 4' },
      { label: 'unit', value: 'convos/day · illustrative' },
      { label: 'caveat', value: 'signal quality ≠ signal quantity' },
    ],
    tags: ['learning','tempo','signal'],
    weight: 0.86,
  },
  {
    id: 'crit-cost',
    type: 'criterion',
    title: 'Capital & team cost',
    catalog: 'ST-041 · CRITERION',
    family: 'criteria',
    summary: 'Real money out and real energy spent — weighted so sustainable choices score higher than heroic ones.',
    body: [
      'The budget constraint is illustrative (under $2k) but the team constraint is absolute: two people with existing commitments. A launch strategy that requires sustained heroics is not just tiring, it is fragile — one illness, one outage, one bad day can stall the whole plan.',
      'Cost here includes emotional cost. The community-first path was the only one the team described without using anxiety-coded language in interviews. That is data, not softness.',
    ],
    readings: [
      { label: 'scoring', value: 'stealth 9 · community 7 · lean 4' },
      { label: 'hard limit', value: '2 people · sustained' },
      { label: 'soft signal', value: 'anxiety = information' },
    ],
    tags: ['cost','sustainability','team'],
    weight: 0.8,
  },
  {
    id: 'crit-distribution',
    type: 'criterion',
    title: 'Distribution potential',
    catalog: 'ST-042 · CRITERION',
    family: 'criteria',
    summary: 'The likelihood that this launch creates advocates who bring the next wave — not just users who try it once.',
    body: [
      'A launch that produces satisfied users is good; one that produces advocates is geometrically better. The question here is which path most reliably creates people who feel ownership over the product and tell others with personal credibility.',
      'Community-first scores highest here by design — its entire mechanism is advocacy. Stealth premium also scores well because paying customers advocate more reliably than free ones, but the base is smaller. Lean distributes widely but shallowly, relying on volume rather than depth.',
    ],
    readings: [
      { label: 'scoring', value: 'community 9 · stealth 7 · lean 5' },
      { label: 'mechanism', value: 'ownership → word-of-mouth' },
      { label: 'trade-off', value: 'depth vs reach' },
    ],
    tags: ['distribution','advocacy','growth'],
    weight: 0.84,
  },
  {
    id: 'crit-risk',
    type: 'criterion',
    title: 'Downside & reversibility',
    catalog: 'ST-043 · CRITERION',
    family: 'criteria',
    summary: 'If the launch goes badly, how bad is it — and can we undo it? Paths that are easy to reverse score higher.',
    body: [
      'A public launch is largely irreversible: the first impression is set, the narrative is public, and a retreat reads as failure. A community pilot and a stealth premium both preserve the option to re-launch publicly once the product and message are stronger — they are staged, not final. This option value is worth explicitly scoring.',
      'This criterion captures what the other criteria miss: the asymmetry of disappointment. For this product, losing 30 potential users to slow replies costs more than gaining 30 indifferent sign-ups earns.',
    ],
    readings: [
      { label: 'scoring', value: 'stealth 9 · community 8 · lean 3' },
      { label: 'reversibility', value: 'public = irreversible' },
      { label: 'asymmetry', value: 'loss > gain at this size' },
    ],
    tags: ['risk','option-value','reversibility'],
    weight: 0.82,
  },

  // ── RISKS ──
  {
    id: 'risk-visibility',
    type: 'risk',
    title: 'Premature visibility burns the second launch',
    catalog: 'ST-050 · RISK',
    family: 'risks',
    summary: 'Going public early consumes the novelty that a bigger launch later would need. No second first impression.',
    body: [
      'Press, community hunters, and the warm contact list each have a single novelty budget. If the product is public while still rough, those channels produce a muted response that is hard to revive. Several comparable products that launched loudly too early later found their second launch met with “oh, we tried that” rather than curiosity.',
      'Mitigation is staging: a community pilot lets you spend a small amount of novelty on learning; the public novelty is preserved for when the product earns it. The lean path is the only one that spends all the novelty on day 3.',
    ],
    readings: [
      { label: 'severity', value: 'high — novelty is finite' },
      { label: 'likelihood', value: 'medium — depends on polish' },
      { label: 'mitigated by', value: 'community, stealth' },
    ],
    tags: ['visibility','novelty','timing'],
    weight: 0.78,
  },
  {
    id: 'risk-misprice',
    type: 'risk',
    title: 'Mis-pricing alienates the right early users',
    catalog: 'ST-051 · RISK',
    family: 'risks',
    summary: 'Charging too much too early filters out the users whose feedback would most improve the product.',
    body: [
      'The solo-creator segment — which is 60% of the interview sample — shows lower immediate willingness to pay but higher openness to co-creation. A premium price designed to find “serious” users may inadvertently select for people who want a finished tool rather than a work in progress. Those teams give poorer product feedback because they are buying, not building.',
      'This risk is concentrated in the stealth premium path. Community-first avoids it by decoupling access from price; lean avoids it by making access free.',
    ],
    readings: [
      { label: 'severity', value: 'medium — feedback quality' },
      { label: 'likelihood', value: 'medium-high — price untested' },
      { label: 'exposed path', value: 'stealth premium' },
    ],
    tags: ['pricing','filter','feedback'],
    weight: 0.74,
  },
  {
    id: 'risk-capacity-breach',
    type: 'risk',
    title: 'Support load overwhelms the team',
    catalog: 'ST-052 · RISK',
    family: 'risks',
    summary: 'If public inbound exceeds 15 quality conversations per day, building stops and replies slow — compounding into churn.',
    body: [
      'The capacity audit (ST-034) makes this concrete: public launch inbound is estimated at 50–80/day, capacity at ~15/day alongside building. Without pre-built support material, the team must choose between answering slowly or building slowly. Either choice is visible to the user and damages the same trust the launch is trying to create.',
      'This is not a hypothetical concern: 2 of 3 team members flagged this as their primary anxiety. An unmanageable support spike in the first week can consume the whole 14-day window in recovery.',
    ],
    readings: [
      { label: 'severity', value: 'high — window consumed' },
      { label: 'likelihood', value: 'high for lean · low otherwise' },
      { label: 'trigger', value: '>15 convos/day + building' },
    ],
    tags: ['capacity','load','burnout'],
    weight: 0.8,
  },
  {
    id: 'risk-echo-chamber',
    type: 'risk',
    title: 'The private cohort becomes an echo chamber',
    catalog: 'ST-053 · RISK',
    family: 'risks',
    summary: '30 hand-picked users who already like you tell you what you want to hear — optimising for applause, not truth.',
    body: [
      'Community-first carries a subtle distortion risk: the cohort is chosen for enthusiasm, not representativeness. Their requests may reflect a future that only they want, and the product can drift toward serving a small, vocal group rather than the broader market. Several products that did this discovered their product-market fit was with the pilot group alone.',
      'Mitigation requires deliberate counter-sampling: reserving slots for skeptics, tracking dissent, and testing the product with cold audiences before committing the full roadmap to the cohort’s preferences.',
    ],
    readings: [
      { label: 'severity', value: 'medium — roadmap drift' },
      { label: 'likelihood', value: 'medium — selection bias' },
      { label: 'mitigation', value: 'counter-sample skeptics' },
    ],
    tags: ['bias','feedback','sampling'],
    weight: 0.72,
  },

  // ── TASKS ──
  {
    id: 'task-message',
    type: 'task',
    title: 'Lock the launch message',
    catalog: 'ST-060 · TASK',
    family: 'tasks',
    summary: 'One paragraph that answers: who is this for, what does it do, and why now. No hedging.',
    body: [
      'Everything downstream — the landing page, the personal outreach, the onboarding — branches from this paragraph. Until it exists, no asset can be built with confidence, and the team keeps re-debating in every meeting. The landing page test (ST-031) suggests that sharper, narrower messaging converts better than broad curiosity.',
      'Time estimate: 2 hours of writing, 1 hour of review with two disconfirming voices (one skeptic, one ideal user).',
    ],
    readings: [
      { label: 'estimate', value: '3h · day 1' },
      { label: 'blocks', value: 'landing page, outreach copy' },
      { label: 'needs', value: 'audience decision (ST-002)' },
    ],
    tags: ['copy','positioning','blocking'],
    weight: 0.82,
    status: 'todo',
  },
  {
    id: 'task-waitlist-triage',
    type: 'task',
    title: 'Triage the 47-person waitlist',
    catalog: 'ST-061 · TASK',
    family: 'tasks',
    summary: 'Score every waitlist entry for fit, separate true advocates from polite interest, draft personal invites.',
    body: [
      'The waitlist is the strongest distribution asset — 47 people who already opted in, 11 with detailed notes. Triage means reading each note, tagging for segment (solo vs small-team), scoring for enthusiasm and fit, and drafting a personal invitation that references what they actually said. Generic invites waste this asset.',
      'For community-first and stealth paths, this is the first real engagement. For lean public, it is validation that the organic interest is genuine.',
    ],
    readings: [
      { label: 'estimate', value: '2h · day 1–2' },
      { label: 'input', value: 'waitlist notes (ST-033)' },
      { label: 'output', value: '30 ranked invites' },
    ],
    tags: ['triage','outreach','distribution'],
    weight: 0.78,
    status: 'todo',
    dependsOn: ['task-message'],
  },
  {
    id: 'task-onboarding-flow',
    type: 'task',
    title: 'Design the first-10-minutes onboarding',
    catalog: 'ST-062 · TASK',
    family: 'tasks',
    summary: 'A new user should reach one moment of real value within 10 minutes, without a tutorial video.',
    body: [
      'The waitlist notes (ST-033) reveal that 3 of 7 enthusiastic users expect workflows the product only partially covers. Onboarding must therefore set its scope early — showing clearly what the product does in the first session, rather than promising everything and delivering confusion.',
      'The team has a draft onboarding but has not timed it, and has not tested it with cold users. The 10-minute bar is ambitious relative to current flow, which takes ~18 minutes in internal testing.',
    ],
    readings: [
      { label: 'estimate', value: '1 day · day 2–3' },
      { label: 'current time', value: '~18 min internal' },
      { label: 'target', value: '<10 min to value' },
    ],
    tags: ['onboarding','ux','scope'],
    weight: 0.8,
    status: 'todo',
    dependsOn: ['task-message'],
  },
  {
    id: 'task-pricing-page',
    type: 'task',
    title: 'Publish a real pricing page',
    catalog: 'ST-063 · TASK',
    family: 'tasks',
    summary: 'One plain page with 2–3 tiers, a short justification, and a clear answer to “what happens to my data if I leave?”',
    body: [
      'The competitor scan (ST-032) shows most tools anchor at $10–$20 entry; the team has not yet committed to where they sit. But without a pricing page, every sales conversation becomes a negotiation, and the product’s perceived professionalism drops. Even a waitlisted launch needs a pricing answer ready for when people ask.',
      'This task is independent of which launch alternative is chosen — all three need a pricing page — but the numbers change: community-first can offer founding pricing; stealth premium needs confident premium pricing; lean public can defer pricing longer.',
    ],
    readings: [
      { label: 'estimate', value: 'half day · day 3' },
      { label: 'tiers', value: '2–3 · plain language' },
      { label: 'required for', value: 'stealth most, lean least' },
    ],
    tags: ['pricing','trust','page'],
    weight: 0.74,
    status: 'todo',
    dependsOn: ['task-message'],
  },
  {
    id: 'task-pilot-ops',
    type: 'task',
    title: 'Set up pilot operations — templates & cadence',
    catalog: 'ST-064 · TASK',
    family: 'tasks',
    summary: 'Shared doc templates, a feedback intake form, and a weekly cadence so the private cohort feels like participants, not testers.',
    body: [
      'If the community-first or stealth path is chosen, the pilot itself needs operational design. How does the team collect feedback without losing it in chat? How often does the cohort hear what changed because of them? When does the cohort end? These are the mechanics that turn 30 invited users into a distribution engine rather than a support burden.',
      'For lean public, this task becomes lightweight: a single feedback form and a public changelog replace the full pilot ops.',
    ],
    readings: [
      { label: 'estimate', value: 'half day · day 2' },
      { label: 'critical for', value: 'community-first, stealth' },
      { label: 'lightweight for', value: 'lean' },
    ],
    tags: ['operations','pilot','cadence'],
    weight: 0.76,
    status: 'todo',
    dependsOn: ['task-waitlist-triage'],
  },
  {
    id: 'task-public-assets',
    type: 'task',
    title: 'Build public launch assets',
    catalog: 'ST-065 · TASK',
    family: 'tasks',
    summary: 'A short manifesto, 3 social posts, a 90-second demo, and a help doc that answers the 5 questions everyone asks.',
    body: [
      'Public assets are the same whether the launch is lean or staged — only the timing changes. Lean ships them on day 3; community-first on day 10; stealth on day 14+. Building them early means they sit ready, removing time pressure when the decision is made.',
      'The demo is the highest-effort item. It should show the work, not the interface chrome — 90 seconds of a real decision flowing through STRATA, narrated simply. Stock footage and abstract animations will actively undermine the product’s distinctiveness.',
    ],
    readings: [
      { label: 'estimate', value: '1.5 days · day 3–5' },
      { label: 'timing', value: 'built early, shipped per strategy' },
      { label: 'hardest part', value: '90s real-work demo' },
    ],
    tags: ['content','demo','launch'],
    weight: 0.85,
    status: 'todo',
    dependsOn: ['task-message', 'task-onboarding-flow', 'task-pricing-page'],
  },

  // ── NOTE / CONSTRAINT ──
  {
    id: 'note-stakeholder',
    type: 'note',
    title: 'Stakeholder note — Maya & Jon',
    catalog: 'ST-070 · NOTE',
    family: 'synthesis',
    summary: 'Two stakeholders with different risk tolerances. Maya favours bold public signal; Jon favours staged validation. Both need to be able to advocate for the chosen path.',
    body: [
      'Maya (advisor, former operator) has seen several products stall in “private pilot purgatory” and believes public momentum is hard to manufacture later. She is biased toward lean, and knows it. Jon (cofounder, engineering) has shouldered support crises before and knows viscerally what 80 inbound a day feels like with two people. He is biased toward community-first, and knows it.',
      'The right decision must give each a real reason to commit. If it is lean, Jon needs a concrete support plan he believes in. If it is community-first, Maya needs a public date she can put on a calendar. The decision brief must address both by name.',
    ],
    readings: [
      { label: 'maya bias', value: 'lean — fears pilot purgatory' },
      { label: 'jon bias', value: 'community — fears support crisis' },
      { label: 'needs', value: 'both must authentically advocate' },
    ],
    tags: ['stakeholder','advocacy','alignment'],
    weight: 0.76,
  },
  {
    id: 'note-constraint',
    type: 'note',
    title: 'Hard constraint — calendar & health',
    catalog: 'ST-071 · NOTE',
    family: 'synthesis',
    summary: 'A non-negotiable personal commitment on day 8 removes one team member for 48 hours. Any plan must survive this gap.',
    body: [
      'This is not a soft constraint. One person is unavailable for days 8–9, which leaves the remaining team at half capacity precisely when a lean launch would be in its highest inbound window. This was not factored into the initial “14 days” framing — it was discovered after the audit and changes the capacity math materially.',
      'Plans that concentrate risk in days 7–10 are therefore structurally weaker than they first appeared. This is the strongest factual argument for staging the launch outside that window.',
    ],
    readings: [
      { label: 'unavailable', value: 'days 8–9 · one person' },
      { label: 'capacity then', value: '50% · lean peak window' },
      { label: 'implication', value: 'avoid risk concentration day 7–10' },
    ],
    tags: ['constraint','calendar','capacity'],
    weight: 0.8,
  },

  // ── DECISION & OUTCOME ──
  {
    id: 'decision-draft',
    type: 'decision',
    title: 'Decision — leaning Community-First',
    catalog: 'ST-080 · DECISION',
    family: 'synthesis',
    summary: 'Pre-decision lean: Community-First scores highest on reversibility, distribution, and team sustainability — but the team has not yet fully committed.',
    body: [
      'On current scoring, Community-First wins on three of four criteria (distribution, cost, reversibility) while trailing on speed-to-learning. The risks that most concern the team — visibility burn, capacity breach — are both concentrated in Lean. Stealth premium was seriously considered for its option value but lost on feedback quality and the misprice risk.',
      'The open questions are: can the team define a public date that satisfies Maya, and can the cohort be counter-sampled to avoid echo chamber effects? If both answers are yes, the path is clear. If not, the decision re-opens and the scoring changes.',
      'This is not a final decision. The team is using STRATA itself to track the evidence — and this note will be updated when they record a formal verdict.',
    ],
    readings: [
      { label: 'leading score', value: 'community-first · 3/4 criteria' },
      { label: 'trailing', value: 'lean · speed only' },
      { label: 'open questions', value: 'public date + anti-echo' },
      { label: 'status', value: 'pre-decision · not final' },
    ],
    tags: ['decision','scoring','open'],
    weight: 0.9,
  },
  {
    id: 'outcome-brief',
    type: 'outcome',
    title: 'Launch Brief — v0.1 (draft)',
    catalog: 'ST-081 · OUTCOME',
    family: 'synthesis',
    summary: 'A one-page brief the team will use to coordinate the launch once the direction is locked. Currently in draft — tasks, owners, and dates are still moving.',
    body: [
      'The brief is the artifact every other entity produces. It has one paragraph of context, one chosen direction with its rationale, a week-by-week task sequence with dependencies, a named risk and mitigation per risk, and a single success metric for the 14-day window.',
      'Right now the brief points to Community-First, with a public expansion on day 10 and a support handoff plan that accounts for the day 8–9 gap. The success metric is “15 cohort members actively shape the product and 5 bring someone new” — a distribution metric, not a vanity metric. It will be finalised after the waitlist triage and the message lock.',
    ],
    readings: [
      { label: 'current direction', value: 'community-first (draft)' },
      { label: 'public expansion', value: 'day 10 · staged' },
      { label: 'success metric', value: '15 active · 5 bring new' },
      { label: 'status', value: 'draft · depends on 3 tasks' },
    ],
    tags: ['brief','coordination','metric'],
    weight: 0.84,
  },
];

export const ENTITY_BY_ID: Record<string, StrataEntity> = Object.fromEntries(
  ENTITIES.map(e => [e.id, e])
);

// ─── RELATIONS ────────────────────────────────────────────────────────────

export const RELATIONS: StrataRelation[] = [
  // Question layer
  { from: 'q-launch', to: 'q-audience', kind: 'related-to', note: 'The audience decision shapes the launch strategy.' },
  { from: 'q-launch', to: 'alt-lean', kind: 'related-to', note: 'One candidate answer to the central question.' },
  { from: 'q-launch', to: 'alt-community', kind: 'related-to', note: 'One candidate answer to the central question.' },
  { from: 'q-launch', to: 'alt-stealth', kind: 'related-to', note: 'One candidate answer to the central question.' },
  { from: 'q-audience', to: 'ev-interviews', kind: 'related-to', note: 'Audience interviews directly inform this question.' },

  // Alternatives evaluate against criteria
  { from: 'alt-lean', to: 'crit-speed', kind: 'evaluates', note: 'Lean scores highest on speed-to-learning (9/9).' },
  { from: 'alt-community', to: 'crit-distribution', kind: 'evaluates', note: 'Community scores highest on distribution (9/9).' },
  { from: 'alt-stealth', to: 'crit-risk', kind: 'evaluates', note: 'Stealth scores highest on reversibility (9/9).' },
  { from: 'alt-lean', to: 'crit-risk', kind: 'evaluates', note: 'Lean scores lowest on reversibility (3/9).' },
  { from: 'alt-stealth', to: 'crit-speed', kind: 'evaluates', note: 'Stealth scores lowest on learning speed (4/9).' },
  { from: 'alt-community', to: 'crit-cost', kind: 'evaluates', note: 'Community balances cost well (7/9).' },

  // Alternatives vs alternatives
  { from: 'alt-lean', to: 'alt-community', kind: 'contradicts', note: 'One spends public novelty immediately; the other preserves it.' },
  { from: 'alt-community', to: 'alt-stealth', kind: 'contradicts', note: 'One optimises for advocacy; the other for validation.' },
  { from: 'alt-lean', to: 'alt-stealth', kind: 'contradicts', note: 'One is loud and fast; the other quiet and priced high.' },

  // Claims support alternatives
  { from: 'claim-speed-wins', to: 'alt-lean', kind: 'supports', note: 'The speed argument is Lean’s strongest claim.' },
  { from: 'claim-community-compounds', to: 'alt-community', kind: 'supports', note: 'Compounding advocacy is Community’s engine.' },
  { from: 'claim-price-signals', to: 'alt-stealth', kind: 'supports', note: 'Price-as-filter supports Stealth premium.' },

  // Claims ↔ evidence
  { from: 'claim-speed-wins', to: 'ev-team-capacity', kind: 'contradicts', note: 'Team capacity evidence limits how fast Lean can actually go.' },
  { from: 'claim-community-compounds', to: 'ev-waitlist-signals', kind: 'supports', note: 'Waitlist signals suggest real advocates exist.' },
  { from: 'claim-price-signals', to: 'ev-interviews', kind: 'contradicts', note: 'Interviews show only 5/18 willing to pay now.' },

  // Evidence network
  { from: 'ev-interviews', to: 'ev-waitlist-signals', kind: 'related-to', note: 'Both study the same audience from different angles.' },
  { from: 'ev-landing-test', to: 'ev-competitor-pricing', kind: 'related-to', note: 'Messaging and pricing both inform positioning.' },
  { from: 'ev-interviews', to: 'ev-landing-test', kind: 'supports', note: 'Interview pains validate which landing message resonates.' },
  { from: 'ev-competitor-pricing', to: 'ev-waitlist-signals', kind: 'related-to', note: 'Pricing context vs observed demand.' },
  { from: 'ev-team-capacity', to: 'ev-waitlist-signals', kind: 'contradicts', note: 'Capacity limits what waitlist enthusiasm would demand.' },
  { from: 'ev-team-capacity', to: 'note-constraint', kind: 'supports', note: 'A capacity audit that hardens the calendar constraint.' },

  // Source-like grounding
  { from: 'ev-interviews', to: 'crit-distribution', kind: 'supports', note: 'Interview split informs which distribution path has believers.' },
  { from: 'ev-competitor-pricing', to: 'crit-cost', kind: 'evaluates', note: 'Pricing scan sets the cost-relevant market anchor.' },
  { from: 'ev-team-capacity', to: 'crit-cost', kind: 'evaluates', note: 'Capacity directly determines the cost scoring.' },
  { from: 'ev-landing-test', to: 'task-message', kind: 'supports', note: 'Landing test provides the input for the message lock.' },

  // Risks block alternatives
  { from: 'risk-visibility', to: 'alt-lean', kind: 'blocks', note: 'Lean burns the novelty a second launch would need.' },
  { from: 'risk-capacity-breach', to: 'alt-lean', kind: 'blocks', note: 'Support breach is the Lean-specific failure mode.' },
  { from: 'risk-misprice', to: 'alt-stealth', kind: 'blocks', note: 'Stealth lives or dies on pricing confidence.' },
  { from: 'risk-echo-chamber', to: 'alt-community', kind: 'blocks', note: 'Community needs explicit anti-echo sampling.' },
  { from: 'risk-visibility', to: 'risk-capacity-breach', kind: 'related-to', note: 'Both describe Lean-specific concentrated risk.' },
  { from: 'note-constraint', to: 'risk-capacity-breach', kind: 'supports', note: 'Calendar constraint makes capacity breach more likely.' },

  // Tasks & dependencies
  { from: 'task-message', to: 'q-audience', kind: 'depends-on', note: 'Message needs the audience decision.' },
  { from: 'task-waitlist-triage', to: 'task-message', kind: 'depends-on', note: 'Triage copy needs the locked message.' },
  { from: 'task-waitlist-triage', to: 'ev-waitlist-signals', kind: 'related-to', note: 'Triage is the action on the waitlist evidence.' },
  { from: 'task-onboarding-flow', to: 'task-message', kind: 'depends-on', note: 'Scope clarity comes from the message.' },
  { from: 'task-pricing-page', to: 'task-message', kind: 'depends-on', note: 'Pricing narrative shares the paragraph.' },
  { from: 'task-pricing-page', to: 'ev-competitor-pricing', kind: 'related-to', note: 'Pricing page is informed by the scan.' },
  { from: 'task-pilot-ops', to: 'task-waitlist-triage', kind: 'depends-on', note: 'Ops need the ranked cohort.' },
  { from: 'task-pilot-ops', to: 'risk-echo-chamber', kind: 'related-to', note: 'Ops design must mitigate echo chamber.' },
  { from: 'task-public-assets', to: 'task-message', kind: 'depends-on', note: 'Manifesto and posts all branch from the paragraph.' },
  { from: 'task-public-assets', to: 'task-onboarding-flow', kind: 'depends-on', note: 'Demo shows the onboarding flow.' },
  { from: 'task-public-assets', to: 'task-pricing-page', kind: 'depends-on', note: 'Assets reference pricing.' },

  // Synthesis layer
  { from: 'decision-draft', to: 'alt-community', kind: 'supports', note: 'Current leaning: community-first scores highest.' },
  { from: 'decision-draft', to: 'crit-risk', kind: 'evaluates', note: 'Decision is weighted heavily on reversibility.' },
  { from: 'decision-draft', to: 'note-constraint', kind: 'supports', note: 'Calendar gap is a hard input to the decision.' },
  { from: 'decision-draft', to: 'note-stakeholder', kind: 'related-to', note: 'Stakeholder alignment is an explicit decision input.' },
  { from: 'note-stakeholder', to: 'alt-lean', kind: 'related-to', note: 'Maya advocates for lean.' },
  { from: 'note-stakeholder', to: 'alt-community', kind: 'related-to', note: 'Jon leans community-first.' },
  { from: 'note-constraint', to: 'alt-lean', kind: 'blocks', note: 'Calendar gap directly undermines lean.' },
  { from: 'outcome-brief', to: 'decision-draft', kind: 'produces', note: 'The brief is produced by the decision.' },
  { from: 'outcome-brief', to: 'task-public-assets', kind: 'depends-on', note: 'Brief needs all assets ready.' },
  { from: 'outcome-brief', to: 'task-pilot-ops', kind: 'depends-on', note: 'Brief needs pilot ops defined.' },
  { from: 'outcome-brief', to: 'ev-team-capacity', kind: 'related-to', note: 'Brief must account for real capacity.' },

  // Cross-family synthesis
  { from: 'ev-interviews', to: 'alt-community', kind: 'supports', note: 'Interview enthusiasm suggests community path viability.' },
  { from: 'ev-landing-test', to: 'alt-lean', kind: 'supports', note: 'High CTR hints lean public could find an audience.' },
  { from: 'ev-competitor-pricing', to: 'claim-price-signals', kind: 'contradicts', note: 'Market pricing makes premium positioning harder.' },
  { from: 'claim-speed-wins', to: 'crit-speed', kind: 'supports', note: 'Claim provides theory behind the criterion.' },
  { from: 'risk-visibility', to: 'crit-distribution', kind: 'related-to', note: 'Visibility risk is the inverse of distribution hope.' },
];

export function neighboursOf(id: string): string[] {
  const out: string[] = [];
  for (const e of RELATIONS) {
    if (e.from === id) out.push(e.to);
    else if (e.to === id) out.push(e.from);
  }
  return out;
}

export function edgesOf(id: string): StrataRelation[] {
  return RELATIONS.filter(e => e.from === id || e.to === id);
}

export function entitiesOfType(type: EntityType): StrataEntity[] {
  return ENTITIES.filter(e => e.type === type);
}

export function entitiesOfFamily(family: FamilyId): StrataEntity[] {
  return ENTITIES.filter(e => e.family === family);
}

export const TAGS: string[] = Array.from(
  ENTITIES.reduce((acc, n) => { n.tags.forEach(t => acc.add(t)); return acc; }, new Set<string>())
).sort();

/** Degree = how connected */
export function degreeOf(id: string): number { return edgesOf(id).length; }

// ─── Compatibility shims — so existing engine/modes can use strata graph ───
export const NODES = ENTITIES;
export const EDGES = RELATIONS;
export const NODE_BY_ID = ENTITY_BY_ID;
// Type aliases for old Deep Field names
export type FieldNode = StrataEntity;
export type FieldEdge = StrataRelation;
export type EdgeKind = RelationKind;
export const EDGE_KIND_LABEL = RELATION_LABEL;
