#!/usr/bin/env node
/*
 * generate.js  -  resume DOCX generator (Node.js + docx 9.6.1)
 *
 * PROVENANCE
 *  The helper functions below (sectionHeading, bullet, entryHeader, subLine, skillLine),
 *  the numbering config, and every numeric value are the ones used by the approved script
 *  (Approved_Resume_BA generate.js). What is NEW in this file is only the data-driven wrapper:
 *  reading the resume from JSON, reading numbers from config/style.json, section dispatch,
 *  and the optional photo. Fidelity test: evidence/fidelity_report.md.
 *
 *  Usage: node generate.js --input input/sample_resume.json --out output/Sample_Resume.docx
 *                          [--style config/style.json] [--photo assets/photo.jpg]
 */
"use strict";
const fs = require("fs");
const path = require("path");
const {
  Document, Packer, Paragraph, TextRun, AlignmentType, BorderStyle, LevelFormat,
  convertInchesToTwip, ImageRun,
  HorizontalPositionAlign, HorizontalPositionRelativeFrom, VerticalPositionRelativeFrom,
  TextWrappingType, TextWrappingSide,
} = require("docx");

// ---------- CLI ----------
const args = {};
for (let i = 2; i < process.argv.length; i += 2) args[process.argv[i].replace(/^--/, "")] = process.argv[i + 1];
if (!args.input || !args.out) {
  console.error("usage: node generate.js --input resume.json --out out.docx [--style style.json] [--photo photo.jpg]");
  process.exit(1);
}
const here = __dirname;
const S = JSON.parse(fs.readFileSync(args.style || path.join(here, "config", "style.json"), "utf8"));
const R = JSON.parse(fs.readFileSync(args.input, "utf8"));
const photoPath = args.photo || null;

// ---------- unit helpers (pt -> docx units) ----------
const tw = (pt) => Math.round(pt * 20);   // twips
const hp = (pt) => Math.round(pt * 2);    // half-points
const FONT = S.font_requested;
const BLACK = S.color.text;
const GRAY = S.color.muted;
const J = AlignmentType.JUSTIFIED;
const align = (flag) => (flag ? { alignment: J } : {});

// ---------- approved helper functions (unchanged logic) ----------
function sectionHeading(text) {
  return new Paragraph({
    spacing: { before: tw(S.spacing_pt.section_before), after: tw(S.spacing_pt.section_after) },
    border: { bottom: { style: BorderStyle.SINGLE, size: S.rule.size_eighth_pt, color: BLACK, space: S.rule.space_pt } },
    children: [new TextRun({ text: text.toUpperCase(), bold: true, size: hp(S.size_pt.section_heading), font: FONT, color: BLACK })],
  });
}
function bullet(text) {
  return new Paragraph({
    numbering: { reference: "bullet-list", level: 0 },
    ...align(S.justify.bullets),
    spacing: { after: tw(S.spacing_pt.bullet_after) },
    children: [new TextRun({ text, size: hp(S.size_pt.body), font: FONT, color: BLACK })],
  });
}
function entryHeader(title, dates) {
  const kids = [new TextRun({ text: title, bold: true, size: hp(S.size_pt.entry_title), font: FONT, color: BLACK })];
  if (dates) kids.push(new TextRun({ text: "\t" + dates, italics: true, size: hp(S.size_pt.entry_date), font: FONT, color: GRAY }));
  return new Paragraph({
    spacing: { after: tw(S.spacing_pt.entry_after) },
    tabStops: [{ type: "right", position: convertInchesToTwip(S.tab_stop_in) }],
    children: kids,
  });
}
function subLine(text) {
  return new Paragraph({
    ...align(S.justify.subline),
    spacing: { after: tw(S.spacing_pt.subline_after) },
    children: [new TextRun({ text, italics: true, size: hp(S.size_pt.subline), font: FONT, color: GRAY })],
  });
}
function skillLine(label, value) {
  return new Paragraph({
    ...align(S.justify.skills),
    spacing: { after: tw(S.spacing_pt.skill_after) },
    children: [
      new TextRun({ text: label + ": ", bold: true, size: hp(S.size_pt.body), font: FONT, color: BLACK }),
      new TextRun({ text: value, size: hp(S.size_pt.body), font: FONT, color: BLACK }),
    ],
  });
}

// With a photo, the text column is ~5.7 in wide, so a one-line contact string wraps mid-item.
// Split it into two short lines instead (items [0, split) and [split, end]).
function contactParagraphs() {
  const run = (items, after) => new Paragraph({
    spacing: { after: tw(after) },
    children: [new TextRun({ text: items.join(S.separators.contact), size: hp(S.size_pt.contact), font: FONT, color: BLACK })],
  });
  if (!photoPath) return [run(R.contact, S.spacing_pt.contact_after)];
  const k = S.photo.contact_split_at;
  return [run(R.contact.slice(0, k), S.spacing_pt.contact_after), run(R.contact.slice(k), S.photo.contact_after_pt_when_photo)];
}

// ---------- header (name / headline / contact, optional photo) ----------
function header() {
  const nameKids = [];
  if (photoPath) {
    const ext = path.extname(photoPath).slice(1).toLowerCase().replace("jpeg", "jpg");
    nameKids.push(new ImageRun({
      type: ext, data: fs.readFileSync(photoPath),
      transformation: { width: S.photo.width_px, height: S.photo.height_px },
      altText: { title: "Profile photo", description: "Profile photo", name: "Profile photo" },
      floating: {
        horizontalPosition: { relative: HorizontalPositionRelativeFrom.MARGIN, align: HorizontalPositionAlign.RIGHT },
        verticalPosition: { relative: VerticalPositionRelativeFrom.MARGIN, offset: 0 },
        wrap: { type: TextWrappingType.SQUARE, side: TextWrappingSide.LEFT },
      },
    }));
  }
  nameKids.push(new TextRun({ text: R.name, bold: true, size: hp(S.size_pt.name), font: FONT, color: BLACK }));
  return [
    new Paragraph({ spacing: { after: tw(S.spacing_pt.name_after) }, children: nameKids }),
    new Paragraph({
      spacing: { after: tw(S.spacing_pt.headline_after) },
      children: [new TextRun({ text: R.headline.join(S.separators.headline), bold: true, size: hp(S.size_pt.headline), font: FONT, color: BLACK })],
    }),
    ...contactParagraphs(),
  ];
}

// ---------- section dispatch ----------
function section(sec) {
  const out = [sectionHeading(sec.heading)];
  switch (sec.type) {
    case "paragraph":
      out.push(new Paragraph({
        ...align(S.justify.summary),
        spacing: { after: tw(S.spacing_pt.summary_after) },
        children: [new TextRun({ text: sec.text, size: hp(S.size_pt.body), font: FONT, color: BLACK })],
      }));
      break;
    case "entries":
      for (const e of sec.items) {
        out.push(entryHeader(e.title, e.dates));
        if (e.sub) out.push(subLine(e.sub));
        for (const b of e.bullets || []) out.push(bullet(b));
      }
      break;
    case "skills":
      for (const s of sec.items) out.push(skillLine(s.label, s.items.join(S.separators.skill_items)));
      break;
    case "bullets":
      for (const b of sec.items) out.push(bullet(b));
      break;
    case "inline_list":
      out.push(new Paragraph({
        spacing: { after: tw(S.spacing_pt.inline_list_after) },
        children: [new TextRun({ text: sec.items.join(S.separators.inline_list), size: hp(S.size_pt.body), font: FONT, color: BLACK })],
      }));
      break;
    default:
      throw new Error("unknown section type: " + sec.type);
  }
  return out;
}

// ---------- document ----------
const children = [...header(), ...R.sections.flatMap(section)];
const doc = new Document({
  numbering: {
    config: [{
      reference: "bullet-list",
      levels: [{
        level: 0, format: LevelFormat.BULLET, text: S.bullet.char, alignment: AlignmentType.LEFT,
        style: { paragraph: { indent: { left: convertInchesToTwip(S.bullet.left_in), hanging: convertInchesToTwip(S.bullet.hanging_in) } } },
      }],
    }],
  },
  sections: [{
    properties: { page: { margin: {
      top: convertInchesToTwip(S.page.margin_top_in), bottom: convertInchesToTwip(S.page.margin_bottom_in),
      left: convertInchesToTwip(S.page.margin_left_in), right: convertInchesToTwip(S.page.margin_right_in),
    } } },
    children,
  }],
});
Packer.toBuffer(doc).then((buf) => {
  fs.mkdirSync(path.dirname(path.resolve(args.out)), { recursive: true });
  fs.writeFileSync(args.out, buf);
  console.log("wrote " + args.out);
});
