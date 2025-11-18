import { sveltekit } from '@sveltejs/kit/vite';
import { defineConfig } from 'vite';

export default defineConfig({
	plugins: [sveltekit()],
	server: {
		host: true,
		port: 5173,
		hmr: {
			clientPort: 3000
		},
		proxy: {
			'/api': {
				target: 'http://api:8080', // Corrected target for Docker Compose
				changeOrigin: true
			}
		}
	}
});