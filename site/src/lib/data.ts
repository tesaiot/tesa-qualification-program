// SPDX-FileCopyrightText: 2026 Thai Embedded Systems Association (TESA)
// SPDX-License-Identifier: Apache-2.0
//
// The skills x lessons view model written by scripts/sync_content.py (src/generated/site-data.json).
import raw from '../generated/site-data.json';
import { pick, type Lang } from './strings';

export type Coverage = 'none' | 'developed' | 'assessed';
export interface Skill {
	id: string;
	th: string;
	en: string;
	group: string;
	importance: 'R' | 'Rec' | 'P' | null;
	origin: string;
	coverage: Coverage;
	dev_max: number | null;
	ass_max: number | null;
	n_dev: number;
	n_ass: number;
	courses: string[];
	deprecated: boolean;
}
export interface Group {
	id: string;
	th: string;
	en: string;
	skills: string[];
}
export interface Area {
	id: string;
	th: string;
	en: string;
	groups: Group[];
}
export interface CourseCol {
	id: string;
	short: string;
	title: { th: string; en: string };
	route: string | null;
	lessons: number;
}
export interface Cell {
	dev: number | null;
	ass: number | null;
	n: number;
}
export interface SiteData {
	areas: Area[];
	skills: Record<string, Skill>;
	courses: CourseCol[];
	matrix: Record<string, Record<string, Cell>>;
	importance: Record<string, { th: string; en: string }>;
	totals: {
		skills: number;
		lessons: number;
		none: number;
		developed: number;
		assessed: number;
		by_importance: Record<string, { total: number; covered: number }>;
	};
}

export const siteData = raw as unknown as SiteData;

/** Headings for Starlight's table of contents on the roadmap page. */
export function roadmapHeadings(lang: Lang) {
	return siteData.areas.flatMap((area) => {
		const groups = area.groups.filter((g) => g.skills.length > 0);
		if (groups.length === 0) return [];
		return [
			{ depth: 2, slug: `area-${area.id}`, text: pick(area, lang) },
			...groups.map((g) => ({ depth: 3, slug: `group-${g.id}`, text: pick(g, lang) })),
		];
	});
}
