'use client';

import { useEffect, useRef } from 'react';
import { useGSAP } from '@gsap/react';
import gsap from 'gsap';
import { ScrollTrigger } from 'gsap/ScrollTrigger';

gsap.registerPlugin(ScrollTrigger);

/**
 * StrataExplainer — GSAP + ScrollTrigger editorial sequence.
 *
 * A short scroll-linked diagram showing how behavioural evidence
 * flows through the Interface Compiler into a new structure.
 * This is the ONLY place ScrollTrigger is used — the workspace
 * itself must not depend on scroll animations.
 */
export function StrataExplainer() {
  const rootRef = useRef<HTMLDivElement>(null);
  const trackRef = useRef<HTMLDivElement>(null);

  useGSAP(() => {
    const ctx = gsap.context(() => {
      const steps = rootRef.current?.querySelectorAll('.explain-step');
      if (!steps?.length) return;

      gsap.fromTo(steps,
        { opacity: 0.2, y: 18 },
        {
          opacity: 1, y: 0, stagger: 0.18, duration: 0.6, ease: 'power2.out',
          scrollTrigger: {
            trigger: trackRef.current,
            start: 'top 80%',
            end: 'bottom 55%',
            scrub: 0.6,
          },
        }
      );

      // the connecting line draws as you scroll
      const line = rootRef.current?.querySelector('.explain-line');
      if (line) {
        gsap.fromTo(line,
          { scaleY: 0 },
          {
            scaleY: 1, duration: 1, ease: 'none',
            transformOrigin: 'top center',
            scrollTrigger: {
              trigger: trackRef.current,
              start: 'top 70%',
              end: 'bottom 40%',
              scrub: 0.8,
            },
          }
        );
      }
    }, rootRef);

    return () => ctx.revert();
  }, []);

  return (
    <div ref={trackRef} style={{ padding: '40px 0 60px' }}>
      <div ref={rootRef} className="explain">
        <div className="explain__header">
          <span className="eyebrow">The Interface Compiler</span>
          <h2 className="display" style={{ fontSize: '1.8rem', marginTop: 8 }}>
            How it decides to rebuild.
          </h2>
          <p className="mono" style={{ fontSize: '0.72rem', color: 'var(--ink-faint)', marginTop: 8, maxWidth: 520 }}>
            Every meaningful interaction becomes evidence. The engine scores candidate
            compositions and only restructures when the advantage is clear and durable.
          </p>
        </div>

        <div className="explain__flow">
          <div className="explain__track">
            <div className="explain-line" />
          </div>

          <div className="explain-step">
            <span className="explain-step__n">01</span>
            <h3 className="explain-step__title">You act</h3>
            <p className="explain-step__body">Open an entity, follow a relation, filter, compare. Each action is a typed event with minimal context — no keystroke logging, no surveillance.</p>
          </div>

          <div className="explain-step">
            <span className="explain-step__n">02</span>
            <h3 className="explain-step__title">Evidence accumulates</h3>
            <p className="explain-step__body">Recent events weigh heavier (half-life ≈ 18 actions). The engine maintains 11 continuous feature signals and a confidence estimate.</p>
          </div>

          <div className="explain-step">
            <span className="explain-step__n">03</span>
            <h3 className="explain-step__title">Candidates are scored</h3>
            <p className="explain-step__body">Each structural paradigm is scored on alignment, relevance, context preservation, viewport fit, and switching cost. A credible read must clear evidentiary bars.</p>
          </div>

          <div className="explain-step">
            <span className="explain-step__n">04</span>
            <h3 className="explain-step__title">Only the best wins</h3>
            <p className="explain-step__body">The engine needs ≥42% confidence and a 5% margin, plus 9s since the last switch. If unclear, it holds. Every change is explained in the reconfiguration manifest.</p>
          </div>
        </div>
      </div>

      <style>{`
        .explain { max-width: 720px; margin: 0 auto; padding: 0 20px; }
        .explain__header { text-align: center; margin-bottom: 28px; }
        .explain__flow { display: grid; grid-template-columns: 32px 1fr; gap: 0; position: relative; }
        .explain__track { position: relative; display: flex; justify-content: center; }
        .explain-line { position: absolute; top: 8px; bottom: 8px; width: 1px; background: var(--accent); opacity: 0.5; }
        .explain-step { padding: 14px 0 18px 18px; border-left: 1px solid transparent; }
        .explain-step__n { font-family: var(--mono); font-size: 0.58rem; letter-spacing: 0.14em; color: var(--accent); display: block; margin-bottom: 4px; }
        .explain-step__title { font-family: var(--serif); font-size: 1.05rem; font-weight: 500; margin: 0 0 4px; color: var(--ink); }
        .explain-step__body { font-family: var(--sans); font-size: 0.82rem; line-height: 1.55; color: var(--ink-dim); margin: 0; max-width: 520px; }
      `}</style>
    </div>
  );
}
