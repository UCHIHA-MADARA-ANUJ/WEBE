export const SHOWS = [
  {
    id: 'sonny-boy',
    title: 'Sonny Boy',
    shortTitle: 'SONNY BOY',
    year: '2021',
    detail: '12 episodes · Madhouse',
    tags: ['Surreal', 'Coming of age', 'Sci-fi'],
    moods: ['strange', 'quiet', 'thoughtful'],
    logline: 'A class drifts beyond the rules of the world they knew.',
    synopsis: 'A school building slips into another dimension, and its students begin to develop strange abilities. What follows is less a battle for answers than a beautiful, disorienting search for a way home.',
    note: 'For the days when a story can leave a question open.',
    yearRank: 1,
  },
  {
    id: 'odd-taxi',
    title: 'Odd Taxi',
    shortTitle: 'ODD TAXI',
    year: '2021',
    detail: '13 episodes · OLM',
    tags: ['Mystery', 'Crime', 'Dialogue'],
    moods: ['mystery', 'quiet', 'thoughtful'],
    logline: 'Every passenger leaves a clue. None of them know it yet.',
    synopsis: 'A taciturn taxi driver moves through a city full of small talk, strange coincidences, and people hiding something. Separate conversations slowly converge around the disappearance of a high-school girl.',
    note: 'A tightly plotted mystery that rewards paying attention.',
    yearRank: 2,
  },
  {
    id: 'eizouken',
    title: 'Keep Your Hands Off Eizouken!',
    shortTitle: 'EIZOUKEN!',
    year: '2020',
    detail: '12 episodes · Science SARU',
    tags: ['Creative', 'Comedy', 'Coming of age'],
    moods: ['warm', 'electric', 'thoughtful'],
    logline: 'Three friends turn impossible ideas into moving pictures.',
    synopsis: 'A trio of students forms an animation club and builds entire worlds out of their own imagination. The joy is in watching their ideas become drawings, motion, and a reason to keep creating.',
    note: 'A love letter to making things with your friends.',
    yearRank: 3,
  },
  {
    id: 'mob-psycho',
    title: 'Mob Psycho 100',
    shortTitle: 'MOB PSYCHO 100',
    year: '2016–22',
    detail: '37 episodes · Bones',
    tags: ['Supernatural', 'Action', 'Coming of age'],
    moods: ['electric', 'warm', 'strange'],
    logline: 'The most powerful person in the room is trying to be kind.',
    synopsis: 'Shigeo “Mob” Kageyama is a quiet middle-schooler with enormous psychic power. He would rather improve as a person than use it, even when the world around him gets increasingly bizarre.',
    note: 'Big feelings, explosive animation, unexpectedly gentle heart.',
    yearRank: 4,
  },
  {
    id: 'violet-evergarden',
    title: 'Violet Evergarden',
    shortTitle: 'VIOLET EVERGARDEN',
    year: '2018',
    detail: '13 episodes · Kyoto Animation',
    tags: ['Drama', 'Letters', 'Quiet'],
    moods: ['quiet', 'heartfelt', 'thoughtful'],
    logline: 'A former soldier learns to give shape to other people’s words.',
    synopsis: 'Violet begins work as an Auto Memory Doll, writing letters for people who cannot find the words themselves. Each assignment brings her closer to understanding a phrase she once heard and could not understand.',
    note: 'For a patient, beautifully observed emotional journey.',
    yearRank: 5,
  },
  {
    id: 'edgerunners',
    title: 'Cyberpunk: Edgerunners',
    shortTitle: 'EDGERUNNERS',
    year: '2022',
    detail: '10 episodes · Studio Trigger',
    tags: ['Sci-fi', 'Action', 'Tragedy'],
    moods: ['electric', 'intense', 'heartfelt'],
    logline: 'A kid with nothing left to lose runs at the speed of the city.',
    synopsis: 'In Night City, David Martinez throws himself into the world of outlaw mercenaries known as edgerunners. It is a short, loud story about ambition, chosen family, and what a city can take from you.',
    note: 'A high-voltage sprint with a bruised, human center.',
    yearRank: 6,
  },
  {
    id: 'frieren',
    title: 'Frieren: Beyond Journey’s End',
    shortTitle: 'FRIEREN',
    year: '2023',
    detail: '28 episodes · Madhouse',
    tags: ['Fantasy', 'Adventure', 'Quiet'],
    moods: ['quiet', 'heartfelt', 'thoughtful'],
    logline: 'The adventure is over. Now the long way home begins.',
    synopsis: 'Long after a heroic party defeats the Demon King, the elf mage Frieren begins to understand the time she shared with her companions. A reflective fantasy about memory, friendship, and the lives that continue after the ending.',
    note: 'A gentle road story with the scale of a legend.',
    yearRank: 7,
  },
  {
    id: 'tatami-galaxy',
    title: 'The Tatami Galaxy',
    shortTitle: 'TATAMI GALAXY',
    year: '2010',
    detail: '11 episodes · Madhouse',
    tags: ['Surreal', 'Comedy', 'Time loop'],
    moods: ['strange', 'electric', 'thoughtful'],
    logline: 'One campus. Many possible lives. The same two years, again.',
    synopsis: 'A nameless student keeps revisiting his university years, each time choosing a different club and imagining a better life. A fast, funny, densely animated maze about regret and the choices still in front of us.',
    note: 'Best watched at its own brisk, wonderfully strange pace.',
    yearRank: 8,
  },
];

export const MOODS = [
  { id: 'any', label: 'No mood, just browse' },
  { id: 'strange', label: 'A little strange' },
  { id: 'quiet', label: 'Quiet hours' },
  { id: 'electric', label: 'High voltage' },
  { id: 'heartfelt', label: 'Feel something' },
  { id: 'mystery', label: 'Something to solve' },
  { id: 'warm', label: 'Warm & human' },
];

// Original, hand-authored geometric cover studies; these are not official key art.
export function coverArt(id, extraClass = '') {
  const art = {
    'sonny-boy': `<svg viewBox="0 0 180 240" class="cover-illustration" aria-hidden="true" focusable="false"><rect width="180" height="240" fill="#c8b894"/><circle cx="124" cy="55" r="38" fill="#e87552"/><path d="M0 168 48 113l35 34 27-31 70 62v62H0Z" fill="#293f50"/><path d="M0 203h180v37H0z" fill="#14252c"/><path d="M41 144v-28h24v48M89 150v-44h19v51M135 166v-30h16v42" fill="none" stroke="#e7d9b6" stroke-width="3"/><path d="M15 29h28M15 39h18" stroke="#293f50" stroke-width="2"/><circle cx="26" cy="90" r="2" fill="#293f50"/><circle cx="45" cy="79" r="1.5" fill="#293f50"/></svg>`,
    'odd-taxi': `<svg viewBox="0 0 180 240" class="cover-illustration" aria-hidden="true" focusable="false"><rect width="180" height="240" fill="#202a30"/><circle cx="139" cy="44" r="24" fill="#d6c9aa"/><path d="M0 104h29v43H0zm38-26h32v69H38zm42 17h28v52H80zm39-39h26v91h-26zm36 30h25v61h-25z" fill="#38474a"/><path d="M0 157h180v83H0z" fill="#111719"/><path d="m25 188 13-25h88l20 25v26H25z" fill="#d88452"/><path d="m49 169 8-14h43l13 14z" fill="#a9c0bf"/><path d="M19 215h143" stroke="#d9cbae" stroke-width="2" stroke-dasharray="13 12"/><circle cx="53" cy="214" r="9" fill="#171b1a" stroke="#d6c9aa" stroke-width="2"/><circle cx="127" cy="214" r="9" fill="#171b1a" stroke="#d6c9aa" stroke-width="2"/><path d="M82 184h18" stroke="#e7d9b6" stroke-width="2"/></svg>`,
    eizouken: `<svg viewBox="0 0 180 240" class="cover-illustration" aria-hidden="true" focusable="false"><rect width="180" height="240" fill="#d6caae"/><path d="M-12 163 47 63l31 47 25-31 89 112v49H-12z" fill="#64806d"/><path d="m31 162 39-59 16 24-29 49z" fill="#dd7858"/><path d="m97 144 41-72 46 75-38-19-26 31z" fill="#e9b648"/><path d="M18 29h73v52H18z" fill="#17211f" stroke="#f1e8d2" stroke-width="4"/><path d="m34 68 17-24 13 14 13-20" fill="none" stroke="#df7757" stroke-width="4"/><circle cx="129" cy="39" r="16" fill="#e87552"/><path d="M20 196h139M20 207h92" stroke="#f1e8d2" stroke-width="3" opacity=".8"/></svg>`,
    'mob-psycho': `<svg viewBox="0 0 180 240" class="cover-illustration" aria-hidden="true" focusable="false"><rect width="180" height="240" fill="#72547c"/><circle cx="89" cy="112" r="76" fill="#d76f55"/><circle cx="89" cy="112" r="58" fill="none" stroke="#edc788" stroke-width="3"/><circle cx="89" cy="112" r="37" fill="none" stroke="#edc788" stroke-width="2"/><path d="M0 195 30 158l21 19 32-41 31 44 22-24 44 41v43H0z" fill="#30283c"/><path d="M87 72c-16 0-25 13-25 28 0 13 7 22 7 36h37c0-14 7-23 7-36 0-15-10-28-26-28Z" fill="#eadcbd"/><path d="M72 112h32m-27 12h22" stroke="#30283c" stroke-width="3"/><path d="M15 33h29m-29 8h17" stroke="#edc788" stroke-width="2"/></svg>`,
    'violet-evergarden': `<svg viewBox="0 0 180 240" class="cover-illustration" aria-hidden="true" focusable="false"><rect width="180" height="240" fill="#a9b4b2"/><path d="M0 195c34-18 56-36 80-79s36-54 84-71v195H0z" fill="#536a71"/><path d="M-8 176c40 0 60-24 82-61s39-51 108-69" fill="none" stroke="#d9caad" stroke-width="3"/><path d="M67 118c-13-7-23-18-18-29 7-14 25-4 25 6 0-10 17-19 24-6 6 12-7 24-25 31l-3 96" fill="#dd8b6d" stroke="#f1e4ca" stroke-width="2"/><path d="m43 144-19-12m39-33-17-18m56-20 17-14m-44 85 28 3" stroke="#f0dfc1" stroke-width="2"/><path d="M18 29h50M18 37h32" stroke="#40575f" stroke-width="2"/></svg>`,
    edgerunners: `<svg viewBox="0 0 180 240" class="cover-illustration" aria-hidden="true" focusable="false"><rect width="180" height="240" fill="#222233"/><path d="M0 144h21V89h18v55h16V56h24v88h13V99h18v45h17V69h24v75h29v96H0z" fill="#393854"/><path d="M0 177 47 122l22 19 24-55 20 46 30-42 37 58v92H0z" fill="#bb5b5e" opacity=".9"/><path d="M12 186h156M28 203h126" stroke="#76c0bc" stroke-width="2"/><path d="M20 36h78M20 43h49" stroke="#f1d6b4" stroke-width="2"/><circle cx="132" cy="42" r="15" fill="#76c0bc"/><path d="M132 23v38m-19-19h38" stroke="#222233" stroke-width="2"/></svg>`,
    frieren: `<svg viewBox="0 0 180 240" class="cover-illustration" aria-hidden="true" focusable="false"><rect width="180" height="240" fill="#8e99a5"/><circle cx="135" cy="54" r="28" fill="#dfd1b3"/><path d="M0 183 34 141l28 21 38-57 30 34 23-29 27 38v92H0z" fill="#3c5360"/><path d="M23 192c42-6 65-22 92-65 19-30 34-41 54-49" fill="none" stroke="#c2c9b4" stroke-width="3"/><path d="M88 129c-15-6-18-22-7-28 10-5 18 4 17 12 5-11 19-11 22-1 4 12-10 21-24 24l-8 48" fill="#d7d0b4"/><path d="M20 27h46m-46 8h28" stroke="#344b58" stroke-width="2"/></svg>`,
    'tatami-galaxy': `<svg viewBox="0 0 180 240" class="cover-illustration" aria-hidden="true" focusable="false"><rect width="180" height="240" fill="#b88b61"/><path d="M0 0h180v240H0z" fill="#ab755d"/><path d="M14 19h152v202H14z" fill="none" stroke="#272d2c" stroke-width="10"/><path d="M37 44h105v154H37z" fill="none" stroke="#d9c29b" stroke-width="8"/><path d="M58 66h64v111H58z" fill="#38453e"/><path d="M58 121h64m-32-55v111" stroke="#d9c29b" stroke-width="4"/><path d="M85 56 98 77 85 96 99 117 85 139 99 161" fill="none" stroke="#db7858" stroke-width="7"/><circle cx="130" cy="43" r="8" fill="#dfc9a1"/></svg>`,
  };
  return `<span class="cover-art ${extraClass}" aria-hidden="true">${art[id] || art['sonny-boy']}</span>`;
}

export function getShow(id) {
  return SHOWS.find((show) => show.id === id) || SHOWS[0];
}

export function relatedShows(id, count = 3) {
  const source = getShow(id);
  return SHOWS
    .filter((show) => show.id !== source.id)
    .map((show) => ({
      show,
      overlap: show.tags.filter((tag) => source.tags.includes(tag)).length,
      moodOverlap: show.moods.filter((mood) => source.moods.includes(mood)).length,
    }))
    .sort((a, b) => (b.overlap * 3 + b.moodOverlap) - (a.overlap * 3 + a.moodOverlap) || a.show.yearRank - b.show.yearRank)
    .slice(0, count)
    .map(({ show }) => show);
}

export function fitScore(show, profile) {
  const interests = profile?.metrics?.tagCounts || {};
  const max = Math.max(1, ...Object.values(interests));
  const affinity = show.tags.reduce((sum, tag) => sum + (interests[tag] || 0), 0);
  const saved = profile?.savedIds?.includes(show.id) ? 1 : 0;
  return Math.min(98, 72 + Math.round((affinity / max) * 18) + saved * 8);
}
