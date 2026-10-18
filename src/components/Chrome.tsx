'use client';

import { useState } from 'react';
import Link from 'next/link';
import { useEngine } from '@/engine/store';
import { ARCHETYPES, PARADIGM_ORDER, PARADIGMS } from '@/engine/types';

// Display remapping: new STRATA names overlay old paradigm IDs
// Engine IDs stay stable (codex etc) so persistence doesn't break.
// Display names below are what the judge sees.
export const PARADIGM_DISPLAY: Record<string, { name: string; tagline: string }> = {
  codex:         { name: 'Brief',       tagline: 'One question, one entity at a time.' },
  constellation: { name: 'Atlas',       tagline: 'A map of the whole decision.' },
  mosaic:        { name: 'Board',       tagline: 'A dense board that re-tiles itself.' },
  lattice:       { name: 'Matrix',      tagline: 'Index + evidence, side by side.' },
  console:       { name: 'Command',     tagline: 'A prompt. You type, it answers.' },
  zen:           { name: 'Focus',       tagline: 'One entity, full bleed.' },
};

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
      <Link href="/" className="brand" style={{ textDecoration: 'none' }}>
        <span className="brand__mark">Strata</span>
        <span className="brand__sub">the interface follows the work</span>
      </Link>

      <button
        className="genbadge"
        title="Force the next generation — unlock behaviour, re-seed the arrangement"
        onClick={() => { setBusy(true); mutate(); setTimeout(() => setBusy(false), 320); }}
      >
        {busy ? '···' : 'gen'} <b>{genome.generation}</b>
      </button>

      <div className="bar__spacer" />

      <nav className="switcher" aria-label="structure">
        {PARADIGM_ORDER.map((p) => {
          const ps = PARADIGMS[p];
          const disp = PARADIGM_DISPLAY[p] ?? { name: ps.name, tagline: ps.tagline };
          return (
            <button
              key={p}
              className="switch"
              data-on={paradigm === p}
              onClick={() => setParadigm(p, true)}
              title={`${disp.name} — ${disp.tagline}`}
            >
              <span className="switch__glyph">{ps.glyph}</span>
              <span className="switch__name">{disp.name}</span>
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
          ◉ pinned
        </button>
      )}

      <div
        className="readout"
        title={classification.blank ? 'the engine has no read on you yet' : `the engine reads you as ${top} — ${confidence}% confidence`}
      >
        <span className="readout__glyph">{classification.blank ? '◌' : spec?.glyph}</span>
        <span className="readout__bar"><span className="readout__fill" style={{ width: `${confidence}%` }} /></span>
        <b>{classification.blank ? 'listening' : `${confidence}%`}</b>
      </div>

      {primary.nodeId && (
        <button className="btn btn--accent btn--sm bar__primary" title={primary.label} onClick={() => onNavigate(primary.nodeId as string)}>
          {shorten(primary.label, 28)}
        </button>
      )}

      <button className="btn btn--sm" onClick={onMind} title="open the mind panel">Mind</button>

      <Link href="/lab" className="btn btn--sm" title="Evolution Lab — inspect the engine">
        Lab
      </Link>
    </header>
  );
}
