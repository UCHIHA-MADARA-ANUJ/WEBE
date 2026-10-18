'use client';

import { useState } from 'react';
import Link from 'next/link';
import { useEngine } from '@/engine/store';
import { ARCHETYPES, PARADIGM_ORDER, PARADIGMS } from '@/engine/types';

export const PARADIGM_DISPLAY: Record<string, { name: string; tagline: string }> = {
  codex:         { name: 'Brief',       tagline: 'One question, one entity at a time.' },
  constellation: { name: 'Atlas',       tagline: 'A map of the whole decision.' },
  mosaic:        { name: 'Board',       tagline: 'A dense board that re-tiles itself.' },
  lattice:       { name: 'Matrix',      tagline: 'Index + evidence, side by side.' },
  console:       { name: 'Command',     tagline: 'A prompt. You type, it answers.' },
  zen:           { name: 'Focus',       tagline: 'One entity, full bleed.' },
};

function shorten(text: string, max = 28) {
  return text.length > max ? `${text.slice(0, max - 1).trimEnd()}…` : text;
}

export function Chrome({ onMind, onNavigate }: { onMind: () => void; onNavigate: (id: string) => void }) {
  const { paradigm, setParadigm, pinned, classification, genome, primary } = useEngine();
  const top = classification.top;
  const spec = ARCHETYPES.find((a) => a.id === top);
  const confidence = Math.round(classification.confidence * 100);

  return (
    <header className="bar">
      <Link href="/" className="brand" style={{ textDecoration: 'none' }}>
        <span className="brand__mark">Strata</span>
        <span className="brand__sub">The interface follows the work</span>
      </Link>

      {/* primary action is the hero — not buried */}
      {primary.nodeId && (
        <button className="btn btn--accent btn--sm bar__primary" onClick={() => onNavigate(primary.nodeId as string)}>
          {shorten(primary.label)}
        </button>
      )}

      <div className="bar__spacer" />

      {/* minimal paradigm indicator — not 6 buttons shouting at you */}
      <div className="bar__paradigm">
        <span className="bar__paradigm-glyph">{PARADIGMS[paradigm].glyph}</span>
        <span className="bar__paradigm-name">{PARADIGM_DISPLAY[paradigm]?.name ?? paradigm}</span>
        {pinned && <span className="bar__paradigm-pin">● pinned</span>}
      </div>

      <div className="bar__divider" />

      <button className="btn btn--ghost btn--sm" onClick={onMind}>
        Why this layout?
      </button>
      <Link href="/lab" className="btn btn--sm">
        Lab
      </Link>
    </header>
  );
}
