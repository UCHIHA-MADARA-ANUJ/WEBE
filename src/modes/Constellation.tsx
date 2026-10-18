import { useCallback, useEffect, useMemo, useRef, useState } from 'react';
import {
  EDGES,
  FAMILIES,
  FAMILY_ORDER,
  NODE_BY_ID,
  NODES,
  neighboursOf,
  type FieldNode,
} from '../content/graph';
import { mulberry32 } from '../engine/genome';
import { useEngine } from '../engine/store';
import { familyColor } from '../components/common';
import type { ModeProps } from './types';

interface Pt {
  x: number;
  y: number;
}

const VIEW = 520;

/**
 * A deterministic force relaxation. The graph is a real force-directed
 * layout seeded from the visitor's own generation seed, so two visitors
 * can literally be looking at different maps of the same corpus.
 */
function relax(
  nodes: FieldNode[],
  seed: number,
): Record<string, Pt> {
  const rng = mulberry32(seed ^ 0xabcd);
  const pos: Record<string, Pt> = {};
  const vel: Record<string, Pt> = {};

  const familyAngle: Record<string, number> = {};
  FAMILY_ORDER.forEach((f, i) => {
    familyAngle[f] = (i / FAMILY_ORDER.length) * Math.PI * 2 - Math.PI / 2;
  });

  const byFamily = new Map<string, FieldNode[]>();
  for (const n of nodes) {
    const arr = byFamily.get(n.family) ?? [];
    arr.push(n);
    byFamily.set(n.family, arr);
  }

  for (const [family, arr] of byFamily) {
    const base = familyAngle[family] ?? 0;
    arr.forEach((n, i) => {
      const spread = (i / Math.max(1, arr.length)) * 0.8 - 0.4;
      const a = base + spread;
      const r = 150 + (i % 3) * 46 + rng() * 24;
      pos[n.id] = { x: Math.cos(a) * r, y: Math.sin(a) * r };
      vel[n.id] = { x: 0, y: 0 };
    });
  }

  const ids = nodes.map((n) => n.id);
  const adjacency = new Map<string, string[]>();
  for (const e of EDGES) {
    if (!adjacency.has(e.from)) adjacency.set(e.from, []);
    if (!adjacency.has(e.to)) adjacency.set(e.to, []);
    adjacency.get(e.from)!.push(e.to);
    adjacency.get(e.to)!.push(e.from);
  }

  const ITER = 420;
  for (let it = 0; it < ITER; it++) {
    const cool = 1 - it / ITER;

    for (let i = 0; i < ids.length; i++) {
      for (let j = i + 1; j < ids.length; j++) {
        const a = pos[ids[i]];
        const b = pos[ids[j]];
        let dx = a.x - b.x;
        let dy = a.y - b.y;
        let d2 = dx * dx + dy * dy;
        if (d2 < 1) {
          dx = (rng() - 0.5) * 2;
          dy = (rng() - 0.5) * 2;
          d2 = dx * dx + dy * dy + 0.01;
        }
        const d = Math.sqrt(d2);
        const force = (2600 / d2) * cool;
        const fx = (dx / d) * force;
        const fy = (dy / d) * force;
        vel[ids[i]].x += fx;
        vel[ids[i]].y += fy;
        vel[ids[j]].x -= fx;
        vel[ids[j]].y -= fy;
      }
    }

    for (const e of EDGES) {
      const a = pos[e.from];
      const b = pos[e.to];
      if (!a || !b) continue;
      const dx = b.x - a.x;
      const dy = b.y - a.y;
      const d = Math.max(1, Math.hypot(dx, dy));
      const target = 108;
      const f = ((d - target) / d) * 0.055 * cool;
      vel[e.from].x += dx * f;
      vel[e.from].y += dy * f;
      vel[e.to].x -= dx * f;
      vel[e.to].y -= dy * f;
    }

    for (const id of ids) {
      const v = vel[id];
      v.x *= 0.82;
      v.y *= 0.82;
      v.x += -pos[id].x * 0.0016 * cool;
      v.y += -pos[id].y * 0.0016 * cool;
      pos[id].x += v.x;
      pos[id].y += v.y;
    }
  }

  // normalise into view
  let minX = Infinity;
  let maxX = -Infinity;
  let minY = Infinity;
  let maxY = -Infinity;
  for (const id of ids) {
    minX = Math.min(minX, pos[id].x);
    maxX = Math.max(maxX, pos[id].x);
    minY = Math.min(minY, pos[id].y);
    maxY = Math.max(maxY, pos[id].y);
  }
  const cx = (minX + maxX) / 2;
  const cy = (minY + maxY) / 2;
  const span = Math.max(maxX - minX, maxY - minY) || 1;
  const k = (VIEW * 1.72) / span;
  const out: Record<string, Pt> = {};
  for (const id of ids) {
    out[id] = { x: (pos[id].x - cx) * k, y: (pos[id].y - cy) * k };
  }
  return out;
}

/**
 * CONSTELLATION — the spatial paradigm.
 *
 * Contract: nothing is a list, everything is a position. You pan, zoom and
 * trace relations by hovering. Depth is replaced by geometry. The only way
 * to read an object is to fly to it.
 */
export function ConstellationMode({ focus, navigate }: ModeProps) {
  const { genome, signals, note, related } = useEngine();
  const [hovered, setHovered] = useState<string | null>(null);
  const [isolate, setIsolate] = useState(false);
  const [dragging, setDragging] = useState(false);
  const [view, setView] = useState({ x: 0, y: 0, k: 1 });
  const svgRef = useRef<SVGSVGElement | null>(null);
  const dragStart = useRef<{ x: number; y: number; vx: number; vy: number } | null>(null);
  const animRef = useRef<number | null>(null);

  const positions = useMemo(() => relax(NODES, genome.seed), [genome.seed]);
  const focused = focus ?? null;

  const neighbours = useMemo(
    () => (focused ? new Set(neighboursOf(focused)) : new Set<string>()),
    [focused],
  );

  const visible = useMemo(() => {
    if (!isolate || !focused) return null;
    return new Set([focused, ...neighboursOf(focused)]);
  }, [isolate, focused]);

  /* ---- camera ---- */
  const toUser = useCallback((clientX: number, clientY: number) => {
    const svg = svgRef.current;
    if (!svg) return { x: 0, y: 0 };
    const ctm = svg.getScreenCTM();
    if (!ctm) return { x: 0, y: 0 };
    const pt = svg.createSVGPoint();
    pt.x = clientX;
    pt.y = clientY;
    const p = pt.matrixTransform(ctm.inverse());
    return { x: p.x, y: p.y };
  }, []);

  const onWheel = useCallback(
    (e: React.WheelEvent) => {
      e.preventDefault();
      const u = toUser(e.clientX, e.clientY);
      setView((v) => {
        const k = Math.max(0.35, Math.min(4.5, v.k * (e.deltaY < 0 ? 1.12 : 0.89)));
        const gx = (u.x - v.x) / v.k;
        const gy = (u.y - v.y) / v.k;
        return { k, x: u.x - gx * k, y: u.y - gy * k };
      });
    },
    [toUser],
  );

  const onPointerDown = useCallback(
    (e: React.PointerEvent) => {
      (e.target as Element).setPointerCapture?.(e.pointerId);
      const u = toUser(e.clientX, e.clientY);
      dragStart.current = { x: u.x, y: u.y, vx: view.x, vy: view.y };
      setDragging(true);
    },
    [toUser, view],
  );

  const onPointerMove = useCallback(
    (e: React.PointerEvent) => {
      if (!dragStart.current) return;
      const u = toUser(e.clientX, e.clientY);
      setView((v) => ({
        ...v,
        x: dragStart.current!.vx + (u.x - dragStart.current!.x),
        y: dragStart.current!.vy + (u.y - dragStart.current!.y),
      }));
    },
    [toUser],
  );

  const onPointerUp = useCallback(() => {
    dragStart.current = null;
    setDragging(false);
  }, []);

  const flyTo = useCallback(
    (id: string, k = 2.1) => {
      const p = positions[id];
      if (!p) return;
      if (animRef.current) cancelAnimationFrame(animRef.current);
      const from = { ...view };
      const to = { x: -p.x * k, y: -p.y * k, k };
      const t0 = performance.now();
      const dur = 720;
      const step = (now: number) => {
        const t = Math.min(1, (now - t0) / dur);
        const e = 1 - Math.pow(1 - t, 3);
        setView({
          x: from.x + (to.x - from.x) * e,
          y: from.y + (to.y - from.y) * e,
          k: from.k + (to.k - from.k) * e,
        });
        if (t < 1) animRef.current = requestAnimationFrame(step);
      };
      animRef.current = requestAnimationFrame(step);
    },
    [positions, view],
  );

  useEffect(() => {
    return () => {
      if (animRef.current) cancelAnimationFrame(animRef.current);
    };
  }, []);

  /* ---- a jump: the most distant object you have not seen ---- */
  const jump = useCallback(() => {
    const anchor = focused ?? genome.visited[genome.visited.length - 1] ?? NODES[0].id;
    const seen = new Set(genome.visited);
    const candidates = NODES.filter((n) => !seen.has(n.id));
    const pool = candidates.length ? candidates : NODES;
    let best = pool[0];
    let bestD = -1;
    for (const c of pool) {
      const d = Math.hypot(positions[c.id].x - positions[anchor].x, positions[c.id].y - positions[anchor].y);
      if (d > bestD) {
        bestD = d;
        best = c;
      }
    }
    flyTo(best.id, 2.4);
    note('pan');
  }, [focused, genome.visited, positions, flyTo, note]);

  const focusNode = focused ? NODE_BY_ID[focused] : null;

  const edgeHighlight = (from: string, to: string) =>
    hovered && (from === hovered || to === hovered) ? 'true' : 'false';

  return (
    <div
      className="constellation"
      data-drag={dragging}
      onWheel={onWheel}
      onPointerDown={onPointerDown}
      onPointerMove={onPointerMove}
      onPointerUp={onPointerUp}
      onPointerLeave={onPointerUp}
    >
      <svg
        ref={svgRef}
        className="constellation__svg"
        viewBox={`${-VIEW} ${-VIEW} ${VIEW * 2} ${VIEW * 2}`}
        preserveAspectRatio="xMidYMid meet"
      >
        <g transform={`translate(${view.x} ${view.y}) scale(${view.k})`}>
          {FAMILY_ORDER.map((f) => {
            const members = NODES.filter((n) => n.family === f);
            if (!members.length) return null;
            const cx = members.reduce((a, m) => a + positions[m.id].x, 0) / members.length;
            const cy = members.reduce((a, m) => a + positions[m.id].y, 0) / members.length;
            const spread = Math.max(
              ...members.map((m) => Math.hypot(positions[m.id].x - cx, positions[m.id].y - cy)),
            );
            return (
              <text
                key={f}
                className="cfamily-label"
                x={cx}
                y={cy - spread - 34}
                textAnchor="middle"
              >
                {FAMILIES[f].label}
              </text>
            );
          })}

          {EDGES.map((e, i) => {
            const a = positions[e.from];
            const b = positions[e.to];
            if (!a || !b) return null;
            const hidden = visible && !(visible.has(e.from) && visible.has(e.to));
            if (hidden) return null;
            const mx = (a.x + b.x) / 2;
            const my = (a.y + b.y) / 2;
            const nx = -(b.y - a.y) * 0.08;
            const ny = (b.x - a.x) * 0.08;
            return (
              <path
                key={i}
                className="cedge"
                data-hi={edgeHighlight(e.from, e.to)}
                d={`M ${a.x} ${a.y} Q ${mx + nx} ${my + ny} ${b.x} ${b.y}`}
                opacity={hovered ? 0.25 : 0.7}
              />
            );
          })}

          {NODES.map((n) => {
            const p = positions[n.id];
            if (!p) return null;
            const hidden = visible && !visible.has(n.id);
            if (hidden) return null;
            const isActive = n.id === focused;
            const isNeighbour = neighbours.has(n.id);
            const r = 4.2 + n.weight * 6.2;
            const dim = hovered && !isNeighbour && hovered !== n.id;
            return (
              <g
                key={n.id}
                className="cnode"
                transform={`translate(${p.x} ${p.y})`}
                opacity={dim ? 0.28 : 1}
                onMouseEnter={() => setHovered(n.id)}
                onMouseLeave={() => setHovered((h) => (h === n.id ? null : h))}
                onClick={(e) => {
                  e.stopPropagation();
                  navigate(n.id);
                  note('edge');
                }}
                onDoubleClick={(e) => {
                  e.stopPropagation();
                  flyTo(n.id, 2.6);
                }}
              >
                <circle className="cnode__halo" r={r * 4.2} />
                {n.weight > 0.85 && (
                  <circle
                    className="cnode__glow"
                    r={r * 2.6}
                    style={{ color: familyColor(n.family) }}
                  />
                )}
                <circle
                  className="cnode__dot"
                  r={r}
                  stroke={familyColor(n.family)}
                  data-active={isActive}
                  data-visited={genome.visited.includes(n.id)}
                  fill={isActive ? familyColor(n.family) : undefined}
                />
                <text
                  className="cnode__label"
                  y={r + 12}
                  textAnchor="middle"
                  data-active={isActive}
                  style={{ fontSize: 11 }}
                >
                  {n.title}
                </text>
              </g>
            );
          })}
        </g>
      </svg>

      <div className="maptools">
        <button className="btn btn--sm" onClick={() => setView({ x: 0, y: 0, k: 1 })}>
          reset view
        </button>
        <button className="btn btn--sm" onClick={jump}>
          jump ✦
        </button>
        <button
          className="btn btn--sm"
          data-on={isolate}
          onClick={() => setIsolate((v) => !v)}
          style={isolate ? { borderColor: 'var(--accent)', color: 'var(--accent)' } : undefined}
        >
          {isolate ? 'isolate on' : 'isolate'}
        </button>
        <button className="btn btn--sm" onClick={() => setView((v) => ({ ...v, k: Math.min(4.5, v.k * 1.25) }))}>
          +
        </button>
        <button className="btn btn--sm" onClick={() => setView((v) => ({ ...v, k: Math.max(0.35, v.k * 0.8) }))}>
          −
        </button>
      </div>

      <div className="legend">
        {FAMILY_ORDER.map((f) => (
          <div className="legend__row" key={f}>
            <span className="dot" style={{ background: familyColor(f) }} />
            {FAMILIES[f].label}
          </div>
        ))}
        <div className="legend__row" style={{ marginTop: 4, opacity: 0.7 }}>
          {signals.path.length} visited · {NODES.length} objects
        </div>
      </div>

      {focusNode && (
        <aside className="dossier">
          <div className="dossier__head">
            <div className="codex__cat" style={{ marginBottom: 6 }}>
              <span className="dot" style={{ background: familyColor(focusNode.family) }} />
              <span className="eyebrow">{focusNode.catalog}</span>
            </div>
            <h2 className="dossier__title">{focusNode.title}</h2>
            <p className="dossier__summary">{focusNode.summary}</p>
            <div style={{ display: 'flex', gap: 6, flexWrap: 'wrap' }}>
              {focusNode.tags.map((t) => (
                <span className="tag" key={t}>
                  {t}
                </span>
              ))}
            </div>
          </div>
          <div className="dossier__body">
            <div className="prose" style={{ fontSize: '0.97rem' }}>
              {focusNode.body.slice(0, 2).map((p, i) => (
                <p key={i}>{p}</p>
              ))}
            </div>
            <div className="readings" style={{ margin: '1.4em 0' }}>
              {focusNode.readings.slice(0, 3).map((r) => (
                <div className="reading" key={r.label}>
                  <div className="reading__k">{r.label}</div>
                  <div className="reading__v">{r.value}</div>
                </div>
              ))}
            </div>
            <div className="eyebrow" style={{ marginBottom: 4 }}>
              relations
            </div>
            {related(focusNode.id)
              .slice(0, 6)
              .map((r) => {
                const other = NODE_BY_ID[r.id];
                if (!other) return null;
                return (
                  <button
                    key={r.id}
                    className="relation"
                    onClick={() => navigate(r.id)}
                  >
                    <span className="relation__t">{other.title}</span>
                    <span className="relation__k">{r.kind.replace(/-/g, ' ')}</span>
                  </button>
                );
              })}
          </div>
        </aside>
      )}
    </div>
  );
}
