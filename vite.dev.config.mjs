import { defineConfig, mergeConfig } from 'vite';
import baseConfig from './vite.config.mjs';

export default mergeConfig(baseConfig, defineConfig({
  mode: 'development',
  build: {
    sourcemap: true,
    minify: false,
  },
  server: {
    hmr: {
      port: 8000,
    },
    watch: {
      usePolling: true,
    },
  },
}));