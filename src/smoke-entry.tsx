/**
 * Headless harness entry point (not part of the shipped bundle).
 * Mounts the real App inside jsdom and exposes a small driver API.
 */
import { createRoot } from 'react-dom/client';
import App from './App';
import { testBus } from './engine/store';
import { NODES, NODE_BY_ID, neighboursOf } from './content/graph';

declare global {
  interface Window {
    __DF_TEST__?: boolean;
    DeepField?: unknown;
  }
}

window.__DF_TEST__ = true;

function api() {
  const a = testBus.api;
  if (!a) throw new Error('engine not mounted');
  return a;
}

const DeepField = {
  mount(el: HTMLElement) {
    createRoot(el).render(<App />);
  },
  snapshot() {
    const a = api();
    const s = a.signals;
    const f = a.classification.features;
    return {
      generation: a.genome.generation,
      visits: a.genome.visits,
      seed: a.genome.seed,
      paradigm: a.paradigm,
      top: a.classification.top,
      confidence: a.classification.confidence,
      opens: s.opens,
      steps: s.steps,
      jumps: s.jumps,
      fastScrolls: s.fastScrolls,
      scan: f.scan,
      dwell: f.dwell,
      volume: f.volume,
      queryActions: f.query,
      trail: a.features.trail,
      visited: a.genome.visited.length,
    };
  },
  pickNode(seed = 0) {
    return NODES[Math.abs(seed) % NODES.length].id;
  },
  relatedOf(id: string) {
    return neighboursOf(id);
  },
  title(id: string) {
    return NODE_BY_ID[id]?.title ?? id;
  },
  async simulate(kind: string, payload: Record<string, unknown> = {}) {
    const a = api();
    switch (kind) {
      case 'open':
        a.openNode(payload.id as string);
        break;
      case 'scroll':
        a.noteScroll(
          (payload.pixels as number) ?? 800,
          (payload.velocity as number) ?? 400,
          (payload.dt as number) ?? 100,
        );
        break;
      case 'filter':
        a.noteFilter((payload.tag as string) ?? 'x');
        break;
      case 'search':
        a.noteSearch((payload.q as string) ?? 'x');
        break;
      case 'command':
        a.noteCommand((payload.cmd as string) ?? 'help');
        window.dispatchEvent(
          new CustomEvent('df:command', { detail: (payload.cmd as string) ?? 'help' }),
        );
        break;
      case 'mutate':
        a.mutate();
        break;
      case 'forceParadigm':
        a.setParadigm(payload.paradigm as never, true);
        break;
      default:
        break;
    }
    await new Promise((r) => setTimeout(r, 0));
  },
};

window.DeepField = DeepField;
export default DeepField;
