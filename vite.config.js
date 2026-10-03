import { defineConfig } from 'vite';

// 127.0.0.1:5190 on purpose: another local project already answers on localhost:5173 (IPv6),
// so the Vite default would open the wrong site.
export default defineConfig({
  server: {
    host: '127.0.0.1',
    port: 5190,
    strictPort: true,
    open: false,
    watch: { ignored: ['**/tools/**'] },
  },
});
