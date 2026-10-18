import { useEffect, useMemo, useRef, useState } from 'react';
import { NODE_BY_ID, NODES, TAGS } from '../content/graph';
import { useEngine } from '../engine/store';
import { PARADIGM_ORDER, PARADIGMS } from '../engine/types';
import type { ModeProps } from './types';

interface Line {
  cls: 'sys' | 'ok' | 'hi' | 'err' | 'head';
  text: string;
}

/**
 * CONSOLE — verbs, not buttons.
 *
 * Contract: no chrome at all, just a prompt. The valid command set changes
 * as the engine learns what you are trying to do, and the site answers in
 * prose as well as structure.
 */
export function ConsoleMode({ focus, navigate, openMind }: ModeProps) {
  const {
    genome,
    classification,
    features,
    trail,
    signals,
    setParadigm,
    mutate,
    reset,
    noteSearch,
    noteFilter,
  } = useEngine();

  const [lines, setLines] = useState<Line[]>([]);
  const [input, setInput] = useState('');
  const [history, setHistory] = useState<string[]>([]);
  const [hIdx, setHIdx] = useState(-1);
  const inputRef = useRef<HTMLInputElement | null>(null);
  const outRef = useRef<HTMLDivElement | null>(null);
  const bootedRef = useRef(false);

  const emit = (cls: Line['cls'], text: string) =>
    setLines((prev) => [...prev, { cls, text }].slice(-300));

  const emitAll = (items: Line[]) => setLines((prev) => [...prev, ...items].slice(-300));

  const commands = useMemo(() => {
    const list: { name: string; desc: string; locked?: boolean }[] = [
      { name: 'help', desc: 'list the verbs currently available' },
      { name: 'list', desc: 'every object in the corpus' },
      { name: 'open <id>', desc: 'open an object by number or slug' },
      { name: 'go <n>', desc: 'jump to a stop on your trail' },
      { name: 'trail', desc: 'your personalised route' },
      { name: 'find <text>', desc: 'search the corpus' },
      { name: 'tag <name>', desc: 'list objects carrying a tag' },
      { name: 'relations', desc: 'relations of the current object' },
      { name: 'stats', desc: 'how the engine currently reads you' },
      { name: 'mind', desc: 'open the mind panel' },
      { name: 'layout <name>', desc: 'restructure the interface' },
      { name: 'gen', desc: 'generation and unlocked behaviour' },
      { name: 'mutate', desc: 'force the next generation' },
      { name: 'about', desc: 'what this thing is' },
      { name: 'clear', desc: 'clear the buffer' },
    ];
    if (features.trail) list.splice(5, 0, { name: 'chapters', desc: 'a syllabus drawn from your trail' });
    if (features.compare)
      list.splice(6, 0, { name: 'compare <a> <b>', desc: 'put two objects side by side' });
    return list;
  }, [features]);

  useEffect(() => {
    if (bootedRef.current) return;
    bootedRef.current = true;
    emitAll([
      { cls: 'head', text: 'DEEP FIELD · live atlas of the cosmos' },
      {
        cls: 'sys',
        text: `generation ${genome.generation} · ${genome.visits} visit${genome.visits === 1 ? '' : 's'} · read as ${classification.top} (${Math.round(classification.confidence * 100)}%)`,
      },
      { cls: 'sys', text: 'the site has no fixed shape. it is listening for how you move.' },
      { cls: 'sys', text: "type 'help' for the verbs that exist right now." },
      { cls: 'sys', text: '' },
    ]);
    // eslint-disable-next-line react-hooks/exhaustive-deps
  }, []);

  useEffect(() => {
    const el = outRef.current;
    if (el) el.scrollTop = el.scrollHeight;
  }, [lines]);

  useEffect(() => {
    inputRef.current?.focus();
  }, []);

  const resolve = (token: string): FieldNodeLike | null => {
    const t = token.trim().toLowerCase();
    if (!t) return null;
    const n = parseInt(t, 10);
    if (!Number.isNaN(n)) return NODES[n - 1] ?? null;
    const slug = t.replace(/[^a-z0-9]+/g, '-');
    return (
      NODES.find((x) => x.id === slug) ??
      NODES.find((x) => x.title.toLowerCase() === t) ??
      NODES.find((x) => x.title.toLowerCase().includes(t)) ??
      null
    );
  };

  const run = (raw: string) => {
    const line = raw.trim();
    emit('hi', `❯ ${line}`);
    if (!line) return;
    setHistory((h) => [line, ...h].slice(0, 40));

    const [cmd, ...args] = line.split(/\s+/);
    const arg = args.join(' ');

    switch (cmd.toLowerCase()) {
      case 'help': {
        emit('head', 'available verbs');
        for (const c of commands) emit('sys', `  ${c.name.padEnd(18)}${c.desc}`);
        emit('sys', '');
        break;
      }
      case 'list': {
        emit('head', 'corpus');
        NODES.forEach((n, i) => {
          emit('sys', `  ${String(i + 1).padStart(2, '0')}  ${n.title.padEnd(30)} ${n.family}`);
        });
        break;
      }
      case 'open': {
        const n = resolve(arg);
        if (!n) {
          emit('err', `no object matches "${arg}"`);
          break;
        }
        navigate(n.id);
        emit('ok', `▸ ${n.title}`);
        emit('sys', `  ${n.summary}`);
        emit('sys', '');
        emit('sys', n.body[0]);
        break;
      }
      case 'go': {
        const n = parseInt(arg, 10);
        const id = trail[n - 1];
        if (!id) {
          emit('err', `trail has ${trail.length} stops`);
          break;
        }
        const node = NODE_BY_ID[id];
        navigate(id);
        emit('ok', `▸ stop ${n} — ${node?.title}`);
        break;
      }
      case 'trail': {
        emit('head', 'your route');
        trail.forEach((id, i) => {
          const n = NODE_BY_ID[id];
          emit('sys', `  ${String(i + 1).padStart(2, '0')}  ${n?.title ?? id}`);
        });
        break;
      }
      case 'chapters': {
        if (!features.chapters) {
          emit('err', 'chapters unlock at generation 4 — try "mutate"');
          break;
        }
        emit('head', 'syllabus');
        trail.forEach((id, i) => {
          const n = NODE_BY_ID[id];
          emit('sys', `  ${String(i + 1).padStart(2, '0')}  ${n?.family ?? ''} · ${n?.title ?? id}`);
        });
        break;
      }
      case 'find': {
        if (!arg) {
          emit('err', 'find what?');
          break;
        }
        noteSearch(arg);
        const q = arg.toLowerCase();
        const hits = NODES.filter(
          (n) =>
            n.title.toLowerCase().includes(q) ||
            n.summary.toLowerCase().includes(q) ||
            n.body.some((b) => b.toLowerCase().includes(q)),
        );
        emit('head', `${hits.length} match${hits.length === 1 ? '' : 'es'}`);
        hits.forEach((n) => emit('sys', `  ${n.title}`));
        break;
      }
      case 'tag': {
        if (!arg) {
          emit('head', 'tags in the corpus');
          TAGS.forEach((t) => emit('sys', `  ${t}`));
          break;
        }
        noteFilter(arg);
        const hits = NODES.filter((n) => n.tags.includes(arg.toLowerCase()));
        emit('head', `${hits.length} object${hits.length === 1 ? '' : 's'} tagged "${arg}"`);
        hits.forEach((n) => emit('sys', `  ${n.title}`));
        break;
      }
      case 'relations': {
        const id = focus ?? signals.path[signals.path.length - 1];
        const n = id ? NODE_BY_ID[id] : null;
        if (!n) {
          emit('err', 'nothing is open yet');
          break;
        }
        emit('head', `relations of ${n.title}`);
        n.body.slice(0, 1).forEach((b) => emit('sys', b));
        break;
      }
      case 'compare': {
        if (!features.compare) {
          emit('err', 'compare unlocks at generation 3 — try "mutate"');
          break;
        }
        const a = resolve(args[0] ?? '');
        const b = resolve(args[1] ?? '');
        if (!a || !b) {
          emit('err', 'usage: compare <a> <b>');
          break;
        }
        const shared = a.tags.filter((t) => b.tags.includes(t));
        emit('head', `${a.title}  vs  ${b.title}`);
        emit('sys', `  shared tags: ${shared.join(', ') || 'none'}`);
        emit('sys', `  ${a.summary}`);
        emit('sys', `  ${b.summary}`);
        break;
      }
      case 'stats': {
        emit('head', 'engine read');
        Object.entries(classification.scores)
          .sort((x, y) => y[1] - x[1])
          .forEach(([k, v]) =>
            emit('sys', `  ${k.padEnd(15)}${'█'.repeat(Math.round(v * 24)).padEnd(24)} ${Math.round(v * 100)}%`),
          );
        emit('sys', '');
        classification.reasons.forEach((r) => emit('sys', `  · ${r}`));
        break;
      }
      case 'mind': {
        emit('sys', 'opening the mind panel');
        openMind();
        break;
      }
      case 'layout': {
        const target = arg.toLowerCase();
        const p = PARADIGM_ORDER.find((x) => x === target || PARADIGMS[x].name.toLowerCase() === target);
        if (!p) {
          emit('err', `unknown structure. try: ${PARADIGM_ORDER.join(', ')}`);
          break;
        }
        setParadigm(p, true);
        emit('ok', `▸ restructured into ${PARADIGMS[p].name}`);
        break;
      }
      case 'gen': {
        emit('head', 'procedural state');
        emit('sys', `  generation   ${genome.generation}`);
        emit('sys', `  visits      ${genome.visits}`);
        emit('sys', `  unlocked    ${Object.entries(features).filter(([, v]) => v).map(([k]) => k).join(', ') || 'none'}`);
        emit('sys', `  objects seen ${new Set(genome.visited).size}`);
        break;
      }
      case 'mutate': {
        mutate();
        emit('ok', '▸ structure mutated — a new generation is unfolding');
        break;
      }
      case 'reset': {
        reset();
        emit('sys', 'memory erased. the site forgets you.');
        break;
      }
      case 'about': {
        emit('head', 'about');
        emit('sys', 'DEEP FIELD is a website with no fixed interface.');
        emit('sys', 'it observes how you move and rebuilds its own layout, hierarchy');
        emit('sys', 'and vocabulary around that behaviour. nothing is sent anywhere —');
        emit('sys', 'the model of you lives in this browser only.');
        break;
      }
      case 'clear': {
        setLines([]);
        break;
      }
      case 'ls':
      case 'dir': {
        emit('sys', 'no such directory. try "list".');
        break;
      }
      default: {
        emit('err', `unknown verb "${cmd}" — type "help"`);
      }
    }
  };

  /* external drivers (other paradigms, the harness) can speak to the console */
  const runRef = useRef(run);
  runRef.current = run;
  useEffect(() => {
    const onCmd = (e: Event) => {
      const detail = (e as CustomEvent<string>).detail;
      if (detail) runRef.current(detail);
    };
    window.addEventListener('df:command', onCmd);
    return () => window.removeEventListener('df:command', onCmd);
  }, []);

  const onKeyDown = (e: React.KeyboardEvent<HTMLInputElement>) => {
    if (e.key === 'Enter') {
      const v = input;
      setInput('');
      run(v);
    } else if (e.key === 'ArrowUp') {
      e.preventDefault();
      const idx = Math.min(history.length - 1, hIdx + 1);
      if (idx >= 0 && history[idx]) {
        setHIdx(idx);
        setInput(history[idx]);
      }
    } else if (e.key === 'ArrowDown') {
      e.preventDefault();
      const idx = hIdx - 1;
      setHIdx(idx);
      setInput(idx >= 0 ? history[idx] ?? '' : '');
    }
  };

  return (
    <div className="console" onClick={() => inputRef.current?.focus()}>
      <div className="console__out" ref={outRef}>
        {lines.map((l, i) => (
          <div className={`cline cline--${l.cls}`} key={i}>
            {l.text || '\u00a0'}
          </div>
        ))}
      </div>

      <div className="console__cmds">
        {commands.slice(0, 6).map((c) => (
          <button
            key={c.name}
            className="chip"
            onClick={() => {
              setInput(c.name.split(' ')[0] + ' ');
              inputRef.current?.focus();
            }}
          >
            {c.name}
          </button>
        ))}
      </div>

      <div className="console__prompt">
        <span className="console__caret">❯</span>
        <input
          ref={inputRef}
          className="console__input"
          value={input}
          placeholder="say something…"
          onChange={(e) => setInput(e.target.value)}
          onKeyDown={onKeyDown}
          autoComplete="off"
          spellCheck={false}
        />
        <span className="mono" style={{ fontSize: '0.6rem', color: 'var(--ink-faint)' }}>
          {commands.length} verbs · gen {genome.generation}
        </span>
      </div>
    </div>
  );
}

type FieldNodeLike = (typeof NODES)[number];
