// SPDX-FileCopyrightText: 2026 Thai Embedded Systems Association (TESA)
// SPDX-License-Identifier: Apache-2.0
//
// Three small page behaviours for TESA Open Knowledge:
//  1. Drag handles between the frames: the reader sets the width of the course navigation (left)
//     and of "On this page" (right). Double-click or Home resets; arrow keys move 16 px.
//     Widths are remembered in this browser only (localStorage; the page works without it).
//  2. Links in the page content (and any link to another site) open in a new tab, so the lesson stays open.
//  3. Licence names (CC BY 4.0, CC BY-NC 4.0, MIT, ...) explain themselves in a small box on hover, focus or tap.
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

	// Links in the document open in a new tab so the lesson stays where it was (owner's request):
	// every link inside the page content and the lesson boxes, plus any link to another site.
	// Navigation stays in the same tab: sidebar, header, previous/next, course cards, and anchors
	// within the same page.
	const CONTENT = '.sl-markdown-content, .tok-meta-box, .tok-cite, .tok-lesson-end';
	const NAVIGATION = '.tok-card, nav, .sidebar-content, .pagination-links, header, .tok-credit, .right-sidebar';
	function openLinksInNewTab() {
		for (const a of document.querySelectorAll('a[href]')) {
			const href = a.getAttribute('href') || '';
			if (href.startsWith('#')) continue;
			let url;
			try { url = new URL(href, location.href); } catch { continue; }
			if (url.protocol !== 'http:' && url.protocol !== 'https:') continue;
			const samePage = url.origin === location.origin && url.pathname === location.pathname;
			if (samePage) continue;
			const external = url.origin !== location.origin;
			const inContent = !!a.closest(CONTENT) && !a.closest(NAVIGATION);
			if (!external && !inContent) continue;
			a.target = '_blank';
			const rel = new Set((a.getAttribute('rel') || '').split(/\s+/).filter(Boolean));
			rel.add('noopener');
			if (external) rel.add('noreferrer');
			a.setAttribute('rel', [...rel].join(' '));
		}
	}

	// Licence names explain themselves: point at (or tab to, or tap) "CC BY 4.0", "CC-BY-NC-4.0", "MIT", ... anywhere
	// in the page and a small box says in one or two sentences what the licence allows, with a link to the licence
	// deed. Text inside code and the box itself are left alone.
	const LICENCES = {
		'by': {
			name: 'CC BY 4.0',
			th: 'ใช้ แบ่งปัน และดัดแปลงได้ ทั้งเพื่อการค้าและไม่ใช่การค้า โดยต้องให้เครดิตเจ้าของงาน บอกชื่อสัญญาอนุญาต และบอกว่าแก้อะไรไป',
			en: 'You may use, share and adapt it, commercially or not, as long as you credit the author, name the licence and say what you changed.',
			url: 'https://creativecommons.org/licenses/by/4.0/deed.',
		},
		'by-nc': {
			name: 'CC BY-NC 4.0',
			th: 'ใช้ แบ่งปัน และดัดแปลงได้เฉพาะที่ไม่ใช่เพื่อการค้า โดยต้องให้เครดิตเจ้าของงาน บอกชื่อสัญญาอนุญาต และบอกว่าแก้อะไรไป ถ้าจะใช้เพื่อการค้าต้องขออนุญาตก่อน',
			en: 'You may use, share and adapt it for non-commercial purposes only, crediting the author, naming the licence and saying what you changed. Commercial use needs permission.',
			url: 'https://creativecommons.org/licenses/by-nc/4.0/deed.',
		},
		'by-sa': {
			name: 'CC BY-SA 4.0',
			th: 'ใช้ แบ่งปัน และดัดแปลงได้ ต้องให้เครดิต และถ้าดัดแปลง ต้องเผยแพร่งานที่ดัดแปลงภายใต้สัญญาอนุญาตเดียวกันนี้',
			en: 'You may use, share and adapt it with credit; if you adapt it, you must share your version under this same licence.',
			url: 'https://creativecommons.org/licenses/by-sa/4.0/deed.',
		},
		'cc0': {
			name: 'CC0 1.0',
			th: 'เจ้าของสละสิทธิ์แล้ว ใช้ได้อิสระโดยไม่ต้องขออนุญาตและไม่ต้องให้เครดิต (แต่การให้เครดิตก็ยังเป็นมารยาทที่ดี)',
			en: 'The owner has waived their rights: use it freely, no permission or credit required (credit is still good manners).',
			url: 'https://creativecommons.org/publicdomain/zero/1.0/',
		},
		'mit': {
			name: 'MIT',
			th: 'สัญญาอนุญาตของโค้ด ใช้ แก้ และนำไปใช้ในงานเพื่อการค้าได้ ขอเพียงคงข้อความลิขสิทธิ์และสัญญาอนุญาตไว้ในสำเนา',
			en: 'A code licence: use, change and ship it, commercially too, as long as the copyright and licence notice stay with the copies.',
			url: 'https://opensource.org/license/mit',
		},
		'apache': {
			name: 'Apache-2.0',
			th: 'สัญญาอนุญาตของโค้ด ใช้ แก้ และนำไปใช้ในงานเพื่อการค้าได้ ต้องคงไฟล์ NOTICE และบอกว่าแก้ไฟล์ใด และได้สิทธิ์ในสิทธิบัตรที่เกี่ยวกับโค้ดด้วย',
			en: 'A code licence: use, change and ship it, commercially too; keep the NOTICE file, mark the files you changed, and receive a patent licence for the code.',
			url: 'https://www.apache.org/licenses/LICENSE-2.0',
		},
	};
	const LIC_RX = /\bCC[ -]BY[ -]NC[ -]4\.0\b|\bCC[ -]BY[ -]SA[ -]4\.0\b|\bCC[ -]BY[ -]4\.0\b|\bCC0(?:[ -]1\.0)?\b|\bApache[ -]2\.0\b|\bMIT\b/g;
	const LIC_TEST = new RegExp(LIC_RX.source);   // no /g: .test() must not carry lastIndex between nodes
	const licKey = (s) => {
		const u = s.toUpperCase();
		if (u.includes('NC')) return 'by-nc';
		if (u.includes('SA')) return 'by-sa';
		if (u.startsWith('CC0')) return 'cc0';
		if (u.startsWith('CC')) return 'by';
		if (u.startsWith('APACHE')) return 'apache';
		return 'mit';
	};
	const SKIP = 'code, pre, script, style, textarea, kbd, samp, .tok-lic, #tok-lic-tip, .expressive-code';

	function explainLicences() {
		const tip = document.createElement('div');
		tip.id = 'tok-lic-tip';
		tip.setAttribute('role', 'tooltip');
		tip.hidden = true;
		document.body.appendChild(tip);
		let hideTimer = 0;
		const show = (el) => {
			clearTimeout(hideTimer);
			const lic = LICENCES[el.dataset.lic];
			const deed = lic.url.endsWith('deed.') ? lic.url + (th ? 'th' : 'en') : lic.url;
			tip.innerHTML = '';
			const title = document.createElement('strong');
			title.textContent = lic.name;
			const text = document.createElement('p');
			text.textContent = th ? lic.th : lic.en;
			const more = document.createElement('a');
			more.href = deed;
			more.target = '_blank';
			more.rel = 'noopener noreferrer';
			more.textContent = th ? 'อ่านสัญญาอนุญาตฉบับเต็ม' : 'Read the licence';
			tip.append(title, text, more);
			tip.hidden = false;
			const r = el.getBoundingClientRect();
			const w = Math.min(320, window.innerWidth - 16);
			tip.style.width = `${w}px`;
			const left = Math.min(Math.max(8, r.left + window.scrollX), window.scrollX + window.innerWidth - w - 8);
			const below = r.bottom + 8 + tip.offsetHeight < window.innerHeight;
			tip.style.left = `${left}px`;
			tip.style.top = `${(below ? r.bottom + 6 : r.top - tip.offsetHeight - 6) + window.scrollY}px`;
			el.setAttribute('aria-describedby', 'tok-lic-tip');
		};
		const hide = (delay = 150) => {
			clearTimeout(hideTimer);
			hideTimer = setTimeout(() => { tip.hidden = true; }, delay);
		};
		tip.addEventListener('mouseenter', () => clearTimeout(hideTimer));
		tip.addEventListener('mouseleave', () => hide());
		document.addEventListener('keydown', (e) => { if (e.key === 'Escape') hide(0); });

		const walker = document.createTreeWalker(document.body, NodeFilter.SHOW_TEXT, {
			acceptNode: (n) => (n.parentElement && !n.parentElement.closest(SKIP) && LIC_TEST.test(n.nodeValue)
				? NodeFilter.FILTER_ACCEPT : NodeFilter.FILTER_REJECT),
		});
		const nodes = [];
		while (walker.nextNode()) nodes.push(walker.currentNode);
		for (const node of nodes) {
			const frag = document.createDocumentFragment();
			let last = 0;
			node.nodeValue.replace(LIC_RX, (m, offset) => {
				frag.append(node.nodeValue.slice(last, offset));
				const span = document.createElement('span');
				span.className = 'tok-lic';
				span.dataset.lic = licKey(m);
				span.tabIndex = 0;
				span.textContent = m;
				span.addEventListener('mouseenter', () => show(span));
				span.addEventListener('mouseleave', () => hide());
				span.addEventListener('focus', () => show(span));
				span.addEventListener('blur', () => hide());
				// A tap shows the box (touch screens have no hover); inside a link the link still works.
				span.addEventListener('click', (e) => {
					if (span.closest('a')) return;
					e.preventDefault();
					if (tip.hidden) show(span); else hide(0);
				});
				frag.append(span);
				last = offset + m.length;
				return m;
			});
			frag.append(node.nodeValue.slice(last));
			node.replaceWith(frag);
		}
	}

	function init() {
		for (const side of Object.keys(SIDES)) {
			if (root.hasAttribute(SIDES[side].attr)) makeHandle(side);
		}
		openLinksInNewTab();
		explainLicences();
	}

	if (document.readyState === 'loading') document.addEventListener('DOMContentLoaded', init);
	else init();
})();
