import { useEffect, useRef, useState } from 'react';
import { useEngine } from '../engine/store';
import { NODE_BY_ID } from '../content/graph';

/**
 * The engine's own voice, in a single line at the foot of the window.
 * It narrates what the engine is noticing, live, as you move.
 */
export function StatusBar() {
  const { signals, classification, genome, paradigm } = useEngine();
  const [note, setNote] = useState('the engine is listening — move, and it will reorganise');
  const [flash, setFlash] = useState(false);
  const last = useRef({
    fast: 0,
    steps: 0,
    jumps: 0,
    opens: 0,
    top: classification.top,
    gen: genome.generation,
  });

  const say = (text: string) => {
    setNote(text);
    setFlash(true);
    window.setTimeout(() => setFlash(false), 400);
  };

  useEffect(() => {
    const l = last.current;

    if (signals.fastScrolls > l.fast) {
      l.fast = signals.fastScrolls;
      say(
        signals.fastScrolls >= 3
          ? `${signals.fastScrolls} fast scrolls — skimmer weight rising, density preferred`
          : `fast scroll ${Math.round(signals.peakVelocity)} px/s — velocity recorded`,
      );
    } else if (signals.steps > l.steps) {
      l.steps = signals.steps;
      say('followed a stated relation — linearity up, sequence preferred');
    } else if (signals.jumps > l.jumps) {
      l.jumps = signals.jumps;
      say('jumped across the field — breadth up, map preferred');
    } else if (signals.opens > l.opens) {
      l.opens = signals.opens;
      const id = signals.path[signals.path.length - 1];
      const title = NODE_BY_ID[id]?.title;
      if (title) say(`opened ${title}`);
    }

    if (classification.top !== l.top) {
      l.top = classification.top;
      say(`read shifted → ${classification.top} (${Math.round(classification.confidence * 100)}%)`);
    }
    if (genome.generation !== l.gen) {
      l.gen = genome.generation;
      say(`generation ${genome.generation} — structure re-seeded, new behaviour unlocked`);
    }
    // eslint-disable-next-line react-hooks/exhaustive-deps
  }, [signals, classification, genome]);

  return (
    <div className="statusbar" role="status" aria-live="polite">
      <span className="statusbar__dot" style={{ opacity: flash ? 1 : 0.4 }} />
      <span className="statusbar__note">{note}</span>
      <span className="statusbar__spacer" />
      <span className="statusbar__meta">
        {paradigm}
        <span style={{ opacity: 0.4 }}> · </span>
        {classification.blank
          ? 'no read yet'
          : `read ${classification.top} ${Math.round(classification.confidence * 100)}%`}
        <span style={{ opacity: 0.4 }}> · </span>
        gen {genome.generation}
        <span style={{ opacity: 0.4 }}> · </span>
        {genome.visited.length} seen
      </span>
    </div>
  );
}
