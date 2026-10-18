'use client';

import { useMemo, useState } from 'react';
import { JOURNEYS } from '@/lib/replay/journey-fixtures';
import { runJourney, type ReplayResult } from '@/lib/replay/replay-engine';
import { PARADIGM_DISPLAY } from '@/components/Chrome';
import { PARADIGMS } from '@/engine/types';

export function JourneyReplay({ focus, navigate }: { focus: string | null; navigate: (id: string) => void }) {
  const [selected, setSelected] = useState<string>(JOURNEYS[0].id);
  const [step, setStep] = useState<number | null>(null);

  const journey = useMemo(() => JOURNEYS.find(j => j.id === selected) ?? JOURNEYS[0], [selected]);
  const result: ReplayResult = useMemo(() => runJourney(journey), [journey]);
  const currentStep = step !== null ? result.steps[step] : null;

  return (
    <div>
      {/* journey picker */}
      <div className="journey-picker">
        {JOURNEYS.map(j => (
          <button
            key={j.id}
            className="journey-card"
            data-on={j.id === selected}
            onClick={() => { setSelected(j.id); setStep(null); }}
            style={{ borderColor: j.id === selected ? j.color : undefined, background: j.id === selected ? `${j.color}0d` : undefined }}
          >
            <span className="journey-card__glyph" style={{ color: j.color }}>{j.glyph}</span>
            <span className="journey-card__label">{j.label}</span>
            <span className="journey-card__blurb">{j.blurb}</span>
            <span className="journey-card__meta">{j.events.length} events</span>
          </button>
        ))}
      </div>

      <div className="replay-result">
        <div className="replay-head">
          <span className="eyebrow">Result — same engine, different evidence</span>
          <span className="replay-final" style={{ color: '#0A0A0A' }}>
            Constellation → <b style={{ color: PARADIGMS[result.finalParadigm]?.archetype ? undefined : undefined }}>{PARADIGM_DISPLAY[result.finalParadigm]?.name ?? result.finalParadigm}</b>
            <span className="mono" style={{ fontSize: '0.7rem', marginLeft: 8, color: 'var(--ink-faint)' }}>
              {result.finalClassification.top} · {Math.round(result.confidence*100)}%
            </span>
          </span>
          {result.history.some(p => p !== result.history[0]) && (
            <span className="mono" style={{ fontSize: '0.65rem', color: 'var(--ink-faint)' }}>
              Restructured {result.steps.filter(s=>s.decided).length} time(s): {result.steps.filter(s=>s.decided).map(s => `${s.paradigm}`).join(' → ')}
            </span>
          )}
        </div>

        {/* step timeline */}
        <div className="replay-timeline">
          <input
            type="range"
            min={0}
            max={result.steps.length - 1}
            value={step ?? result.steps.length - 1}
            onChange={e => setStep(parseInt(e.target.value))}
            style={{ width: '100%', accentColor: journey.color }}
          />
          <div className="replay-steps">
            {result.steps.map((s, i) => (
              <button
                key={i}
                className="replay-step"
                data-on={step === i}
                data-decided={s.decided}
                onClick={() => setStep(i)}
                title={s.reason}
              >
                <span className="replay-step__n">{i+1}</span>
                <span className="replay-step__kind">{s.event.kind}</span>
                <span className="replay-step__paradigm">{PARADIGM_DISPLAY[s.paradigm]?.name ?? s.paradigm}</span>
                {s.decided && <span className="replay-step__badge">restructured</span>}
              </button>
            ))}
          </div>
        </div>

        {/* detail of selected step */}
        {currentStep && (
          <div className="replay-detail">
            <div className="replay-detail__head">
              Step {currentStep.index+1}: <b>{currentStep.event.kind}</b>
              {currentStep.event.target && <> → <code>{currentStep.event.target}</code></>}
              {currentStep.event.query && <> “{currentStep.event.query}”</>}
              {currentStep.event.tag && <> #{currentStep.event.tag}</>}
            </div>
            {currentStep.event.note && <div className="mono" style={{ fontSize: '0.7rem', color: 'var(--ink-faint)', fontStyle: 'italic' }}>{currentStep.event.note}</div>}
            <div className="mono" style={{ fontSize: '0.68rem', color: 'var(--ink-soft)', marginTop: 8 }}>
              Read as <b>{currentStep.classification.top}</b> · {Math.round(currentStep.classification.confidence*100)}% · margin {Math.round(currentStep.classification.margin*100)}% · evidence {currentStep.classification.evidence}
            </div>
            <div className="mono" style={{ fontSize: '0.65rem', color: 'var(--ink-faint)', marginTop: 4 }}>"{currentStep.reason}"</div>
          </div>
        )}

        {/* run in isolation note */}
        <div className="mono" style={{ fontSize: '0.6rem', color: 'var(--ink-faint)', marginTop: 16, padding: '10px 12px', background: 'var(--paper-2)', border: '1px solid var(--line)', lineHeight: 1.6 }}>
          This simulation runs <b>the same</b> <code>classify()</code> + <code>decideParadigm()</code> code the live workspace uses, with a fresh profile.
          It is not a hardcoded layout — the result changes if you change the engine’s weights or thresholds.
        </div>

        <div className="replay-actions">
          <button className="btn btn--sm" onClick={() => setStep(null)}>show final</button>
          <button className="btn btn--sm" onClick={() => setStep(0)}>from start</button>
          {result.steps.length > 0 && <button className="btn btn--accent btn--sm" onClick={() => { const next = (step ?? -1) + 1; if (next < result.steps.length) setStep(next); else setStep(0); }}>next step →</button>}
        </div>
      </div>

      {/* all journeys at a glance */}
      <div style={{ marginTop: 32, borderTop: '1px solid var(--line)', paddingTop: 20 }}>
        <div className="eyebrow" style={{ marginBottom: 12 }}>All journeys from the same start — do they diverge?</div>
        <div style={{ display: 'flex', gap: 8, flexWrap: 'wrap' }}>
          {JOURNEYS.map(j => {
            const r = runJourney(j);
            return (
              <div key={j.id} className="journey-chip" style={{ borderColor: j.color }}>
                <span style={{ color: j.color }}>{j.glyph} {j.label}</span>
                <span className="mono" style={{ fontSize: '0.62rem' }}>→ {PARADIGM_DISPLAY[r.finalParadigm]?.name ?? r.finalParadigm} · {Math.round(r.confidence*100)}%</span>
              </div>
            );
          })}
        </div>
        {(() => {
          const all = JOURNEYS.map(j => runJourney(j).finalParadigm);
          const uniq = new Set(all);
          return (
            <div className="mono" style={{ fontSize: '0.68rem', color: uniq.size > 1 ? 'var(--accent-2)' : 'var(--ink-faint)', marginTop: 10 }}>
              {uniq.size > 1 ? `✓ ${uniq.size} distinct final structures from ${all.length} journeys — the engine diverges.` : `All converged to ${all[0]} — try adding more contrasting behaviours.`}
            </div>
          );
        })()}
      </div>
    </div>
  );
}
