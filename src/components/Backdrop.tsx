import { useMemo } from 'react';
import { mulberry32 } from '../engine/genome';

const STAR_COUNT = 140;

/** The sky behind everything. It is procedural, but it never rearranges the UI. */
export function Backdrop({ seed }: { seed: number }) {
  const stars = useMemo(() => {
    const rng = mulberry32(seed ^ 0x5eed);
    return Array.from({ length: STAR_COUNT }, () => ({
      left: rng() * 100,
      top: rng() * 100,
      size: 0.6 + rng() * 1.7,
      dur: 3 + rng() * 7,
      delay: rng() * 6,
      op: 0.2 + rng() * 0.6,
    }));
  }, [seed]);

  return (
    <div className="backdrop" aria-hidden="true">
      <div className="stars">
        {stars.map((s, i) => (
          <span
            key={i}
            className="star"
            style={{
              left: `${s.left}%`,
              top: `${s.top}%`,
              width: `${s.size}px`,
              height: `${s.size}px`,
              opacity: s.op,
              ['--dur' as string]: `${s.dur}s`,
              ['--delay' as string]: `${s.delay}s`,
            }}
          />
        ))}
      </div>
    </div>
  );
}
