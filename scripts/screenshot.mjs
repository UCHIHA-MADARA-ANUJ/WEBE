/**
 * Visual capture harness.
 *
 * Renders the real app in a headless Chromium and writes screenshots to
 * /tmp/shots so the design can be reviewed without a display.
 *
 *   npm run build && npm run preview &   # serve on :4173
 *   node scripts/screenshot.mjs
 */
import chromium from '@sparticuz/chromium';
import puppeteer from 'puppeteer-core';
import { mkdirSync, existsSync, writeFileSync, readFileSync } from 'node:fs';
import { brotliDecompressSync } from 'node:zlib';
import { execFileSync } from 'node:child_process';

const URL = process.env.SHOT_URL || 'http://127.0.0.1:4173/';
const OUT = process.env.SHOT_OUT || '/tmp/shots';
mkdirSync(OUT, { recursive: true });

/* the bundled chromium needs NSS, which the sandbox does not ship */
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
    '--font-render-hinting=none',
  ],
  executablePath: exe,
  headless: true,
  protocolTimeout: 60000,
});

const page = await browser.newPage();
await page.setViewport({ width: 1440, height: 900, deviceScaleFactor: 1 });
page.on('console', (m) => {
  if (m.type() === 'error') console.log('  [console error]', m.text().slice(0, 200));
});
page.on('pageerror', (e) => console.log('  [page error]', String(e).slice(0, 300)));

await page.goto(URL, { waitUntil: 'load', timeout: 30000 });
const wait = (ms) => new Promise((r) => setTimeout(r, ms));
await wait(1200);

const shot = async (name) => {
  await page.screenshot({ path: `${OUT}/${name}.png` });
  console.log('  wrote', `${OUT}/${name}.png`);
};

await shot('01-cold');

// open a node from the constellation
const node = await page.$('.cnode');
if (node) {
  await node.click();
  await wait(900);
  await shot('02-constellation-dossier');
}

// codex
await page.evaluate(() => {
  const b = [...document.querySelectorAll('.switch')].find((x) => /codex/i.test(x.textContent || ''));
  b?.click();
});
await wait(900);
await shot('03-codex');

// lattice
await page.evaluate(() => {
  const b = [...document.querySelectorAll('.switch')].find((x) => /lattice/i.test(x.textContent || ''));
  b?.click();
});
await wait(900);
await shot('04-lattice');

// mosaic
await page.evaluate(() => {
  const b = [...document.querySelectorAll('.switch')].find((x) => /mosaic/i.test(x.textContent || ''));
  b?.click();
});
await wait(900);
await shot('05-mosaic');

// console
await page.evaluate(() => {
  const b = [...document.querySelectorAll('.switch')].find((x) => /console/i.test(x.textContent || ''));
  b?.click();
});
await wait(700);
await page.type('.console__input', 'help');
await page.keyboard.press('Enter');
await wait(500);
await page.type('.console__input', 'open 5');
await page.keyboard.press('Enter');
await wait(600);
await shot('06-console');

// zen
await page.evaluate(() => {
  const b = [...document.querySelectorAll('.switch')].find((x) => /zen/i.test(x.textContent || ''));
  b?.click();
});
await wait(900);
await shot('07-zen');

// mind panel
await page.evaluate(() => {
  const b = [...document.querySelectorAll('.bar .btn')].find((x) => /mind/i.test(x.textContent || ''));
  b?.click();
});
await wait(700);
await shot('08-mind');

// mobile
await page.setViewport({ width: 414, height: 896, deviceScaleFactor: 2 });
await page.evaluate(() => {
  const b = [...document.querySelectorAll('.switch')].find((x) => /codex/i.test(x.textContent || ''));
  b?.click();
});
await wait(900);
await shot('09-mobile');

await browser.close();
console.log('done');
