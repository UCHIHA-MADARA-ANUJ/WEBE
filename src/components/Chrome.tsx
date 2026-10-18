'use client';

import Link from 'next/link';
import { useEngine } from '@/engine/store';

function shorten(text: string, max = 28) {
  return text.length > max ? `${text.slice(0, max - 1).trimEnd()}…` : text;
}

export const PARADIGM_DISPLAY_REMAP: Record<string, { name: string; tagline: string }> = {
  codex:         { name: 'Brief',       tagline: 'One question, one entity at a time.' },
  constellation: { name: 'Atlas',       tagline: 'A map of the whole decision.' },
  mosaic:        { name: 'Board',       tagline: 'A dense board that re-tiles itself.' },
  lattice:       { name: 'Matrix',      tagline: 'Index + evidence, side by side.' },
  console:       { name: 'Command',     tagline: 'A prompt. You type, it answers.' },
  zen:           { name: 'Focus',       tagline: 'One entity, full bleed.' },
};

export function Chrome({
  onMind,
  onNavigate,
}: {
  onMind: () => void;
  onNavigate: (id: string) => void;
}) {
  const { paradigm, primary, genome } = useEngine();
  const disp = PARADIGM_DISPLAY_REMAP[paradigm] ?? { name: paradigm, tagline: '' };

  return (
    <header className="bar bar--minimal">
      <Link href="/" className="brand brand--minimal" style={{ textDecoration: 'none' }}>
        <span className="brand__mark">STRATA</span>
        <span className="brand__sub">The interface follows the work</span>
      </Link>

      <div className="bar__spacer" />

      {/* paradigm indicator — subtle, not a wall of 6 */}
      <div className="bar__paradigm" title={`${disp.name} — ${disp.tagline}`}>
        <span className="bar__paradigm-dot" />
        <span className="bar__paradigm-name">{disp.name}</span>
      </div>

      <div className="bar__divider" />

      {primary.nodeId && (
        <button className="btn btn--accent btn--sm bar__primary" title={primary.label} onClick={() => onNavigate(primary.nodeId as string)}>
          {shorten(primary.label, 28)} →
        </button>
      )}

      <button className="bar__link" onClick={onMind}>Why this layout?</button>

      <Link href="/lab" className="bar__link bar__link--ghost">
        Lab
      </Link>

      <span className="bar__gen" title={`generation ${genome.generation}`}>· gen {genome.generation}</span>
    </header>
  );
}

// re-export for compat where imported
export { PARADIGM_DISPLAY_REMAP as PARADIGM_DISPLAY };
