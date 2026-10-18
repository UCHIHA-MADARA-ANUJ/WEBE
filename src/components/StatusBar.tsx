'use client';

import { useEffect, useRef, useState } from 'react';
import { useEngine } from '@/engine/store';
import { ENTITY_BY_ID } from '@/content/graph';
import { PARADIGM_DISPLAY } from './Chrome';

export function StatusBar() {
  const { signals, classification, genome, paradigm } = useEngine();
  const [note, setNote] = useState('STRATA is listening — work on the project and it will restructure.');
  const [flash, setFlash] = useState(false);
  const last = useRef({ fast: 0, steps: 0, jumps: 0, opens: 0, top: classification.top, gen: genome.generation });

  const say = (text: string) => { setNote(text); setFlash(true); setTimeout(() => setFlash(false), 400); };

  useEffect(() => {
    const l = last.current;
    if (signals.fastScrolls > l.fast) {
      l.fast = signals.fastScrolls;
      say(signals.fastScrolls >= 3 ? `${signals.fastScrolls} fast motions — skimmer weight rising, density preferred` : `fast motion ${Math.round(signals.peakVelocity)} px/s — velocity recorded`);
    } else if (signals.steps > l.steps) { l.steps = signals.steps; say('followed a typed relation — linearity up, sequence preferred'); }
    else if (signals.jumps > l.jumps) { l.jumps = signals.jumps; say('jumped across the project — breadth up, map preferred'); }
    else if (signals.opens > l.opens) {
      l.opens = signals.opens;
      const id = signals.path[signals.path.length-1];
      const title = ENTITY_BY_ID[id]?.title;
      if (title) say(`opened ${title}`);
    }
    if (classification.top !== l.top) { l.top = classification.top; say(`read shifted → ${classification.top} (${Math.round(classification.confidence*100)}%)`); }
    if (genome.generation !== l.gen) { l.gen = genome.generation; say(`generation ${genome.generation} — arrangement re-seeded`); }
    // eslint-disable-next-line react-hooks/exhaustive-deps
  }, [signals, classification, genome]);

  const name = PARADIGM_DISPLAY[paradigm]?.name ?? paradigm;

  return (
    <div className="statusbar" role="status" aria-live="polite">
      <span className="statusbar__dot" style={{ opacity: flash ? 1 : 0.6 }} />
      <span className="statusbar__note">{note}</span>
      <span className="statusbar__spacer" />
      <span className="statusbar__meta">
        {name} <span style={{ opacity: 0.35 }}>·</span> {classification.blank ? 'no read' : `read ${classification.top} ${Math.round(classification.confidence*100)}%`} <span style={{ opacity: 0.35 }}>·</span> gen {genome.generation} <span style={{ opacity: 0.35 }}>·</span> {genome.visited.length} seen
      </span>
    </div>
  );
}
