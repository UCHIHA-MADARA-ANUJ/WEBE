/**
 * Compatibility shim — all imports of `../content/graph` now resolve to the
 * STRATA graph. The previous DEEP FIELD corpus is preserved as
 * `deepfield-graph.ts` and can be re-enabled by changing this single line.
 */
export * from './strata-graph';
