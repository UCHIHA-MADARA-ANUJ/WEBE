'use client';

import { useEffect, useRef } from 'react';

/**
 * Lenis — progressive enhancement for outer-document scrolling.
 * Does not touch nested work surfaces (codex rail, lattice index, mosaic).
 * Respects prefers-reduced-motion.
 */
export function LenisProvider({ children }: { children: React.ReactNode }) {
  const lenisRef = useRef<any>(null);

  useEffect(() => {
    const prefersReduced = window.matchMedia('(prefers-reduced-motion: reduce)').matches;
    if (prefersReduced) return;

    let rafId = 0;
    let lenis: any = null;

    (async () => {
      try {
        const LenisMod = await import('lenis');
        const Lenis = (LenisMod as any).default ?? LenisMod;
        lenis = new Lenis({
          duration: 1.15,
          easing: (t: number) => Math.min(1, 1.001 - Math.pow(2, -10 * t)),
          orientation: 'vertical',
          gestureOrientation: 'vertical',
          smoothWheel: true,
          wheelMultiplier: 0.9,
          touchMultiplier: 1.6,
        });
        lenisRef.current = lenis;

        const raf = (time: number) => {
          lenis.raf(time);
          rafId = requestAnimationFrame(raf);
        };
        rafId = requestAnimationFrame(raf);

        // Integrate ScrollTrigger if GSAP is present — don't compete
        try {
          const gsapMod = await import('gsap');
          const { ScrollTrigger } = await import('gsap/ScrollTrigger');
          gsapMod.gsap.registerPlugin(ScrollTrigger);
          lenis.on('scroll', ScrollTrigger.update);
        } catch {
          // GSAP not critical for scroll
        }
      } catch {
        // Lenis unavailable — native scroll is fine
      }
    })();

    return () => {
      cancelAnimationFrame(rafId);
      if (lenis) lenis.destroy?.();
    };
  }, []);

  return <>{children}</>;
}
