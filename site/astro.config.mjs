// SPDX-FileCopyrightText: 2026 Thai Embedded Systems Association (TESA)
// SPDX-License-Identifier: Apache-2.0
// @ts-check
//
// TESA Open Knowledge — Astro + Starlight configuration.
// Origin, base path, repo URL and the sidebar are NOT written here: scripts/sync_content.py
// reads site.config.yaml and the course tree and writes them to src/generated/*.json.
import { existsSync, readFileSync } from 'node:fs';
import { fileURLToPath } from 'node:url';
import { defineConfig } from 'astro/config';
import starlight from '@astrojs/starlight';

/** @param {string} name */
function generated(name) {
	const path = fileURLToPath(new URL(`./src/generated/${name}`, import.meta.url));
	if (!existsSync(path)) {
		throw new Error(
			`[site] ${path} is missing.\n` +
				'Generate the content first (from the repo root): python3 site/scripts/sync_content.py\n' +
				'See site/README.md.'
		);
	}
	return JSON.parse(readFileSync(path, 'utf8'));
}

const siteConfig = generated('site-config.json');
const sidebar = generated('sidebar.json');
const base = String(siteConfig.site.base || '').replace(/\/$/, '');

// Frame widths the reader dragged (public/tok-layout.js) are applied before first paint, so the page
// does not jump. Wrapped in try: storage can be blocked, and the default widths are then used.
const restoreWidths =
	"try{var r=document.documentElement,l=localStorage.getItem('tok-left-width'),t=localStorage.getItem('tok-toc-width');" +
	"if(l)r.style.setProperty('--sl-sidebar-width',l+'px');if(t)r.style.setProperty('--tok-toc-width',t+'px')}catch(e){}";

export default defineConfig({
	site: siteConfig.site.origin,
	base: siteConfig.site.base,
	trailingSlash: 'always',
	// Astro 7 defaults to JSX whitespace rules ('jsx'); keep HTML rules so inline Thai text and
	// links in our components keep their spaces.
	compressHTML: true,
	integrations: [
		starlight({
			title: siteConfig.site.title,
			description: siteConfig.site.description.th,
			defaultLocale: 'root',
			locales: {
				root: { label: 'ไทย', lang: 'th' },
				en: { label: 'English', lang: 'en' },
			},
			social: [{ icon: 'github', label: 'GitHub', href: siteConfig.repo.url }],
			sidebar,
			customCss: [
				'@fontsource/ibm-plex-sans-thai/400.css',
				'@fontsource/ibm-plex-sans-thai/600.css',
				'@fontsource/ibm-plex-sans-thai/700.css',
				'@fontsource/ibm-plex-mono/400.css',
				'./src/styles/custom.css',
			],
			components: {
				// Credit line + "How to cite TESA" link on every page (BUILD_SPEC §1.9).
				Footer: './src/components/Footer.astro',
				// Lesson header box, review questions and the "cite this lesson" box.
				MarkdownContent: './src/components/MarkdownContent.astro',
			},
			head: [
				{ tag: 'script', content: restoreWidths },
				{ tag: 'script', attrs: { src: `${base}/tok-layout.js`, defer: true } },
			],
			favicon: '/favicon.svg',
			lastUpdated: false,
			pagination: true,
			tableOfContents: { minHeadingLevel: 2, maxHeadingLevel: 3 },
		}),
	],
});
