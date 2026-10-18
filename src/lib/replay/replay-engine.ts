/**
 * STRATA — Replay Engine
 *
 * Runs a journey's events through the REAL production engine (classify → decide)
 * using an isolated profile, then returns the resulting classification and composition.
 * This is the prove-it for judges: the journeys diverge because the engine did the math.
 */

import { classify, computeFeatures, contextFrom } from '@/engine/classify';
import { decideParadigm } from '@/engine/decide';
import { emptySignals, type Classification, type ParadigmId } from '@/engine/types';
import { NODES, neighboursOf } from '@/content/graph';
import type { Journey } from './journey-fixtures';

export interface ReplayStep {
  index: number;
  event: Journey['events'][number];
  classification: Classification;
  paradigm: ParadigmId;
  decided: boolean;
  reason: string;
}

export interface ReplayResult {
  journeyId: string;
  label: string;
  glyph: string;
  steps: ReplayStep[];
  finalParadigm: ParadigmId;
  finalClassification: Classification;
  confidence: number;
  history: ParadigmId[]; // paradigm after each step
}

const isNeighbour = (a: string, b: string) => neighboursOf(a).includes(b);

export function runJourney(journey: Journey, startingParadigm: ParadigmId = 'constellation'): ReplayResult {
  const signals = emptySignals(Date.now());
  const history: ParadigmId[] = [];
  const steps: ReplayStep[] = [];
  let current: ParadigmId = startingParadigm;
  let elapsed = 0;

  for (let i = 0; i < journey.events.length; i++) {
    const ev = journey.events[i];
    elapsed += 1200; // synthetic time between events

    // apply event to signals
    switch (ev.kind) {
      case 'open': {
        const id = ev.target!;
        if (signals.path.length > 0) {
          const prev = signals.path[signals.path.length - 1];
          if (isNeighbour(prev, id)) signals.steps++; else signals.jumps++;
        }
        signals.path.push(id);
        signals.openTimes.push(Date.now() + elapsed);
        signals.opens++;
        if (signals.seen.includes(id)) signals.revisits++; else signals.seen.push(id);
        signals.lastNode = id;
        signals.focusOpen = true;
        signals.focusStart = Date.now() + elapsed;
        signals.actions.open++;
        if (ev.dwellMs) { signals.focusMs += ev.dwellMs; signals.elapsedMs += ev.dwellMs; }
        signals.elapsedMs = elapsed + (ev.dwellMs ?? 0);
        break;
      }
      case 'edge': {
        const id = ev.target!;
        if (signals.path.length > 0) {
          const prev = signals.path[signals.path.length - 1];
          if (isNeighbour(prev, id)) signals.steps++; else signals.jumps++;
        }
        signals.path.push(id);
        signals.openTimes.push(Date.now() + elapsed);
        signals.opens++;
        if (signals.seen.includes(id)) signals.revisits++; else signals.seen.push(id);
        signals.lastNode = id;
        signals.focusOpen = true;
        signals.focusStart = Date.now() + elapsed;
        signals.actions.edge++;
        signals.elapsedMs = elapsed;
        break;
      }
      case 'search': {
        signals.actions.search++;
        if (ev.query) signals.queries.push(ev.query);
        break;
      }
      case 'filter': {
        signals.actions.filter++;
        if (ev.tag) signals.filters.push(ev.tag);
        break;
      }
      case 'command': {
        signals.actions.command++;
        if (ev.cmd) signals.commands.push(ev.cmd);
        break;
      }
      case 'scroll': {
        signals.scrollPixels += ev.pixels ?? 0;
        signals.scrollSeconds += (ev.dtMs ?? 0) / 1000;
        signals.peakVelocity = Math.max(signals.peakVelocity, ev.velocity ?? 0);
        if ((ev.velocity ?? 0) > 900) signals.fastScrolls++;
        break;
      }
      case 'dwell': {
        signals.focusMs += ev.dwellMs ?? 0;
        signals.elapsedMs += ev.dwellMs ?? 0;
        break;
      }
      case 'pointer': {
        signals.pointerPx += Math.min(ev.pixels ?? 0, 60);
        signals.pointerMs += Math.min(ev.dtMs ?? 0, 120);
        const v = signals.pointerMs > 0 ? signals.pointerPx / (signals.pointerMs / 1000) : 0;
        signals.peakPointer = Math.max(signals.peakPointer, v);
        break;
      }
    }

    signals.elapsedMs = elapsed;

    // classify & decide via real engine
    const features = computeFeatures(signals, isNeighbour);
    const cls = classify(features, contextFrom(signals));
    cls.evidence = signals.opens + Object.values(signals.actions).reduce((a, b) => a + b, 0) + Math.floor(signals.scrollPixels / 800);

    const decision = decideParadigm(cls, current, false);
    const decided = decision.changed;
    if (decided) current = decision.paradigm;
    history.push(current);

    steps.push({
      index: i,
      event: ev,
      classification: cls,
      paradigm: current,
      decided,
      reason: decided ? decision.reason : `holding ${current} — ${decision.reason}`,
    });
  }

  const finalCls = steps.length ? steps[steps.length - 1].classification : classify(computeFeatures(signals, isNeighbour), contextFrom(signals));

  return {
    journeyId: journey.id,
    label: journey.label,
    glyph: journey.glyph,
    steps,
    finalParadigm: current,
    finalClassification: finalCls,
    confidence: finalCls.confidence,
    history,
  };
}

export function compareResults(results: ReplayResult[]) {
  const diverged = new Set(results.map(r => r.finalParadigm)).size > 1;
  const paradigms = results.map(r => ({ id: r.journeyId, label: r.label, paradigm: r.finalParadigm, confidence: r.confidence }));
  return { diverged, paradigms, count: results.length };
}
