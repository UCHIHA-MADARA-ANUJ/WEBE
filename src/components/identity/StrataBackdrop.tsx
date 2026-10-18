'use client';

import { useMemo } from 'react';
import { mulberry32 } from '@/engine/genome';

/**
 * Warm editorial backdrop — not a starfield.
 * A subtle paper texture + procedural warm grain seeded by the generation.
 * Replaces the cosmic backdrop with something that belongs in a decision workspace.
 */
export function StrataBackdrop({ seed }: { seed: number }) {
  const flecks = useMemo(() => {
    const rng = mulberry32(seed ^ 0x7a3e);
    return Array.from({ length: 64 }, () => ({
      left: rng() * 100,
      top: rng() * 100,
      size: 0.8 + rng() * 1.6,
      opacity: 0.03 + rng() * 0.05,
    }));
  }, [seed]);

  return (
    <div className="strata-backdrop" aria-hidden="true">
      <div className="strata-backdrop__grain">
        {flecks.map((f, i) => (
          <span
            key={i}
            className="strata-fleck"
            style={{
              left: `${f.left}%`,
              top: `${f.top}%`,
              width: `${f.size}px`,
              height: `${f.size}px`,
              opacity: f.opacity,
            }}
          />
        ))}
      </div>
      <div className="strata-backdrop__rule" />
    </div>
  );
}
