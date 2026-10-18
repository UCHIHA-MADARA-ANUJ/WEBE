import { useState } from 'react';
import { useEngine } from '../engine/store';
import { ARCHETYPES, PARADIGM_ORDER, PARADIGMS } from '../engine/types';

function shorten(text: string, max = 30) {
  return text.length > max ? `${text.slice(0, max - 1).trimEnd()}…` : text;
}

export function Chrome({
  onMind,
  onNavigate,
}: {
  onMind: () => void;
  onNavigate: (id: string) => void;
}) {
  const { paradigm, setParadigm, pinned, classification, genome, primary, mutate } = useEngine();
  const [busy, setBusy] = useState(false);

  const top = classification.top;
  const spec = ARCHETYPES.find((a) => a.id === top);
  const confidence = Math.round(classification.confidence * 100);

  return (
    <header className="bar">
      <div className="brand" onClick={() => window.scrollTo({ top: 0 })}>
        <span className="brand__mark">Deep Field</span>
        <span className="brand__sub">living atlas</span>
      </div>

      <button
        className="genbadge"
        title="Force the next generation — unlock behaviour, re-seed the arrangement"
        onClick={() => {
          setBusy(true);
          mutate();
          window.setTimeout(() => setBusy(false), 320);
        }}
      >
        {busy ? '···' : 'gen'} <b>{genome.generation}</b>
      </button>

      <div className="bar__spacer" />

      <nav className="switcher" aria-label="structure">
        {PARADIGM_ORDER.map((p) => {
          const ps = PARADIGMS[p];
          return (
            <button
              key={p}
              className="switch"
              data-on={paradigm === p}
              onClick={() => setParadigm(p, true)}
              title={`${ps.name} — ${ps.tagline}`}
            >
              <span className="switch__glyph">{ps.glyph}</span>
              <span className="switch__name">{ps.name}</span>
              {genome.used.includes(p) && paradigm !== p && (
                <span className="switch__badge" title="you have used this structure" />
              )}
            </button>
          );
        })}
      </nav>

      {pinned && (
        <button
          className="pinbtn"
          title="Release the engine — let it restructure on its own again"
          onClick={() => setParadigm(paradigm, false)}
        >
          ◉
        </button>
      )}

      <div
        className="readout"
        title={
          classification.blank
            ? 'the engine has no read on you yet'
            : `the engine reads you as ${top} — ${confidence}% confidence`
        }
      >
        <span className="readout__glyph">{classification.blank ? '◌' : spec?.glyph}</span>
        <span className="readout__bar">
          <span className="readout__fill" style={{ width: `${confidence}%` }} />
        </span>
        <b>{classification.blank ? 'listening' : `${confidence}%`}</b>
      </div>

      {primary.nodeId && (
        <button
          className="btn btn--accent btn--sm bar__primary"
          title={primary.label}
          onClick={() => onNavigate(primary.nodeId as string)}
        >
          {shorten(primary.label, 28)}
        </button>
      )}

      <button className="btn btn--sm" onClick={onMind} title="open the mind panel">
        Mind
      </button>
    </header>
  );
}
