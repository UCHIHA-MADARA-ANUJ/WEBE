'use client';

import { motion, AnimatePresence } from 'motion/react';

/**
 * StructuralTransition — Motion-driven hierarchy reassembly.
 * Uses `layout` and `layoutId` so a reorganisation feels like the work
 * being reassembled, not a screen swap.
 */
export function StructuralTransition({
  children,
  id,
}: {
  children: React.ReactNode;
  id: string;
}) {
  return (
    <AnimatePresence mode="wait">
      <motion.div
        key={id}
        layout
        initial={{ opacity: 0, y: 8, filter: 'blur(6px)' }}
        animate={{ opacity: 1, y: 0, filter: 'blur(0px)' }}
        exit={{ opacity: 0, y: -8, filter: 'blur(4px)' }}
        transition={{
          layout: { duration: 0.45, ease: [0.22, 0.61, 0.36, 1] },
          opacity: { duration: 0.28 },
          filter: { duration: 0.35 },
        }}
        style={{ height: '100%' }}
      >
        {children}
      </motion.div>
    </AnimatePresence>
  );
}

/** Shared-element wrapper for entity cards that persist across paradigm switches */
export function SharedEntity({ id, children }: { id: string; children: React.ReactNode }) {
  return (
    <motion.div layoutId={`entity-${id}`} layout transition={{ duration: 0.4, ease: [0.22, 0.61, 0.36, 1] }}>
      {children}
    </motion.div>
  );
}
