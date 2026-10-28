#!/usr/bin/env python3
"""
generate_py.py - RECONSTRUCTED Python port of generate.js (python-docx).

STATUS: RECONSTRUCTION. The approved resume was NOT produced by this file. It was produced by
the Node.js script (generate.js). This port exists so an environment without Node can still
produce the same look. It reads the same input JSON and the same config/style.json.
How close it is to the Node output is measured in evidence/fidelity_report.md.

Usage: python3 generate_py.py --input input/sample_resume.json --out output/Sample_Resume.docx
                              [--style config/style.json] [--photo assets/photo.jpg]
"""
import argparse, json, os
from docx import Document
from docx.shared import Pt, Mm, Inches, Twips, Emu, RGBColor
from docx.enum.text import WD_ALIGN_PARAGRAPH, WD_TAB_ALIGNMENT
from docx.oxml import parse_xml
from docx.oxml.ns import nsdecls, qn

ap = argparse.ArgumentParser()
ap.add_argument("--input", required=True); ap.add_argument("--out", required=True)
ap.add_argument("--style", default=os.path.join(os.path.dirname(os.path.abspath(__file__)), "config", "style.json"))
ap.add_argument("--photo", default=None)
A = ap.parse_args()
S = json.load(open(A.style, encoding="utf-8"))
R = json.load(open(A.input, encoding="utf-8"))

tw = lambda pt: round(pt * 20)          # twips
FONT = S["font_requested"]
def rgb(h): return RGBColor.from_string(h.upper())
BLACK, GRAY = rgb(S["color"]["text"]), rgb(S["color"]["muted"])

# pPr children that must come AFTER pBdr / numPr (schema order)
AFTER_PBDR = ('w:shd','w:tabs','w:suppressAutoHyphens','w:kinsoku','w:wordWrap','w:overflowPunct','w:topLinePunct',
              'w:autoSpaceDE','w:autoSpaceDN','w:bidi','w:adjustRightInd','w:snapToGrid','w:spacing','w:ind',
              'w:contextualSpacing','w:mirrorIndents','w:suppressOverlap','w:jc','w:textDirection','w:textAlignment',
              'w:textboxTightWrap','w:outlineLvl','w:divId','w:cnfStyle','w:rPr','w:sectPr','w:pPrChange')
AFTER_NUMPR = ('w:suppressLineNumbers','w:pBdr') + AFTER_PBDR

doc = Document()
sec = doc.sections[0]
sec.page_width, sec.page_height = Mm(210), Mm(297)                       # A4 (python-docx default is Letter)
sec.top_margin, sec.bottom_margin = Inches(S["page"]["margin_top_in"]), Inches(S["page"]["margin_bottom_in"])
sec.left_margin, sec.right_margin = Inches(S["page"]["margin_left_in"]), Inches(S["page"]["margin_right_in"])

# Mimic docx-js: the approved DOCX has EMPTY document defaults and a bare Normal style (no default font,
# size or line spacing). python-docx's template adds 11pt + 1.15 line spacing, which changes line heights,
# so strip them. Every run in this file sets its own font and size explicitly.
_dd = doc.styles.element.find(qn("w:docDefaults"))
for _c in list(_dd): _dd.remove(_c)
_dd.append(parse_xml(f'<w:rPrDefault {nsdecls("w")}/>')); _dd.append(parse_xml(f'<w:pPrDefault {nsdecls("w")}/>'))
_normal = doc.styles["Normal"].element
for _tag in ("w:pPr", "w:rPr"):
    _el = _normal.find(qn(_tag))
    if _el is not None: _normal.remove(_el)
sec.header_distance = sec.footer_distance = Twips(708); sec.gutter = Twips(0)   # docx-js defaults

# Mimic docx-js settings.xml: Word compatibility mode 15 and nothing else. python-docx's template ships
# mode 14 + useFELayout + other switches, which makes LibreOffice break some lines one word earlier.
_st = doc.settings.element
for _c in list(_st): _st.remove(_c)
for _x in ('<w:displayBackgroundShape %s/>', '<w:evenAndOddHeaders %s w:val="false"/>',
           '<w:compat %s><w:compatSetting w:val="15" w:name="compatibilityMode" w:uri="http://schemas.microsoft.com/office/word"/></w:compat>'):
    _st.append(parse_xml(_x % nsdecls("w")))

# ---- real bullet list definition (same glyph and indents as generate.js) ----
numbering = doc.part.numbering_part.element
ABS_ID = NUM_ID = 90
import math
left_tw, hang_tw = math.floor(S["bullet"]["left_in"] * 1440), math.floor(S["bullet"]["hanging_in"] * 1440)   # docx-js floors (316, 259)
abstract = parse_xml(
    f'<w:abstractNum {nsdecls("w")} w:abstractNumId="{ABS_ID}"><w:multiLevelType w:val="hybridMultilevel"/>'
    f'<w:lvl w:ilvl="0"><w:start w:val="1"/><w:numFmt w:val="bullet"/><w:lvlText w:val="{S["bullet"]["char"]}"/>'
    f'<w:lvlJc w:val="left"/><w:pPr><w:ind w:left="{left_tw}" w:hanging="{hang_tw}"/></w:pPr></w:lvl></w:abstractNum>')
first_num = numbering.find(qn("w:num"))
(first_num.addprevious(abstract) if first_num is not None else numbering.append(abstract))
numbering.append(parse_xml(f'<w:num {nsdecls("w")} w:numId="{NUM_ID}"><w:abstractNumId w:val="{ABS_ID}"/></w:num>'))

# docx-js puts every bullet in a BARE "List Paragraph" style (no indent, no contextual spacing).
# python-docx's template version adds ind=720 and contextualSpacing, so replace it with the bare one.
_lp = doc.styles.element.xpath('w:style[@w:styleId="ListParagraph"]')
for _e in _lp: doc.styles.element.remove(_e)
doc.styles.element.append(parse_xml(f'<w:style {nsdecls("w")} w:type="paragraph" w:styleId="ListParagraph"><w:name w:val="List Paragraph"/><w:basedOn w:val="Normal"/><w:qFormat/></w:style>'))

def run(p, text, size_pt, bold=False, italic=False, color=BLACK):
    # Emit the same run properties as docx-js: only write bold/italic when true, and add the complex-script
    # twins (bCs, iCs, szCs), so LibreOffice lays out the runs identically.
    r = p.add_run(text)
    r.font.name = FONT; r.font.size = Pt(size_pt); r.font.color.rgb = color
    if bold: r.bold = True
    if italic: r.italic = True
    rPr = r._r.get_or_add_rPr()
    for a in ("w:ascii", "w:hAnsi", "w:cs", "w:eastAsia"): rPr.rFonts.set(qn(a), FONT)
    if bold: rPr.append(parse_xml(f'<w:bCs {nsdecls("w")}/>'))
    if italic: rPr.append(parse_xml(f'<w:iCs {nsdecls("w")}/>'))
    rPr.append(parse_xml(f'<w:szCs {nsdecls("w")} w:val="{round(size_pt * 2)}"/>'))
    return r

def para(after_pt, before_pt=0.0, justify=False):
    p = doc.add_paragraph(); pf = p.paragraph_format
    pf.space_before, pf.space_after = Twips(tw(before_pt)), Twips(tw(after_pt))
    if justify: p.alignment = WD_ALIGN_PARAGRAPH.JUSTIFY
    return p

# ---- approved helper functions, ported ----
def section_heading(text):
    p = para(S["spacing_pt"]["section_after"], S["spacing_pt"]["section_before"])
    bdr = parse_xml(f'<w:pBdr {nsdecls("w")}><w:bottom w:val="single" w:sz="{S["rule"]["size_eighth_pt"]}" '
                    f'w:space="{S["rule"]["space_pt"]}" w:color="{S["color"]["text"]}"/></w:pBdr>')
    p._p.get_or_add_pPr().insert_element_before(bdr, *AFTER_PBDR)
    run(p, text.upper(), S["size_pt"]["section_heading"], bold=True)

def bullet(text):
    p = para(S["spacing_pt"]["bullet_after"], justify=S["justify"]["bullets"])
    p.style = doc.styles["List Paragraph"]
    numpr = parse_xml(f'<w:numPr {nsdecls("w")}><w:ilvl w:val="0"/><w:numId w:val="{NUM_ID}"/></w:numPr>')
    p._p.get_or_add_pPr().insert_element_before(numpr, *AFTER_NUMPR)
    run(p, text, S["size_pt"]["body"])

def entry_header(title, dates):
    p = para(S["spacing_pt"]["entry_after"])
    p.paragraph_format.tab_stops.add_tab_stop(Twips(round(S["tab_stop_in"] * 1440)), WD_TAB_ALIGNMENT.RIGHT)
    run(p, title, S["size_pt"]["entry_title"], bold=True)
    if dates: run(p, "\t" + dates, S["size_pt"]["entry_date"], italic=True, color=GRAY)

def sub_line(text):
    run(para(S["spacing_pt"]["subline_after"], justify=S["justify"]["subline"]), text, S["size_pt"]["subline"], italic=True, color=GRAY)

def skill_line(label, value):
    p = para(S["spacing_pt"]["skill_after"], justify=S["justify"]["skills"])
    run(p, label + ": ", S["size_pt"]["body"], bold=True); run(p, value, S["size_pt"]["body"])

def add_floating_photo(r, path):
    shape = r.add_picture(path, width=Emu(S["photo"]["width_px"] * 9525), height=Emu(S["photo"]["height_px"] * 9525))
    inline = shape._inline
    anchor = parse_xml(f'''<wp:anchor {nsdecls("wp","a","pic","r")} distT="0" distB="0" distL="91440" distR="0"
      simplePos="0" relativeHeight="251658240" behindDoc="0" locked="0" layoutInCell="1" allowOverlap="0">
      <wp:simplePos x="0" y="0"/>
      <wp:positionH relativeFrom="margin"><wp:align>right</wp:align></wp:positionH>
      <wp:positionV relativeFrom="margin"><wp:posOffset>0</wp:posOffset></wp:positionV>
      <wp:extent cx="{inline.extent.cx}" cy="{inline.extent.cy}"/>
      <wp:effectExtent l="0" t="0" r="0" b="0"/>
      <wp:wrapSquare wrapText="left"/>
      <wp:docPr id="{inline.docPr.id}" name="Profile photo" descr="Profile photo"/>
      <wp:cNvGraphicFramePr/>
    </wp:anchor>''')
    anchor.append(inline.find(qn("a:graphic")))
    inline.getparent().replace(inline, anchor)

# ---- header ----
p = para(S["spacing_pt"]["name_after"])
if A.photo: add_floating_photo(p.add_run(""), A.photo)
run(p, R["name"], S["size_pt"]["name"], bold=True)
run(para(S["spacing_pt"]["headline_after"]), S["separators"]["headline"].join(R["headline"]), S["size_pt"]["headline"], bold=True)
if A.photo:   # photo narrows the text column to ~5.7 in: split contact into two short lines (same rule as generate.js)
    k = S["photo"]["contact_split_at"]
    run(para(S["spacing_pt"]["contact_after"]), S["separators"]["contact"].join(R["contact"][:k]), S["size_pt"]["contact"])
    run(para(S["photo"]["contact_after_pt_when_photo"]), S["separators"]["contact"].join(R["contact"][k:]), S["size_pt"]["contact"])
else:
    run(para(S["spacing_pt"]["contact_after"]), S["separators"]["contact"].join(R["contact"]), S["size_pt"]["contact"])

# ---- sections ----
for sec_ in R["sections"]:
    section_heading(sec_["heading"])
    t = sec_["type"]
    if t == "paragraph":
        run(para(S["spacing_pt"]["summary_after"], justify=S["justify"]["summary"]), sec_["text"], S["size_pt"]["body"])
    elif t == "entries":
        for e in sec_["items"]:
            entry_header(e["title"], e.get("dates"))
            if e.get("sub"): sub_line(e["sub"])
            for b in e.get("bullets", []): bullet(b)
    elif t == "skills":
        for s in sec_["items"]: skill_line(s["label"], S["separators"]["skill_items"].join(s["items"]))
    elif t == "bullets":
        for b in sec_["items"]: bullet(b)
    elif t == "inline_list":
        run(para(S["spacing_pt"]["inline_list_after"]), S["separators"]["inline_list"].join(sec_["items"]), S["size_pt"]["body"])
    else:
        raise SystemExit("unknown section type: " + t)

os.makedirs(os.path.dirname(os.path.abspath(A.out)), exist_ok=True)
doc.save(A.out)
print("wrote " + A.out)
