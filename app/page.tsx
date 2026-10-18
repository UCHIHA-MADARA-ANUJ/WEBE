'use client';

import { useCallback, useEffect, useState } from 'react';
import { motion, AnimatePresence } from 'motion/react';
import { Chrome } from '@/components/Chrome';
import { MindPanel } from '@/components/MindPanel';
import { Reconfigure } from '@/components/Reconfigure';
import { StatusBar } from '@/components/StatusBar';
import { StrataBackdrop } from '@/components/identity/StrataBackdrop';
import { StrataMark } from '@/components/identity/StrataMark';
import { LenisProvider } from '@/components/motion/LenisProvider';
import { useEngine, EngineProvider } from '@/engine/store';
import { CodexMode } from '@/modes/Codex';
import { ConstellationMode } from '@/modes/Constellation';
import { ConsoleMode } from '@/modes/Console';
import { LatticeMode } from '@/modes/Lattice';
import { MosaicMode } from '@/modes/Mosaic';
import { ZenMode } from '@/modes/Zen';

function ColdOpen({ onBegin }: { onBegin: (id: string) => void }) {
  const { genome } = useEngine();
  return (
    <div className="coldcard">
      <div className="coldcard__mark">
        <StrataMark size={42} />
      </div>
      <h1>
        This workspace has
        <br />
        no fixed shape.
      </h1>
      <p>
        STRATA is a decision workspace that watches how you work — what you open,
        how you compare, whether you follow dependencies or jump — then restructures
        its own navigation, hierarchy and workflows around that behaviour. Two people
        working on the same project will not see the same interface.
      </p>
      <div className="coldcard__hint">
        <span><b>generation {genome.generation}</b></span>
        <span>click any entity to begin</span>
        <span>the mind panel shows the read</span>
      </div>
      <div style={{ marginTop: 26, display: 'flex', gap: 10, justifyContent: 'center' }}>
        <button className="btn btn--accent" onClick={() => onBegin('q-launch')}>
          begin with the question →
        </button>
        <button className="btn" onClick={() => onBegin('alt-lean')}>
          jump to alternatives →
        </button>
      </div>
    </div>
  );
}

function Shell() {
  const { paradigm, noteScroll, notePointer, cold, genome, openNode } = useEngine();
  const [focus, setFocus] = useState<string | null>(null);
  const [mind, setMind] = useState(false);

  const handleNavigate = useCallback(
    (id: string) => {
      openNode(id);
      setFocus(id);
    },
    [openNode],
  );

  // global scroll telemetry
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

  // pointer telemetry
  useEffect(() => {
    let lastX = 0;
    let lastY = 0;
    let lastT = performance.now();
    let started = false;
    const onMove = (e: PointerEvent) => {
      const now = performance.now();
      if (!started) {
        lastX = e.clientX; lastY = e.clientY; lastT = now; started = true; return;
      }
      const dx = e.clientX - lastX;
      const dy = e.clientY - lastY;
      const dist = Math.hypot(dx, dy);
      const dt = now - lastT;
      if (dist > 0.5 && dt > 0) notePointer(dist, dt);
      lastX = e.clientX; lastY = e.clientY; lastT = now;
    };
    window.addEventListener('pointermove', onMove, { passive: true });
    return () => window.removeEventListener('pointermove', onMove);
  }, [notePointer]);

  const props = { focus, navigate: handleNavigate, openMind: () => setMind(true) };

  return (
    <div className="app" data-paradigm={paradigm} data-mind={mind}>
      <StrataBackdrop seed={genome.seed} />
      <Chrome onMind={() => setMind(v => !v)} onNavigate={handleNavigate} />
      <main className="stage">
        <AnimatePresence mode="wait">
          <motion.div
            key={paradigm}
            className="paradigm-stage"
            initial={{ opacity: 0, y: 8 }}
            animate={{ opacity: 1, y: 0 }}
            exit={{ opacity: 0, y: -8 }}
            transition={{ duration: 0.32, ease: [0.22, 0.61, 0.36, 1] }}
            layout
          >
            {paradigm === 'codex' && <CodexMode {...props} />}
            {paradigm === 'constellation' && <ConstellationMode {...props} />}
            {paradigm === 'mosaic' && <MosaicMode {...props} />}
            {paradigm === 'lattice' && <LatticeMode {...props} />}
            {paradigm === 'console' && <ConsoleMode {...props} />}
            {paradigm === 'zen' && <ZenMode {...props} />}
          </motion.div>
        </AnimatePresence>
        {cold && paradigm === 'constellation' && <ColdOpen onBegin={handleNavigate} />}
      </main>
      <StatusBar />
      <MindPanel open={mind} onClose={() => setMind(false)} />
      <Reconfigure />
    </div>
  );
}

export default function Page() {
  return (
    <LenisProvider>
      <EngineProvider>
        <Shell />
      </EngineProvider>
    </LenisProvider>
  );
}
