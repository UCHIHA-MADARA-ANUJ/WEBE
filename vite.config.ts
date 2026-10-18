import { defineConfig } from 'vite';
import react from '@vitejs/plugin-react';

// @ts-ignore - untyped for vite-only path alias
export default defineConfig({
  base: './',
  plugins: [react()],
  resolve: {
    alias: {
      '@': '/src',
    },
  },
  server: {
    host: '0.0.0.0',
    allowedHosts: true,
    port: 5173,
  },
  preview: {
    host: '0.0.0.0',
    allowedHosts: true,
    port: 4173,
  },
  build: {
    target: 'es2020',
    chunkSizeWarningLimit: 1200,
  },
});
