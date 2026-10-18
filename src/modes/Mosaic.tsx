import { useEffect, useLayoutEffect, useMemo, useRef, useState } from 'react';
import { NODE_BY_ID, TAGS, type FieldNode } from '../content/graph';
import { orderFor } from '../engine/genome';
import { useEngine } from '../engine/store';
import { familyColor, Prose, Readings } from '../components/common';
import type { ModeProps } from './types';

function sameOrder(a: string[], b: string[]) {
  if (a.length !== b.length) return false;
  for (let i = 0; i < a.length; i++) if (a[i] !== b[i]) return false;
  return true;
}

/**
 * MOSAIC — the dense board.
 *
 * Contract: information density is the point. You scan, hover for a quick
 * read, and the board silently re-sorts itself as your interests shift.
 * Nothing is committed until you open it.
 */
export function MosaicMode({ focus, navigate }: ModeProps) {
  const { genome, note, noteFilter, noteSearch, related } = useEngine();
  const [query, setQuery] = useState('');
  const [tag, setTag] = useState<string | null>(null);
  const [open, setOpen] = useState<string | null>(focus);
  const gridRef = useRef<HTMLDivElement | null>(null);
  const rects = useRef(new Map<string, DOMRect>());
  const genomeRef = useRef(genome);
  genomeRef.current = genome;

  const [order, setOrder] = useState<string[]>(() => orderFor(genome));

  /* the board re-sorts itself as your interest accumulates */
  useEffect(() => {
    const id = window.setInterval(() => {
      const g = genomeRef.current;
      const next = orderFor(g, { weights: g.nodeInterest });
      setOrder((prev) => (sameOrder(prev, next) ? prev : next));
    }, 2600);
    return () => window.clearInterval(id);
  }, []);

  /* FLIP: tiles physically slide to their new positions */
  useLayoutEffect(() => {
    const grid = gridRef.current;
    if (!grid) return;
    const moves: [HTMLElement, number, number][] = [];
    grid.querySelectorAll<HTMLElement>('[data-flip]').forEach((el) => {
      const id = el.dataset.flip!;
      const prev = rects.current.get(id);
      const next = el.getBoundingClientRect();
      if (prev) {
        const dx = prev.left - next.left;
        const dy = prev.top - next.top;
        if (Math.abs(dx) > 1 || Math.abs(dy) > 1) moves.push([el, dx, dy]);
      }
      rects.current.set(id, next);
    });
    for (const [el, dx, dy] of moves) {
      el.animate(
        [{ transform: `translate(${dx}px, ${dy}px)` }, { transform: 'translate(0,0)' }],
        { duration: 560, easing: 'cubic-bezier(0.16, 1, 0.3, 1)' },
      );
    }
  }, [order]);

  const tiles = useMemo(() => {
    const q = query.trim().toLowerCase();
    return order
      .map((id) => NODE_BY_ID[id])
      .filter(Boolean)
      .filter((n: FieldNode) => {
        if (tag && !n.tags.includes(tag)) return false;
        if (!q) return true;
        return (
          n.title.toLowerCase().includes(q) ||
          n.summary.toLowerCase().includes(q) ||
          n.catalog.toLowerCase().includes(q) ||
          n.tags.some((t) => t.includes(q))
        );
      });
  }, [order, query, tag]);

  const openNode = open ? NODE_BY_ID[open] : null;
  const maxInterest = Math.max(
    0.0001,
    ...tiles.map((t) => genome.nodeInterest[t.id] ?? 0),
  );

  return (
    <div className="mosaic">
      <div className="mosaic__bar">
        <input
          className="lattice__input"
          style={{ maxWidth: 220 }}
          placeholder="filter the field…"
          value={query}
          onChange={(e) => {
            setQuery(e.target.value);
            noteSearch(e.target.value);
          }}
        />
        {TAGS.slice(0, 12).map((t) => (
          <button
            key={t}
            className="chip"
            data-on={tag === t}
            onClick={() => {
              const next = tag === t ? null : t;
              setTag(next);
              noteFilter(t);
            }}
          >
            {t}
          </button>
        ))}
        <span style={{ flex: 1 }} />
        <span className="eyebrow">
          {tiles.length} tiles · re-sorting live
        </span>
      </div>

      <div className="mosaic__grid" ref={gridRef}>
        {tiles.map((n) => {
          const interest = genome.nodeInterest[n.id] ?? 0;
          return (
            <div
              key={n.id}
              className="tile"
              data-flip={n.id}
              data-open={open === n.id}
              data-seen={genome.visited.includes(n.id)}
              style={{ ['--fh' as string]: familyColor(n.family) }}
              onClick={() => {
                setOpen(n.id);
                navigate(n.id);
              }}
            >
              <div className="tile__head">
                <span className="dot" style={{ background: familyColor(n.family) }} />
                <span className="tile__fam">{n.family}</span>
                {genome.visited.includes(n.id) && (
                  <span className="tile__fam" style={{ marginLeft: 'auto' }}>
                    seen
                  </span>
                )}
              </div>
              <h3 className="tile__title">{n.title}</h3>
              <p className="tile__summary">{n.summary}</p>
              <div className="tile__foot">
                <span>{n.tags.slice(0, 2).join(' · ')}</span>
                <span className="tile__bar">
                  <span
                    className="tile__barfill"
                    style={{ width: `${(interest / maxInterest) * 100}%` }}
                  />
                </span>
              </div>
              <div className="tile__peek" onClick={(e) => e.stopPropagation()}>
                <button
                  className="btn btn--sm"
                  onClick={() => {
                    setOpen(n.id);
                  }}
                >
                  read
                </button>
                <button
                  className="btn btn--sm"
                  onClick={() => {
                    const rel = related(n.id)[0]?.id;
                    if (rel) {
                      note('edge');
                      navigate(rel);
                    }
                  }}
                >
                  follow a relation
                </button>
              </div>
            </div>
          );
        })}
      </div>

      {openNode && (
        <div
          style={{
            position: 'fixed',
            left: 0,
            right: 0,
            bottom: 0,
            zIndex: 60,
            borderTop: '1px solid var(--line-strong)',
            background: 'linear-gradient(0deg, rgba(6,9,17,0.98), rgba(8,12,22,0.95))',
            backdropFilter: 'blur(16px)',
            padding: '18px 24px 22px',
            display: 'grid',
            gridTemplateColumns: 'minmax(0,1fr) auto',
            gap: 24,
            alignItems: 'start',
            boxShadow: '0 -30px 70px rgba(0,0,0,0.5)',
            animation: 'fadeUp 0.4s var(--ease-out) both',
          }}
        >
          <div style={{ minWidth: 0, maxHeight: '42vh', overflowY: 'auto' }}>
            <div className="codex__cat" style={{ marginBottom: 6 }}>
              <span className="dot" style={{ background: familyColor(openNode.family) }} />
              <span className="eyebrow">{openNode.catalog}</span>
            </div>
            <h2 className="display" style={{ fontSize: '1.7rem', margin: '0 0 6px' }}>
              {openNode.title}
            </h2>
            <p
              className="serif"
              style={{ fontStyle: 'italic', color: 'var(--ink-dim)', margin: '0 0 12px' }}
            >
              {openNode.summary}
            </p>
            <Prose node={openNode} />
            <Readings node={openNode} />
          </div>
          <div style={{ display: 'flex', flexDirection: 'column', gap: 8 }}>
            <button className="btn btn--sm" onClick={() => setOpen(null)}>
              close
            </button>
            <button
              className="btn btn--sm btn--accent"
              onClick={() => {
                const rel = related(openNode.id)[0]?.id;
                if (rel) {
                  note('edge');
                  navigate(rel);
                }
              }}
            >
              follow a relation →
            </button>
          </div>
        </div>
      )}
    </div>
  );
}
