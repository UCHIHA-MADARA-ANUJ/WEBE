/**
 * DEEP FIELD — the corpus.
 *
 * A connected graph of 35 objects, arranged so that any two of them are
 * reachable through a chain of typed relations. The Evolution Engine never
 * mutates these facts; it mutates the *arrangement* — which nodes surface
 * first, which are neighbours, what actions exist, and what shape the
 * interface takes while you move through them.
 */

export type FamilyId =
  | 'cosmology'
  | 'phenomena'
  | 'physics'
  | 'structures'
  | 'instruments'
  | 'frontier'
  | 'time';

export interface Family {
  id: FamilyId;
  label: string;
  hue: number; // base hue used by the constellation layout
  blurb: string;
}

export const FAMILIES: Record<FamilyId, Family> = {
  cosmology: {
    id: 'cosmology',
    label: 'Cosmology',
    hue: 196,
    blurb: 'The large-scale story: how the universe began and what it is made of.',
  },
  phenomena: {
    id: 'phenomena',
    label: 'Phenomena',
    hue: 28,
    blurb: 'Things that happen out there, observed as light, particles or pressure.',
  },
  physics: {
    id: 'physics',
    label: 'Physics',
    hue: 268,
    blurb: 'The rules everything obeys, and the places where they get extreme.',
  },
  structures: {
    id: 'structures',
    label: 'Structures',
    hue: 168,
    blurb: 'The architecture: stars, clusters, disks, filaments and voids.',
  },
  instruments: {
    id: 'instruments',
    label: 'Instruments',
    hue: 48,
    blurb: 'The machines and methods that let us argue with the sky.',
  },
  frontier: {
    id: 'frontier',
    label: 'Frontier',
    hue: 320,
    blurb: 'Open questions, unresolved conflicts, and the things we cannot explain yet.',
  },
  time: {
    id: 'time',
    label: 'Time',
    hue: 210,
    blurb: 'Clocks, horizons and the strange arithmetic of looking backwards.',
  },
};

export const FAMILY_ORDER: FamilyId[] = [
  'cosmology',
  'phenomena',
  'physics',
  'structures',
  'instruments',
  'frontier',
  'time',
];

export interface Reading {
  label: string;
  value: string;
}

export interface FieldNode {
  id: string;
  title: string;
  catalog: string;
  family: FamilyId;
  summary: string;
  body: string[];
  readings: Reading[];
  tags: string[];
  /** 0..1 — how much light this object throws on the others. */
  weight: number;
}

export interface FieldEdge {
  from: string;
  to: string;
  kind: EdgeKind;
  note: string;
}

export type EdgeKind =
  | 'origin-of'
  | 'evidence-for'
  | 'powered-by'
  | 'revealed-by'
  | 'measured-by'
  | 'hosts'
  | 'contrasts-with'
  | 'sibling-of'
  | 'causes'
  | 'scales-to';

export const EDGE_KIND_LABEL: Record<EdgeKind, string> = {
  'origin-of': 'origin of',
  'evidence-for': 'evidence for',
  'powered-by': 'powered by',
  'revealed-by': 'revealed by',
  'measured-by': 'measured by',
  hosts: 'hosts',
  'contrasts-with': 'contrasts with',
  'sibling-of': 'sibling of',
  causes: 'causes',
  'scales-to': 'scales to',
};

export const NODES: FieldNode[] = [
  {
    id: 'cmb',
    title: 'Cosmic Microwave Background',
    catalog: 'DF-001 · COSMOLOGY',
    family: 'cosmology',
    summary: 'The afterglow of creation still filling the sky at 2.7 kelvin.',
    body: [
      '380,000 years after the Big Bang the universe cooled enough for electrons and protons to bind into neutral hydrogen. Light decoupled from matter at that moment and has been travelling ever since, stretched by expansion into microwaves. It is the oldest light we can see, and the reason we can draw the universe’s first map.',
      'The temperature is astonishingly uniform — around 2.725 K, varying by only a few parts in 100,000. Those tiny ripples are not noise. They are the frozen sound waves of the primordial plasma, and they encode the exact recipe for everything that followed: how much matter, how fast expansion, when dark energy took over.',
    ],
    readings: [
      { label: 'temperature', value: '2.725 K' },
      { label: 'release', value: '380,000 yr after t₀' },
      { label: 'anisotropy', value: 'ΔT/T ≈ 10⁻⁵' },
      { label: 'age of light', value: '13.8 Gyr' },
    ],
    tags: ['origin', 'light', 'evidence', 'expansion'],
    weight: 1,
  },
  {
    id: 'inflation',
    title: 'Inflation',
    catalog: 'DF-002 · COSMOLOGY',
    family: 'cosmology',
    summary: 'A fraction of a second in which the universe multiplied itself enormously.',
    body: [
      'Inflation proposes that between roughly 10⁻³⁶ and 10⁻³² seconds, space expanded by a factor of at least 10²⁸. It was proposed in 1981 as a solution to three problems at once: why the universe is flat, why regions of opposite sky have the same temperature, and where quantum fluctuations came from.',
      'Those quantum fluctuations are the mechanism. Inflated space stretched a microscopic foam of random energy into cosmic scales, and the slight density excesses in that foam became galaxies. Inflation is still an hypothesis — the search for its signature is a polarization signal called B-mode, and the detection remains unconfirmed.',
    ],
    readings: [
      { label: 'duration', value: '10⁻³⁶ – 10⁻³² s' },
      { label: 'expansion factor', value: '≥ 10²⁸' },
      { label: 'purpose', value: 'flatten + seed' },
      { label: 'signature', value: 'B-mode polarisation' },
    ],
    tags: ['origin', 'expansion', 'quantum', 'frontier'],
    weight: 0.86,
  },
  {
    id: 'big-bang',
    title: 'The Big Bang',
    catalog: 'DF-003 · COSMOLOGY',
    family: 'cosmology',
    summary: 'Not an explosion but an expansion of space itself, still running.',
    body: [
      'The name is a misnomer that stuck. There was no blast in a pre-existing void; there was space, densely packed and hot, and it has been expanding ever since. The expansion is the single most consequential fact in cosmology because it means every distant galaxy is also a past version of its neighbour.',
      'The timeline compresses hard. In the first 10⁻⁴³ seconds the universe was a plasma too hot to describe with current physics. By 20 minutes, protons and neutrons had fused into the first nuclei — mostly hydrogen, some helium, traces of lithium — in a ratio that still matches the oldest stars we can see.',
    ],
    readings: [
      { label: 'current age', value: '13.797 ± 0.023 Gyr' },
      { label: 'nucleosynthesis', value: '3 – 20 min' },
      { label: 'H : He', value: '3 : 1 by mass' },
      { label: 'recombination', value: '380,000 yr' },
    ],
    tags: ['origin', 'density', 'expansion', 'light'],
    weight: 1,
  },
  {
    id: 'dark-matter',
    title: 'Dark Matter',
    catalog: 'DF-004 · COSMOLOGY',
    family: 'cosmology',
    summary: 'Five times more matter than everything we can see, and we only know it by its shadow.',
    body: [
      'Rotation curves were the first clue. Spiral galaxies rotate far faster at their edges than the visible mass allows, as though something invisible is holding them together. Then lensing, then the Bullet Cluster — where two clusters passed through each other and the dark component clearly did not interact with itself.',
      'The standard candidate is cold dark matter: a slow-moving, electromagnetically neutral particle. We have not found it. The searches have narrowed to a shrinking window of masses, and the field now also considers primordial black holes, axions, and sterile neutrinos. The Bullet Cluster system is the cleanest evidence, because two colliding dark halos stayed spatially separated from the two colliding gas clouds.',
    ],
    readings: [
      { label: 'share of energy', value: '≈ 27%' },
      { label: 'ratio to visible', value: '5 : 1' },
      { label: 'best direct test', value: 'Bullet Cluster 1E 0657' },
      { label: 'status', value: 'undetected directly' },
    ],
    tags: ['dark', 'gravity', 'frontier', 'evidence'],
    weight: 0.95,
  },
  {
    id: 'dark-energy',
    title: 'Dark Energy',
    catalog: 'DF-005 · COSMOLOGY',
    family: 'cosmology',
    summary: 'The name for whatever is stretching the universe apart faster and faster.',
    body: [
      'Supernova surveys in 1998 found distant Type Ia supernovae dimmer than expected. The universe was not slowing down in its expansion — it was accelerating. Whatever causes that accounts for roughly 68% of all energy in the cosmos, which makes it the dominant component of everything.',
      'The simplest model is a cosmological constant, a constant energy density that stays the same as space expands. It is elegant and has a serious problem: its measured value is about 10⁻¹²⁰ in Planck units, and nothing in particle physics explains why it should be that small rather than 10⁵⁶ times larger. The coincidence is usually called the cosmological constant problem.',
    ],
    readings: [
      { label: 'share of energy', value: '≈ 68%' },
      { label: 'acceleration onset', value: 'z ≈ 0.6' },
      { label: 'model', value: 'Λ (cosmological const.)' },
      { label: 'problem', value: '120 orders of magnitude' },
    ],
    tags: ['dark', 'expansion', 'frontier', 'energy'],
    weight: 0.9,
  },
  {
    id: 'redshift',
    title: 'Redshift',
    catalog: 'DF-006 · PHENOMENA',
    family: 'phenomena',
    summary: 'The stretched fingerprint of a receding source — the ruler of the whole field.',
    body: [
      'A photon is stretched whenever the space it crosses is expanding. Define redshift as 1 + z = λ_observed / λ_emitted. A galaxy at z = 1 is not moving at twice light speed; it is at the boundary where the expansion itself is carrying it away faster than light.',
      'Measuring redshift is how we know how far away things are, and therefore how the universe has expanded over time. The Sandage–Loeb test settled the question of whether the expansion was an illusion: as the universe expands, the cobalt absorption line in a distant quasar’s spectrum drifts toward longer wavelengths, a change of a few parts in 10,000 that can only be explained by real expansion.',
    ],
    readings: [
      { label: 'definition', value: '1+z = λobs / λemit' },
      { label: 'Hubble era', value: 'z ≈ 0.1 – 0.3' },
      { label: 'expansion now', value: 'z = 0' },
      { label: 'oldest light', value: 'z ≈ 1100' },
    ],
    tags: ['light', 'expansion', 'measurement'],
    weight: 0.92,
  },
  {
    id: 'lensing',
    title: 'Gravitational Lensing',
    catalog: 'DF-007 · PHENOMENA',
    family: 'phenomena',
    summary: 'Mass bends light, so we can see things that are not there.',
    body: [
      'In 1912 Einstein predicted that light passing near a massive body is deflected by twice the Newtonian amount, and in 1919 two expeditions measured the deflection of starlight during a solar eclipse. It was one of the first observational confirmations of general relativity, and it turned gravity from a force into geometry.',
      'Strong lensing produces arcs, Einstein rings and multiple images; weak lensing subtly shears background galaxies. Weak lensing over large sky surveys is now one of the primary ways to map dark matter — it measures the mass, not the light. Lensing also lets us watch supernovae multiple times, and to weigh galaxy clusters from the separation of their images.',
    ],
    readings: [
      { label: 'deflection', value: '4GM / c²b' },
      { label: 'einstein ring', value: 'SDSS J1226+2149' },
      { label: 'uses', value: 'mass mapping, multiply-imaged SN' },
      { label: 'confirmed', value: '1919 eclipse' },
    ],
    tags: ['gravity', 'light', 'evidence', 'measurement'],
    weight: 0.88,
  },
  {
    id: 'quasar',
    title: 'Quasar',
    catalog: 'DF-008 · PHENOMENA',
    family: 'phenomena',
    summary: 'Galaxies powered by a black hole, bright enough to be seen across the observable universe.',
    body: [
      'A quasar is a galaxy whose central supermassive black hole is eating. As matter falls inward it heats to millions of kelvin and radiates across the spectrum, outshining the tens of billions of stars around it. Less than one percent of massive galaxies host an active nucleus at any given time.',
      'Quasars are also time machines. The most distant ones are seen as they were within a billion years of the Big Bang, meaning black holes grew to a billion solar masses in a period the universe had barely finished building the galaxies that host them. How they did that is an unsolved problem in high-energy astrophysics.',
    ],
    readings: [
      { label: 'host mass', value: '10⁹ M☉ supermassive' },
      { label: 'luminosity', value: 'up to 10⁴¹ W' },
      { label: 'redshift range', value: 'z ≈ 0.1 – 7' },
      { label: 'fraction of galaxies', value: '< 1% active' },
    ],
    tags: ['light', 'energy', 'galaxies', 'frontier'],
    weight: 0.9,
  },
  {
    id: 'pulsar',
    title: 'Pulsar',
    catalog: 'DF-009 · PHENOMENA',
    family: 'phenomena',
    summary: 'A lighthouse made of neutron star, ticking with millisecond precision.',
    body: [
      'A pulsar is a rapidly rotating neutron star whose misaligned magnetic field sweeps a beam of radio waves across the sky like a lighthouse. Jocelyn Bell Burnell noticed the first in 1967, in a chart of scintillation sources that looked like static. The word is a contraction of "pulsating radio source".',
      'Because the timing is so clean, pulsars became the best clocks in the universe and a laboratory for extreme physics. The Hulse–Taylor binary pulsar lost orbital energy exactly as general relativity predicted, an indirect confirmation of gravitational radiation, and earned the 1993 Nobel Prize. Millisecond pulsars in old binaries are neutron stars that have been spun up by transfer of angular momentum from a companion.',
    ],
    readings: [
      { label: 'fastest', value: 'PSR J1740−5340 · 1.4 ms' },
      { label: 'discovered', value: '1967' },
      { label: 'typical field', value: '10¹² G' },
      { label: 'signal', value: 'radio, optical, X-ray, γ' },
    ],
    tags: ['stars', 'light', 'cycles', 'time'],
    weight: 0.82,
  },
  {
    id: 'supernova',
    title: 'Supernova',
    catalog: 'DF-010 · PHENOMENA',
    family: 'phenomena',
    summary: 'The death of a star, and the reason we know how far away things are.',
    body: [
      'Type Ia supernovae are standard candles. Because a white dwarf has a hard mass ceiling, it detonates at nearly the same luminosity every time, and the dimming of that flash tells you exactly how far away it happened. Comparing Type Ia brightness against redshift revealed the accelerating expansion of the universe.',
      'Type II supernovae are core collapse: a massive star runs out of fuel, its iron core implodes, and the rebound shock flings the envelope outward at 10% of light speed. These are the universe’s heavy element factories. The Crab Nebula and SN 1987A — whose neutrinos arrived three hours before its light, as predicted — are the two we can study in detail.',
    ],
    readings: [
      { label: 'types', value: 'Ia (thermonuclear), II (collapse)' },
      { label: 'peak', value: '10⁹ × solar luminosity' },
      { label: 'elements made', value: 'up to iron-group' },
      { label: 'SNe seen', value: '> 10,000 since 1990' },
    ],
    tags: ['stars', 'light', 'measurement', 'cycles'],
    weight: 0.9,
  },
  {
    id: 'black-hole',
    title: 'Black Hole',
    catalog: 'DF-011 · PHYSICS',
    family: 'physics',
    summary: 'A region where the escape velocity exceeds the speed of light.',
    body: [
      'At the centre of every large galaxy sits a supermassive black hole, and at the centre of every large star sits a stellar one. Both are defined the same way: inside a radius called the Schwarzschild radius, no signal can get out. For a Sun-mass black hole that radius is about 3 km; for Sagittarius A*, 4.3 million solar masses, it is about 12 million km.',
      'The Event Horizon Telescope imaged the shadow of the black hole in M87 in 2019 and of Sagittarius A* in 2022, resolving emission about 20 times smaller than the light-crossing size of the event horizon. The rings matched general relativity’s predictions remarkably well, including the photon ring. Black holes remain the single best laboratory for quantum gravity, because the horizon is where general relativity and quantum mechanics must both apply.',
    ],
    readings: [
      { label: 'sgr a*', value: '4.3 × 10⁶ M☉' },
      { label: 'm87*', value: '6.5 × 10⁹ M☉' },
      { label: 'shadow imaged', value: '2019 / 2022' },
      { label: 'escape velocity', value: '> c' },
    ],
    tags: ['gravity', 'density', 'frontier', 'dark'],
    weight: 1,
  },
  {
    id: 'accretion-disk',
    title: 'Accretion Disk',
    catalog: 'DF-012 · PHYSICS',
    family: 'physics',
    summary: 'A whirlpool of gas, heated to millions of kelvin by falling into a black hole.',
    body: [
      'Gas cannot fall straight in. Angular momentum makes it orbit, and differential rotation makes it heat through friction and magnetic turbulence, radiating at X-ray and ultraviolet wavelengths. This is the engine room of an active galactic nucleus and of X-ray binaries.',
      'Some disks launch jets — collimated plasma streams that travel at relativistic speed for thousands of light years. M87’s jet is one of the most studied structures in the sky, and its 2017 EHT resolution showed the shadow sitting inside a ring of emission produced by the photon orbit, with the jet emerging from exactly that point.',
    ],
    readings: [
      { label: 'temperature', value: '10⁶ – 10⁷ K' },
      { label: 'timescale', value: 'hours to days' },
      { label: 'efficiency', value: 'up to ~40% of rest mass' },
      { label: 'jet speed', value: '≈ 0.99 c' },
    ],
    tags: ['energy', 'density', 'cycles', 'gravity'],
    weight: 0.85,
  },
  {
    id: 'hawking',
    title: 'Hawking Radiation',
    catalog: 'DF-013 · PHYSICS',
    family: 'physics',
    summary: 'The prediction that black holes are not black, and slowly leak themselves away.',
    body: [
      'In 1974 Stephen Hawking combined quantum field theory with curved spacetime and found that a black hole emits a thermal spectrum at a temperature inversely proportional to its mass. A solar-mass black hole would sit at roughly 6 × 10⁻⁸ K — colder than the cosmic microwave background, and so invisible in practice. A small black hole, in a collider or the early universe, would be hot.',
      'The deeper problem is the information paradox. If a black hole evaporates completely, where did the information in it go? Hawking’s own calculation says it is lost, which conflicts with quantum mechanics’ unitarity. The last few years have produced an increasingly convincing resolution using islands in quantum gravity and replica wormholes, reproducing the Page curve — but the argument is still theoretical.',
    ],
    readings: [
      { label: 'temperature', value: '6.3 × 10⁻⁸ K (1 M☉)' },
      { label: 'evaporation time', value: '10⁶⁷ yr (1 M☉)' },
      { label: 'proposed', value: '1974' },
      { label: 'open problem', value: 'information paradox' },
    ],
    tags: ['quantum', 'dark', 'frontier', 'time'],
    weight: 0.84,
  },
  {
    id: 'event-horizon',
    title: 'Event Horizon',
    catalog: 'DF-014 · PHYSICS',
    family: 'physics',
    summary: 'The boundary, not the object — and it is not a surface of solid matter.',
    body: [
      'The event horizon is a one-way membrane in spacetime. Nothing inside it can send anything out, but anything inside can still send light outward to the rest of the universe. It has no material structure, no temperature, no charge. It is a causal boundary, defined entirely by what could have happened.',
      'The event horizon is also global rather than local. The event horizon of the black hole in your galactic centre is a surface that is partly shaped by the entire future history of the universe, including the matter that will fall in centuries from now. Its area appears in the Hawking temperature and in the laws of black hole mechanics, which is why the same formula shows up in thermodynamics.',
    ],
    readings: [
      { label: 'solar schwarzschild r', value: '2.95 km' },
      { label: 'not a surface', value: 'no local signature' },
      { label: 'one-way', value: 'causal boundary' },
      { label: 'enters', value: 'Hawking temperature, area law' },
    ],
    tags: ['gravity', 'time', 'quantum', 'frontier'],
    weight: 0.8,
  },
  {
    id: 'neutron-star',
    title: 'Neutron Star',
    catalog: 'DF-015 · PHYSICS',
    family: 'physics',
    summary: 'A city-sized nucleus with a teaspoon of mass, and the densest thing we can make.',
    body: [
      'When a massive star’s core collapses, protons and electrons are crushed together into neutrons. What remains is roughly 20 kilometres across and around 1.4 solar masses — densities of 10¹² grams per cubic centimetre, where a teaspoon of material weighs about a billion tonnes. Above about 2.1 solar masses it collapses further, into a black hole.',
      'Neutron stars are the densest laboratories in the universe and the only ones we can visit in the sense that we hear them. Their radii, masses and tidal deformabilities, measured by NICER and by LIGO/Virgo, constrain the equation of state of ultradense matter — a test of how matter behaves when the protons and neutrons themselves stop being meaningful.',
    ],
    readings: [
      { label: 'radius', value: '≈ 10 – 13 km' },
      { label: 'mass', value: '1.0 – 2.1 M☉' },
      { label: 'density', value: '10¹² g/cm³' },
      { label: 'tightest binary', value: 'PSR J0740+6620 · 2.08 ms' },
    ],
    tags: ['density', 'stars', 'gravity', 'measurement'],
    weight: 0.86,
  },
  {
    id: 'magnetar',
    title: 'Magnetar',
    catalog: 'DF-016 · PHENOMENA',
    family: 'phenomena',
    summary: 'A neutron star with a magnetic field a quadrillion times Earth’s.',
    body: [
      'Most neutron stars have fields around 10¹² gauss. A magnetar has 10¹⁴ to 10¹⁵. SGR 1806-20, the most extreme known, has released an estimated 10⁴⁶ joules in a single second — briefly outshining the entire Milky Way, and briefly brighter than anything else in the sky since the Big Bang.',
      'The field is generated by the star’s violent spin-down, and it powers the soft gamma repeaters, whose short bursts are thought to be crust fractures like sheet tearing. Giant flares have been detected in every wavelength, and their tails revealed a dense magnetised wind in the Crab Nebula that was not in anyone’s model.',
    ],
    readings: [
      { label: 'field', value: '10¹⁴ – 10¹⁵ G' },
      { label: 'record flare', value: 'SGR 1806-20 · 10⁴⁶ J' },
      { label: 'duration', value: 'milliseconds' },
      { label: 'crack metaphor', value: 'neutron star crust fracture' },
    ],
    tags: ['stars', 'energy', 'density', 'cycles'],
    weight: 0.72,
  },
  {
    id: 'globular-cluster',
    title: 'Globular Cluster',
    catalog: 'DF-017 · STRUCTURES',
    family: 'structures',
    summary: 'A hundred thousand ancient stars, bound together in a sphere older than most galaxies.',
    body: [
      'Globular clusters are dense, roughly spherical swarms of 10⁵ to 10⁶ old red stars, orbiting their galactic centres in a halo. Harlow Shapley used the distances to them via variable stars to work out that the Sun was not at the centre of the galaxy — the centre is in Sagittarius, about 26,000 light years away, and our galaxy is one of many.',
      'They are fossil records. Their stars are among the oldest known, and their chemical composition tells us what the early universe was making. Most contain no gas at all, so no new stars form. A handful hide a concentration of intermediate-mass black holes in their centres, and a few host the densest star systems ever found — tidal captures of stars on collision courses.',
    ],
    readings: [
      { label: 'population', value: '10⁵ – 10⁶ stars' },
      { label: 'age', value: '12 – 13 Gyr' },
      { label: 'known in Milky Way', value: '150+' },
      { label: 'shapley', value: '1924 · galaxy centre found' },
    ],
    tags: ['stars', 'density', 'galaxies', 'time'],
    weight: 0.74,
  },
  {
    id: 'spiral-galaxy',
    title: 'Spiral Galaxy',
    catalog: 'DF-018 · STRUCTURES',
    family: 'structures',
    summary: 'A rotating disk of stars with a bright core, and the shape of our own address.',
    body: [
      'Spiral arms are not rigid structures that rotate with the disk. As early as the 1920s, measurements showed the arms move slower than the stars near the core — a density wave, like a traffic jam that holds its shape while cars pass through it. Star formation happens where the wave compresses gas.',
      'The spiral shape is a consequence of angular momentum: infalling gas carries angular momentum, forms a disk, and differential rotation winds up the arms. About two-thirds of bright galaxies are spirals, and a fraction of those are barred, including the Milky Way itself, whose core bar is visible in infrared surveys.',
    ],
    readings: [
      { label: 'disk thickness', value: '~1,000 ly' },
      { label: 'arm count', value: '2 – 5' },
      { label: 'our address', value: 'Milky Way, barred spiral' },
      { label: 'core distance', value: '26,000 ly' },
    ],
    tags: ['galaxies', 'cycles', 'formation', 'light'],
    weight: 0.84,
  },
  {
    id: 'nebula',
    title: 'Nebula',
    catalog: 'DF-019 · STRUCTURES',
    family: 'structures',
    summary: 'A cloud of gas, lit from within by the stars it is making.',
    body: [
      'Emission nebulae glow because ultraviolet light from hot newborn stars ionises the hydrogen around them and makes it re-emit. Reflection nebulae merely scatter starlight and look blue. Dark nebulae are dense enough to block the light of everything behind them — the Horsehead is a silhouette, and the Pillars of Creation are a column of dust in the Eagle Nebula.',
      'They are short-lived on a human scale. A giant molecular cloud collapsing into stars lives only a few million years before the radiation blows it apart, which is why star-forming regions look violent: the same clouds are the raw material and the thing that destroys them.',
    ],
    readings: [
      { label: 'types', value: 'emission / reflection / dark' },
      { label: 'scale', value: '10 – 300 ly' },
      { label: 'lifetime', value: '~10⁶ yr' },
      { label: 'famous', value: 'Orion, Eagle, Horsehead' },
    ],
    tags: ['stars', 'formation', 'light', 'density'],
    weight: 0.76,
  },
  {
    id: 'protoplanetary-disk',
    title: 'Protoplanetary Disk',
    catalog: 'DF-020 · STRUCTURES',
    family: 'structures',
    summary: 'The dusty pancake around a young star where planets are assembled.',
    body: [
      'A newborn star is surrounded by the remnant of the cloud it collapsed from: a rotating disk of gas and dust, only a few million years old. ALMA imaged HL Tau in 2015 and resolved concentric gaps carved by forming planets — the first direct evidence of planet formation caught in the act.',
      'Chemistry is the interesting part. The disk is cold enough for water, ammonia and methane to freeze onto dust grains, which move inward and deliver building blocks to the forming world. The snow line, at roughly 150 K in our own solar system, marks where water ice becomes stable and the composition of planets changes.',
    ],
    readings: [
      { label: 'resolved gaps', value: 'HL Tau · ALMA 2015' },
      { label: 'lifetime', value: '< 10⁷ yr' },
      { label: 'snow line', value: '≈ 150 K' },
      { label: 'our own', value: '4.6 Gyr ago' },
    ],
    tags: ['formation', 'planets', 'density', 'time'],
    weight: 0.78,
  },
  {
    id: 'exoplanet',
    title: 'Exoplanet',
    catalog: 'DF-021 · FRONTIER',
    family: 'frontier',
    summary: 'A planet orbiting a star other than our own — thousands of them, none in our image.',
    body: [
      'The first confirmed detections came in 1995 around a pulsar, then in the same year around 51 Pegasi — a hot Jupiter in a three-day orbit, and an uncomfortable place for a gas giant to be. Today the count is in the thousands and the population is stranger than anyone predicted: super-Earths, sub-Neptunes, and worlds in the gap between them.',
      'Two methods dominate. Transits watch for the tiny dimming as a planet crosses its star; radial velocity watches for the star’s wobble, detected by Doppler shift. Transits need luck with alignment but also yield the planet’s size; radial velocity yields mass. Together they give density — and density is how we tell a rock from a balloon.',
    ],
    readings: [
      { label: 'confirmed', value: '> 5,500' },
      { label: 'methods', value: 'transit + radial velocity' },
      { label: 'commonest', value: 'sub-Neptune' },
      { label: 'first', value: '51 Pegasi b · 1995' },
    ],
    tags: ['planets', 'frontier', 'light', 'measurement'],
    weight: 0.88,
  },
  {
    id: 'habitable-zone',
    title: 'Habitable Zone',
    catalog: 'DF-022 · FRONTIER',
    family: 'frontier',
    summary: 'The band around a star where a rocky world could hold liquid water.',
    body: [
      'The classic Goldilocks zone for a Sun-like star runs from roughly 0.95 to 1.37 AU, where surface temperatures might allow liquid water. Modern versions add tidal locking, atmospheric retention, magnetic fields and the long-term stability of the star itself. It is a filter, not a guarantee.',
      'Finding a candidate is cheap; proving it is not. JWST can measure atmospheric molecules for a handful of worlds, and the biosignature debate — whether a gas like dimethyl sulfide on a K2-18b means life — is where the field is going next. The real barrier is that we can only study planets that happen to align with our line of sight.',
    ],
    readings: [
      { label: 'sun-like zone', value: '0.95 – 1.37 AU' },
      { label: 'filters', value: 'tides, atmosphere, magnetism' },
      { label: 'spectroscopy', value: 'JWST transmission' },
      { label: 'caveat', value: 'alignment bias' },
    ],
    tags: ['planets', 'frontier', 'formation'],
    weight: 0.8,
  },
  {
    id: 'jwst',
    title: 'James Webb Space Telescope',
    catalog: 'DF-023 · INSTRUMENTS',
    family: 'instruments',
    summary: 'A 6.5-metre mirror at the second Lagrange point, staring at the first galaxies.',
    body: [
      'JWST is the largest telescope ever placed in space: a segmented 6.5 m primary mirror, gold-coated, operating at about 40 kelvin, parked 1.5 million km from Earth at L2 where the Sun, Earth and Moon always sit on the same side of its orbit.',
      'Its deepest field, from 12.5 hours of exposure, turned up galaxies at redshift 13 — light that left the universe 320 million years after the Big Bang, when it was 2% of its present age. It has also taken direct images of exoplanet atmospheres, measured winds on a brown dwarf, and taken the chemistry of a supernova remnant.',
    ],
    readings: [
      { label: 'mirror', value: '6.5 m segmented' },
      { label: 'position', value: 'L2 · 1.5e6 km' },
      { label: 'temperature', value: '≈ 40 K' },
      { label: 'deepest record', value: 'z ≈ 13' },
    ],
    tags: ['instruments', 'light', 'frontier', 'formation'],
    weight: 0.87,
  },
  {
    id: 'hubble',
    title: 'Hubble Space Telescope',
    catalog: 'DF-024 · INSTRUMENTS',
    family: 'instruments',
    summary: 'The instrument that turned the sky from a fog of points into a place with structure.',
    body: [
      'Launched in 1990 with a flawed mirror, Hubble was repaired in orbit five times — including the 1993 correction that made its optics essentially perfect. It delivered the deep field, the Hubble tuning fork of galaxy morphology, the Cepheid distances that pinned down the Hubble constant, and thousands of spectra.',
      'The Hubble constant is the one number the two most precise measurements disagree about. Hubble’s distance ladder puts it near 73 km/s/Mpc; the CMB under a flat ΛCDM model puts it near 67.4. The tension is real, and it may be evidence that the standard model of cosmology is incomplete. Hubble and JWST now overlap in the infrared, cross-calibrating the two.',
    ],
    readings: [
      { label: 'mirror', value: '2.4 m' },
      { label: 'launched', value: '1990' },
      { label: 'servicing missions', value: '5' },
      { label: 'H₀ tension', value: '73 vs 67.4' },
    ],
    tags: ['instruments', 'light', 'frontier', 'evidence'],
    weight: 0.84,
  },
  {
    id: 'chandra',
    title: 'Chandra X-ray Observatory',
    catalog: 'DF-025 · INSTRUMENTS',
    family: 'instruments',
    summary: 'The sharpest eye ever pointed at the hottest, most violent parts of the sky.',
    body: [
      'X-rays come from gas at millions of kelvin — accretion disks, shock fronts, cluster gas. Earth’s atmosphere absorbs them, so Chandra was designed to mirror them through nested grazing-incidence optics, achieving an angular resolution of about one arcsecond, roughly 1,000 times better than any earlier X-ray telescope.',
      'It found the Bullet Cluster separation that is today the strongest evidence for collisionless dark matter, it imaged the Cassiopeia A supernova remnant in three dimensions, and it can detect the hot halo of a galaxy cluster — a tracer of dark matter that is independent of lensing.',
    ],
    readings: [
      { label: 'orbit', value: 'highly elliptical, 139,000 km' },
      { label: 'resolution', value: '0.5″' },
      { label: 'band', value: '0.5 – 10 keV' },
      { label: 'famous target', value: 'Bullet Cluster' },
    ],
    tags: ['instruments', 'energy', 'evidence', 'measurement'],
    weight: 0.72,
  },
  {
    id: 'vlbi',
    title: 'Very Long Baseline Interferometry',
    catalog: 'DF-026 · INSTRUMENTS',
    family: 'instruments',
    summary: 'A telescope the size of Earth, stitched together from radio dishes across the planet.',
    body: [
      'Signals from separated telescopes are recorded against atomic clocks and combined, so the array resolves detail far finer than any single dish. The technique was developed in the 1960s, and the resulting radio sky — quasars with jets extending to light years, jets that appear to move faster than light because they are nearly pointed at us — redefined how jets were understood.',
      'The Event Horizon Telescope extended the technique to 1.3 mm, the size of a photon orbit around a supermassive black hole. Correlating eight facilities across four continents produced the first images of black hole shadows, in 2019 and 2022, and the technique is now being extended into space with a proposed space VLBI mission.',
    ],
    readings: [
      { label: 'baseline', value: 'Earth’s diameter' },
      { label: 'eht frequency', value: '1.3 mm' },
      { label: 'resolution', value: '~20 μas' },
      { label: 'first shadow', value: 'M87* · 2019' },
    ],
    tags: ['instruments', 'light', 'frontier', 'measurement'],
    weight: 0.75,
  },
  {
    id: 'ligo',
    title: 'Gravitational Wave Detectors',
    catalog: 'DF-027 · INSTRUMENTS',
    family: 'instruments',
    summary: 'Two 4-kilometre interferometers listening for the stretching of space itself.',
    body: [
      'LIGO’s arms are 4 km long vacuum tubes with mirrors hung at the ends. A passing gravitational wave stretches and squeezes the whole apparatus by a factor of about 10⁻²¹, and the light inside the interferometer reads that change. In September 2015 the two sites heard the same chirp: the merger of two black holes, 1.3 billion light years away.',
      'That chirp was also a new kind of telescope. Because gravitational waves travel at the speed of light and are not blocked by matter, LIGO and its partners Virgo and KAGRA can see through dust and through the interiors of stellar mergers. The detections have delivered masses of black holes that were thought impossible, and neutron star mergers that produced kilonova light and heavy gold.',
    ],
    readings: [
      { label: 'arm length', value: '4 km' },
      { label: 'strain sensitivity', value: '~10⁻²¹' },
      { label: 'first detection', value: 'GW150914 · 2015' },
      { label: 'now', value: '90+ candidates in O4' },
    ],
    tags: ['instruments', 'gravity', 'frontier', 'cycles'],
    weight: 0.83,
  },
  {
    id: 'grb',
    title: 'Gamma-Ray Burst',
    catalog: 'DF-028 · FRONTIER',
    family: 'frontier',
    summary: 'The brightest flashes in the universe, and the death rattle of massive stars.',
    body: [
      'A gamma-ray burst releases in seconds the energy output of the Sun over its entire lifetime. They come in two flavours: long ones lasting more than two seconds, tied to the collapse of massive stars in the collapsar model, and short ones under two seconds, from the merger of two compact objects.',
      'On 13 March 2008, GRB 080319B was bright enough to be seen with the naked eye from an Earth where the Sun was below the horizon, and its afterglow was seen for weeks — the light of a dying star that had travelled 7.5 billion light years. Gamma rays cannot be seen from the ground, so we have been listening to space since the 1960s, and the picture is still being revised.',
    ],
    readings: [
      { label: 'energy', value: '10⁵³ – 10⁵⁴ erg' },
      { label: 'duration', value: 'ms – hours' },
      { label: 'naked eye', value: 'GRB 080319B · 2008' },
      { label: 'types', value: 'collapsar / merger' },
    ],
    tags: ['light', 'energy', 'frontier', 'stars'],
    weight: 0.7,
  },
  {
    id: 'frb',
    title: 'Fast Radio Burst',
    catalog: 'DF-029 · FRONTIER',
    family: 'frontier',
    summary: 'Millisecond radio flashes from deep space — some of them repeating on a schedule.',
    body: [
      'Discovered by chance in 2007 in the archival data of a pulsar survey, a fast radio burst is a burst of radio energy lasting milliseconds, releasing as much energy in that instant as a modest solar flare over days. The mechanism was a puzzle until 2020, when one burst was traced to a magnetar in a nearby galaxy.',
      'But not all of them. Repeating sources with precise periodicities look like a binary neutron star whose companion is being tidally deformed. CHIME and the ASKAP telescope have catalogued thousands, and their distribution — mostly outside the Milky Way’s plane, and none in the Magellanic Clouds — is a clue to their true homes.',
    ],
    readings: [
      { label: 'duration', value: '~1 ms' },
      { label: 'energy', value: '10³⁸ – 10⁴¹ J' },
      { label: 'first repeater', value: 'FRB 121102' },
      { label: 'likely source', value: 'magnetar / binary' },
    ],
    tags: ['light', 'cycles', 'frontier', 'measurement'],
    weight: 0.71,
  },
  {
    id: 'cosmic-web',
    title: 'The Cosmic Web',
    catalog: 'DF-030 · STRUCTURES',
    family: 'structures',
    summary: 'Galaxies arranged in filaments and knots, with voids between them.',
    body: [
      'On the largest scales, matter is not scattered. Redshift surveys show a lacy network: sheets and filaments of galaxies hundreds of millions of light years long, meeting at dense knots where rich clusters sit, and vast nearly empty voids between the threads. It is a cosmic spiderweb, and the phrase came from a 1989 paper by Bond, Klypin and Efstathiou.',
      'The web is the amplified version of the primordial foam. Tiny density excesses from inflation grew under gravity, and the growth was channelised by matter streaming along the lowest potential-energy valleys. Structure formation is still running: the web’s mesh is being stretched by dark energy, and in a distant future the filaments will break into isolated islands.',
    ],
    readings: [
      { label: 'filament length', value: '~10⁹ ly' },
      { label: 'void size', value: '~10⁸ ly' },
      { label: 'term coined', value: 'Bond, Klypin & Efstathiou 1989' },
      { label: 'survey', value: '2MASS / DESI' },
    ],
    tags: ['galaxies', 'formation', 'emptiness', 'dark'],
    weight: 0.79,
  },
  {
    id: 'simulation',
    title: 'Cosmological Simulation',
    catalog: 'DF-031 · INSTRUMENTS',
    family: 'instruments',
    summary: 'A universe assembled in a supercomputer, billions of years in a few hours.',
    body: [
      'Simulators start with a box of dark matter particles carrying the tiny primordial fluctuations, add gas and the rules of gravity and gas physics, and let gravity do the work. A run covering 13.8 billion years and a few hundred million light years may involve 10¹⁰ particles and consume the output of hundreds of thousands of CPU cores for weeks.',
      'The Millennium and Illustris runs produced the familiar cosmic web and let astronomers compare a simulation with the real sky, galaxy by galaxy. The practice has made cosmology falsifiable in a way it was not before: if the simulation does not reproduce the observed distribution of galaxy properties, the underlying model is wrong, and we can find out which assumption to discard.',
    ],
    readings: [
      { label: 'particles', value: 'up to 10¹⁰' },
      { label: 'spans', value: '13.8 Gyr in hours' },
      { label: 'example', value: 'Millennium, IllustrisTNG' },
      { label: 'purpose', value: 'test ΛCDM' },
    ],
    tags: ['instruments', 'formation', 'galaxies', 'evidence'],
    weight: 0.73,
  },
  {
    id: 'lookback-time',
    title: 'Lookback Time',
    catalog: 'DF-032 · TIME',
    family: 'time',
    summary: 'Every telescope is also a time machine pointed the wrong way.',
    body: [
      'Light takes 4.24 years to reach us from Proxima Centauri, 2.5 million from Andromeda, and 13.8 billion from the cosmic microwave background. Looking far away is the same as looking far back, and the expansion complicates the arithmetic: the Hubble time and the age of the universe are not the same quantity, because expansion has been happening the whole way.',
      'This gives the field a natural stratigraphy. The cosmic background is the floor, z = 6 to 10 is the era of reionization, z = 2 is peak quasar activity, and z = 0 is now. When JWST finds galaxies at z = 13, it is not just looking further back — it is testing whether galaxies could form that fast, which is a question about the first 300 million years.',
    ],
    readings: [
      { label: 'nearest star', value: '4.24 yr' },
      { label: 'cmb age', value: '13.8 Gyr' },
      { label: 'reionization', value: 'z ≈ 6 – 10' },
      { label: 'cosmic dawn', value: 'z ≈ 20' },
    ],
    tags: ['time', 'light', 'origin', 'expansion'],
    weight: 0.86,
  },
  {
    id: 'time-dilation',
    title: 'Time Dilation',
    catalog: 'DF-033 · TIME',
    family: 'time',
    summary: 'Clocks disagree — by speed, by gravity, and by the mere fact of moving.',
    body: [
      'Special relativity: a clock in motion ticks slower. Gravitational relativity: a clock deeper in a gravitational field ticks slower. Both effects are real, small, and constantly verified. GPS satellites would be out by 11 microseconds per day if relativistic corrections were not applied, which would be enough to destroy the system’s positional accuracy.',
      'The astrophysical version is spectacular. Light from a neutron star’s surface is blueshifted by the star’s gravity, while light from the disk that produced it is redshifted by the disk’s speed. Measure both and you recover the black hole’s spin — the same technique that produced the first image of a black hole’s shadow.',
    ],
    readings: [
      { label: 'special relativity', value: 'moving clocks slow' },
      { label: 'gravitational', value: 'deeper clocks slow' },
      { label: 'gps correction', value: '11 μs / day' },
      { label: 'applied', value: 'spin measurement' },
    ],
    tags: ['time', 'gravity', 'evidence', 'measurement'],
    weight: 0.76,
  },
  {
    id: 'standard-candle',
    title: 'Standard Candle',
    catalog: 'DF-034 · INSTRUMENTS',
    family: 'instruments',
    summary: 'The candle whose known brightness turns brightness into distance.',
    body: [
      'A standard candle is an object whose luminosity you know without measuring its distance, so that comparing apparent and absolute brightness yields the distance. Type Ia supernovae, Cepheid variables and the brightest red supergiants each work this way, forming a ladder of rungs that calibrates the whole cosmic distance scale.',
      'Each rung has a systematic uncertainty, and errors propagate. The tension between the ladder (73.0 ± 1.0) and the CMB (67.4 ± 0.5) is not a blunder but a measurement disagreement — a live test of whether dark energy, neutrino physics, or the expansion history is different from the standard model.',
    ],
    readings: [
      { label: 'rungs', value: 'Cepheid → SNe Ia → CMB' },
      { label: 'rung 1', value: 'Cepheids · 10 – 100 Mpc' },
      { label: 'rung 2', value: 'Type Ia · 10⁹ Mpc' },
      { label: 'tension', value: '73.0 vs 67.4' },
    ],
    tags: ['instruments', 'measurement', 'light', 'frontier'],
    weight: 0.77,
  },
  {
    id: 'parallax',
    title: 'Parallax',
    catalog: 'DF-035 · INSTRUMENTS',
    family: 'instruments',
    summary: 'The oldest geometric trick in astronomy, now measuring a billion billion stars.',
    body: [
      'Hold your thumb at arm’s length and move your eye: it shifts against the background. Do the same with Earth’s orbit and you get an angle of 1 arcsecond for a distance of one parsec, 3.26 light years. Bessel measured it for 61 Cygni in 1838 and the first distance to a star outside the solar system was established.',
      'Gaia has now measured the parallaxes of nearly two billion sources with a precision approaching 20 microarcseconds, and the aim is 10. That will give true three-dimensional positions for a billion stars, turning the galaxy from a projection into a map with depth — and letting us find, and weigh, planets by the wobble of their stars.',
    ],
    readings: [
      { label: 'parsec', value: '3.26 light years' },
      { label: '1st stellar parallax', value: '61 Cygni · 1838' },
      { label: 'gaia sources', value: '~1.8 billion' },
      { label: 'target precision', value: '10 μas' },
    ],
    tags: ['instruments', 'measurement', 'galaxies', 'light'],
    weight: 0.74,
  },
];

export const EDGES: FieldEdge[] = [
  { from: 'big-bang', to: 'cmb', kind: 'origin-of', note: 'The background is the direct afterglow of the initial state.' },
  { from: 'cmb', to: 'inflation', kind: 'evidence-for', note: 'Flatness and scale-invariant fluctuations match the inflationary prediction.' },
  { from: 'inflation', to: 'cosmic-web', kind: 'origin-of', note: 'Primordial fluctuations are the seeds that grow into the web.' },
  { from: 'cmb', to: 'dark-matter', kind: 'evidence-for', note: 'The third acoustic peak fixes the physical density of matter.' },
  { from: 'cmb', to: 'dark-energy', kind: 'evidence-for', note: 'Geometry and distance to last scattering constrain the dark energy density.' },
  { from: 'cmb', to: 'redshift', kind: 'measured-by', note: 'z ≈ 1100 is where the background is observed today.' },
  { from: 'big-bang', to: 'lookback-time', kind: 'causes', note: 'An expanding universe separates us from the beginning in space and time.' },
  { from: 'redshift', to: 'lookback-time', kind: 'causes', note: 'Redshift is the measurable form of lookback time.' },
  { from: 'lookback-time', to: 'hubble', kind: 'measured-by', note: 'Telescopes turn lookback time into images of earlier epochs.' },
  { from: 'lookback-time', to: 'jwst', kind: 'measured-by', note: 'The redshifted light of the first galaxies is JWST’s target.' },
  { from: 'dark-matter', to: 'cosmic-web', kind: 'causes', note: 'Dark matter provides the gravitational scaffolding for structure.' },
  { from: 'dark-matter', to: 'lensing', kind: 'revealed-by', note: 'Mass that does not shine is still visible in bent light.' },
  { from: 'dark-matter', to: 'dark-energy', kind: 'sibling-of', note: 'Together they form 95% of the energy budget.' },
  { from: 'dark-energy', to: 'cosmic-web', kind: 'causes', note: 'Acceleration is tearing the filaments apart into islands.' },
  { from: 'dark-energy', to: 'time-dilation', kind: 'contrasts-with', note: 'One dilates time; the other dilates space.' },
  { from: 'lensing', to: 'dark-matter', kind: 'measured-by', note: 'Weak lensing maps the dark matter directly.' },
  { from: 'lensing', to: 'spiral-galaxy', kind: 'hosts', note: 'Galaxies act as the lenses that create the arcs.' },
  { from: 'lensing', to: 'vlbi', kind: 'sibling-of', note: 'Both are precision measurements of curved spacetime.' },
  { from: 'lensing', to: 'chandra', kind: 'measured-by', note: 'X-ray maps of cluster gas confirm the mass maps.' },
  { from: 'black-hole', to: 'accretion-disk', kind: 'hosts', note: 'The disk is the black hole’s engine, wrapped around it.' },
  { from: 'accretion-disk', to: 'quasar', kind: 'powered-by', note: 'An actively fed disk makes a galaxy a quasar.' },
  { from: 'quasar', to: 'spiral-galaxy', kind: 'sibling-of', note: 'Most quasars live inside ordinary spiral galaxies.' },
  { from: 'quasar', to: 'vlbi', kind: 'measured-by', note: 'VLBI resolved jets and beamed emission from quasars.' },
  { from: 'quasar', to: 'redshift', kind: 'measured-by', note: 'Quasars span the largest redshift range of any population.' },
  { from: 'black-hole', to: 'event-horizon', kind: 'origin-of', note: 'The horizon is the defining boundary of the object.' },
  { from: 'black-hole', to: 'hawking', kind: 'causes', note: 'Curved spacetime at the horizon produces the radiation.' },
  { from: 'event-horizon', to: 'hawking', kind: 'causes', note: 'The horizon area sets the temperature.' },
  { from: 'hawking', to: 'time-dilation', kind: 'causes', note: 'Evaporation ties a black hole’s mass to its clock.' },
  { from: 'event-horizon', to: 'time-dilation', kind: 'causes', note: 'Gravity near the horizon stretches clocks measurably.' },
  { from: 'black-hole', to: 'neutron-star', kind: 'scales-to', note: 'Collapse above ~2.1 solar masses is the endpoint of a neutron star.' },
  { from: 'neutron-star', to: 'magnetar', kind: 'origin-of', note: 'A magnetar is a neutron star with an extreme field.' },
  { from: 'neutron-star', to: 'pulsar', kind: 'sibling-of', note: 'Both are rotating neutron stars; the field decides the rest.' },
  { from: 'pulsar', to: 'neutron-star', kind: 'revealed-by', note: 'The pulse train is how we find them.' },
  { from: 'magnetar', to: 'frb', kind: 'powered-by', note: 'Magnetar bursts are the leading explanation for repeaters.' },
  { from: 'pulsar', to: 'frb', kind: 'sibling-of', note: 'Both are millisecond radio transients with neutron star links.' },
  { from: 'neutron-star', to: 'ligo', kind: 'revealed-by', note: 'Tidal deformation in the waveform constrains the equation of state.' },
  { from: 'ligo', to: 'black-hole', kind: 'measured-by', note: 'The chirp measures the masses of merging black holes.' },
  { from: 'ligo', to: 'neutron-star', kind: 'measured-by', note: 'Kilonova afterglow identifies neutron star mergers.' },
  { from: 'supernova', to: 'neutron-star', kind: 'origin-of', note: 'Core collapse leaves a neutron star or a black hole.' },
  { from: 'supernova', to: 'standard-candle', kind: 'measured-by', note: 'Type Ia supernovae are the top rung of the distance ladder.' },
  { from: 'supernova', to: 'dark-energy', kind: 'evidence-for', note: 'Distant Type Ia supernovae revealed the acceleration.' },
  { from: 'supernova', to: 'nebula', kind: 'causes', note: 'The explosion shapes the remnant nebula around it.' },
  { from: 'supernova', to: 'grb', kind: 'sibling-of', note: 'Long-duration bursts are collapsars in disguise.' },
  { from: 'supernova', to: 'magnetar', kind: 'causes', note: 'Magnetars are born in the same kind of collapse.' },
  { from: 'standard-candle', to: 'parallax', kind: 'measured-by', note: 'Geometric parallax anchors the bottom of the ladder.' },
  { from: 'standard-candle', to: 'hubble', kind: 'measured-by', note: 'Cepheids and supernovae calibrate the Hubble constant.' },
  { from: 'parallax', to: 'spiral-galaxy', kind: 'measured-by', note: 'Distances from parallax place the Sun in the galaxy.' },
  { from: 'parallax', to: 'exoplanet', kind: 'measured-by', note: 'Gaia astrometry finds planets by stellar wobble.' },
  { from: 'hubble', to: 'redshift', kind: 'measured-by', note: 'Spectra from Hubble give precise redshifts.' },
  { from: 'hubble', to: 'spiral-galaxy', kind: 'evidence-for', note: 'The tuning fork of galaxy morphology came from deep plates.' },
  { from: 'hubble', to: 'cmb', kind: 'measured-by', note: 'Hubble deep field frames anchor the CMB distance scale.' },
  { from: 'jwst', to: 'exoplanet', kind: 'measured-by', note: 'Transmission spectroscopy reads exoplanet atmospheres.' },
  { from: 'jwst', to: 'habitable-zone', kind: 'measured-by', note: 'Atmospheric chemistry is the current test for habitability.' },
  { from: 'jwst', to: 'lookback-time', kind: 'measured-by', note: 'Deep fields reach redshift 13.' },
  { from: 'chandra', to: 'accretion-disk', kind: 'measured-by', note: 'X-ray brightness traces the inner disk temperature.' },
  { from: 'chandra', to: 'supernova', kind: 'measured-by', note: 'The shock front of a young remnant glows in X-rays.' },
  { from: 'vlbi', to: 'black-hole', kind: 'measured-by', note: 'The shadow is a shadow of the horizon.' },
  { from: 'vlbi', to: 'accretion-disk', kind: 'measured-by', note: 'The ring emission traces the photon orbit in the disk.' },
  { from: 'vlbi', to: 'quasar', kind: 'measured-by', note: 'Beamed jets resolve at microarcsecond scales.' },
  { from: 'exoplanet', to: 'protoplanetary-disk', kind: 'origin-of', note: 'Planets condense out of disks like ours.' },
  { from: 'protoplanetary-disk', to: 'nebula', kind: 'sibling-of', note: 'Both are stages of star formation.' },
  { from: 'nebula', to: 'spiral-galaxy', kind: 'hosts', note: 'Nebulae are the bright nurseries in spiral arms.' },
  { from: 'nebula', to: 'pulsar', kind: 'origin-of', note: 'The Crab Nebula holds a pulsar at its centre.' },
  { from: 'spiral-galaxy', to: 'globular-cluster', kind: 'hosts', note: 'Globular clusters orbit in the galactic halo.' },
  { from: 'globular-cluster', to: 'lookback-time', kind: 'measured-by', note: 'Cluster ages set the timeline of early chemistry.' },
  { from: 'cosmic-web', to: 'spiral-galaxy', kind: 'hosts', note: 'Filaments feed galaxies with gas and heat them.' },
  { from: 'cosmic-web', to: 'simulation', kind: 'evidence-for', note: 'Simulations reproduce the web; surveys compare them.' },
  { from: 'simulation', to: 'dark-matter', kind: 'evidence-for', note: 'Only dark matter runs produce the observed web.' },
  { from: 'simulation', to: 'inflation', kind: 'evidence-for', note: 'Initial conditions trace back to the inflationary foam.' },
  { from: 'simulation', to: 'cosmic-web', kind: 'origin-of', note: 'Simulations produce the web they are compared against.' },
  { from: 'habitable-zone', to: 'exoplanet', kind: 'sibling-of', note: 'A filter applied to the exoplanet population.' },
  { from: 'habitable-zone', to: 'protoplanetary-disk', kind: 'causes', note: 'The zone is set by where water can condense.' },
  { from: 'grb', to: 'black-hole', kind: 'powered-by', note: 'Collapsars bury a newborn black hole in a jet.' },
  { from: 'grb', to: 'lookback-time', kind: 'measured-by', note: 'High-z bursts are backlights for the early universe.' },
  { from: 'frb', to: 'magnetar', kind: 'powered-by', note: 'One burst was localised to a magnetar in a nearby galaxy.' },
  { from: 'frb', to: 'pulsar', kind: 'contrasts-with', note: 'Bursts are irregular; pulsars are metronomic.' },
  { from: 'neutron-star', to: 'time-dilation', kind: 'measured-by', note: 'Relativistic redshifts read the spin directly.' },
  { from: 'time-dilation', to: 'redshift', kind: 'sibling-of', note: 'Both are shifts in the frequency of light.' },
  { from: 'big-bang', to: 'redshift', kind: 'origin-of', note: 'The expansion that began it is what stretches every wavelength.' },
];

export const NODE_BY_ID: Record<string, FieldNode> = Object.fromEntries(
  NODES.map((n) => [n.id, n]),
);

/** tag vocabulary derived from the corpus, used for the interest vector */
export const TAGS: string[] = Array.from(
  NODES.reduce((acc, n) => {
    n.tags.forEach((t) => acc.add(t));
    return acc;
  }, new Set<string>()),
).sort();

export const EDGE_KINDS = Object.keys(EDGE_KIND_LABEL) as EdgeKind[];

export function neighboursOf(id: string): string[] {
  const out: string[] = [];
  for (const e of EDGES) {
    if (e.from === id) out.push(e.to);
    else if (e.to === id) out.push(e.from);
  }
  return out;
}

export function edgesOf(id: string): FieldEdge[] {
  return EDGES.filter((e) => e.from === id || e.to === id);
}

export function degreeOf(id: string): number {
  return edgesOf(id).length;
}
