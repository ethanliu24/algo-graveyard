import { defineConfig, mergeConfig } from 'vite';
import baseConfig from './vite.config.mjs';

export default mergeConfig(baseConfig, defineConfig({
  mode: 'production',
  build: {
    sourcemap: false,
    minify: 'terser',
    terserOptions: {
      compress: {
        drop_console: true,
      },
    },
    rollupOptions: {
      output: {
        manualChunks: (id) => {
          if (id.includes('node_modules')) {
            return 'vendor';
          }
        },
      },
    },
  },
}));