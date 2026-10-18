export interface ModeProps {
  /** the entry currently in focus, if any */
  focus: string | null;
  /** ask the site to open an entry (records the interaction, too) */
  navigate: (id: string) => void;
  /** open the engine's mind panel */
  openMind: () => void;
}
