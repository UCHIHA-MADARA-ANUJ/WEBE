import { useEffect, useMemo } from 'react';
import { NODE_BY_ID } from '../content/graph';
import { useEngine } from '../engine/store';
import { Catalog, Prose, Readings, Relations } from '../components/common';
import type { ModeProps } from './types';

/**
 * CODEX — a reading column.
 *
 * Contract: one object at a time. The universe is folded into a thin rail
 * on the left (the spine). Navigation is sequential; you move forward along
 * a route, and the column *is* the index. Nothing is spatial, nothing is
 * simultaneous.
 */
export function CodexMode({ focus, navigate }: ModeProps) {
  const { genome, trail, signals, related } = useEngine();

  const current = focus ?? trail[0] ?? genome.visited[genome.visited.length - 1] ?? null;
  const node = current ? NODE_BY_ID[current] : null;

  const trailIndex = current ? trail.indexOf(current) : -1;

  const next = useMemo(() => {
    if (!current) return null;
    if (trailIndex >= 0 && trailIndex < trail.length - 1) return trail[trailIndex + 1];
    const rel = related(current);
    return rel[0]?.id ?? null;
  }, [current, trail, trailIndex, related]);

  const previous = useMemo(() => {
    if (!current) return null;
    if (trailIndex > 0) return trail[trailIndex - 1];
    const path = signals.path;
    if (path.length > 1) return path[path.length - 2];
    return null;
  }, [current, trail, trailIndex, signals.path]);

  useEffect(() => {
    const onKey = (e: KeyboardEvent) => {
      const el = e.target as HTMLElement | null;
      if (el && (el.tagName === 'INPUT' || el.tagName === 'TEXTAREA')) return;
      if (e.key === 'j' || e.key === 'ArrowDown') {
        if (next) {
          e.preventDefault();
          navigate(next);
        }
      } else if (e.key === 'k' || e.key === 'ArrowUp') {
        if (previous) {
          e.preventDefault();
          navigate(previous);
        }
      }
    };
    window.addEventListener('keydown', onKey);
    return () => window.removeEventListener('keydown', onKey);
  }, [next, previous, navigate]);

  if (!node) {
    return (
      <div className="codex">
        <div className="codex__main">
          <div className="codex__inner">
            <p className="prose">The column is empty. Choose an entry from the rail.</p>
          </div>
        </div>
      </div>
    );
  }

  return (
    <div className="codex">
      <aside className="codex__spine">
        <div className="codex__spine-title">Your route</div>
        {trail.map((id, i) => {
          const n = NODE_BY_ID[id];
          if (!n) return null;
          return (
            <button
              key={id}
              className="codex__step"
              data-on={id === current}
              data-seen={genome.visited.includes(id)}
              onClick={() => navigate(id)}
            >
              <span className="codex__step-n">{String(i + 1).padStart(2, '0')}</span>
              <span className="codex__step-t">{n.title}</span>
            </button>
          );
        })}

        {signals.path.length > 0 && (
          <>
            <div className="codex__spine-title" style={{ paddingTop: 20 }}>
              Session path
            </div>
            {signals.path
              .slice()
              .reverse()
              .map((id, i) => {
                const n = NODE_BY_ID[id];
                if (!n) return null;
                return (
                  <button
                    key={`${id}-${i}`}
                    className="codex__step"
                    data-on={id === current}
                    onClick={() => navigate(id)}
                  >
                    <span className="codex__step-n">·</span>
                    <span className="codex__step-t">{n.title}</span>
                  </button>
                );
              })}
          </>
        )}
      </aside>

      <div className="codex__main">
        <article className="codex__inner" key={node.id}>
          <Catalog node={node} />
          <h1 className="display codex__title">{node.title}</h1>
          <p className="codex__summary">{node.summary}</p>
          <Prose node={node} />
          <Readings node={node} />
          <Relations node={node} onOpen={(id) => navigate(id)} />
        </article>

        <div className="codex__nav">
          {previous && (
            <button className="btn btn--sm" onClick={() => navigate(previous)}>
              ← back
            </button>
          )}
          {next && (
            <button className="btn btn--sm btn--accent" onClick={() => navigate(next)}>
              continue →
            </button>
          )}
          <span className="spacer" />
          <span className="codex__hint">
            {trailIndex >= 0 ? `stop ${trailIndex + 1} of ${trail.length} on your route` : 'off-route'}
            {'  ·  '}
            j / k to move
          </span>
        </div>
      </div>
    </div>
  );
}
