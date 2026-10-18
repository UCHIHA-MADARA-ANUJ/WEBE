import { useEffect, useState } from 'react';
import { useEngine } from '../engine/store';
import { NODE_BY_ID } from '../content/graph';
import { PARADIGMS } from '../engine/types';

export function Reconfigure() {
  const { manifest, setParadigm } = useEngine();
  const [visible, setVisible] = useState(false);
  const [key, setKey] = useState(0);

  useEffect(() => {
    if (!manifest) return;
    setKey((k) => k + 1);
    setVisible(true);
    const t = window.setTimeout(() => setVisible(false), manifest.manual ? 2600 : 6600);
    return () => window.clearTimeout(t);
  }, [manifest]);

  if (!manifest || !visible) return null;

  const to = PARADIGMS[manifest.to];
  const from = PARADIGMS[manifest.from];

  /* a manual change gets a quiet note; an engine change gets the full
     manifest of what it did and why */
  if (manifest.manual) {
    return (
      <div className="toast" key={key} onClick={() => setVisible(false)}>
        <span className="toast__k">structure</span>
        <span className="toast__v">
          {from.name} <span className="arrow">→</span> <b>{to.name}</b>
        </span>
        <span className="toast__n">the engine is watching, not steering</span>
      </div>
    );
  }

  return (
    <div className="reconf" onClick={() => setVisible(false)} key={key}>
      <div className="reconf__card" onClick={(e) => e.stopPropagation()}>
        <div className="reconf__kicker">structure reconfigured</div>
        <h3 className="reconf__head">{manifest.headline}</h3>

        <dl className="reconf__rows">
          <div className="reconf__row">
            <dt>layout</dt>
            <dd>
              <span style={{ opacity: 0.55 }}>{from.name}</span>
              <span className="arrow">→</span>
              <b>{to.name}</b>
              <div style={{ fontSize: '0.76rem', color: 'var(--ink-faint)', marginTop: 4 }}>
                {to.contract}
              </div>
            </dd>
          </div>

          <div className="reconf__row">
            <dt>verbs</dt>
            <dd>
              {to.verbs.map((v) => (
                <span key={v} style={{ marginRight: 12 }}>
                  {v}
                </span>
              ))}
            </dd>
          </div>

          {manifest.promoted.length > 0 && (
            <div className="reconf__row">
              <dt>promoted</dt>
              <dd>
                {manifest.promoted.map((id) => (
                  <span key={id} style={{ marginRight: 12 }}>
                    {NODE_BY_ID[id]?.title ?? id}
                  </span>
                ))}
              </dd>
            </div>
          )}

          <div className="reconf__row">
            <dt>because</dt>
            <dd>
              {manifest.reasons.map((r, i) => (
                <div key={i} style={{ marginBottom: 2 }}>
                  {r}
                </div>
              ))}
              <div style={{ color: 'var(--ink-faint)', marginTop: 4, fontSize: '0.76rem' }}>
                read as <b>{manifest.archetype}</b> at {Math.round(manifest.confidence * 100)}%
                confidence
              </div>
            </dd>
          </div>
        </dl>

        <div className="reconf__actions">
          <button className="btn btn--sm" onClick={() => setVisible(false)}>
            keep it
          </button>
          <button
            className="btn btn--sm btn--accent"
            onClick={() => {
              setParadigm(manifest.to, true);
              setVisible(false);
            }}
          >
            pin {to.name}
          </button>
        </div>
      </div>
    </div>
  );
}
