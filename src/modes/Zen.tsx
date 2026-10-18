import { useMemo } from 'react';
import { NODE_BY_ID } from '../content/graph';
import { useEngine } from '../engine/store';
import { familyColor } from '../components/common';
import type { ModeProps } from './types';

/**
 * ZEN — one object, full bleed.
 *
 * Contract: there is no index, no rail, no alternative. The only decisions
 * are to go deeper, to return, or to let the site choose. Everything else
 * is removed on purpose.
 */
export function ZenMode({ focus, navigate }: ModeProps) {
  const { genome, trail, related, signals } = useEngine();

  const current = focus ?? trail[0] ?? genome.visited[genome.visited.length - 1] ?? null;
  const node = current ? NODE_BY_ID[current] : null;

  const deeper = useMemo(() => {
    if (!current) return null;
    const rel = related(current);
    if (rel.length) return rel[0].id;
    const idx = trail.indexOf(current);
    return trail[(idx + 1) % trail.length] ?? null;
  }, [current, related, trail]);

  const back = useMemo(() => {
    const path = signals.path;
    if (path.length > 1) return path[path.length - 2];
    return null;
  }, [signals.path]);

  const chosen = useMemo(() => {
    const unseen = trail.filter((id) => !genome.visited.includes(id));
    if (unseen.length) return unseen[Math.floor(Math.random() * unseen.length)];
    return trail[Math.floor(Math.random() * Math.max(1, trail.length))] ?? null;
  }, [trail, genome.visited]);

  if (!node) {
    return (
      <div className="zen">
        <div className="zen__inner">
          <p className="prose">Nothing held. Choose something from the field.</p>
        </div>
      </div>
    );
  }

  return (
    <div className="zen">
      <div className="zen__inner" key={node.id}>
        <div
          className="codex__cat"
          style={{ justifyContent: 'center', marginBottom: 4 }}
        >
          <span className="dot" style={{ background: familyColor(node.family) }} />
          <span className="eyebrow">{node.catalog}</span>
        </div>

        <h1 className="zen__title">{node.title}</h1>
        <p className="zen__summary">{node.summary}</p>

        <div className="zen__body">
          {node.body.map((p, i) => (
            <p key={i}>{p}</p>
          ))}
        </div>

        <div className="zen__choices">
          {deeper && (
            <button className="btn btn--accent" onClick={() => navigate(deeper)}>
              go deeper →
            </button>
          )}
          {chosen && chosen !== node.id && (
            <button className="btn" onClick={() => navigate(chosen)}>
              let it choose
            </button>
          )}
          {back && (
            <button className="btn btn--ghost" onClick={() => navigate(back)}>
              ← return
            </button>
          )}
        </div>
      </div>
    </div>
  );
}
