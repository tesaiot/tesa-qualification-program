// SPDX-FileCopyrightText: 2026 Thai Embedded Systems Association (TESA)
// SPDX-License-Identifier: Apache-2.0
//
// UI words for our own components (Starlight's chrome is already translated to Thai by Starlight).
// Values that come from YAML (skill names, level names, statuses) arrive already paired {th, en}.

export type Lang = 'th' | 'en';
export type Pair = { th?: string | null; en?: string | null };

export const langOf = (lang: string | undefined | null): Lang =>
	lang && lang.toLowerCase().startsWith('en') ? 'en' : 'th';

export function pick(value: unknown, lang: Lang, fallback = ''): string {
	if (value == null) return fallback;
	if (typeof value === 'string') return value;
	if (typeof value === 'object') {
		const v = value as Record<string, unknown>;
		for (const key of [lang, 'th', 'en']) {
			const s = v[key];
			if (typeof s === 'string' && s.trim()) return s;
		}
	}
	return fallback;
}

/** import.meta.env.BASE_URL without its trailing slash ("" when the site lives at the root). */
export const BASE = import.meta.env.BASE_URL.replace(/\/+$/, '');

/** Site URL for a page route ("courses/x/y", "" for home) in a locale. */
export function href(route: string | null | undefined, lang: Lang): string | null {
	if (route == null) return null;
	return `${BASE}${lang === 'en' ? '/en' : ''}${route ? `/${route}` : ''}/`;
}

export const fill = (text: string, vars: Record<string, string | number>) =>
	text.replace(/\{(\w+)\}/g, (_, k) => String(vars[k] ?? `{${k}}`));

const th = {
	lessonInfo: 'ข้อมูลบทเรียน',
	courseInfo: 'ข้อมูลหลักสูตร',
	course: 'หลักสูตร',
	module: 'โมดูล',
	level: 'ระดับ',
	time: 'เวลาโดยประมาณ',
	minutes: 'นาที',
	hours: 'ชั่วโมง',
	hardware: 'อุปกรณ์',
	emulator: 'BENTO Emulator (ไม่ต้องมีบอร์ด)',
	develops: 'ทักษะที่ฝึก',
	assesses: 'ทักษะที่ประเมิน',
	toLevel: 'ถึง',
	atLevel: 'ที่',
	evidence: 'หลักฐาน',
	prereq: 'ควรเรียนก่อน',
	none: 'ไม่มี',
	status: 'สถานะ',
	audience: 'เหมาะกับ',
	licence: 'สัญญาอนุญาต',
	lessons: 'บทเรียน',
	modules: 'โมดูล',
	openSlides: 'เปิดสไลด์',
	openSlidesEn: 'สไลด์ภาษาอังกฤษ',
	openIde: 'เปิด BENTO IDE',
	sourceFiles: 'ไฟล์ของบทเรียนบน GitHub',
	courseFiles: 'ไฟล์ของหลักสูตรบน GitHub',
	noticeReport: 'แจ้งปัญหาบน GitHub',
	videosTitle: 'วิดีโอประกอบ',
	videosCourseTitle: 'วิดีโอประกอบหลักสูตร',
	videosIntro: 'ดูบน YouTube (เปิดในแท็บใหม่)',
	videosBy: 'วิดีโอโดย',
	videosPlaylist: 'ดูทั้งชุดใน playlist',
	quizTitle: 'คำถามทบทวน',
	quizIntro: 'ลองตอบเองก่อน แล้วค่อยเปิดดูเฉลย',
	showAnswer: 'ดูเฉลย',
	answer: 'คำตอบ',
	correctOrder: 'ลำดับที่ถูก',
	objective: 'เป้าหมายข้อ',
	citeTitle: 'อ้างอิงบทเรียนนี้',
	citeIntro:
		'ถ้านำบทเรียนนี้ไปสอน ทำสไลด์ หรือทำเอกสารต่อ ให้อ้างอิงด้วยข้อความนี้ ถ้าดัดแปลงเนื้อหา ให้เติม{adapted}ต่อท้ายชื่อบทเรียน',
	citeOther: 'ข้อความอ้างอิงภาษาอังกฤษ',
	copy: 'คัดลอก',
	copied: 'คัดลอกแล้ว',
	lessonLink: 'ลิงก์บทเรียน',
	upstream: 'บทเรียนนี้ดัดแปลงจากต้นฉบับด้านล่าง เมื่ออ้างอิงให้คงเครดิตต้นฉบับไว้ด้วย',
	citeGuide: 'วิธีอ้างอิง TESA ฉบับเต็ม',
	howToCite: 'วิธีอ้างอิง TESA',
	footerNote: 'เนื้อหาเผยแพร่ภายใต้ CC BY-NC 4.0 นำไปใช้ต่อในงานที่ไม่ใช่เพื่อการค้าได้ โปรดอ้างอิงสมาคมสมองกลฝังตัวไทย (TESA) ทุกครั้ง',
	// roadmap
	roadmapTitle: 'แผนที่ทักษะ',
	roadmapDesc: 'แผนที่ทักษะระบบสมองกลฝังตัวของ TESA พร้อมสถานะว่าทักษะใดมีบทเรียนแล้ว',
	roadmapIntro:
		'ทักษะทั้ง {n} ข้อของแผนที่ทักษะ TESA จัดเป็นหมวดและกลุ่ม สีพื้นของแต่ละทักษะคือความสำคัญตาม Roadmap ต้นฉบับ ' +
		'ส่วนสัญลักษณ์และข้อความบอกว่าในคลังนี้มีบทเรียนที่พัฒนาหรือประเมินทักษะนั้นแล้วหรือยัง กดที่ทักษะเพื่อดูว่าเรียนได้จากบทไหน',
	summary: 'มีบทเรียนแล้ว {covered} จาก {n} ทักษะ (ประเมินแล้ว {assessed}) · ทักษะที่ Roadmap จัดว่าจำเป็น (R) มีบทเรียนแล้ว {rCovered} จาก {rTotal}',
	legendImp: 'ความสำคัญตาม Roadmap',
	legendCov: 'สถานะในคลังบทเรียน',
	covNone: 'ยังไม่มี',
	covDev: 'พัฒนา',
	covAss: 'ประเมิน',
	covNoneLong: 'ยังไม่มีบทเรียน',
	covDevLong: 'มีบทเรียนพัฒนาทักษะนี้',
	covAssLong: 'มีบทเรียนประเมินทักษะนี้',
	groupCount: 'มีบทเรียน {covered}/{n}',
	tableView: 'ดูรายการทักษะแบบตาราง',
	matrixView: 'ดูตารางความครอบคลุมรายหลักสูตร',
	eerCredit:
		'ดัดแปลงจาก Embedded Systems Engineering Roadmap ของ Meysam Parvizi (CC BY-SA 4.0) ข้อมูลแผนที่ทักษะเผยแพร่ภายใต้ CC BY-SA 4.0',
	// coverage
	coverageTitle: 'ตารางความครอบคลุมทักษะ',
	coverageDesc: 'ทักษะแต่ละข้อมีบทเรียนในหลักสูตรใด และไปถึงระดับไหน',
	coverageIntro:
		'แต่ละแถวคือทักษะหนึ่งข้อ แต่ละคอลัมน์คือหลักสูตร ช่องที่มีค่าบอกระดับสูงสุดที่บทเรียนในหลักสูตรนั้นพัฒนาหรือประเมินทักษะนั้น ' +
		'บนจอเล็กเลื่อนตารางไปทางขวาได้',
	colSkill: 'ทักษะ',
	colTotal: 'จำนวนหลักสูตร',
	devTo: 'พัฒนาถึง',
	assAt: 'ประเมินที่',
	devAbbr: 'พ',
	assAbbr: 'ป',
	legendCells: 'ในตาราง: พ = มีบทเรียนพัฒนาถึงระดับนั้น, ป = มีบทเรียนประเมินที่ระดับนั้น',
	noCourses: 'ยังไม่มีหลักสูตรในคลัง',
	tableLabel: 'ตารางทักษะกับหลักสูตร (เลื่อนแนวนอนได้)',
};

const en: typeof th = {
	lessonInfo: 'About this lesson',
	courseInfo: 'About this course',
	course: 'Course',
	module: 'Module',
	level: 'Level',
	time: 'Estimated time',
	minutes: 'min',
	hours: 'hours',
	hardware: 'Hardware',
	emulator: 'BENTO Emulator (no board needed)',
	develops: 'Skills practised',
	assesses: 'Skills assessed',
	toLevel: 'to',
	atLevel: 'at',
	evidence: 'evidence',
	prereq: 'Before this lesson',
	none: 'None',
	status: 'Status',
	audience: 'For',
	licence: 'Licence',
	lessons: 'lessons',
	modules: 'modules',
	openSlides: 'Open the slides',
	openSlidesEn: 'English slides',
	openIde: 'Open BENTO IDE',
	sourceFiles: 'Lesson files on GitHub',
	courseFiles: 'Course files on GitHub',
	noticeReport: 'Report it on GitHub',
	videosTitle: 'Companion videos',
	videosCourseTitle: 'Companion videos for this course',
	videosIntro: 'Watch on YouTube (opens in a new tab)',
	videosBy: 'Videos by',
	videosPlaylist: 'The whole series in the playlist',
	quizTitle: 'Review questions',
	quizIntro: 'Answer on your own first, then open the answer.',
	showAnswer: 'Show answer',
	answer: 'Answer',
	correctOrder: 'Correct order',
	objective: 'Objective',
	citeTitle: 'Cite this lesson',
	citeIntro:
		'If you teach from this lesson or reuse it in slides or documents, credit it with the text below. If you changed it, add{adapted} after the title.',
	citeOther: 'Thai attribution',
	copy: 'Copy',
	copied: 'Copied',
	lessonLink: 'Lesson link',
	upstream: 'This lesson adapts the source below; keep its credit too.',
	citeGuide: 'Full guide: how to cite TESA',
	howToCite: 'How to cite TESA',
	footerNote: 'Content is licensed CC BY-NC 4.0. Reuse it non-commercially and credit the Thai Embedded Systems Association (TESA) every time.',
	roadmapTitle: 'Skill roadmap',
	roadmapDesc: 'The TESA embedded systems skill map, showing which skills already have lessons.',
	roadmapIntro:
		'All {n} skills of the TESA skill map, by area and group. The background colour of each skill is its importance on the original roadmap; ' +
		'the symbol and text say whether a lesson in this library develops or assesses it yet. Select a skill to see where to learn it.',
	summary: '{covered} of {n} skills have a lesson ({assessed} assessed) · Required (R) skills with a lesson: {rCovered} of {rTotal}',
	legendImp: 'Roadmap importance',
	legendCov: 'Lesson coverage',
	covNone: 'none yet',
	covDev: 'developed',
	covAss: 'assessed',
	covNoneLong: 'No lesson yet',
	covDevLong: 'A lesson develops this skill',
	covAssLong: 'A lesson assesses this skill',
	groupCount: '{covered}/{n} with lessons',
	tableView: 'All skills as a table',
	matrixView: 'Coverage by course',
	eerCredit:
		'Adapted from the Embedded Systems Engineering Roadmap by Meysam Parvizi (CC BY-SA 4.0). Skill map data is licensed CC BY-SA 4.0.',
	coverageTitle: 'Skill coverage matrix',
	coverageDesc: 'Which course has lessons for each skill, and to what level.',
	coverageIntro:
		'Each row is a skill and each column a course. A filled cell gives the highest level a lesson in that course develops or assesses. ' +
		'On a small screen, scroll the table sideways.',
	colSkill: 'Skill',
	colTotal: 'Courses',
	devTo: 'developed to',
	assAt: 'assessed at',
	devAbbr: 'D',
	assAbbr: 'A',
	legendCells: 'In the table: D = a lesson develops the skill to that level, A = a lesson assesses it at that level',
	noCourses: 'No course in the library yet',
	tableLabel: 'Skills by course (scrolls horizontally)',
};

export const S = { th, en };
