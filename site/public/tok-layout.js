// SPDX-FileCopyrightText: 2026 Thai Embedded Systems Association (TESA)
// SPDX-License-Identifier: Apache-2.0
//
// Two small page behaviours for TESA Open Knowledge:
//  1. Drag handles between the frames: the reader sets the width of the course navigation (left)
//     and of "On this page" (right). Double-click or Home resets; arrow keys move 16 px.
//     Widths are remembered in this browser only (localStorage; the page works without it).
//  2. Links to other sites (GitHub, Developer Hub, ...) open in a new tab, so the lesson stays open.
(() => {
	const root = document.documentElement;
	const th = (root.lang || 'th').startsWith('th');
	const SIDES = {
		left: {
			cssVar: '--sl-sidebar-width',
			key: 'tok-left-width',
			min: 12, // rem
			max: 34,
			attr: 'data-has-sidebar',
			label: th
				? 'ปรับความกว้างของสารบัญหลักสูตร: ลากซ้ายขวา หรือกดลูกศร · ดับเบิลคลิกเพื่อคืนค่าเดิม'
				: 'Resize the course navigation: drag, or use the arrow keys · double-click to reset',
		},
		right: {
			cssVar: '--tok-toc-width',
			key: 'tok-toc-width',
			min: 10,
			max: 30,
			attr: 'data-has-toc',
			label: th
				? 'ปรับความกว้างของ "ในหน้านี้": ลากซ้ายขวา หรือกดลูกศร · ดับเบิลคลิกเพื่อคืนค่าเดิม'
				: 'Resize "On this page": drag, or use the arrow keys · double-click to reset',
		},
	};
	const MIN_CONTENT_REM = 28;

	const store = {
		get(k) { try { return localStorage.getItem(k); } catch { return null; } },
		set(k, v) { try { localStorage.setItem(k, v); } catch { /* private mode: keep it for this page only */ } },
		del(k) { try { localStorage.removeItem(k); } catch { /* ignore */ } },
	};
	const remPx = () => parseFloat(getComputedStyle(root).fontSize) || 16;
	const widthOf = (side) => {
		const v = getComputedStyle(root).getPropertyValue(SIDES[side].cssVar).trim();
		if (v.endsWith('rem')) return parseFloat(v) * remPx();
		return parseFloat(v) || 0;
	};

	function clamp(side, px) {
		const s = SIDES[side];
		const other = side === 'left' ? 'right' : 'left';
		const otherPx = root.hasAttribute(SIDES[other].attr) ? widthOf(other) : 0;
		const room = window.innerWidth - otherPx - MIN_CONTENT_REM * remPx();
		const max = Math.min(s.max * remPx(), Math.max(s.min * remPx(), room));
		return Math.round(Math.min(Math.max(px, s.min * remPx()), max));
	}

	function apply(side, px, handle, save) {
		const w = clamp(side, px);
		root.style.setProperty(SIDES[side].cssVar, `${w}px`);
		if (handle) handle.setAttribute('aria-valuenow', String(w));
		if (save) store.set(SIDES[side].key, String(w));
	}

	function reset(side, handle) {
		root.style.removeProperty(SIDES[side].cssVar);
		store.del(SIDES[side].key);
		if (handle) handle.setAttribute('aria-valuenow', String(Math.round(widthOf(side))));
	}

	function makeHandle(side) {
		const s = SIDES[side];
		const h = document.createElement('div');
		h.className = `tok-resizer tok-resizer-${side}`;
		h.setAttribute('role', 'separator');
		h.setAttribute('aria-orientation', 'vertical');
		h.setAttribute('aria-label', s.label);
		h.setAttribute('aria-valuemin', String(Math.round(s.min * remPx())));
		h.setAttribute('aria-valuemax', String(Math.round(s.max * remPx())));
		h.setAttribute('aria-valuenow', String(Math.round(widthOf(side))));
		h.title = s.label;
		h.tabIndex = 0;

		h.addEventListener('pointerdown', (e) => {
			if (e.button !== 0) return;
			e.preventDefault();
			h.setPointerCapture(e.pointerId);
			root.classList.add('tok-resizing');
			const move = (ev) => apply(side, side === 'left' ? ev.clientX : window.innerWidth - ev.clientX, h, false);
			const up = () => {
				h.removeEventListener('pointermove', move);
				h.removeEventListener('pointerup', up);
				h.removeEventListener('pointercancel', up);
				root.classList.remove('tok-resizing');
				apply(side, widthOf(side), h, true);
			};
			h.addEventListener('pointermove', move);
			h.addEventListener('pointerup', up);
			h.addEventListener('pointercancel', up);
		});
		h.addEventListener('dblclick', () => reset(side, h));
		h.addEventListener('keydown', (e) => {
			const grow = side === 'left' ? 'ArrowRight' : 'ArrowLeft';
			const shrink = side === 'left' ? 'ArrowLeft' : 'ArrowRight';
			if (e.key === grow || e.key === shrink) {
				e.preventDefault();
				apply(side, widthOf(side) + (e.key === grow ? 16 : -16), h, true);
			} else if (e.key === 'Home') {
				e.preventDefault();
				reset(side, h);
			}
		});
		document.body.appendChild(h);
	}

	function openExternalInNewTab() {
		for (const a of document.querySelectorAll('a[href]')) {
			let url;
			try { url = new URL(a.getAttribute('href'), location.href); } catch { continue; }
			if ((url.protocol === 'http:' || url.protocol === 'https:') && url.origin !== location.origin) {
				a.target = '_blank';
				const rel = new Set((a.getAttribute('rel') || '').split(/\s+/).filter(Boolean));
				rel.add('noopener');
				rel.add('noreferrer');
				a.setAttribute('rel', [...rel].join(' '));
			}
		}
	}

	function init() {
		for (const side of Object.keys(SIDES)) {
			if (root.hasAttribute(SIDES[side].attr)) makeHandle(side);
		}
		openExternalInNewTab();
	}

	if (document.readyState === 'loading') document.addEventListener('DOMContentLoaded', init);
	else init();
})();
