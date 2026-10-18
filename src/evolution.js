const STORAGE_KEY = 'frame-shift.profile.v1';
const QUICK_READ_MS = 9_000;
const DEEP_READ_MS = 12_000;

function freshProfile() {
  return {
    version: 1,
    visits: 0,
    lastVisitAt: 0,
    savedIds: [],
    events: [],
    metrics: {
      opens: 0,
      deepReads: 0,
      fastSkims: 0,
      linearAdvances: 0,
      topicSwitches: 0,
      savesAdded: 0,
      skips: 0,
      dwellTotalMs: 0,
      maxDepth: 0,
      tagCounts: {},
      moodCounts: {},
      openCounts: {},
      lastTag: null,
      lastShowId: null,
    },
  };
}

function normalizeProfile(raw) {
  const base = freshProfile();
  if (!raw || typeof raw !== 'object') return base;
  const metrics = { ...base.metrics, ...(raw.metrics || {}) };
  metrics.tagCounts = metrics.tagCounts && typeof metrics.tagCounts === 'object' ? metrics.tagCounts : {};
  metrics.moodCounts = metrics.moodCounts && typeof metrics.moodCounts === 'object' ? metrics.moodCounts : {};
  metrics.openCounts = metrics.openCounts && typeof metrics.openCounts === 'object' ? metrics.openCounts : {};
  return {
    ...base,
    ...raw,
    visits: Number(raw.visits) || 0,
    lastVisitAt: Number(raw.lastVisitAt) || 0,
    savedIds: Array.isArray(raw.savedIds) ? raw.savedIds : [],
    events: Array.isArray(raw.events) ? raw.events.slice(-80) : [],
    metrics,
  };
}

function persist(profile) {
  try {
    localStorage.setItem(STORAGE_KEY, JSON.stringify(profile));
  } catch (error) {
    // The experience still works for this session if storage is unavailable.
    console.warn('FRAME/SHIFT could not save this local profile.', error);
  }
}

function loadAndStartVisit() {
  let profile;
  try {
    profile = normalizeProfile(JSON.parse(localStorage.getItem(STORAGE_KEY) || 'null'));
  } catch {
    profile = freshProfile();
  }
  const now = Date.now();
  // A reload during the same browsing session is not counted as a return visit.
  if (!profile.lastVisitAt || now - profile.lastVisitAt > 30 * 60 * 1000) {
    profile.visits += 1;
  }
  profile.lastVisitAt = now;
  persist(profile);
  return profile;
}

export function createEvolutionEngine() {
  let profile = loadAndStartVisit();
  let focused = null;

  function log(type, detail = {}) {
    profile.events.push({ type, at: Date.now(), ...detail });
    profile.events = profile.events.slice(-80);
    persist(profile);
  }

  function countDeepRead(reason) {
    if (!focused || focused.deepCounted) return;
    focused.deepCounted = true;
    profile.metrics.deepReads += 1;
    log('deep-read', { id: focused.id, reason });
  }

  function closeFocused() {
    if (!focused) return;
    const duration = Math.max(0, Date.now() - focused.startedAt);
    const depth = focused.depth || 0;
    const metrics = profile.metrics;
    metrics.dwellTotalMs += duration;
    metrics.maxDepth = Math.max(metrics.maxDepth, depth);
    if (!focused.deepCounted && (duration >= DEEP_READ_MS || depth >= 0.56)) countDeepRead('close');
    else if (!focused.deepCounted && duration >= 1_200 && duration < QUICK_READ_MS) metrics.fastSkims += 1;
    log('close', { id: focused.id, seconds: Math.round(duration / 1000), depth: Math.round(depth * 100) });
    focused = null;
  }

  function recordOpen(show) {
    if (!show) return;
    if (focused?.id === show.id) return;
    closeFocused();
    const metrics = profile.metrics;
    const firstTag = show.tags?.[0] || 'Untitled';
    if (metrics.lastTag && metrics.lastTag !== firstTag) metrics.topicSwitches += 1;
    metrics.opens += 1;
    metrics.lastTag = firstTag;
    metrics.lastShowId = show.id;
    metrics.openCounts[show.id] = (metrics.openCounts[show.id] || 0) + 1;
    for (const tag of show.tags || []) metrics.tagCounts[tag] = (metrics.tagCounts[tag] || 0) + 1;
    for (const mood of show.moods || []) metrics.moodCounts[mood] = (metrics.moodCounts[mood] || 0) + 1;
    focused = { id: show.id, startedAt: Date.now(), depth: 0 };
    log('open', { id: show.id, tags: show.tags || [] });
  }

  function recordDepth(value) {
    if (!focused) return;
    const depth = Math.max(0, Math.min(1, value));
    focused.depth = Math.max(focused.depth, depth);
    if (focused.depth >= 0.56) countDeepRead('scroll-depth');
  }

  function observeDwell() {
    if (focused && Date.now() - focused.startedAt >= DEEP_READ_MS) countDeepRead('dwell-time');
  }

  function recordAdvance(show) {
    profile.metrics.linearAdvances += 1;
    log('advance', { id: show?.id || null });
    recordOpen(show);
  }

  function recordSkip(show) {
    profile.metrics.skips += 1;
    log('skip', { id: show?.id || null });
    if (show) recordOpen(show);
    else persist(profile);
  }

  function toggleSave(show) {
    const index = profile.savedIds.indexOf(show.id);
    if (index >= 0) {
      profile.savedIds.splice(index, 1);
      log('remove-save', { id: show.id });
      return false;
    }
    profile.savedIds.push(show.id);
    profile.metrics.savesAdded += 1;
    for (const tag of show.tags || []) profile.metrics.tagCounts[tag] = (profile.metrics.tagCounts[tag] || 0) + 1;
    for (const mood of show.moods || []) profile.metrics.moodCounts[mood] = (profile.metrics.moodCounts[mood] || 0) + 1;
    log('save', { id: show.id, tags: show.tags || [] });
    return true;
  }

  function recordMood(mood) {
    if (mood && mood !== 'any') {
      profile.metrics.moodCounts[mood] = (profile.metrics.moodCounts[mood] || 0) + 1;
      log('mood', { mood });
    }
  }

  function recordAction(type, detail = {}) {
    log(type, detail);
  }

  function getScores() {
    const m = profile.metrics;
    const completedOpens = Math.max(1, m.opens - (focused ? 1 : 0));
    const averageDwell = m.dwellTotalMs / completedOpens;
    const tagVariety = Object.keys(m.tagCounts).length;
    const repeats = Object.values(m.openCounts).reduce((sum, count) => sum + Math.max(0, count - 1), 0);
    const deepRate = m.deepReads / Math.max(1, m.deepReads + m.fastSkims);
    return {
      orbit: Math.max(0, Math.min(100, 9 + tagVariety * 5 + m.topicSwitches * 9 - m.linearAdvances * 4)),
      run: Math.min(100, m.linearAdvances * 34 + m.deepReads * 19 + Math.round(deepRate * 10)),
      pulse: Math.min(100, m.skips * 29 + m.fastSkims * 15 + (m.opens >= 2 && averageDwell > 0 && averageDwell < QUICK_READ_MS ? 13 : 0)),
      shelf: Math.min(100, profile.savedIds.length * 34 + repeats * 10 + Math.max(0, profile.visits - 1) * 22),
    };
  }

  function getLens() {
    const m = profile.metrics;
    const scores = getScores();
    const completedOpens = Math.max(1, m.opens - (focused ? 1 : 0));
    const averageDwell = m.dwellTotalMs / completedOpens;

    // Strong collection intent has priority: this should feel like a deliberate front-door change.
    if (profile.savedIds.length >= 2 || (profile.visits >= 2 && profile.savedIds.length >= 1)) return 'shelf';

    // The signal gates keep one accidental click from changing the whole navigation model.
    const eligible = [];
    if (m.linearAdvances >= 1 || (m.deepReads >= 2 && m.deepReads > m.fastSkims)) eligible.push('run');
    if (m.skips >= 2 || (m.fastSkims >= 2 && m.fastSkims > m.deepReads && averageDwell < 15_000)) eligible.push('pulse');
    if (m.opens >= 3 && m.topicSwitches >= 2) eligible.push('orbit');
    if (!eligible.length) return 'orbit';
    return eligible.sort((a, b) => scores[b] - scores[a])[0];
  }

  function getReason(lens = getLens()) {
    const m = profile.metrics;
    const topTag = Object.entries(m.tagCounts).sort((a, b) => b[1] - a[1])[0]?.[0];
    if (lens === 'shelf') {
      return `You’ve kept ${profile.savedIds.length} ${profile.savedIds.length === 1 ? 'title' : 'titles'} close${topTag ? `, with ${topTag.toLowerCase()} in the mix` : ''}. Your shelf is now the front door.`;
    }
    if (lens === 'run') return 'You’ve been following one thing into the next. The index has become a guided route.';
    if (lens === 'pulse') return 'You’re moving at watch-pick speed. The index is keeping the choices short and decisive.';
    if (m.topicSwitches >= 2) return 'You keep crossing between different kinds of stories. The connected map is staying open.';
    if (topTag) return `You’ve opened a few ${topTag.toLowerCase()} signals. The map is keeping neighboring threads close.`;
    return 'A few clicks will reveal your pattern. For now, the whole story map is open.';
  }

  function reset() {
    profile = freshProfile();
    focused = null;
    profile.visits = 1;
    profile.lastVisitAt = Date.now();
    persist(profile);
  }

  return {
    get profile() { return profile; },
    getLens,
    getScores,
    getReason,
    recordOpen,
    recordDepth,
    observeDwell,
    recordAdvance,
    recordSkip,
    toggleSave,
    recordMood,
    recordAction,
    closeFocused,
    reset,
  };
}
