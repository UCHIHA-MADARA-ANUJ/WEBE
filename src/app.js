import { SHOWS, MOODS, coverArt, getShow, relatedShows, fitScore } from './data.js';
import { createEvolutionEngine } from './evolution.js';

const root = document.querySelector('#app');
const engine = createEvolutionEngine();
const modeNames = { orbit: 'Orbit', run: 'Run', pulse: 'Pulse', shelf: 'Shelf' };
const modeDescriptions = {
  orbit: 'A connected map for the curious.',
  run: 'A guided route for the deep reader.',
  pulse: 'A short list for the quick picker.',
  shelf: 'A workspace for the stories you keep.',
};
const mapPositions = {
  'sonny-boy': [15, 21],
  'odd-taxi': [50, 15],
  eizouken: [83, 25],
  'mob-psycho': [23, 56],
  'violet-evergarden': [60, 54],
  edgerunners: [84, 68],
  frieren: [50, 84],
  'tatami-galaxy': [15, 82],
};

const state = {
  selected: engine.profile.metrics.lastShowId || 'sonny-boy',
  previewLens: null,
  lensMenuOpen: false,
  panel: null,
  detailId: null,
  searchQuery: '',
  mood: 'any',
  pulseIndex: 0,
  shelfSelected: null,
  compareId: null,
  toast: '',
  toastTimer: null,
};

const esc = (value) => String(value ?? '').replace(/[&<>"']/g, (character) => ({
  '&': '&amp;', '<': '&lt;', '>': '&gt;', '"': '&quot;', "'": '&#39;',
}[character]));
const activeLens = () => state.previewLens || engine.getLens();
const savedIds = () => engine.profile.savedIds;
const isSaved = (id) => savedIds().includes(id);
const showById = (id) => getShow(id);
const titleFor = (lens) => modeNames[lens] || modeNames.orbit;

function selectedShow() {
  return showById(state.selected);
}

function setToast(message) {
  window.clearTimeout(state.toastTimer);
  state.toast = message;
  state.toastTimer = window.setTimeout(() => {
    state.toast = '';
    render();
  }, 3600);
}

function perform(action) {
  const oldLens = engine.getLens();
  action();
  const newLens = engine.getLens();
  if (oldLens !== newLens) {
    setToast(`AUTO LENS SHIFT · ${titleFor(oldLens).toUpperCase()} → ${titleFor(newLens).toUpperCase()}`);
  } else {
    render();
  }
}

function cover(show, extraClass = '') {
  return coverArt(show.id, extraClass);
}

function saveButton(show, extraClass = '') {
  const saved = isSaved(show.id);
  return `<button class="save-control ${extraClass}" type="button" data-action="save" data-id="${esc(show.id)}" aria-pressed="${saved}" aria-label="${saved ? 'Remove' : 'Add'} ${esc(show.title)} ${saved ? 'from' : 'to'} your shelf">
    <span class="save-glyph" aria-hidden="true">${saved ? '−' : '+'}</span><span>${saved ? 'ON YOUR SHELF' : 'SAVE FOR LATER'}</span>
  </button>`;
}

function renderHeader(lens) {
  const previewLabel = state.previewLens ? `PREVIEW · ${titleFor(state.previewLens).toUpperCase()}` : `AUTO LENS · ${titleFor(lens).toUpperCase()}`;
  return `<a class="skip-link" href="#main">Skip to the index</a>
    <header class="site-header">
      <div class="header-inner">
        <a class="wordmark" href="#top" aria-label="FRAME/SHIFT home" data-action="home">
          <span class="frame-mark" aria-hidden="true"><i></i><i></i><i></i><i></i></span>
          <span class="wordmark-text">FRAME<span class="wordmark-slash">/</span>SHIFT</span>
          <span class="wordmark-edition">ANIME INDEX<br>VOL. 01</span>
        </a>
        <div class="header-controls">
          <span class="local-indicator"><span class="local-dot"></span>LOCAL PROFILE</span>
          <button class="header-icon-button search-trigger" type="button" data-action="search" aria-label="Search the index">
            <svg viewBox="0 0 24 24" aria-hidden="true"><circle cx="10.8" cy="10.8" r="6.6"></circle><path d="m16 16 4.4 4.4"></path></svg><span>SEARCH</span>
          </button>
          <button class="shelf-shortcut" type="button" data-action="open-shelf" aria-label="Open your shelf, ${savedIds().length} saved titles">
            <span class="shelf-shortcut-mark" aria-hidden="true">⌑</span><span>SHELF</span><b>${String(savedIds().length).padStart(2, '0')}</b>
          </button>
          <div class="lens-control-wrap">
            <button class="lens-trigger ${state.previewLens ? 'is-preview' : ''}" type="button" data-action="toggle-lenses" aria-expanded="${state.lensMenuOpen}" aria-haspopup="true">
              <span class="lens-pulse" aria-hidden="true"></span>
              <span class="lens-trigger-copy"><small>${esc(previewLabel.split(' · ')[0])}</small><strong>${esc(previewLabel.split(' · ')[1] || titleFor(lens).toUpperCase())}</strong></span>
              <svg viewBox="0 0 16 16" aria-hidden="true"><path d="m4 6 4 4 4-4"></path></svg>
            </button>
            ${state.lensMenuOpen ? renderLensMenu() : ''}
          </div>
        </div>
      </div>
    </header>`;
}

function renderLensMenu() {
  return `<div class="lens-menu" role="menu" aria-label="Choose an interface preview">
    <div class="menu-heading"><span>THE FOUR LENSES</span><span>PREVIEW ONLY</span></div>
    <button class="lens-menu-item ${!state.previewLens ? 'is-current' : ''}" type="button" role="menuitem" data-action="auto-lens">
      <span class="menu-item-number">A</span><span><strong>Follow my behavior</strong><small>Let the index keep adapting</small></span>${!state.previewLens ? '<b class="menu-check">●</b>' : ''}
    </button>
    ${Object.keys(modeNames).map((lens, index) => `<button class="lens-menu-item ${state.previewLens === lens ? 'is-current' : ''}" type="button" role="menuitem" data-action="preview-lens" data-lens="${lens}">
      <span class="menu-item-number">0${index + 1}</span><span><strong>${modeNames[lens]}</strong><small>${modeDescriptions[lens]}</small></span>${state.previewLens === lens ? '<b class="menu-check">●</b>' : ''}
    </button>`).join('')}
    <p class="menu-footnote">Choosing a preview is not a signal. Opens, saves, skips, and reading still teach Auto.</p>
  </div>`;
}

function renderHero(lens) {
  const profile = engine.profile;
  const m = profile.metrics;
  const uniqueTags = Object.keys(m.tagCounts).length;
  return `<section class="hero" id="top" aria-labelledby="hero-title">
      <div class="hero-copy">
        <div class="eyebrow"><span class="eyebrow-line"></span> A PERSONAL INDEX OF ANIME</div>
        <h1 id="hero-title">Not a list.<br><em>A way in.</em></h1>
        <p class="hero-deck">A living anime index that notices how you wander, linger, and save — then builds a different route around you.</p>
        <div class="hero-foot"><span class="hero-index">FRAME/SHIFT <b>—</b> 001</span><span class="scroll-cue"><span class="scroll-cue-line"></span> SCROLL TO EXPLORE</span></div>
      </div>
      <aside class="engine-card" aria-label="Current interface lens">
        <div class="engine-card-top"><span class="eyebrow">YOUR CURRENT LENS</span><span class="auto-stamp"><span class="local-dot"></span>${state.previewLens ? 'PREVIEW' : 'AUTO'}</span></div>
        <div class="engine-lens-title"><span class="lens-index">0${Object.keys(modeNames).indexOf(lens) + 1}</span><h2>${esc(titleFor(lens))}</h2></div>
        <p class="engine-reason">${esc(state.previewLens ? `Previewing ${titleFor(lens)}. Your live profile is still learning.` : engine.getReason(lens))}</p>
        <div class="engine-card-bottom">
          <div class="signal-count"><b>${String(m.opens).padStart(2, '0')}</b><span>signals<br>opened</span></div>
          <div class="signal-count"><b>${String(uniqueTags).padStart(2, '0')}</b><span>threads<br>touched</span></div>
          <button class="text-link" type="button" data-action="explain">HOW IT LEARNS <span aria-hidden="true">↗</span></button>
        </div>
        <div class="engine-card-rule" aria-hidden="true"></div>
        <div class="engine-card-caption"><span>01—04</span><span>THE INDEX IS NOT FIXED</span></div>
      </aside>
    </section>`;
}

function renderModeIntro(lens) {
  const copy = {
    orbit: { number: '01', eyebrow: 'OPEN STRUCTURE', title: 'Follow a signal. See what it touches.', text: 'This is the whole field, not a ranked list. Pick a title; its neighboring ideas will come into focus.' },
    run: { number: '02', eyebrow: 'LINEAR STRUCTURE', title: 'One thread at a time.', text: 'Stay with a story long enough for the next one to make sense. The route is yours to keep moving through.' },
    pulse: { number: '03', eyebrow: 'QUICK STRUCTURE', title: 'One good pick. No endless scroll.', text: 'Start with a feeling. Get a small, considered set of titles, with one clear place to begin.' },
    shelf: { number: '04', eyebrow: 'PERSONAL STRUCTURE', title: 'Keep the stories that stay.', text: 'Your saved titles move to the front. Compare their tones, find the overlap, and build a queue of your own.' },
  }[lens];
  return `<section class="mode-intro" aria-labelledby="mode-title">
      <div class="mode-intro-number"><span>${copy.number}</span><i></i><small>OF 04<br>STRUCTURES</small></div>
      <div class="mode-intro-copy"><div class="eyebrow"><span class="eyebrow-line"></span>${copy.eyebrow}</div><h2 id="mode-title">${copy.title}</h2><p>${copy.text}</p></div>
      <div class="mode-intro-side"><span class="mode-name-ghost">${titleFor(lens).toUpperCase()}</span><button class="mode-preview-link" type="button" data-action="toggle-lenses">CHANGE LENS <span aria-hidden="true">↗</span></button></div>
    </section>`;
}

function renderTagButtons(tags, className = '') {
  return `<div class="tag-list ${className}">${tags.map((tag) => `<button class="tag-chip" type="button" data-action="tag-search" data-tag="${esc(tag)}">${esc(tag)}</button>`).join('')}</div>`;
}

function renderMiniShow(show, options = {}) {
  const { action = 'open-title', active = false, meta = show.tags[0], compact = false } = options;
  return `<button type="button" class="mini-show ${compact ? 'is-compact' : ''} ${active ? 'is-active' : ''}" data-action="${action}" data-id="${esc(show.id)}">
      ${cover(show, 'mini-show-cover')}
      <span class="mini-show-copy"><small>${esc(meta)}</small><strong>${esc(show.title)}</strong><em>${esc(show.detail)}</em></span>
      <span class="mini-show-arrow" aria-hidden="true">↗</span>
    </button>`;
}

function renderOrbit() {
  const selected = selectedShow();
  const relation = relatedShows(selected.id, 2);
  const lines = `<svg class="thread-lines" viewBox="0 0 1000 540" preserveAspectRatio="none" aria-hidden="true">
      <path d="M150 113 C270 38 386 63 500 81"/><path d="M500 81 C622 56 740 73 830 135"/>
      <path d="M150 113 C150 185 185 231 230 302"/><path d="M500 81 C445 170 520 226 600 292"/>
      <path d="M830 135 C856 218 868 301 840 367"/><path d="M230 302 C340 300 475 278 600 292"/>
      <path d="M600 292 C648 354 574 407 500 448"/><path d="M230 302 C196 355 166 395 150 437"/>
      <path d="M840 367 C737 411 646 433 500 448"/><circle cx="500" cy="81" r="3"/><circle cx="600" cy="292" r="3"/><circle cx="230" cy="302" r="3"/>
    </svg>`;
  return `<div class="orbit-layout mode-view">
    <section class="map-card" aria-label="Interactive anime story constellation">
      <div class="map-card-head"><div><span class="panel-kicker">FIELD MAP / 08 TITLES</span><h3>Stories in orbit</h3></div><span class="map-coordinates">35° 41′ N<br>139° 41′ E</span></div>
      <div class="constellation-map">${lines}<div class="map-axis" aria-hidden="true"><span>WANDER</span><span>FOLLOW</span></div>
        ${SHOWS.map((show, index) => {
          const [x, y] = mapPositions[show.id] || [50, 50];
          return `<button type="button" class="orbit-node ${selected.id === show.id ? 'is-selected' : ''}" style="--x:${x}%;--y:${y}%;--node:${index + 1}" data-action="open-title" data-id="${esc(show.id)}" aria-pressed="${selected.id === show.id}">
            <span class="orbit-node-art">${cover(show)}</span><span class="orbit-node-label">${esc(show.shortTitle)}</span><span class="orbit-node-tag">${esc(show.tags[0])}</span>
          </button>`;
        }).join('')}
      </div>
      <div class="map-card-foot"><span><i class="legend-point"></i> SELECT A SIGNAL TO OPEN ITS THREAD</span><span>LINES SHOW SHARED MOODS, NOT RANK</span></div>
    </section>
    <aside class="signal-panel" aria-label="Selected anime details">
      <div class="signal-panel-head"><span class="panel-kicker">OPEN SIGNAL <b>—</b> ${String(SHOWS.findIndex((show) => show.id === selected.id) + 1).padStart(2, '0')}</span><span class="panel-mark">F/S</span></div>
      <div class="signal-feature">
        <div class="signal-cover-wrap">${cover(selected, 'signal-cover')}<span class="cover-corner-label">${esc(selected.year)}</span></div>
        <div class="signal-meta"><span class="eyebrow">${esc(selected.detail)}</span><h3>${esc(selected.title)}</h3><p class="signal-logline">${esc(selected.logline)}</p></div>
      </div>
      <p class="signal-synopsis">${esc(selected.synopsis)}</p>
      ${renderTagButtons(selected.tags, 'signal-tags')}
      <div class="signal-actions">${saveButton(selected)}<button type="button" class="button-primary" data-action="follow-thread" data-id="${esc(selected.id)}">FOLLOW THIS THREAD <span aria-hidden="true">↗</span></button></div>
      <div class="related-block"><div class="related-heading"><span class="panel-kicker">NEAR THIS SIGNAL</span><span>SHARED THREADS</span></div>${relation.map((show) => renderMiniShow(show, { compact: true, meta: show.tags.find((tag) => selected.tags.includes(tag)) || show.tags[0] })).join('')}</div>
      <div class="panel-footnote"><span class="tiny-star" aria-hidden="true">✳</span><span>${esc(selected.note)}</span></div>
    </aside>
  </div>`;
}

function runQueue() {
  const first = selectedShow();
  const related = relatedShows(first.id, 5);
  return [first, ...related];
}

function renderRun() {
  const route = runQueue();
  const selected = route[0];
  return `<div class="run-layout mode-view">
    <aside class="route-rail">
      <div class="route-rail-top"><span class="panel-kicker">YOUR ROUTE</span><span class="route-counter">${String(route.length).padStart(2, '0')} SIGNALS</span></div>
      <h3>A thread<br>worth following.</h3>
      <p class="route-intro">A loose sequence based on the themes in ${esc(selected.shortTitle)}. Follow it, skip ahead, or leave the route at any time.</p>
      <div class="route-list" aria-label="Thread sequence">${route.map((show, index) => `<button type="button" class="route-step ${show.id === selected.id ? 'is-current' : ''}" data-action="run-step" data-id="${esc(show.id)}" aria-current="${show.id === selected.id ? 'step' : 'false'}"><span class="route-step-number">0${index + 1}</span><span class="route-step-copy"><strong>${esc(show.title)}</strong><small>${esc(show.tags.slice(0, 2).join(' / '))}</small></span><span class="route-step-state" aria-hidden="true">${show.id === selected.id ? '●' : '○'}</span></button>`).join('')}</div>
      <div class="route-rail-foot"><span class="route-line-mark"></span><span>YOU CAN LEAVE THE ROUTE<br>WITHOUT LOSING YOUR PLACE</span></div>
    </aside>
    <article class="reading-card">
      <div class="reading-card-head"><span class="panel-kicker">THREAD 01 <b>—</b> A CLOSER LOOK</span><span class="reading-number">01<span>/</span>${String(route.length).padStart(2, '0')}</span></div>
      <div class="reading-feature">
        <div class="reading-art-wrap">${cover(selected, 'reading-cover')}<span class="art-index">FRAME STUDY / ${String(selected.yearRank).padStart(2, '0')}</span></div>
        <div class="reading-copy"><span class="eyebrow">${esc(selected.detail)}</span><h3>${esc(selected.title)}</h3><p class="reading-logline">${esc(selected.logline)}</p><div class="reading-rule"></div><p class="reading-synopsis">${esc(selected.synopsis)}</p>${renderTagButtons(selected.tags, 'reading-tags')}<p class="reading-note"><span class="tiny-star" aria-hidden="true">✳</span>${esc(selected.note)}</p>
          <div class="reading-actions">${saveButton(selected)}<button type="button" class="button-primary" data-action="run-next" data-id="${esc(route[1]?.id || selected.id)}">${route[1] ? 'CONTINUE THE THREAD' : 'READ THIS AGAIN'} <span aria-hidden="true">→</span></button></div>
        </div>
      </div>
      <div class="reading-card-foot"><span>THE ROUTE IS MADE FROM YOUR LAST OPEN SIGNAL</span><button type="button" data-action="leave-run">BACK TO THE MAP <span aria-hidden="true">↗</span></button></div>
    </article>
  </div>`;
}

function pulseQueue() {
  const filtered = SHOWS.filter((show) => state.mood === 'any' || show.moods.includes(state.mood));
  const pool = filtered.length ? filtered : SHOWS;
  return [...pool].sort((a, b) => fitScore(b, engine.profile) - fitScore(a, engine.profile) || a.yearRank - b.yearRank);
}

function renderPulse() {
  const queue = pulseQueue();
  const index = state.pulseIndex % queue.length;
  const pick = queue[index];
  const shortlist = queue.filter((show) => show.id !== pick.id).slice(0, 3);
  const moodLabel = MOODS.find((mood) => mood.id === state.mood)?.label || 'No mood, just browse';
  return `<div class="pulse-layout mode-view">
    <section class="pulse-picker">
      <div class="pulse-picker-head"><span class="panel-kicker">TONIGHT’S SIGNAL <b>—</b> ${String(index + 1).padStart(2, '0')} / ${String(queue.length).padStart(2, '0')}</span><span class="pulse-stamp"><i></i> ONE PICK AT A TIME</span></div>
      <div class="mood-filter"><span class="filter-label">SET A FEELING</span><div class="mood-chips">${MOODS.map((mood) => `<button type="button" class="mood-chip ${state.mood === mood.id ? 'is-active' : ''}" data-action="set-mood" data-mood="${esc(mood.id)}" aria-pressed="${state.mood === mood.id}">${esc(mood.label)}</button>`).join('')}</div></div>
      <article class="pick-card">
        <div class="pick-art-stage"><span class="pick-art-orbit" aria-hidden="true"></span>${cover(pick, 'pick-cover')}<span class="pick-art-caption">A FRAME/SHIFT STUDY<br>NOT OFFICIAL KEY ART</span><span class="pick-match">${fitScore(pick, engine.profile)}<small>% FIT</small></span></div>
        <div class="pick-copy"><span class="eyebrow">${esc(pick.detail)} <b>—</b> ${esc(pick.moods[0].toUpperCase())}</span><h3>${esc(pick.title)}</h3><p class="pick-logline">${esc(pick.logline)}</p><div class="pick-reason"><span class="tiny-star" aria-hidden="true">✳</span><p><b>WHY THIS ONE</b><br>${esc(state.mood === 'any' ? `It carries a thread from your current profile${Object.keys(engine.profile.metrics.tagCounts).length ? ' without asking you to commit to a genre' : ' and gives the map somewhere to start'}.` : `It sits in the ${moodLabel.toLowerCase()} pocket you picked.`)}</p></div><div class="pick-tags">${renderTagButtons(pick.tags)}</div>
          <div class="pick-actions">${saveButton(pick)}<button type="button" class="button-primary" data-action="title-detail" data-id="${esc(pick.id)}">OPEN THE FILE <span aria-hidden="true">↗</span></button><button type="button" class="skip-pick" data-action="skip-pick">NOT THIS ONE <span aria-hidden="true">→</span></button></div>
        </div>
      </article>
    </section>
    <aside class="pulse-shortlist"><div class="shortlist-heading"><span class="panel-kicker">THREE OTHER SIGNALS</span><span class="shortlist-count">${String(shortlist.length).padStart(2, '0')}</span></div><p class="shortlist-copy">A small queue, not a bottomless feed.</p><div class="shortlist-list">${shortlist.map((show, i) => `<div class="shortlist-item"><span class="shortlist-number">0${i + 2}</span>${renderMiniShow(show, { compact: true, action: 'open-title', meta: show.tags[0] })}<span class="shortlist-fit">${fitScore(show, engine.profile)}%<small>FIT</small></span></div>`).join('')}</div><div class="pulse-quiet-note"><span>⌁</span><p>Choosing “not this one” helps the index learn your pace. It doesn’t add a title to your history.</p></div></aside>
  </div>`;
}

function renderShelf() {
  const saved = savedIds().map((id) => showById(id));
  const selected = saved.find((show) => show.id === state.shelfSelected) || saved[0] || selectedShow();
  const suggestions = relatedShows(selected.id, 5).filter((show) => !savedIds().includes(show.id));
  const compare = saved.find((show) => show.id === state.compareId && show.id !== selected.id) || saved.find((show) => show.id !== selected.id) || suggestions[0];
  const hasSaved = saved.length > 0;
  return `<div class="shelf-layout mode-view">
    <aside class="shelf-rail"><div class="shelf-rail-heading"><span class="panel-kicker">KEPT CLOSE</span><b>${String(saved.length).padStart(2, '0')}</b></div><h3>Your shelf<br>so far.</h3><p>Saved titles stay here, even when the rest of the index changes shape.</p>
      ${hasSaved ? `<div class="shelf-list">${saved.map((show, index) => `<button class="shelf-item ${selected.id === show.id ? 'is-active' : ''}" type="button" data-action="select-shelf" data-id="${esc(show.id)}" aria-pressed="${selected.id === show.id}"><span class="shelf-item-index">0${index + 1}</span>${cover(show, 'shelf-thumb')}<span><strong>${esc(show.title)}</strong><small>${esc(show.tags.slice(0, 2).join(' / '))}</small></span><i aria-hidden="true">↗</i></button>`).join('')}</div>` : `<div class="empty-shelf"><span class="empty-shelf-mark">＋</span><strong>No titles kept yet.</strong><small>Save a couple of stories to give this space its shape.</small></div>`}
      <button type="button" class="rail-action" data-action="toggle-lenses">${hasSaved ? 'PREVIEW ANOTHER LENS' : 'EXPLORE THE MAP'} <span aria-hidden="true">↗</span></button>
    </aside>
    <section class="comparison-space"><div class="comparison-head"><div><span class="panel-kicker">THE COMPARISON TABLE</span><h3>What do these stories share?</h3></div><span class="comparison-mark">F/S <i>—</i> PRIVATE CUT</span></div>
      ${hasSaved ? `<div class="comparison-grid">
        <article class="compare-card compare-main"><div class="compare-art">${cover(selected, 'compare-cover')}<span class="compare-art-label">YOUR PICK / 01</span></div><div class="compare-copy"><span class="eyebrow">${esc(selected.detail)}</span><h4>${esc(selected.title)}</h4><p>${esc(selected.logline)}</p>${renderTagButtons(selected.tags)}<div class="compare-card-foot">${saveButton(selected, 'is-small')}<span class="compare-fit">${fitScore(selected, engine.profile)}<small>% FIT</small></span></div></div></article>
        <div class="compare-bridge"><span>↔</span><small>COMPARE<br>THE FEEL</small></div>
        ${compare ? `<article class="compare-card compare-second"><div class="compare-art">${cover(compare, 'compare-cover')}<span class="compare-art-label">${saved.some((show) => show.id === compare.id) ? 'YOUR PICK / 02' : 'NEARBY SIGNAL'}</span></div><div class="compare-copy"><span class="eyebrow">${esc(compare.detail)}</span><h4>${esc(compare.title)}</h4><p>${esc(compare.logline)}</p>${renderTagButtons(compare.tags)}<div class="compare-card-foot">${saved.some((show) => show.id === compare.id) ? saveButton(compare, 'is-small') : `<button class="save-control" type="button" data-action="save" data-id="${esc(compare.id)}"><span class="save-glyph">+</span><span>ADD TO YOUR SHELF</span></button>`}<span class="compare-fit">${fitScore(compare, engine.profile)}<small>% FIT</small></span></div></div></article>` : `<div class="compare-placeholder"><span>02</span><p>Save one more title and the comparison will take shape.</p></div>`}
      </div>` : `<div class="shelf-empty-stage"><div class="shelf-empty-illustration" aria-hidden="true"><span></span><span></span><span></span><b>＋</b></div><div><span class="eyebrow">THIS SPACE IS YOURS</span><h4>Nothing is pinned down yet.</h4><p>Open a title in the map and save it. The index will bring it here, then reorganize around what you keep.</p><button class="button-primary" type="button" data-action="auto-lens">RETURN TO YOUR LIVE LENS <span aria-hidden="true">↗</span></button></div></div>`}
      <div class="shelf-nearby"><div class="related-heading"><span class="panel-kicker">NEAR YOUR SELECTED SIGNAL</span><span>ADD OR IGNORE</span></div><div class="nearby-list">${suggestions.slice(0, 3).map((show) => `<div class="nearby-suggestion">${renderMiniShow(show, { compact: true, action: 'title-detail', meta: show.tags[0] })}<button class="nearby-save" type="button" data-action="save" data-id="${esc(show.id)}">+ SAVE TO SHELF</button></div>`).join('')}</div></div>
    </section>
  </div>`;
}

function renderMode(lens) {
  const view = lens === 'run' ? renderRun() : lens === 'pulse' ? renderPulse() : lens === 'shelf' ? renderShelf() : renderOrbit();
  return `<div class="mode-section" id="mode-section">${renderModeIntro(lens)}${view}</div>`;
}

function renderFooter() {
  return `<footer class="site-footer"><div class="footer-top"><a class="footer-wordmark" href="#top" data-action="home">FRAME<span>/</span>SHIFT</a><p>AN INDEX THAT MOVES<br>WHEN YOU DO.</p><span class="footer-glyph" aria-hidden="true">✳</span></div><div class="footer-bottom"><span>INDEPENDENT ANIME DISCOVERY CONCEPT · NO AFFILIATION WITH THE TITLES SHOWN</span><div><span><i class="local-dot"></i> YOUR PROFILE STAYS IN THIS BROWSER</span><button type="button" data-action="explain">HOW IT WORKS</button><button type="button" data-action="reset">RESET PROFILE</button></div></div></footer>`;
}

function renderEnginePanel() {
  const p = engine.profile;
  const m = p.metrics;
  const scores = engine.getScores();
  const tagEntries = Object.entries(m.tagCounts).sort((a, b) => b[1] - a[1]).slice(0, 4);
  const stats = [
    ['01', 'Signal opens', m.opens],
    ['02', 'Deep reads', m.deepReads],
    ['03', 'Quick skips', m.skips],
    ['04', 'Linear steps', m.linearAdvances],
    ['05', 'Saved titles', p.savedIds.length],
    ['06', 'Return visits', Math.max(0, p.visits - 1)],
  ];
  return `<div class="modal-backdrop" data-action="close-panel"><section class="engine-dialog" role="dialog" aria-modal="true" aria-labelledby="engine-dialog-title" data-dialog="engine">
    <div class="dialog-top"><span class="eyebrow">FRAME/SHIFT / EVOLUTION ENGINE</span><button class="dialog-close" type="button" data-action="close-panel" aria-label="Close">×</button></div>
    <div class="dialog-main"><div class="dialog-title-block"><span class="engine-dialog-index">F/S — 01</span><h2 id="engine-dialog-title">Not random.<br><em>Responsive.</em></h2><p>The interface looks at the way you move through this index and chooses a more useful shape. There’s no account, server profile, or hidden third-party tracker.</p></div>
      <div class="engine-method"><span class="panel-kicker">WHAT THE INDEX NOTICES</span><ul><li><b>01</b><span>Which titles and story tags you open</span></li><li><b>02</b><span>Whether you jump between themes or follow a route</span></li><li><b>03</b><span>How long you stay and how far you read</span></li><li><b>04</b><span>What you save, skip, or return to later</span></li></ul><div class="topic-readout"><span class="panel-kicker">YOUR MOST-OPENED THREADS</span><div>${tagEntries.length ? tagEntries.map(([tag, count]) => `<span>${esc(tag)} <b>${count}</b></span>`).join('') : '<span class="readout-empty">No pattern yet — explore a few signals.</span>'}</div></div><div class="score-readout"><div class="score-readout-head"><span class="panel-kicker">LIVE LENS WEIGHTS / 0–100</span><span>DECISION SIGNAL</span></div>${Object.entries(scores).map(([lens, score]) => `<div class="score-row ${engine.getLens() === lens ? 'is-active' : ''}"><span>${titleFor(lens)}</span><div class="score-track"><i style="width:${score}%"></i></div><b>${String(score).padStart(2, '0')}</b></div>`).join('')}</div></div></div>
    <div class="lens-explainer"><div class="lens-explainer-heading"><span class="panel-kicker">FOUR STRUCTURES / ONE INDEX</span><span>DETERMINISTIC · DEVICE ONLY</span></div><div class="lens-explainer-grid">
      <article><span>01 / ORBIT</span><h3>Connected map</h3><p>Broad topic-hopping keeps relationships and neighboring titles in the foreground.</p></article>
      <article><span>02 / RUN</span><h3>Guided route</h3><p>A follow-thread action or repeated linear reading turns discovery into a sequence.</p></article>
      <article><span>03 / PULSE</span><h3>Quick pick</h3><p>Repeated fast skips compress the catalogue into a mood-led shortlist.</p></article>
      <article><span>04 / SHELF</span><h3>Compare space</h3><p>Saving two titles, or returning to a saved title, makes your collection the main navigation.</p></article>
    </div></div>
    <div class="dialog-stats">${stats.map(([num, label, value]) => `<div><span>${num}</span><b>${String(value).padStart(2, '0')}</b><small>${label}</small></div>`).join('')}</div>
    <div class="dialog-bottom"><p><span class="local-dot"></span> All signals live in local storage on this device. Clear them any time.</p><button class="text-link" type="button" data-action="reset">RESET MY PROFILE <span aria-hidden="true">↗</span></button></div>
  </section></div>`;
}

function searchResultsMarkup(query) {
  const term = query.trim().toLowerCase();
  const results = SHOWS.filter((show) => !term || [show.title, show.detail, show.logline, ...show.tags, ...show.moods].join(' ').toLowerCase().includes(term));
  if (!results.length) return '<p class="search-empty">No signal found. Try a mood or a story tag.</p>';
  return results.map((show) => `<button class="search-result" type="button" data-action="open-title" data-id="${esc(show.id)}">${cover(show, 'search-result-cover')}<span><small>${esc(show.tags.slice(0, 2).join(' · '))}</small><b>${esc(show.title)}</b><em>${esc(show.logline)}</em></span><i aria-hidden="true">↗</i></button>`).join('');
}

function renderSearchPanel() {
  return `<div class="modal-backdrop" data-action="close-panel"><section class="search-dialog" role="dialog" aria-modal="true" aria-labelledby="search-title" data-dialog="search"><div class="dialog-top"><span class="eyebrow">SEARCH / THE WHOLE INDEX</span><button class="dialog-close" type="button" data-action="close-panel" aria-label="Close">×</button></div><h2 id="search-title">Find a signal.</h2><label class="search-input-wrap"><span aria-hidden="true">⌕</span><input type="search" data-search-input autocomplete="off" placeholder="Title, mood, or story thread…" value="${esc(state.searchQuery)}" aria-label="Search by title, mood, or story thread"><kbd>ESC</kbd></label><div class="search-results" data-search-results>${searchResultsMarkup(state.searchQuery)}</div><p class="search-footnote">Searching doesn’t change your lens. Opening a title does.</p></section></div>`;
}

function renderDetailPanel() {
  const show = showById(state.detailId || state.selected);
  const related = relatedShows(show.id, 2);
  return `<div class="modal-backdrop" data-action="close-panel"><section class="detail-dialog" role="dialog" aria-modal="true" aria-labelledby="detail-title" data-dialog="detail"><button class="dialog-close floating-close" type="button" data-action="close-panel" aria-label="Close">×</button><div class="detail-dialog-art">${cover(show, 'detail-cover')}<span class="cover-corner-label">${esc(show.year)}</span></div><div class="detail-dialog-copy"><span class="eyebrow">${esc(show.detail)}</span><h2 id="detail-title">${esc(show.title)}</h2><p class="detail-logline">${esc(show.logline)}</p><p>${esc(show.synopsis)}</p>${renderTagButtons(show.tags)}<div class="detail-dialog-actions">${saveButton(show)}<button class="button-primary" type="button" data-action="follow-thread" data-id="${esc(show.id)}">FOLLOW THIS THREAD <span aria-hidden="true">↗</span></button></div><div class="detail-related"><span class="panel-kicker">IF THIS STAYS WITH YOU</span>${related.map((item) => renderMiniShow(item, { compact: true })).join('')}</div></div></section></div>`;
}

function renderOverlay() {
  if (state.panel === 'engine') return renderEnginePanel();
  if (state.panel === 'search') return renderSearchPanel();
  if (state.panel === 'detail') return renderDetailPanel();
  return '';
}

function render() {
  if (!root) return;
  const lens = activeLens();
  root.innerHTML = `${renderHeader(lens)}<main id="main" class="page-shell">${renderHero(lens)}${state.toast ? `<div class="shift-toast" role="status"><span class="toast-mark">✳</span>${esc(state.toast)}<button type="button" data-action="dismiss-toast" aria-label="Dismiss notification">×</button></div>` : ''}${renderMode(lens)}</main>${renderFooter()}${renderOverlay()}`;
}

function changeShow(id, linear = false) {
  const show = showById(id);
  state.selected = show.id;
  state.shelfSelected = show.id;
  state.detailId = null;
  state.panel = null;
  state.lensMenuOpen = false;
  if (linear) engine.recordAdvance(show);
  else engine.recordOpen(show);
}

function nextPulsePick() {
  const queue = pulseQueue();
  const current = queue[state.pulseIndex % queue.length];
  const nextIndex = (state.pulseIndex + 1) % queue.length;
  const next = queue[nextIndex];
  state.pulseIndex = nextIndex;
  engine.recordSkip(next || current);
}

function handleAction(button) {
  const action = button.dataset.action;
  const id = button.dataset.id;
  const show = id ? showById(id) : null;
  const wasLens = engine.getLens();

  switch (action) {
    case 'toggle-lenses':
      state.lensMenuOpen = !state.lensMenuOpen;
      break;
    case 'preview-lens':
      state.previewLens = button.dataset.lens;
      state.lensMenuOpen = false;
      state.panel = null;
      break;
    case 'auto-lens':
      state.previewLens = null;
      state.lensMenuOpen = false;
      state.panel = null;
      break;
    case 'open-title':
    case 'open-search-result':
      if (show) changeShow(show.id);
      break;
    case 'open-shelf':
      state.previewLens = 'shelf';
      state.shelfSelected = savedIds()[0] || null;
      state.lensMenuOpen = false;
      break;
    case 'open-title-detail':
    case 'title-detail':
      if (show) {
        engine.recordOpen(show);
        state.selected = show.id;
        state.detailId = show.id;
        state.panel = 'detail';
        state.lensMenuOpen = false;
      }
      break;
    case 'save':
      if (show) {
        const added = engine.toggleSave(show);
        if (added) state.shelfSelected = show.id;
      }
      break;
    case 'follow-thread':
      if (show) {
        state.previewLens = null;
        state.panel = null;
        state.selected = show.id;
        state.shelfSelected = show.id;
        engine.recordAdvance(show);
      }
      break;
    case 'run-next':
      if (show) changeShow(show.id, true);
      break;
    case 'run-step':
      if (show) changeShow(show.id, show.id !== state.selected);
      break;
    case 'leave-run':
      state.previewLens = 'orbit';
      state.selected = state.selected || 'sonny-boy';
      break;
    case 'skip-pick':
      nextPulsePick();
      break;
    case 'set-mood':
      state.mood = button.dataset.mood || 'any';
      state.pulseIndex = 0;
      engine.recordMood(state.mood);
      break;
    case 'select-shelf':
      if (show) {
        state.shelfSelected = show.id;
        state.selected = show.id;
        state.compareId = null;
        engine.recordOpen(show);
      }
      break;
    case 'select-compare':
      if (show) state.compareId = show.id;
      break;
    case 'tag-search':
      state.searchQuery = button.dataset.tag || '';
      state.panel = 'search';
      engine.recordAction('tag', { tag: state.searchQuery });
      break;
    case 'search':
      state.panel = 'search';
      state.searchQuery = '';
      state.lensMenuOpen = false;
      break;
    case 'explain':
      state.panel = 'engine';
      state.lensMenuOpen = false;
      break;
    case 'close-panel':
      if (button.matches('.modal-backdrop') || button.classList.contains('dialog-close')) state.panel = null;
      break;
    case 'reset':
      if (window.confirm('Reset this browser’s FRAME/SHIFT profile and saved titles?')) {
        engine.reset();
        state.previewLens = null;
        state.panel = null;
        state.lensMenuOpen = false;
        state.selected = 'sonny-boy';
        state.shelfSelected = null;
        state.compareId = null;
        state.mood = 'any';
        state.pulseIndex = 0;
        setToast('LOCAL PROFILE RESET · YOUR MAP IS OPEN AGAIN');
      }
      break;
    case 'home':
      state.previewLens = null;
      state.panel = null;
      state.lensMenuOpen = false;
      window.scrollTo({ top: 0, behavior: 'smooth' });
      break;
    case 'dismiss-toast':
      state.toast = '';
      break;
    default:
      return;
  }

  if (engine.getLens() !== wasLens && !state.toast) {
    setToast(`AUTO LENS SHIFT · ${titleFor(wasLens).toUpperCase()} → ${titleFor(engine.getLens()).toUpperCase()}`);
  } else {
    render();
  }

  if (state.panel === 'search') {
    requestAnimationFrame(() => root.querySelector('[data-search-input]')?.focus());
  }
}

root.addEventListener('click', (event) => {
  const button = event.target.closest('[data-action]');
  if (!button || !root.contains(button)) return;
  if (button.matches('.modal-backdrop') && event.target !== button) return;
  event.preventDefault();
  handleAction(button);
});

root.addEventListener('input', (event) => {
  if (!event.target.matches('[data-search-input]')) return;
  state.searchQuery = event.target.value;
  const results = root.querySelector('[data-search-results]');
  if (results) results.innerHTML = searchResultsMarkup(state.searchQuery);
});

window.addEventListener('keydown', (event) => {
  if (event.key === 'Escape') {
    if (state.panel || state.lensMenuOpen) {
      state.panel = null;
      state.lensMenuOpen = false;
      render();
    }
  }
});

window.addEventListener('scroll', () => {
  const before = engine.getLens();
  const maxScroll = document.documentElement.scrollHeight - window.innerHeight;
  if (maxScroll > 0) engine.recordDepth(window.scrollY / maxScroll);
  const after = engine.getLens();
  if (before !== after) setToast(`AUTO LENS SHIFT · ${titleFor(before).toUpperCase()} → ${titleFor(after).toUpperCase()}`);
}, { passive: true });

window.setInterval(() => {
  const before = engine.getLens();
  engine.observeDwell();
  const after = engine.getLens();
  if (before !== after) setToast(`AUTO LENS SHIFT · ${titleFor(before).toUpperCase()} → ${titleFor(after).toUpperCase()}`);
}, 2_000);

window.addEventListener('pagehide', () => engine.closeFocused());

render();
