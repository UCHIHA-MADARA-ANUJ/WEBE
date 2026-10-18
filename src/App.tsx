import { useCallback, useEffect, useState } from 'react';
import { Backdrop } from './components/Backdrop';
import { Chrome } from './components/Chrome';
import { MindPanel } from './components/MindPanel';
import { Reconfigure } from './components/Reconfigure';
import { StatusBar } from './components/StatusBar';
import { EngineProvider, useEngine } from './engine/store';
import { CodexMode } from './modes/Codex';
import { ConstellationMode } from './modes/Constellation';
import { ConsoleMode } from './modes/Console';
import { LatticeMode } from './modes/Lattice';
import { MosaicMode } from './modes/Mosaic';
import { ZenMode } from './modes/Zen';

function ColdOpen({ onBegin }: { onBegin: (id: string) => void }) {
  const { genome } = useEngine();
  return (
    <div className="coldcard">
      <h1>
        This website has
        <br />
        no fixed interface.
      </h1>
      <p>
        DEEP FIELD is a living atlas of the cosmos. It watches how you move — where you
        jump, how fast you scroll, what you linger on — then rebuilds its own layout,
        hierarchy and vocabulary around that behaviour. Two visitors will not see the
        same site.
      </p>
      <div className="coldcard__hint">
        <span>
          <b>generation {genome.generation}</b>
        </span>
        <span>click any object to begin</span>
        <span>the mind panel shows the read</span>
      </div>
      <div style={{ marginTop: '26px' }}>
        <button
          className="btn btn--accent"
          onClick={() => onBegin('cmb')}
        >
          begin at the beginning →
        </button>
      </div>
    </div>
  );
}

function Shell() {
  const { paradigm, noteScroll, notePointer, cold, genome, openNode } = useEngine();
  const [focus, setFocus] = useState<string | null>(null);
  const [mind, setMind] = useState(false);

  /* every activation of an object is both a view change and an observation */
  const handleNavigate = useCallback(
    (id: string) => {
      openNode(id);
      setFocus(id);
    },
    [openNode],
  );

  /* global scroll telemetry */
  useEffect(() => {
    let lastY = window.scrollY;
    let acc = 0;
    let accT = performance.now();
    const onScroll = () => {
      const y = window.scrollY;
      const now = performance.now();
      acc += Math.abs(y - lastY);
      lastY = y;
      if (now - accT > 130) {
        const dt = now - accT;
        noteScroll(acc, (acc / dt) * 1000, dt);
        acc = 0;
        accT = now;
      }
    };
    window.addEventListener('scroll', onScroll, { passive: true });
    return () => window.removeEventListener('scroll', onScroll);
  }, [noteScroll]);

  /* pointer telemetry — a paradigm that does not scroll still has motion */
  useEffect(() => {
    let lastX = 0;
    let lastY = 0;
    let lastT = performance.now();
    let started = false;

    const onMove = (e: PointerEvent) => {
      const now = performance.now();
      if (!started) {
        lastX = e.clientX;
        lastY = e.clientY;
        lastT = now;
        started = true;
        return;
      }
      const dx = e.clientX - lastX;
      const dy = e.clientY - lastY;
      const dist = Math.hypot(dx, dy);
      const dt = now - lastT;
      if (dist > 0.5 && dt > 0) notePointer(dist, dt);
      lastX = e.clientX;
      lastY = e.clientY;
      lastT = now;
    };

    window.addEventListener('pointermove', onMove, { passive: true });
    return () => window.removeEventListener('pointermove', onMove);
  }, [notePointer]);

  const props = { focus, navigate: handleNavigate, openMind: () => setMind(true) };

  return (
    <div className="app" data-paradigm={paradigm} data-mind={mind}>
      <Backdrop seed={genome.seed} />
      <Chrome onMind={() => setMind((v) => !v)} onNavigate={handleNavigate} />
      <main className="stage">
        <div className="paradigm-stage" key={paradigm}>
          {paradigm === 'codex' && <CodexMode {...props} />}
          {paradigm === 'constellation' && <ConstellationMode {...props} />}
          {paradigm === 'mosaic' && <MosaicMode {...props} />}
          {paradigm === 'lattice' && <LatticeMode {...props} />}
          {paradigm === 'console' && <ConsoleMode {...props} />}
          {paradigm === 'zen' && <ZenMode {...props} />}
        </div>
        {cold && paradigm === 'constellation' && <ColdOpen onBegin={handleNavigate} />}
      </main>
      <StatusBar />
      <MindPanel open={mind} onClose={() => setMind(false)} />
      <Reconfigure />
    </div>
  );
}

export default function App() {
  return (
    <EngineProvider>
      <Shell />
    </EngineProvider>
  );
}
