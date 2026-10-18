import type { ReactNode } from 'react';
import { EDGES, FAMILIES, NODE_BY_ID, type FieldNode } from '../content/graph';
import { useEngine } from '../engine/store';

export function familyColor(family: FieldNode['family']): string {
  const f = FAMILIES[family];
  return `hsl(${f.hue} 72% 66%)`;
}

export function nodeColor(id: string): string {
  const n = NODE_BY_ID[id];
  return n ? familyColor(n.family) : 'var(--accent)';
}

/* ------------------------------------------------------------------ */

export function Catalog({ node, color }: { node: FieldNode; color?: string }) {
  return (
    <div className="codex__cat">
      <span className="dot" style={{ background: color ?? familyColor(node.family) }} />
      <span className="eyebrow">{node.catalog}</span>
    </div>
  );
}

export function Readings({ node }: { node: FieldNode }) {
  if (!node.readings.length) return null;
  return (
    <div className="readings">
      {node.readings.map((r) => (
        <div className="reading" key={r.label}>
          <div className="reading__k">{r.label}</div>
          <div className="reading__v">{r.value}</div>
        </div>
      ))}
    </div>
  );
}

export function Relations({
  node,
  onOpen,
  limit,
}: {
  node: FieldNode;
  onOpen: (id: string) => void;
  limit?: number;
}) {
  const rels = EDGES.filter((e) => e.from === node.id || e.to === node.id)
    .map((e) => ({
      id: e.from === node.id ? e.to : e.from,
      kind: e.kind,
      note: e.note,
    }));

  const list = limit ? rels.slice(0, limit) : rels;
  const { note } = useEngine();
  if (!list.length) return null;

  return (
    <div className="relations">
      <div className="eyebrow" style={{ marginBottom: '4px' }}>
        {list.length} relations
      </div>
      {list.map((r, i) => {
        const other = NODE_BY_ID[r.id];
        if (!other) return null;
        return (
          <button
            key={`${r.id}-${i}`}
            className="relation"
            onClick={() => {
              note('edge');
              onOpen(r.id);
            }}
            type="button"
          >
            <span className="relation__t">{other.title}</span>
            <span className="relation__k">{r.kind.replace(/-/g, ' ')}</span>
          </button>
        );
      })}
    </div>
  );
}

export function Prose({ node }: { node: FieldNode }) {
  return (
    <div className="prose">
      {node.body.map((p, i) => (
        <p key={i}>{p}</p>
      ))}
    </div>
  );
}

export function Tags({ node }: { node: FieldNode }) {
  return (
    <div style={{ display: 'flex', gap: 10, flexWrap: 'wrap' }}>
      {node.tags.map((t) => (
        <span className="tag" key={t}>
          {t}
        </span>
      ))}
    </div>
  );
}

export function Panel({ children, label }: { children: ReactNode; label?: string }) {
  return (
    <div className="mind__section">
      {label && <div className="mind__label">{label}</div>}
      {children}
    </div>
  );
}
