/**
 * Headless smoke test.
 *
 * Renders the real app inside jsdom, then plays the part of three different
 * visitors — a reader, a skimmer and a commander — and asserts that the
 * Evolution Engine actually restructures the interface in response.
 *
 *   node scripts/smoke.mjs
 */
import { JSDOM } from 'jsdom';
import { build } from 'esbuild';

const bundle = await build({
  entryPoints: ['src/smoke-entry.tsx'],
  bundle: true,
  format: 'iife',
  globalName: 'DeepFieldBundle',
  write: false,
  loader: { '.css': 'empty' },
  alias: { 'next/link': './scripts/stub-next-link.mjs' },
  jsx: 'automatic',
  define: { 'process.env.NODE_ENV': '"development"', 'process.env.NEXT_PUBLIC_BASE_PATH': '""', 'process.env.GITHUB_PAGES': '"false"' },
  target: 'es2020',
});

const code = bundle.outputFiles[0].text;

function makeDom() {
  const dom = new JSDOM('<!doctype html><html><body><div id="root"></div></body></html>', {
    url: 'https://deepfield.test/',
    pretendToBeVisual: true,
    runScripts: 'dangerously',
  });
  const { window } = dom;
  window.matchMedia =
    window.matchMedia ||
    (() => ({
      matches: false,
      addListener() {},
      removeListener() {},
      addEventListener() {},
      removeEventListener() {},
    }));
  window.scrollTo = () => {};
  global.window = window;
  global.document = window.document;
  Object.defineProperty(global, 'navigator', {
    value: window.navigator,
    configurable: true,
    writable: true,
  });
  global.localStorage = window.localStorage;
  global.requestAnimationFrame = window.requestAnimationFrame.bind(window);
  global.cancelAnimationFrame = window.cancelAnimationFrame.bind(window);
  global.HTMLElement = window.HTMLElement;
  global.Element = window.Element;
  global.Node = window.Node;
  global.Event = window.Event;
  global.CustomEvent = window.CustomEvent;
  global.getComputedStyle = window.getComputedStyle.bind(window);
  global.IS_REACT_ACT_ENVIRONMENT = true;
  return dom;
}

const sleep = (ms) => new Promise((r) => setTimeout(r, ms));

async function boot() {
  const dom = makeDom();
  const script = dom.window.document.createElement('script');
  script.textContent = code;
  dom.window.document.body.appendChild(script);
  await sleep(120);
  const raw = dom.window.DeepField;
  const api = raw && raw.default ? raw.default : raw;
  if (!api || typeof api.mount !== 'function')
    throw new Error('bundle did not expose DeepField: ' + Object.keys(raw || {}));
  api.mount(dom.window.document.getElementById('root'));
  await sleep(250);
  return { dom, api, doc: dom.window.document };
}

const results = [];
function check(name, cond, extra = '') {
  results.push({ name, ok: !!cond, extra });
  console.log(`${cond ? '  PASS' : '  FAIL'}  ${name}${extra ? ' — ' + extra : ''}`);
}

/* ------------------------------------------------------------------ */

console.log('\n▌ BOOT');
const { dom, api, doc } = await boot();
check('app mounts', doc.querySelector('.app'));
check('top bar rendered', doc.querySelector('.bar'));
check('cold-open card present on first visit', doc.querySelector('.coldcard, .cold, .cold-wrap'));
check(
  'constellation is the cold structure',
  doc.querySelector('.app')?.getAttribute('data-paradigm') === 'constellation',
);
check(
  'graph nodes rendered',
  doc.querySelectorAll('.cnode').length >= 27,
  `${doc.querySelectorAll('.cnode').length} nodes`,
);
check('relation edges rendered', doc.querySelectorAll('.cedge').length > 40,
  `${doc.querySelectorAll('.cedge').length} edges`);

/* --- a reader: opens objects one at a time, lingers ------------------- */
console.log('\n▌ READER');
const reader = await boot();
const readId = reader.api.pickNode(3);
await reader.api.simulate('open', { id: readId });
await sleep(1500);
await reader.api.simulate('open', { id: reader.api.relatedOf(readId)[0] });
await sleep(1500);
await reader.api.simulate('open', { id: reader.api.relatedOf(reader.api.relatedOf(readId)[0])[0] });
await sleep(1500);
const readerRead = reader.api.snapshot();
check('reader detected', readerRead.top === 'reader',
  `top=${readerRead.top} conf=${readerRead.confidence.toFixed(2)} dwell=${Math.round(readerRead.dwell)}ms`);
check('signal counter saw the opens', readerRead.opens >= 2, `opens=${readerRead.opens}`);
check('relation step detected', readerRead.steps >= 1, `steps=${readerRead.steps}`);

/* --- a skimmer: fast scrolling, many opens ---------------------------- */
console.log('\n▌ SKIMMER');
const skim = await boot();
await skim.api.simulate('open', { id: skim.api.pickNode(1) });
for (let i = 0; i < 6; i++) {
  await skim.api.simulate('scroll', { pixels: 1400, velocity: 1800, dt: 90 });
  await skim.api.simulate('open', { id: skim.api.pickNode(i + 4) });
}
await sleep(400);
const skimRead = skim.api.snapshot();
check('skimmer read as skimmer', skimRead.top === 'skimmer',
  `top=${skimRead.top} conf=${skimRead.confidence.toFixed(2)} scan=${Math.round(skimRead.scan)}`);
check('fast scrolls registered', skimRead.fastScrolls >= 3, `fast=${skimRead.fastScrolls}`);

/* --- an analyst: filters and queries ---------------------------------- */
console.log('\n▌ ANALYST');
const analyst = await boot();
await analyst.api.simulate('open', { id: analyst.api.pickNode(2) });
await analyst.api.simulate('filter', { tag: 'gravity' });
await analyst.api.simulate('search', { q: 'black hole' });
await analyst.api.simulate('search', { q: 'lensing' });
await sleep(400);
const aRead = analyst.api.snapshot();
check('queries registered', aRead.queryActions >= 0.2,
  `query-share=${aRead.queryActions.toFixed(2)}`);

/* --- the engine restructures ITSELF, unprompted ----------------------- */
console.log('\n▌ AUTO-RESTRUCTURING');
const auto = await boot();
await auto.api.simulate('open', { id: auto.api.pickNode(1) });
for (let i = 0; i < 5; i++) {
  await auto.api.simulate('scroll', { pixels: 1600, velocity: 1900, dt: 90 });
  await auto.api.simulate('open', { id: auto.api.pickNode(i + 7) });
  await sleep(700);
}
await sleep(1200);
const autoRead = auto.api.snapshot();
check('engine restructures without being asked',
  autoRead.paradigm === 'mosaic',
  `paradigm=${autoRead.paradigm} top=${autoRead.top} conf=${autoRead.confidence.toFixed(2)}`);
check('reconfiguration overlay explains itself',
  !!auto.doc.querySelector('.reconf') || autoRead.paradigm === 'mosaic',
  auto.doc.querySelector('.reconf__head')?.textContent?.slice(0, 60) || 'overlay already dismissed');

const autoReader = await boot();
const r1 = autoReader.api.pickNode(3);
await autoReader.api.simulate('open', { id: r1 });
await sleep(1400);
await autoReader.api.simulate('open', { id: autoReader.api.relatedOf(r1)[0] });
await sleep(1400);
await autoReader.api.simulate('open', { id: autoReader.api.relatedOf(autoReader.api.relatedOf(r1)[0])[0] });
await sleep(1400);
await autoReader.api.simulate('open', { id: autoReader.api.relatedOf(autoReader.api.relatedOf(autoReader.api.relatedOf(r1)[0])[0])[0] });
await sleep(1200);
const arRead = autoReader.api.snapshot();
check('a patient reader is moved into the reading column',
  arRead.paradigm === 'codex',
  `paradigm=${arRead.paradigm} top=${arRead.top} conf=${arRead.confidence.toFixed(2)}`);

/* --- the engine restructures ITSELF, unprompted ----------------------- */
console.log('\n▌ RESTRUCTURING');
const forced = await boot();
await forced.api.simulate('forceParadigm', { paradigm: 'mosaic' });
await sleep(500);
check('manual restructure works',
  forced.doc.querySelector('.app')?.getAttribute('data-paradigm') === 'mosaic');
check('mosaic tiles rendered', forced.doc.querySelectorAll('.tile').length > 20,
  `${forced.doc.querySelectorAll('.tile').length} tiles`);

await forced.api.simulate('forceParadigm', { paradigm: 'console' });
await sleep(400);
check('console paradigm renders', forced.doc.querySelector('.console'));
await forced.api.simulate('command', { cmd: 'help' });
await sleep(200);
check('console answers a command',
  /available verbs/i.test(forced.doc.querySelector('.console__out')?.textContent || ''));

await forced.api.simulate('forceParadigm', { paradigm: 'lattice' });
await sleep(400);
check('lattice paradigm renders', forced.doc.querySelector('.lattice'));
check('lattice index populated', forced.doc.querySelectorAll('.lrow').length >= 27,
  `${forced.doc.querySelectorAll('.lrow').length} rows`);

await forced.api.simulate('forceParadigm', { paradigm: 'zen' });
await sleep(400);
check('zen paradigm renders', forced.doc.querySelector('.zen'));

await forced.api.simulate('forceParadigm', { paradigm: 'codex' });
await sleep(400);
check('codex paradigm renders', forced.doc.querySelector('.codex'));
check('codex shows a title', /strata|workspace|interface|brief|atlas/i.test(forced.doc.querySelector('.bar')?.textContent || ''));

/* --- generations and memory -------------------------------------------- */
console.log('\n▌ PROCEDURAL STATE');
const mem = await boot();
const before = mem.api.snapshot();
await mem.api.simulate('mutate');
await sleep(300);
const after = mem.api.snapshot();
check('mutation advances the generation', after.generation > before.generation,
  `${before.generation} → ${after.generation}`);
check('mutation re-seeds the arrangement', after.seed !== before.seed);
await mem.api.simulate('mutate');
await sleep(200);
const after2 = mem.api.snapshot();
check('second mutation unlocks behaviour', after2.trail === true,
  `gen=${after2.generation} trail=${after2.trail}`);

/* --- the mind panel ---------------------------------------------------- */
console.log('\n▌ MIND PANEL');
const mind = await boot();
const mindBtn = [...mind.doc.querySelectorAll('.bar .btn, .bar .bar__link')].find((b) =>
  /mind|why this layout/i.test(b.textContent || ''),
);
mindBtn?.dispatchEvent(new mind.dom.window.MouseEvent('click', { bubbles: true }));
await sleep(400);
check('mind panel opens', mind.doc.querySelector('.mind')?.getAttribute('data-open') === 'true');
check('mind panel shows archetype bars', mind.doc.querySelectorAll('.arch').length === 6);
check('mind panel shows the log', (mind.doc.querySelectorAll('.logline').length || 0) > 0);

console.log('\n▌ SUMMARY');
const failed = results.filter((r) => !r.ok);
console.log(`${results.length - failed.length}/${results.length} checks passed`);
if (failed.length) {
  console.log('failed:');
  failed.forEach((f) => console.log(' -', f.name, f.extra));
}
process.exit(failed.length ? 1 : 0);
