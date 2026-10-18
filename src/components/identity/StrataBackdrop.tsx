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
    return Array.from({ length: 48 }, () => ({
      left: rng() * 100,
      top: rng() * 100,
      size: 1 + rng() * 1.8,
      opacity: 0.04 + rng() * 0.06,
    }));
  }, [seed]);

  return (
    <div className="strata-backdrop" aria-hidden="true">
      {/* warm paper base is CSS; flecks are subtle */}
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
      {/* thin rule accent */}
      <div className="strata-backdrop__rule" />
    </div>
  );
}
