import { defineConfig } from 'vite';
import { resolve } from 'path';
import react from '@vitejs/plugin-react';
import tailwindcss from '@tailwindcss/vite';

export default defineConfig({
  root: resolve(__dirname, 'js/'),
  build: {
    outDir: resolve(__dirname, 'static/dist'),
    emptyOutDir: true,
    rollupOptions: {
      input: {
        home: resolve(__dirname, 'js/components/home/main.js'),
        styles: resolve(__dirname, 'styles/main.css'),
      },
      output: {
        entryFileNames: '[name]/[name].[hash].js',
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
  plugins: [react(), tailwindcss()],
});