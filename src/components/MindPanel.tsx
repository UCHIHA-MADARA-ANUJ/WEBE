import { ARCHETYPES, PARADIGMS, PARADIGM_ORDER } from '../engine/types';
import { useEngine } from '../engine/store';
import { confidenceLabel, normalise } from '../engine/classify';
import { NODE_BY_ID } from '../content/graph';
import { Panel } from './common';

export function MindPanel({ open, onClose }: { open: boolean; onClose: () => void }) {
  const {
    classification,
    genome,
    signals,
    features,
    paradigm,
    setParadigm,
    mutate,
    reset,
  } = useEngine();

  const topTags = Object.entries(genome.interest)
    .sort((a, b) => b[1] - a[1])
    .slice(0, 8);
  const maxTag = topTags[0]?.[1] ?? 1;

  const featRows: [string, string][] = [
    ['opens', String(signals.opens)],
    ['unique', String(new Set(signals.path).size)],
    ['revisits', String(signals.revisits)],
    ['relation steps', String(signals.steps)],
    ['cross jumps', String(signals.jumps)],
    ['scroll px', String(Math.round(signals.scrollPixels))],
    ['peak v px/s', String(Math.round(signals.peakVelocity))],
    ['focus', `${(signals.focusMs / 1000).toFixed(0)}s`],
    ['elapsed', `${(signals.elapsedMs / 1000).toFixed(0)}s`],
    ['commands', String(signals.commands.length)],
    ['queries', String(signals.queries.length)],
    ['filters', String(signals.filters.length)],
    ...Object.entries(signals.actions).map(
      ([k, v]) => [`action:${k}`, String(v)] as [string, string],
    ),
  ];

  return (
    <>
      <div className="scrim" data-open={open} onClick={onClose} />
      <aside
        className="mind"
        data-open={open}
        aria-hidden={!open}
        role="dialog"
        aria-label="The Mind — how the engine reads you"
      >
        <div className="mind__head">
          <div>
            <h2 className="mind__title">The Mind</h2>
            <div className="eyebrow">
              generation {genome.generation} · visit {genome.visits} ·{' '}
              {confidenceLabel(classification.confidence)}
            </div>
          </div>
          <button className="btn btn--sm btn--ghost" onClick={onClose} aria-label="close">
            ✕
          </button>
        </div>

        <div className="mind__body">
          <Panel label="How this works">
            <p
              className="mono"
              style={{ fontSize: '0.66rem', color: 'var(--ink-dim)', lineHeight: 1.75, margin: 0 }}
            >
              This site has no fixed shape. The engine below watches how you move —
              what you open, how long you stay, whether you follow a relation or
              jump across the field, how fast you scroll, whether you type — and
              rebuilds the <b>layout</b>, the <b>hierarchy</b> and the{' '}
              <b>available actions</b> around that behaviour.
              <br />
              <br />
              Read enough and it will restructure on its own, and tell you exactly
              what it changed. Pin a structure with the top bar if you would rather
              it left you alone.
            </p>
          </Panel>

          <Panel label="How it reads you">
            {[...ARCHETYPES]
              .sort((x, y) => (classification.scores[y.id] ?? 0) - (classification.scores[x.id] ?? 0))
              .map((a) => {
              const score = classification.scores[a.id] ?? 0;
              return (
                <div className="arch" key={a.id} data-top={classification.top === a.id}>
                  <div className="arch__name">
                    <span className="arch__glyph">{a.glyph}</span>
                    {a.label}
                  </div>
                  <div className="arch__pct">{Math.round(score * 100)}%</div>
                  <div className="arch__track">
                    <div className="arch__fill" style={{ width: `${score * 100}%` }} />
                  </div>
                </div>
              );
            })}
            <p
              className="mono"
              style={{ fontSize: '0.66rem', color: 'var(--ink-faint)', marginTop: '10px', lineHeight: 1.55 }}
            >
              {ARCHETYPES.find((a) => a.id === classification.top)?.blurb}
            </p>
          </Panel>

          <Panel label="The evidence">
            <ul className="reasons">
              {classification.reasons.map((r, i) => (
                <li key={i}>{r}</li>
              ))}
            </ul>
            <p
              className="mono"
              style={{ fontSize: '0.64rem', color: 'var(--ink-faint)', marginTop: '10px' }}
            >
              {classification.evidence} observations · margin {Math.round(classification.margin * 100)}%
            </p>
          </Panel>

          <Panel label="Signal vector · normalised 0–1">
            <div className="featuregrid">
              {Object.entries(normalise(classification.features)).map(([k, v]) => (
                <div className="feature" key={k}>
                  <div className="feature__k">{k}</div>
                  <div className="feature__v" data-zero={v === 0}>
                    {v.toFixed(2)}
                  </div>
                </div>
              ))}
            </div>
          </Panel>

          <Panel label="Raw observations">
            <div className="featuregrid">
              {featRows.map(([k, v]) => (
                <div className="feature" key={k}>
                  <div className="feature__k">{k}</div>
                  <div className="feature__v" data-zero={v === '0'}>
                    {v}
                  </div>
                </div>
              ))}
            </div>
          </Panel>

          <Panel label="Interest model">
            {topTags.length ? (
              topTags.map(([tag, v]) => (
                <div className="interestrow" key={tag}>
                  <span>{tag}</span>
                  <span className="interestrow__track">
                    <span
                      className="interestrow__fill"
                      style={{ width: `${(v / (maxTag || 1)) * 100}%` }}
                    />
                  </span>
                  <span style={{ textAlign: 'right' }}>{Math.round(v * 100)}</span>
                </div>
              ))
            ) : (
              <p className="mono" style={{ fontSize: '0.68rem', color: 'var(--ink-faint)' }}>
                nothing accumulated yet — open something.
              </p>
            )}
            {genome.visited.length > 0 && (
              <p
                className="mono"
                style={{ fontSize: '0.62rem', color: 'var(--ink-faint)', marginTop: '10px', lineHeight: 1.6 }}
              >
                {genome.visited.length} objects encountered ·{' '}
                {genome.visited
                  .slice(-3)
                  .map((v) => NODE_BY_ID[v]?.title)
                  .filter(Boolean)
                  .join(' → ')}
              </p>
            )}
          </Panel>

          <Panel label="Unlocked behaviour">
            <div className="featuregrid">
              {(['trail', 'compare', 'memory', 'chapters'] as const).map((f) => (
                <div className="feature" key={f}>
                  <div className="feature__k">{f}</div>
                  <div className="feature__v" data-zero={!features[f]}>
                    {features[f] ? 'active' : 'locked'}
                  </div>
                </div>
              ))}
            </div>
            <p
              className="mono"
              style={{ fontSize: '0.62rem', color: 'var(--ink-faint)', marginTop: '10px', lineHeight: 1.6 }}
            >
              Behaviour unlocks with generation. Mutate to advance the structure by hand.
            </p>
            <div style={{ display: 'flex', gap: 8, marginTop: 12, flexWrap: 'wrap' }}>
              <button className="btn btn--sm" onClick={mutate}>
                Mutate structure
              </button>
              <button className="btn btn--sm" onClick={reset}>
                Erase memory
              </button>
            </div>
          </Panel>

          <Panel label="Structural states">
            {PARADIGM_ORDER.map((p) => {
              const spec = PARADIGMS[p];
              return (
                <button
                  key={p}
                  className="relation"
                  onClick={() => setParadigm(p, true)}
                  style={{
                    borderLeft: paradigm === p ? '2px solid var(--accent)' : '2px solid transparent',
                    paddingLeft: paradigm === p ? 10 : 4,
                  }}
                >
                  <span className="relation__t">
                    <span style={{ color: 'var(--accent)', marginRight: 8 }}>{spec.glyph}</span>
                    {spec.name}
                    <span
                      style={{
                        display: 'block',
                        fontFamily: 'var(--sans)',
                        fontSize: '0.76rem',
                        color: 'var(--ink-faint)',
                        marginTop: 3,
                      }}
                    >
                      {spec.contract}
                    </span>
                  </span>
                  <span className="relation__k">
                    {genome.used.includes(p) ? 'used' : '—'}
                  </span>
                </button>
              );
            })}
          </Panel>

          <Panel label="Evolution log">
            {genome.log.length ? (
              genome.log.map((l, i) => (
                <div className="logline" key={`${l.ts}-${i}`} data-kind={l.kind}>
                  <span className="logline__gen">g{l.gen}</span>
                  <span className="logline__txt">{l.text}</span>
                </div>
              ))
            ) : (
              <p className="mono" style={{ fontSize: '0.68rem', color: 'var(--ink-faint)' }}>
                no history yet.
              </p>
            )}
          </Panel>
        </div>
      </aside>
    </>
  );
}
