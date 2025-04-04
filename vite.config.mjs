import { defineConfig } from 'vite';
import { resolve } from 'path';
import react from '@vitejs/plugin-react';

export default defineConfig({
  root: resolve(__dirname, "js/"),
  build: {
    outDir: resolve(__dirname, 'static/js'),
    emptyOutDir: true,
    rollupOptions: {
      input: {
        home: resolve(__dirname, 'js/components/home/main.jsx'),
      },
      output: {
        entryFileNames: '[name]/[name].js',
        chunkFileNames: 'assets/[name].[hash].js',
        assetFileNames: 'assets/[name].[hash].[ext]',
      },
    },
    manifest: true,
  },
  server: {
    strictPort: true,
    port: 3000,
  },
  plugins: [react()],
});