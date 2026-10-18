'use client';

import { useCallback, useEffect, useState } from 'react';
import { motion, AnimatePresence } from 'motion/react';
import { Chrome } from '@/components/Chrome';
import { MindPanel } from '@/components/MindPanel';
import { Reconfigure } from '@/components/Reconfigure';
import { StatusBar } from '@/components/StatusBar';
import { StrataBackdrop } from '@/components/identity/StrataBackdrop';
import { LenisProvider } from '@/components/motion/LenisProvider';
import { useEngine, EngineProvider } from '@/engine/store';
import { CodexMode } from '@/modes/Codex';
import { ConstellationMode } from '@/modes/Constellation';
import { ConsoleMode } from '@/modes/Console';
import { LatticeMode } from '@/modes/Lattice';
import { MosaicMode } from '@/modes/Mosaic';
import { ZenMode } from '@/modes/Zen';
import { ENTITY_BY_ID } from '@/content/graph';

const ALTERNATIVES = [
  { id: 'alt-lean', label: 'Lean Launch', desc: 'Ship day 3, learn in public. Fastest feedback, highest noise.', color: '#DC2626' },
  { id: 'alt-community', label: 'Community-First', desc: '30 people, week 1. Then expand. Trust before scale.', color: '#1E40AF' },
  { id: 'alt-stealth', label: 'Stealth Premium', desc: '10 partners at premium. Prove willingness to pay.', color: '#065F46' },
];

function ColdOpen({ onBegin }: { onBegin: (id: string) => void }) {
  return (
    <div className="coldcard">
      <div className="coldcard__eyebrow">
        <span className="coldcard__live">● LIVE</span> This workspace has no fixed shape
      </div>
      <h1>
        How do we launch<br/>in <em>14 days?</em>
      </h1>
      <p className="coldcard__sub">
        A real decision, with evidence on both sides. Pick a path — watch the workspace rebuild itself around how you work.
      </p>

      <div className="coldcard__cards">
        {ALTERNATIVES.map(a => (
          <button key={a.id} className="coldcard__card" onClick={() => onBegin(a.id)} style={{ ['--c' as string]: a.color }}>
            <span className="coldcard__card-dot" style={{ background: a.color }} />
            <span className="coldcard__card-label">{a.label}</span>
            <span className="coldcard__card-desc">{a.desc}</span>
            <span className="coldcard__card-cta">Open →</span>
          </button>
        ))}
      </div>

      <div className="coldcard__foot">
        <span>Or start at the question →</span>
        <button className="coldcard__textbtn" onClick={() => onBegin('q-launch')}>How do we launch in 14 days?</button>
        <span className="coldcard__hint">The Mind panel shows why it changes. Try two different paths — get two different workspaces.</span>
      </div>
    </div>
  );
}

function Shell() {
  const { paradigm, noteScroll, notePointer, cold, genome, openNode } = useEngine();
  const [focus, setFocus] = useState<string | null>(null);
  const [mind, setMind] = useState(false);

  const handleNavigate = useCallback((id: string) => {
    openNode(id);
    setFocus(id);
  }, [openNode]);

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

  useEffect(() => {
    let lastX = 0, lastY = 0, lastT = performance.now(), started = false;
    const onMove = (e: PointerEvent) => {
      const now = performance.now();
      if (!started) { lastX = e.clientX; lastY = e.clientY; lastT = now; started = true; return; }
      const dx = e.clientX - lastX, dy = e.clientY - lastY;
      const dist = Math.hypot(dx, dy), dt = now - lastT;
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
