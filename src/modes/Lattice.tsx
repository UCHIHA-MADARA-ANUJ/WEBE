import { useEffect, useMemo, useState } from 'react';
import { NODE_BY_ID, NODES, type FieldNode } from '../content/graph';
import { useEngine } from '../engine/store';
import { familyColor, Prose, Readings, Relations } from '../components/common';
import type { ModeProps } from './types';

type SortKey = 'interest' | 'title' | 'family' | 'weight';

/**
 * LATTICE — index on the left, evidence on the right.
 *
 * Contract: a flat, sortable index beside a working detail pane and a
 * comparison strip. Built for holding several objects in mind at once.
 */
export function LatticeMode({ focus, navigate }: ModeProps) {
  const { genome, related, note, noteSearch, features } = useEngine();
  const [query, setQuery] = useState('');
  const [sort, setSort] = useState<SortKey>('interest');
  const [selected, setSelected] = useState<string | null>(focus);
  const [slots, setSlots] = useState<string[]>([]);

  const current = selected ?? focus ?? null;

  const rows = useMemo(() => {
    const q = query.trim().toLowerCase();
    let list: FieldNode[] = NODES.slice();
    if (q) {
      list = list.filter(
        (n) =>
          n.title.toLowerCase().includes(q) ||
          n.summary.toLowerCase().includes(q) ||
          n.tags.some((t) => t.includes(q)) ||
          n.catalog.toLowerCase().includes(q),
      );
    }
    const byInterest = (n: FieldNode) => genome.nodeInterest[n.id] ?? 0;
    list.sort((a, b) => {
      if (sort === 'title') return a.title.localeCompare(b.title);
      if (sort === 'family') return a.family.localeCompare(b.family) || a.title.localeCompare(b.title);
      if (sort === 'weight') return b.weight - a.weight;
      return byInterest(b) - byInterest(a);
    });
    return list;
  }, [query, sort, genome.nodeInterest]);

  useEffect(() => {
    const onKey = (e: KeyboardEvent) => {
      const el = e.target as HTMLElement | null;
      if (el && (el.tagName === 'INPUT' || el.tagName === 'TEXTAREA')) return;
      if (e.key === 'ArrowDown' || e.key === 'ArrowUp') {
        e.preventDefault();
        const idx = rows.findIndex((r) => r.id === current);
        const nextIdx = e.key === 'ArrowDown' ? Math.min(rows.length - 1, idx + 1) : Math.max(0, idx - 1);
        const nxt = rows[nextIdx];
        if (nxt) {
          setSelected(nxt.id);
          navigate(nxt.id);
        }
      }
    };
    window.addEventListener('keydown', onKey);
    return () => window.removeEventListener('keydown', onKey);
  }, [rows, current, navigate]);

  const node = current ? NODE_BY_ID[current] : null;

  const toggleSlot = (id: string) => {
    if (!features.compare) {
      note('compare');
      return;
    }
    setSlots((prev) => {
      if (prev.includes(id)) return prev.filter((x) => x !== id);
      if (prev.length >= 3) return [...prev.slice(1), id];
      return [...prev, id];
    });
    note('compare');
  };

  return (
    <div className="lattice">
      <aside className="lattice__index">
        <div className="lattice__search">
          <input
            className="lattice__input"
            placeholder="search the corpus…"
            value={query}
            onChange={(e) => {
              setQuery(e.target.value);
              noteSearch(e.target.value);
            }}
          />
        </div>
        <div
          style={{
            display: 'flex',
            gap: 6,
            padding: '8px 12px',
            borderBottom: '1px solid var(--line)',
            flexWrap: 'wrap',
          }}
        >
          {(['interest', 'title', 'family', 'weight'] as SortKey[]).map((k) => (
            <button
              key={k}
              className="chip"
              data-on={sort === k}
              onClick={() => setSort(k)}
            >
              {k}
            </button>
          ))}
        </div>
        <div className="lattice__rows">
          {rows.map((n, i) => (
            <button
              key={n.id}
              className="lrow"
              data-on={n.id === current}
              onClick={() => {
                setSelected(n.id);
                navigate(n.id);
              }}
              onDoubleClick={() => toggleSlot(n.id)}
            >
              <span className="lrow__n">{String(i + 1).padStart(2, '0')}</span>
              <span
                className="lrow__t"
                style={{ display: 'flex', alignItems: 'center', gap: 7 }}
              >
                <span className="dot" style={{ background: familyColor(n.family) }} />
                {n.title}
              </span>
              <span className="lrow__w">
                {genome.visited.includes(n.id) ? '●' : '·'}
              </span>
            </button>
          ))}
        </div>
      </aside>

      <div className="lattice__detail">
        {node ? (
          <div className="lattice__inner" key={node.id}>
            <div className="codex__cat">
              <span className="dot" style={{ background: familyColor(node.family) }} />
              <span className="eyebrow">{node.catalog}</span>
            </div>
            <h1 className="display lattice__title">{node.title}</h1>
            <p className="codex__summary">{node.summary}</p>
            <Prose node={node} />
            <Readings node={node} />
            <Relations node={node} onOpen={(id) => navigate(id)} />

            <div style={{ display: 'flex', gap: 8, marginTop: 28, flexWrap: 'wrap' }}>
              <button className="btn btn--sm" onClick={() => toggleSlot(node.id)}>
                {slots.includes(node.id) ? 'remove from comparison' : 'add to comparison'}
              </button>
              {related(node.id)
                .slice(0, 3)
                .map((r) => {
                  const o = NODE_BY_ID[r.id];
                  if (!o) return null;
                  return (
                    <button
                      key={r.id}
                      className="btn btn--sm"
                      onClick={() => {
                        setSelected(r.id);
                        navigate(r.id);
                      }}
                    >
                      → {o.title}
                    </button>
                  );
                })}
            </div>
            {!features.compare && (
              <p
                className="mono"
                style={{ fontSize: '0.62rem', color: 'var(--ink-faint)', marginTop: 12 }}
              >
                comparison unlocks at generation 3 — mutate to reach it.
              </p>
            )}
          </div>
        ) : (
          <div className="lattice__inner">
            <p className="prose">Select an entry from the index.</p>
          </div>
        )}
      </div>

      <div className="lattice__strip">
        <span className="eyebrow" style={{ marginRight: 6 }}>
          comparison
        </span>
        {[0, 1, 2].map((i) => {
          const id = slots[i];
          const n = id ? NODE_BY_ID[id] : null;
          return (
            <button
              key={i}
              className="lattice__slot"
              data-filled={!!n}
              onClick={() => n && navigate(n.id)}
              style={{ textAlign: 'left' }}
            >
              <div className="lattice__slot-k">
                {n ? n.title : `slot ${String.fromCharCode(65 + i)} — empty`}
              </div>
              <div
                className="mono"
                style={{ fontSize: '0.58rem', color: 'var(--ink-faint)', marginTop: 3 }}
              >
                {n ? n.tags.slice(0, 3).join(' · ') : 'double-click a row to place it'}
              </div>
            </button>
          );
        })}
        <span className="eyebrow" style={{ marginLeft: 'auto' }}>
          {slots.length}/3
        </span>
      </div>
    </div>
  );
}
