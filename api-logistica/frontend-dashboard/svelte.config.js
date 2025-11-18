import adapter from '@sveltejs/adapter-static';
import { vitePreprocess } from '@sveltejs/vite-plugin-svelte';

/** @type {import('@sveltejs/kit').Config} */
const config = {
	// Consult https://svelte.dev/docs/kit/integrations
	// for more information about preprocessors
	preprocess: vitePreprocess(),

	kit: {
		// adapter-static is used for static site generation, suitable for serving with Nginx.
		adapter: adapter({
			pages: 'dist',
			assets: 'dist',
			fallback: 'index.html' // For SPA routing
		})
	}
};

export default config;
