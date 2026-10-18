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

// ── Human-first premium Cold Open ──────────────────────────────────────
function ColdOpen({ onBegin }: { onBegin: (id: string) => void }) {
  return (
    <div className="cold">
      {/* soft backdrop already via StrataBackdrop; this is layout */}
      <div className="cold__left">
        <div className="cold__kicker">
          <span className="cold__dot" /> STRATA · Decision workspace
        </div>
        <h1 className="cold__h">
          How do we
          <br />
          <em>launch</em> in
          <br />
          14 days?
        </h1>
        <p className="cold__p">
          You have 200 warm contacts, a working product, and two weeks.
          Pick a path — STRATA reshapes around how you work.
        </p>
        <div className="cold__meta">
          <span>3 paths · 33 pieces of work</span>
          <span className="cold__sep">·</span>
          <span>no setup · just start</span>
        </div>
      </div>

      <div className="cold__right">
        <button className="pathcard" onClick={() => onBegin('alt-lean')} style={{ ['--acc' as string]: '#DC2626' }}>
          <div className="pathcard__top">
            <span className="pathcard__eyebrow">Path A — Fast</span>
            <span className="pathcard__arrow">→</span>
          </div>
          <div className="pathcard__title">Lean Launch</div>
          <div className="pathcard__desc">Ship publicly on day 3. Learn in the open. Daily iterations. Maximum speed.</div>
          <div className="pathcard__stats">
            <span><b>Day 3</b> public</span>
            <span><b>High</b> tempo</span>
            <span><b>Open</b> link</span>
          </div>
        </button>

        <button className="pathcard" onClick={() => onBegin('alt-community')} style={{ ['--acc' as string]: '#1E40AF' }}>
          <div className="pathcard__top">
            <span className="pathcard__eyebrow">Path B — Warm</span>
            <span className="pathcard__arrow">→</span>
          </div>
          <div className="pathcard__title">Community-First</div>
          <div className="pathcard__desc">Seed 30 hand-picked users. Tight feedback loop. Expand in waves.</div>
          <div className="pathcard__stats">
            <span><b>30</b> invites</span>
            <span><b>Day 10</b> public</span>
            <span><b>Medium</b> load</span>
          </div>
        </button>

        <button className="pathcard" onClick={() => onBegin('alt-stealth')} style={{ ['--acc' as string]: '#065F46' }}>
          <div className="pathcard__top">
            <span className="pathcard__eyebrow">Path C — Precise</span>
            <span className="pathcard__arrow">→</span>
          </div>
          <div className="pathcard__title">Stealth Premium</div>
          <div className="pathcard__desc">10 design partners at premium. Prove willingness to pay before you scale.</div>
          <div className="pathcard__stats">
            <span><b>10</b> partners</span>
            <span><b>Paid</b> trial</span>
            <span><b>Low</b> load</span>
          </div>
        </button>

        <button className="cold__ghost" onClick={() => onBegin('q-launch')}>
          Or start from the core question →
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
      const dx = e.clientX - lastX; const dy = e.clientY - lastY;
      const dist = Math.hypot(dx, dy); const dt = now - lastT;
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
            initial={{ opacity: 0, y: 10 }}
            animate={{ opacity: 1, y: 0 }}
            exit={{ opacity: 0, y: -10 }}
            transition={{ duration: 0.36, ease: [0.22, 0.61, 0.36, 1] }}
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
        {cold && (
          <div className="cold-wrap">
            <ColdOpen onBegin={handleNavigate} />
          </div>
        )}
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
