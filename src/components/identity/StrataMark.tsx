'use client';

import { useEffect, useRef } from 'react';

/**
 * STRATA wordmark — the identity animation.
 * Anime.js v4 draws the stratification lines on mount.
 * Each layer is a separate SVG path; anime staggers their stroke-dasharray reveal.
 */
export function StrataMark({ size = 28, animated = true }: { size?: number; animated?: boolean }) {
  const ref = useRef<SVGSVGElement>(null);

  useEffect(() => {
    if (!animated || !ref.current) return;
    let cancelled = false;

    (async () => {
      try {
        const { animate } = await import('animejs');
        if (cancelled) return;
        const el = ref.current;
        if (!el) return;
        // select strata layers for staggered draw
        const layers = el.querySelectorAll<SVGElement>('.strata-layer');
        if (!layers.length) return;
        animate(layers as any, {
          opacity: [0, 1],
          translateY: ['6px', '0px'],
          duration: 700,
          delay: (_el: unknown, i: number) => i * 90,
          ease: 'outExpo',
        } as any);
      } catch {
        // anime not available — no animation, mark stays visible
      }
    })();

    return () => { cancelled = true; };
  }, [animated]);

  return (
    <svg
      ref={ref}
      width={size * 4.2}
      height={size}
      viewBox="0 0 120 28"
      fill="none"
      xmlns="http://www.w3.org/2000/svg"
      aria-label="STRATA wordmark"
      className="strata-mark"
    >
      <text
        x="0"
        y="20"
        className="strata-layer"
        style={{ fontFamily: 'var(--serif)', fontSize: 22, fontWeight: 400, letterSpacing: '0.28em', fill: 'var(--ink)' }}
      >
        STRATA
      </text>
      {/* stratification lines under the wordmark */}
      <g className="strata-layer">
        <line x1="0" y1="24" x2="98" y2="24" stroke="var(--accent)" strokeOpacity="0.65" strokeWidth="1.2" />
      </g>
      <g className="strata-layer">
        <line x1="0" y1="26.5" x2="72" y2="26.5" stroke="var(--accent)" strokeOpacity="0.32" strokeWidth="0.8" />
      </g>
    </svg>
  );
}

export function StrataGlyph({ size = 20 }: { size?: number }) {
  // compact glyph for favicon / small marks
  return (
    <svg width={size} height={size} viewBox="0 0 20 20" fill="none" aria-hidden="true">
      <rect x="2" y="3" width="16" height="3" rx="1" fill="var(--ink)" opacity={0.95} />
      <rect x="2" y="8" width="12" height="3" rx="1" fill="var(--accent)" opacity={0.9} />
      <rect x="2" y="13" width="16" height="3" rx="1" fill="var(--ink)" opacity={0.18} />
    </svg>
  );
}
