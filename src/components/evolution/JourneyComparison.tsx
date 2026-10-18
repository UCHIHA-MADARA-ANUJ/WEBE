'use client';

import { useMemo } from 'react';
import { JOURNEYS } from '@/lib/replay/journey-fixtures';
import { runJourney } from '@/lib/replay/replay-engine';
import { PARADIGM_DISPLAY } from '@/components/Chrome';

export function JourneyComparison() {
  const results = useMemo(() => JOURNEYS.map(j => ({ journey: j, result: runJourney(j) })), []);

  return (
    <div>
      <div className="eyebrow" style={{ marginBottom: 16 }}>
        Side-by-side — same starting graph, different behavioural evidence, different structures.
      </div>

      <div className="comparison-grid">
        {results.map(({ journey, result }) => (
          <div key={journey.id} className="comparison-card" style={{ borderTopColor: journey.color }}>
            <div className="comparison-card__head">
              <span className="comparison-card__glyph" style={{ color: journey.color }}>{journey.glyph}</span>
              <span className="comparison-card__label">{journey.label}</span>
              <span className="comparison-card__paradigm" style={{ background: journey.color, color: 'white' }}>
                {PARADIGM_DISPLAY[result.finalParadigm]?.name ?? result.finalParadigm}
              </span>
            </div>
            <div className="mono" style={{ fontSize: '0.65rem', color: 'var(--ink-faint)', lineHeight: 1.5, marginBottom: 8 }}>
              {journey.blurb}
            </div>
            <div className="mono" style={{ fontSize: '0.65rem', lineHeight: 1.6 }}>
              <div>Read as <b>{result.finalClassification.top}</b> · {Math.round(result.confidence*100)}% · margin {Math.round(result.finalClassification.margin*100)}%</div>
              <div style={{ color: 'var(--ink-faint)' }}>
                Events: {journey.events.length} · restructured: {result.steps.filter(s=>s.decided).length}×
              </div>
              {result.steps.filter(s=>s.decided).length > 0 && (
                <div>Path: {result.steps.map(s=> PARADIGM_DISPLAY[s.paradigm]?.name ?? s.paradigm).join(' → ')}</div>
              )}
            </div>

            {/* mini step strip */}
            <div style={{ marginTop: 10, display: 'flex', gap: 2, flexWrap: 'wrap' }}>
              {result.steps.map((s,i) => (
                <span
                  key={i}
                  className="mini-step"
                  data-decided={s.decided}
                  title={`Step ${i+1}: ${s.event.kind} ${s.event.target ?? ''} → ${s.paradigm} (${Math.round(s.classification.confidence*100)}%)`}
                >
                  {s.event.kind[0]}
                </span>
              ))}
            </div>

            <div className="mono" style={{ fontSize: '0.6rem', color: 'var(--ink-faint)', marginTop: 6 }}>
              {result.finalClassification.reasons[0] ?? ''}
            </div>
          </div>
        ))}
      </div>

      <div className="mono" style={{ fontSize: '0.62rem', color: 'var(--ink-faint)', marginTop: 18, padding: '12px 14px', background: 'var(--paper-2)', border: '1px solid var(--line)', lineHeight: 1.7 }}>
        The same corpus, the same engine, the same thresholds. Different interactions produce different interface structures — not because
        buttons were hardcoded to layouts, but because the affinity scoring genuinely diverges.
        Change the weights in <code>engine/types.ts</code> and these results change.
      </div>
    </div>
  );
}
