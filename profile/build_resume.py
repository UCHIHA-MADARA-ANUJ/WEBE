#!/usr/bin/env python3
"""Mitali Chincholikar — résumé.

Section order follows the standard fresher CV that was sent as reference:
Objective, Education, Skills, Certifications, Internships, Projects,
Extracurricular. Sections with no confirmed content are skipped in the real
file and shown greyed in the draft, so nothing is ever invented.

One content block, four outputs:
  resume.pdf   A4, embedded fonts, selectable text, ATS-safe single column
  resume.docx  editable, real Word XML
  resume.txt   pure ASCII, CRLF, opens in Notepad
  resume-draft.pdf  the same layout with empty sections marked

    python3 build_resume.py
"""
import pathlib
import textwrap

HERE = pathlib.Path(__file__).parent
FONTS = HERE / "fonts"
OUT = HERE / "mitali"

# ── content ────────────────────────────────────────────────────────────────
#  Only facts she has given us. Anything still unconfirmed lives in PENDING
#  and is excluded from the shipped file.
CONTENT = dict(
    name="Mitali Chincholikar",
    role="Computer Science Student",
    tagline="First year \u00b7 artificial intelligence and cybersecurity "
            "alongside the degree",
    location="Pune, Maharashtra, India",
    email="chincholikarmitali@gmail.com",

    objective=(
        "First-year Computer Science student at Dnyan Prasad Global University. "
        "Studies computer science alongside artificial intelligence and "
        "cybersecurity, and works across eight languages, from C and C++ to "
        "JavaScript and Node.js. Runs events for her college club."
    ),

    education=[
        dict(when="2026 \u2014 present",
             school="Dnyan Prasad Global University",
             program="B.Tech / B.Sc. Computer Science",
             detail="School of Technology and Research",
             score=None,
             notes=["First year, enrolled",
                    "Artificial intelligence and machine learning from year two"]),
        dict(when="2025 \u2014 present",
             school="Cybersecurity",
             program="Certification course",
             detail="Alongside the degree",
             score=None,
             notes=[]),
    ],

    skills=[
        ("Languages", "Python, C, C++, Java, SQL"),
        ("Web", "HTML, CSS, JavaScript, Node.js"),
        ("Tools", "VS Code, Windows"),
    ],

    # ── awaiting her answers; empty lists are skipped in the real file ─────
    certifications=[],
    internships=[],
    projects=[],

    activities=[
        "Event manager, Swarang \u2014 her college club. Organises and runs club events.",
        "Badminton \u2014 plays competitively.",
        "Tug of war \u2014 college team.",
    ],
)

#  What is missing, and the exact shape each answer needs. Shown in the draft
#  and written out to RESUME-QUESTIONS.md.
PENDING = [
    ("Academic projects", "One to three. For each: a name, the year, what it "
     "does in one sentence, and what you built it with."),
    ("Internships", "Any, including short or unpaid ones. Role, company, "
     "dates, and two bullet points on what you actually did."),
    ("Certifications", "Any completed course with a certificate, plus the "
     "issuer and the year. The cybersecurity course goes here once finished."),
    ("CGPA or percentage", "Current CGPA, or the Class 12 and Class 10 "
     "percentages. Any one of these strengthens the education block."),
    ("Links", "GitHub, LinkedIn, or a portfolio, if she has them."),
    ("Objective", "The current paragraph is factual. If she is actively "
     "looking for an internship, say so and it changes to a targeted line."),
]

ACCENT = "#A30D28"
ACCENT_SOFT = "#C9646F"
INK = "#111116"
MID = "#4A4A56"
SOFT = "#6E6E7C"
FAINT = "#9A9AA6"
RULE = "#DCDCE2"


# ══ PDF ════════════════════════════════════════════════════════════════════
def build_pdf(path, draft=False):
    from reportlab.pdfgen import canvas
    from reportlab.lib.pagesizes import A4
    from reportlab.pdfbase import pdfmetrics
    from reportlab.pdfbase.ttfonts import TTFont

    for name, f in (("Inter", "Inter-400.ttf"), ("InterMed", "Inter-500.ttf"),
                    ("InterBold", "Inter-600.ttf"), ("Mono", "JBMono-500.ttf"),
                    ("MonoBold", "JBMono-700.ttf")):
        if name not in pdfmetrics.getRegisteredFontNames():
            pdfmetrics.registerFont(TTFont(name, str(FONTS / f)))

    W, H = A4
    M = 51
    RIGHT = W - M
    BODY = M + 92          # everything indented under the date column

    c = canvas.Canvas(str(path), pagesize=A4)
    c.setTitle("Mitali Chincholikar \u2014 Curriculum Vitae"
               + (" (draft)" if draft else ""))
    c.setAuthor("Mitali Chincholikar")

    def sw(t, f, s):
        return pdfmetrics.stringWidth(t, f, s)

    def wrap(text, font, size, width):
        out, cur = [], ""
        for word in text.split():
            t = (cur + " " + word).strip()
            if sw(t, font, size) <= width:
                cur = t
            else:
                if cur:
                    out.append(cur)
                cur = word
        if cur:
            out.append(cur)
        return out

    y = H - M

    # ── header: name left, contact right, one baseline
    c.setFillColor(INK)
    c.setFont("InterBold", 25)
    c.drawString(M, y - 22, CONTENT["name"])

    c.setFont("Mono", 7.4)
    c.setFillColor(MID)
    c.drawRightString(RIGHT, y - 12, CONTENT["email"])
    c.setFillColor(SOFT)
    c.drawRightString(RIGHT, y - 23, CONTENT["location"])

    y -= 38
    c.setFillColor(ACCENT)
    c.setFont("InterMed", 10.2)
    c.drawString(M, y, CONTENT["role"])
    c.setFillColor(SOFT)
    c.setFont("Inter", 9.2)
    c.drawString(M + sw(CONTENT["role"], "InterMed", 10.2) + 10, y,
                 "\u00b7  " + CONTENT["tagline"])

    y -= 22
    c.setStrokeColor(ACCENT)
    c.setLineWidth(1.6)
    c.line(M, y, M + 44, y)
    c.setStrokeColor(RULE)
    c.setLineWidth(0.7)
    c.line(M + 50, y + 0.5, RIGHT, y + 0.5)

    # ── section heading
    def section(title, y):
        c.setFillColor(ACCENT)
        c.setFont("MonoBold", 7.2)
        t = title.upper()
        c.drawString(M, y, t)
        tw = sw(t, "MonoBold", 7.2)
        c.setStrokeColor(ACCENT_SOFT)
        c.setLineWidth(1.3)
        c.line(M, y - 4.5, M + tw + 1, y - 4.5)
        c.setStrokeColor(RULE)
        c.setLineWidth(0.7)
        c.line(M + tw + 10, y - 4, RIGHT, y - 4)
        return y - 21

    def body(text, y, size=9.1, lead=13.4, color=MID, font="Inter",
             indent=0, width=None):
        c.setFillColor(color)
        c.setFont(font, size)
        for ln in wrap(text, font, size, (width or RIGHT - M) - indent):
            c.drawString(M + indent, y, ln)
            y -= lead
        return y

    def bullets(items, y, indent=92, size=8.9):
        for it in items:
            c.setFillColor(ACCENT_SOFT)
            c.setFont("Inter", size)
            c.drawString(M + indent, y, "\u2013")
            c.setFillColor(MID)
            for ln in wrap(it, "Inter", size, RIGHT - (M + indent) - 12):
                c.drawString(M + indent + 11, y, ln)
                y -= 12.6
            y -= 1.6
        return y

    def entry(when, title, sub=None, notes=None, bullets_=None, y=None):
        c.setFillColor(SOFT)
        c.setFont("Mono", 7.2)
        c.drawString(M, y, when.upper())
        c.setFillColor(INK)
        c.setFont("InterMed", 10.2)
        c.drawString(M + 92, y, title)
        if sub:
            y -= 12.6
            c.setFillColor(MID)
            c.setFont("Inter", 9.0)
            c.drawString(M + 92, y, sub)
        if notes:
            y -= 1.4
            for n in notes:
                y -= 11.8
                c.setFillColor(SOFT)
                c.setFont("Inter", 8.5)
                c.drawString(M + 92, y, "\u2014  " + n)
        if bullets_:
            y -= 13
            y = bullets(bullets_, y)
        return y - 15

    def empty(label, y):
        if not draft:
            return y
        c.setFillColor(FAINT)
        c.setFont("Inter", 8.8)
        c.drawString(M + 92, y, f"\u2014  {label}")
        return y - 11

    # ── OBJECTIVE
    y = section("Objective", y - 30)
    y = body(CONTENT["objective"], y) - 8

    # ── EDUCATION
    y = section("Education", y - 2)
    for e in CONTENT["education"]:
        y = entry(e["when"], e["school"], e["program"] + " \u00b7 " + e["detail"],
                  e["notes"], y=y)
    y += 4

    # ── SKILLS
    y = section("Technical Skills", y - 2)
    for label, value in CONTENT["skills"]:
        c.setFillColor(INK)
        c.setFont("InterMed", 9.1)
        c.drawString(M, y, label)
        c.setFillColor(MID)
        c.setFont("Inter", 9.1)
        for i, ln in enumerate(wrap(value, "Inter", 9.1, RIGHT - (M + 92))):
            c.drawString(M + 92, y, ln)
            if i == 0:
                y -= 13.2
        y -= 3
    y -= 8

    # ── CERTIFICATIONS
    if CONTENT["certifications"] or draft:
        y = section("Certifications", y)
        for name_, issuer, when in CONTENT["certifications"]:
            y = entry(when, name_, issuer, y=y)
        if not CONTENT["certifications"]:
            y = empty("no confirmed certifications yet", y)
        y -= 4

    # ── INTERNSHIPS
    if CONTENT["internships"] or draft:
        y = section("Internships", y)
        for it in CONTENT["internships"]:
            y = entry(it["when"], it["role"], it["org"], bullets_=it["bullets"], y=y)
        if not CONTENT["internships"]:
            y = empty("no internships yet", y)
        y -= 4

    # ── PROJECTS
    if CONTENT["projects"] or draft:
        y = section("Academic Projects", y)
        for p in CONTENT["projects"]:
            y = entry(p["when"], p["name"], p.get("stack"), bullets_=p["bullets"], y=y)
        if not CONTENT["projects"]:
            y = empty("project details to be supplied", y)
        y -= 4

    # ── ACTIVITIES
    y = section("Extracurricular Activities", y - 2)
    y = bullets(CONTENT["activities"], y, indent=0)

    # ── footer
    c.setStrokeColor(RULE)
    c.setLineWidth(0.7)
    c.line(M, M + 18, RIGHT, M + 18)
    c.setFillColor(SOFT)
    c.setFont("Mono", 6.8)
    c.drawString(M, M + 7, f"{CONTENT['location']}  \u00b7  {CONTENT['email']}")
    c.drawRightString(RIGHT, M + 7, "Mitali Chincholikar")

    # clickable email
    c.linkURL("mailto:" + CONTENT["email"],
              (M, H - M - 30, M + 220, H - M - 16), relative=0)

    c.showPage()
    c.save()
    return path


# ══ DOCX ═══════════════════════════════════════════════════════════════════
def build_docx(path, draft=False):
    from docx import Document
    from docx.shared import Pt, RGBColor, Cm
    from docx.enum.text import WD_TAB_ALIGNMENT
    from docx.oxml.ns import qn
    from docx.oxml import OxmlElement

    def rgb(h):
        h = h.lstrip("#")
        return RGBColor(int(h[0:2], 16), int(h[2:4], 16), int(h[4:6], 16))

    d = Document()
    s = d.sections[0]
    s.page_height, s.page_width = Cm(29.7), Cm(21.0)
    s.left_margin = s.right_margin = Cm(1.8)
    s.top_margin = s.bottom_margin = Cm(1.6)

    st = d.styles["Normal"]
    st.font.name = "Inter"
    st.font.size = Pt(9.2)
    st.font.color.rgb = rgb(MID)
    st.paragraph_format.space_after = Pt(0)
    st.paragraph_format.line_spacing = 1.22
    st.element.rPr.rFonts.set(qn("w:eastAsia"), "Inter")

    def para(text="", size=9.2, color=MID, bold=False, before=0, after=0,
             font="Inter", spacing=1.22):
        p = d.add_paragraph()
        p.paragraph_format.space_before = Pt(before)
        p.paragraph_format.space_after = Pt(after)
        p.paragraph_format.line_spacing = spacing
        if text:
            r = p.add_run(text)
            r.font.size = Pt(size)
            r.font.color.rgb = rgb(color)
            r.font.bold = bold
            r.font.name = font
        return p

    def rule(color=RULE, sz=6, before=1):
        p = d.add_paragraph()
        p.paragraph_format.space_before = Pt(before)
        p.paragraph_format.space_after = Pt(0)
        pPr = p._p.get_or_add_pPr()
        b = OxmlElement("w:pBdr")
        bo = OxmlElement("w:bottom")
        bo.set(qn("w:val"), "single")
        bo.set(qn("w:sz"), str(sz))
        bo.set(qn("w:space"), "1")
        bo.set(qn("w:color"), color.lstrip("#"))
        b.append(bo)
        pPr.append(b)

    def heading(text):
        para(text.upper(), size=7.4, color=ACCENT, bold=True, before=11,
             after=3, font="Courier New")
        rule()

    def row(left, right, size=10.2, bold=True, color=INK):
        p = d.add_paragraph()
        p.paragraph_format.space_before = Pt(4)
        p.paragraph_format.space_after = Pt(0)
        p.paragraph_format.tab_stops.add_tab_stop(Cm(17.4),
                                                  WD_TAB_ALIGNMENT.RIGHT)
        r = p.add_run(left + "\t")
        r.font.size = Pt(size)
        r.font.bold = bold
        r.font.color.rgb = rgb(color)
        r2 = p.add_run(right.upper())
        r2.font.size = Pt(7.2)
        r2.font.name = "Courier New"
        r2.font.color.rgb = rgb(SOFT)
        return p

    def bullet(text, indent=Cm(0)):
        p = d.add_paragraph()
        p.paragraph_format.left_indent = Cm(0.42) + indent
        p.paragraph_format.first_line_indent = Cm(-0.42)
        p.paragraph_format.space_after = Pt(2)
        r = p.add_run("\u2013  ")
        r.font.color.rgb = rgb(ACCENT_SOFT)
        r.font.size = Pt(8.9)
        r2 = p.add_run(text)
        r2.font.size = Pt(8.9)
        r2.font.color.rgb = rgb(MID)

    # header
    para(CONTENT["name"], size=23, color=INK, bold=True, after=1)
    p = d.add_paragraph()
    p.paragraph_format.space_after = Pt(2)
    p.paragraph_format.tab_stops.add_tab_stop(Cm(17.4), WD_TAB_ALIGNMENT.RIGHT)
    r = p.add_run(CONTENT["role"])
    r.font.size = Pt(10.2)
    r.font.bold = True
    r.font.color.rgb = rgb(ACCENT)
    r2 = p.add_run("\t" + CONTENT["email"])
    r2.font.size = Pt(7.6)
    r2.font.name = "Courier New"
    r2.font.color.rgb = rgb(MID)
    para(CONTENT["tagline"] + "\t" + CONTENT["location"])
    rule(ACCENT, 12, before=5)

    heading("Objective")
    para(CONTENT["objective"], after=2)

    heading("Education")
    for e in CONTENT["education"]:
        row(e["school"], e["when"])
        para(e["program"] + " \u00b7 " + e["detail"], size=9, color=MID)
        for n in e["notes"]:
            para("\u2014  " + n, size=8.6, color=SOFT)

    heading("Technical Skills")
    for label, value in CONTENT["skills"]:
        p = d.add_paragraph()
        p.paragraph_format.space_after = Pt(2)
        r = p.add_run(f"{label}\t")
        r.font.bold = True
        r.font.size = Pt(9.2)
        r.font.color.rgb = rgb(INK)
        r2 = p.add_run(value)
        r2.font.size = Pt(9.2)
        r2.font.color.rgb = rgb(MID)

    if CONTENT["certifications"] or draft:
        heading("Certifications")
        for name_, issuer, when in CONTENT["certifications"]:
            row(name_, when)
            para(issuer, size=9, color=MID)
        if not CONTENT["certifications"]:
            para("\u2014  no confirmed certifications yet", size=8.8,
                 color=FAINT)

    if CONTENT["internships"] or draft:
        heading("Internships")
        for it in CONTENT["internships"]:
            row(it["role"], it["when"])
            para(it["org"], size=9, color=MID)
            for b in it["bullets"]:
                bullet(b)
        if not CONTENT["internships"]:
            para("\u2014  no internships yet", size=8.8, color=FAINT)

    if CONTENT["projects"] or draft:
        heading("Academic Projects")
        for pr in CONTENT["projects"]:
            row(pr["name"], pr["when"])
            if pr.get("stack"):
                para(pr["stack"], size=9, color=MID)
            for b in pr["bullets"]:
                bullet(b)
        if not CONTENT["projects"]:
            para("\u2014  project details to be supplied", size=8.8,
                 color=FAINT)

    heading("Extracurricular Activities")
    for a in CONTENT["activities"]:
        bullet(a)

    para(f"{CONTENT['location']}  \u00b7  {CONTENT['email']}", size=7.4,
         color=SOFT, before=14, font="Courier New")

    d.core_properties.title = "Mitali Chincholikar \u2014 Curriculum Vitae"
    d.core_properties.author = "Mitali Chincholikar"
    d.save(str(path))
    return path


# ══ TXT ════════════════════════════════════════════════════════════════════
def build_txt(path, draft=False):
    L = []
    a = L.append

    def rule(ch="=", n=76):
        a(ch * n)

    a(CONTENT["name"].upper())
    a(CONTENT["role"])
    a(CONTENT["tagline"])
    a(f"{CONTENT['location']}  |  {CONTENT['email']}")
    rule()
    a("")

    a("OBJECTIVE")
    rule("-")
    for ln in textwrap.wrap(CONTENT["objective"], 76):
        a(ln)
    a("")

    a("EDUCATION")
    rule("-")
    for e in CONTENT["education"]:
        a(f"{e['school']}  ({e['when']})")
        a(f"  {e['program']} | {e['detail']}")
        for n in e["notes"]:
            a(f"    - {n}")
        a("")

    a("TECHNICAL SKILLS")
    rule("-")
    for label, value in CONTENT["skills"]:
        a(f"{label}: {value}")
    a("")

    def block(title, rows, empty_note):
        if not rows:
            if not draft:
                return
            a(title.upper())
            rule("-")
            a(f"  - {empty_note}")
            a("")
            return
        a(title.upper())
        rule("-")
        for r in rows:
            a(r)
        a("")

    block("Certifications",
          [f"{n} - {i} ({w})" for n, i, w in CONTENT["certifications"]],
          "no confirmed certifications yet")

    block("Internships",
          [f"{it['role']} | {it['org']} ({it['when']})"
           for it in CONTENT["internships"]],
          "no internships yet")

    block("Academic Projects",
          [f"{p['name']} ({p['when']})" for p in CONTENT["projects"]],
          "project details to be supplied")

    a("EXTRACURRICULAR ACTIVITIES")
    rule("-")
    for x in CONTENT["activities"]:
        for i, ln in enumerate(textwrap.wrap(x, 72)):
            a(("- " if i == 0 else "  ") + ln)
    a("")
    rule()
    a(f"{CONTENT['location']} | {CONTENT['email']}")

    text = "\n".join(L)
    text = text.replace("\u2014", "-").replace("\u00b7", "|")
    text = text.replace("\u2019", "'").replace("\u2013", "-")
    text = text.encode("ascii", "replace").decode("ascii")
    path.write_bytes(text.replace("\n", "\r\n").encode("ascii"))
    return path


# ══ QUESTIONS ══════════════════════════════════════════════════════════════
def build_questions(path):
    L = ["# What to ask her", "",
         "The résumé is built and shipping. These are the only things missing, "
         "in the order that would help most.", "",
         "Send the answers in any format. Loose notes are fine.", ""]
    for i, (topic, detail) in enumerate(PENDING, 1):
        L += [f"## {i}. {topic}", "", detail, ""]
    L += ["---", "",
          "## Already on the résumé, confirm these", "",
          "- **Dnyan Prasad Global University** — she typed *PRASAC*; the "
          "résumé currently says **PRASAD**.",
          "- **Enrolled 2026** — confirm the start year.",
          "- **Git** is not listed under tools because she has not mentioned "
          "it. Say the word and it goes in.", "",
          "## Deliberately left out", "",
          "No CGPA, no projects, no internships, no awards, and no claim that "
          "she is looking for work. Every one of those would be a guess.", "",
          "Once the answers arrive, edit `CONTENT` at the top of "
          "`build_resume.py` and run it again. The sections appear on their "
          "own.", ""]
    path.write_text("\n".join(L), encoding="utf-8")
    return path


def main():
    OUT.mkdir(exist_ok=True)
    jobs = [("resume.pdf", lambda p: build_pdf(p)),
            ("resume.docx", lambda p: build_docx(p)),
            ("resume.txt", lambda p: build_txt(p)),
            ("resume-draft.pdf", lambda p: build_pdf(p, draft=True)),
            ("RESUME-QUESTIONS.md", build_questions)]
    for name, fn in jobs:
        p = fn(OUT / name)
        print(f"  {name:<24}{p.stat().st_size / 1024:8.1f} KB")


if __name__ == "__main__":
    main()
