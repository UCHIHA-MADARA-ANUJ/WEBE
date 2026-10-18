/**
 * End-to-end check in a real browser.
 *
 * Drives the deployed app like a hurried skimmer and like a patient reader,
 * and asserts that the Evolution Engine restructures the interface on its
 * own — capturing the moment it does.
 *
 *   node scripts/live-check.mjs [url]
 */
import chromium from '@sparticuz/chromium';
import puppeteer from 'puppeteer-core';
import { mkdirSync, existsSync, writeFileSync, readFileSync } from 'node:fs';
import { brotliDecompressSync } from 'node:zlib';
import { execFileSync } from 'node:child_process';

const URL = process.argv[2] || process.env.SHOT_URL || 'http://127.0.0.1:4173/';
const OUT = '/tmp/live';
mkdirSync(OUT, { recursive: true });

const LIB_DIR = '/tmp/chromelibs/lib';
if (!existsSync(LIB_DIR)) {
  const br = 'node_modules/@sparticuz/chromium/bin/al2023.tar.br';
  if (existsSync(br)) {
    writeFileSync('/tmp/al2023.tar', brotliDecompressSync(readFileSync(br)));
    execFileSync('tar', ['-xf', '/tmp/al2023.tar', '-C', '/tmp/chromelibs']);
  }
}
if (existsSync(LIB_DIR)) {
  process.env.LD_LIBRARY_PATH = `${LIB_DIR}:${process.env.LD_LIBRARY_PATH || ''}`;
}

const exe = await chromium.executablePath();
const browser = await puppeteer.launch({
  args: [
    '--no-sandbox',
    '--disable-setuid-sandbox',
    '--disable-dev-shm-usage',
    '--disable-gpu',
    '--hide-scrollbars',
    '--mute-audio',
    '--no-zygote',
    '--single-process',
    '--disable-features=site-per-process,NetworkService',
  ],
  executablePath: exe,
  headless: true,
  protocolTimeout: 60000,
});

const wait = (ms) => new Promise((r) => setTimeout(r, ms));
const results = [];
const check = (name, ok, extra = '') => {
  results.push({ name, ok: !!ok, extra });
  console.log(`${ok ? '  PASS' : '  FAIL'}  ${name}${extra ? ' — ' + extra : ''}`);
};

async function session(label, { fast }) {
  const page = await browser.newPage();
  await page.setViewport({ width: 1440, height: 900 });
  await page.goto(URL, { waitUntil: 'load', timeout: 30000 });
  // every visitor gets a clean slate — different people, different versions
  await page.evaluate(() => window.localStorage.clear());
  await page.reload({ waitUntil: 'load', timeout: 30000 });
  await wait(1200);

  const start = await page.$eval('.app', (el) => el.getAttribute('data-paradigm'));

  if (fast) {
    // a hurried visitor: click a lot, never stay
    for (let i = 0; i < 9; i++) {
      await page.evaluate((k) => {
        const nodes = document.querySelectorAll('.cnode');
        nodes[(k * 5 + 3) % nodes.length]?.dispatchEvent(
          new MouseEvent('click', { bubbles: true }),
        );
      }, i);
      await wait(260);
    }
  } else {
    // a patient visitor: open an object, read it, follow one of its relations
    for (let i = 0; i < 4; i++) {
      const nodes = await page.$$('.cnode');
      if (nodes.length) await nodes[i % nodes.length].click();
      await wait(5000);
      const rel = await page.$('.dossier .relation');
      if (rel) await rel.click();
      await wait(300);
    }
  }

  await wait(2500);

  const after = await page.$eval('.app', (el) => el.getAttribute('data-paradigm'));
  const status = await page.$eval('.statusbar__meta', (el) => el.textContent || '').catch(() => '');
  const overlay = await page
    .$eval('.reconf__head', (el) => el.textContent || '')
    .catch(() => '');
  await page.evaluate(() => {
    const b = [...document.querySelectorAll('.bar .btn')].find((x) => /mind/i.test(x.textContent || ''));
    b?.click();
  });
  await wait(400);
  const raw = await page
    .$$eval('.mind .featuregrid', (grids) =>
      grids.map((g) =>
        [...g.querySelectorAll('.feature')]
          .map((e) => `${e.querySelector('.feature__k')?.textContent}=${e.querySelector('.feature__v')?.textContent}`)
          .join(' '),
      ),
    )
    .catch(() => []);
  await page.evaluate(() => {
    const b = [...document.querySelectorAll('.mind .btn')].find((x) => /✕|close/i.test(x.textContent || ''));
    b?.click();
  });
  const scores = await page
    .$$eval('.arch', (els) =>
      els.map((e) => `${e.querySelector('.arch__name')?.textContent}:${e.querySelector('.arch__pct')?.textContent}`),
    )
    .catch(() => []);

  await page.screenshot({ path: `${OUT}/${label}.png` });
  await page.close();
  return { start, after, status, overlay, raw, scores };
}

console.log('\n▌ HURRIED VISITOR');
const fast = await session('fast', { fast: true });
check('structure changed on its own', fast.start !== fast.after, `${fast.start} → ${fast.after}`);
check('it moved to a dense board', fast.after === 'mosaic', `paradigm=${fast.after}`);
check('it explained itself', /unfolded/i.test(fast.overlay), fast.overlay.slice(0, 90));
check('status bar reports the read', /read skimmer/i.test(fast.status), fast.status);
console.log('   raw:', fast.raw.join(' '));
console.log('   scores:', fast.scores.join(' '));

console.log('\n▌ PATIENT VISITOR');
const slow = await session('slow', { fast: false });
check('structure changed on its own', slow.start !== slow.after, `${slow.start} → ${slow.after}`);
check('it moved to a reading column', slow.after === 'codex', `paradigm=${slow.after}`);
check('status bar reports the read', /read reader/i.test(slow.status), slow.status);
console.log('   raw:', slow.raw.join(' '));

console.log('\n▌ SUMMARY');
const failed = results.filter((r) => !r.ok);
console.log(`${results.length - failed.length}/${results.length} checks passed`);
await browser.close();
process.exit(failed.length ? 1 : 0);
