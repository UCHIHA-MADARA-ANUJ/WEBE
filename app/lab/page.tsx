'use client';

import Link from 'next/link';
import { useState } from 'react';
import { Chrome } from '@/components/Chrome';
import { LenisProvider } from '@/components/motion/LenisProvider';
import { JourneyComparison } from '@/components/evolution/JourneyComparison';
import { JourneyReplay } from '@/components/evolution/JourneyReplay';
import { EvolutionLabPanel } from '@/components/evolution/EvolutionLabPanel';
import { StrataBackdrop } from '@/components/identity/StrataBackdrop';
import { EngineProvider, useEngine } from '@/engine/store';

function LabShell() {
  const { genome } = useEngine();
  const [focus, setFocus] = useState<string | null>(null);
  const [activeTab, setActiveTab] = useState<'lab'|'replay'|'compare'>('lab');

  return (
    <div className="app" data-paradigm="lattice">
      <StrataBackdrop seed={genome.seed} />
      <Chrome onMind={() => {}} onNavigate={(id) => setFocus(id)} />

      {/* secondary nav for lab */}
      <div className="lab-nav">
        <Link href="/" className="lab-nav__back">← Workspace</Link>
        <div className="lab-nav__tabs">
          <button data-on={activeTab==='lab'} onClick={() => setActiveTab('lab')}>Live Telemetry</button>
          <button data-on={activeTab==='replay'} onClick={() => setActiveTab('replay')}>Journey Replay</button>
          <button data-on={activeTab==='compare'} onClick={() => setActiveTab('compare')}>Compare</button>
        </div>
        <span className="lab-nav__hint">The Evolution Lab — the engine, inspected.</span>
      </div>

      <main className="lab-main">
        {activeTab === 'lab' && <EvolutionLabPanel />}
        {activeTab === 'replay' && <JourneyReplay focus={focus} navigate={setFocus} />}
        {activeTab === 'compare' && <JourneyComparison />}
      </main>

      <div className="lab-footnote">
        <span>STRATA Evolution Lab · generation {genome.generation} · paradigm {genome.paradigm}</span>
        <span>The journeys below are simulations run through the production engine. Not fabricated layouts — real scoring.</span>
      </div>
    </div>
  );
}

export default function LabPage() {
  return (
    <LenisProvider>
      <EngineProvider>
        <LabShell />
      </EngineProvider>
    </LenisProvider>
  );
}
