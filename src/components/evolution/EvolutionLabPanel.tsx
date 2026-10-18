'use client';

import { useEngine } from '@/engine/store';
import { ARCHETYPES, PARADIGMS } from '@/engine/types';
import { confidenceLabel, normalise } from '@/engine/classify';
import { PARADIGM_DISPLAY } from '@/components/Chrome';

export function EvolutionLabPanel() {
  const { classification, genome, signals, features, paradigm, setParadigm, mutate, reset, manifest, log, trail, promoted } = useEngine();

  const topTags = Object.entries(genome.interest).sort((a,b) => b[1]-a[1]).slice(0,6);
  const maxTag = topTags[0]?.[1] ?? 1;
  const n = (() => { try { return normalise(classification.features); } catch { return null; } })();

  return (
    <div className="evolution-lab">
      {/* header stats */}
      <div className="lab-stats">
        <div className="lab-stat">
          <span className="lab-stat__k">Paradigm</span>
          <span className="lab-stat__v">{PARADIGM_DISPLAY[paradigm]?.name ?? PARADIGMS[paradigm].name}</span>
        </div>
        <div className="lab-stat">
          <span className="lab-stat__k">Read as</span>
          <span className="lab-stat__v">{classification.blank ? '— listening' : classification.top} · {confidenceLabel(classification.confidence)}</span>
        </div>
        <div className="lab-stat">
          <span className="lab-stat__k">Confidence</span>
          <span className="lab-stat__v">{Math.round(classification.confidence*100)}% · margin {Math.round(classification.margin*100)}%</span>
        </div>
        <div className="lab-stat">
          <span className="lab-stat__k">Evidence</span>
          <span className="lab-stat__v">{classification.evidence} events · gen {genome.generation}</span>
        </div>
      </div>

      {/* archetype bars */}
      <section className="mind__section" style={{ borderTop: 'none' }}>
        <div className="mind__label">Archetype scores — how the engine sees you</div>
        {ARCHETYPES.map(a => {
          const score = classification.scores[a.id] ?? 0;
          return (
            <div key={a.id} className="arch" data-top={a.id === classification.top}>
              <span className="arch__name"><span className="arch__glyph">{a.glyph}</span>{a.label}</span>
              <span className="arch__pct">{Math.round(score*100)}%</span>
              <div className="arch__track"><div className="arch__fill" style={{ width: `${Math.round(score*100)}%` }} /></div>
            </div>
          );
        })}
        <ul className="reasons" style={{ marginTop: 10 }}>
          {classification.reasons.map((r,i) => <li key={i}>{r}</li>)}
        </ul>
      </section>

      {/* features */}
      <section className="mind__section">
        <div className="mind__label">Feature vector · raw → normalised</div>
        {n && (
          <div className="featuregrid">
            {Object.entries(n).map(([k,v]) => (
              <div key={k} className="feature">
                <div className="feature__k">{k}</div>
                <div className="feature__v" data-zero={Number(v) < 0.02}>{(Number(v)*100).toFixed(0)}%</div>
              </div>
            ))}
          </div>
        )}
        <div className="mono" style={{ fontSize: '0.62rem', color: 'var(--ink-faint)', marginTop: 8, lineHeight: 1.6 }}>
          dwell {(classification.features.dwell/1000).toFixed(1)}s · scan {Math.round(classification.features.scan)}px/s · cadence {Math.round(classification.features.cadence*100)}% · breadth {Math.round(classification.features.breadth*100)}%
        </div>
      </section>

      {/* interest model */}
      {topTags.length > 0 && (
        <section className="mind__section">
          <div className="mind__label">Interest model — cumulative tag affinity</div>
          {topTags.map(([tag,val]) => (
            <div key={tag} className="interestrow">
              <span>{tag}</span>
              <span className="interestrow__track"><span className="interestrow__fill" style={{ width: `${Math.round((val/maxTag)*100)}%` }} /></span>
              <span>{Math.round(val*100)}%</span>
            </div>
          ))}
        </section>
      )}

      {/* trail / promoted */}
      <section className="mind__section">
        <div className="mind__label">What the engine promotes</div>
        <div className="mono" style={{ fontSize: '0.68rem', color: 'var(--ink-dim)', lineHeight: 1.6 }}>
          <div><b>Trail:</b> {trail.length ? trail.join(' → ') : '— not enough data yet'}</div>
          <div style={{ marginTop: 6 }}><b>Promoted:</b> {promoted.length ? promoted.join(', ') : '—'}</div>
        </div>
      </section>

      {/* manifest */}
      {manifest && (
        <section className="mind__section">
          <div className="mind__label">Last reconfiguration</div>
          <div className="mono" style={{ fontSize: '0.7rem', color: 'var(--ink)', lineHeight: 1.6, background: 'var(--paper-2)', padding: '10px 12px', border: '1px solid var(--line)' }}>
            <div style={{ fontFamily: 'var(--serif)', fontSize: '0.92rem', fontStyle: 'italic', marginBottom: 6 }}>{manifest.headline}</div>
            <div><b>{manifest.fromLabel}</b> → <b>{manifest.toLabel}</b> · {Math.round(manifest.confidence*100)}% · {manifest.manual ? 'manual' : 'automatic'}</div>
            <div style={{ marginTop: 4, color: 'var(--ink-faint)' }}>{manifest.reasons.join(' · ')}</div>
          </div>
        </section>
      )}

      {/* log */}
      <section className="mind__section">
        <div className="mind__label">Evolution log <button className="btn btn--ghost btn--sm" onClick={() => reset()} style={{ fontSize: '0.6rem' }}>clear storage</button></div>
        <div style={{ maxHeight: 220, overflowY: 'auto' }}>
          {log.length === 0 ? <span className="mono" style={{ fontSize: '0.66rem', color: 'var(--ink-faint)' }}>No events yet — interact with the workspace.</span>
            : log.slice(0,12).map((entry,i) => (
              <div key={i} className="logline" data-kind={entry.kind}>
                <span className="logline__gen">g{entry.gen}</span>
                <span className="logline__txt">{entry.text}</span>
              </div>
            ))}
        </div>
      </section>

      {/* actions */}
      <div style={{ display: 'flex', gap: 8, paddingTop: 16, flexWrap: 'wrap' }}>
        <button className="btn btn--sm" onClick={() => mutate()}>mutate generation</button>
        <button className="btn btn--sm" onClick={() => reset()}>erase memory</button>
        {genome.paradigm !== paradigm && (
          <button className="btn btn--sm" onClick={() => setParadigm(genome.paradigm as any, false)}>undo last switch</button>
        )}
      </div>

      <div className="mono" style={{ fontSize: '0.6rem', color: 'var(--ink-faint)', marginTop: 18, borderTop: '1px solid var(--line)', paddingTop: 12, lineHeight: 1.6 }}>
        Engine: affinity scoring (ideal signatures + weighted distance) · confidence ≥ 42% + margin ≥ 5% + 9s gap before restructuring.<br/>
        Persistence: localStorage under <b>strata/genome-v2</b> — scoped to this browser & origin. No server, no sync.
      </div>
    </div>
  );
}
