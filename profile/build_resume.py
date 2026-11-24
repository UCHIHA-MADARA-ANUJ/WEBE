#!/usr/bin/env python3
"""Mitali Chincholikar — résumé.

One content block, three files:

  resume.pdf   print, A4, the one to attach
  resume.docx  editable in Word, Google Docs and LibreOffice
  resume.txt   pure ASCII, CRLF, opens in Notepad

They are generated from the same source so they cannot drift apart. Edit
CONTENT below and rerun; never edit the outputs.

Every line is a fact she gave us. If something is not in here, it is because
nobody has confirmed it yet.

    python3 build_resume.py
"""
import pathlib
import sys

HERE = pathlib.Path(__file__).parent
FONTS = HERE / "fonts"
OUT = HERE / "mitali"

# ── content ────────────────────────────────────────────────────────────────
CONTENT = dict(
    name="Mitali Chincholikar",
    role="Computer Science Student \u00b7 First Year",
    place="Pune, Maharashtra, India",
    email="chincholikarmitali@gmail.com",
    summary=(
        "First-year Computer Science student at Dnyan Prasad Global "
        "University, studying computer science alongside artificial "
        "intelligence and cybersecurity. Works across eight languages, "
        "from C and C++ to JavaScript and Node.js. Runs events for her "
        "college club and plays badminton and tug of war."
    ),
    education=[
        ("2026 \u2014 present", "Dnyan Prasad Global University",
         "B.Tech / B.Sc. Computer Science \u00b7 School of Technology and Research",
         ["First year, enrolled",
          "Artificial intelligence and machine learning from year two"]),
        ("In progress", "Cybersecurity",
         "Certification course alongside the degree", []),
    ],
    skills=[
        ("Languages", "Python, C, C++, Java, SQL, JavaScript"),
        ("Web", "HTML, CSS, Node.js"),
        ("Tools", "VS Code, Git, Windows"),
    ],
    activity=[
        ("Event Manager", "Swarang \u00b7 college club",
         "Organises and runs club events."),
        ("Badminton", "", "Plays competitively."),
        ("Tug of war", "", "Team sport; represents her college."),
    ],
    footer="Pune, Maharashtra, India \u00b7 chincholikarmitali@gmail.com",
)

SECTION_ORDER = ["summary", "education", "skills", "activity"]
TITLES = {"summary": "Profile", "education": "Education",
          "skills": "Technical skills", "activity": "Activities"}

ACCENT = "#A30D28"
ACCENT_SOFT = "#C9646F"
INK = "#111116"
MID = "#4A4A56"
SOFT = "#6E6E7C"
RULE = "#DCDCE2"


# ══ PDF ════════════════════════════════════════════════════════════════════
def build_pdf(path):
    from reportlab.pdfgen import canvas
    from reportlab.lib.pagesizes import A4
    from reportlab.pdfbase import pdfmetrics
    from reportlab.pdfbase.ttfonts import TTFont

    for name, f in (("Inter", "Inter-400.ttf"), ("InterMed", "Inter-500.ttf"),
                    ("InterBold", "Inter-600.ttf"),
                    ("Mono", "JBMono-500.ttf"), ("MonoBold", "JBMono-700.ttf")):
        pdfmetrics.registerFont(TTFont(name, str(FONTS / f)))

    W, H = A4
    M = 52                      # 18mm margin
    RIGHT = W - M
    c = canvas.Canvas(str(path), pagesize=A4)
    c.setTitle("Mitali Chincholikar \u2014 Curriculum Vitae")
    c.setAuthor("Mitali Chincholikar")
    c.setSubject("Computer Science student, first year")

    y = H - M

    # ── header
    c.setFillColor(INK)
    c.setFont("InterBold", 27)
    c.drawString(M, y - 26, CONTENT["name"])

    y -= 26 + 20
    c.setFillColor(MID)
    c.setFont("Inter", 11)
    c.drawString(M, y, CONTENT["role"])

    y -= 17
    c.setFillColor(SOFT)
    c.setFont("Mono", 7.6)
    line = f"{CONTENT['place'].upper()}   \u00b7   {CONTENT['email']}"
    c.drawString(M, y, line)

    y -= 16
    c.setStrokeColor(ACCENT)
    c.setLineWidth(2)
    c.line(M, y, M + 46, y)
    c.setStrokeColor(RULE)
    c.setLineWidth(0.8)
    c.line(M + 52, y + 1, RIGHT, y + 1)

    # ── body
    TEXT_W = RIGHT - M

    def wrap(text, font, size, width):
        words, lines, cur = text.split(), [], ""
        for w in words:
            t = (cur + " " + w).strip()
            if pdfmetrics.stringWidth(t, font, size) <= width:
                cur = t
            else:
                lines.append(cur)
                cur = w
        if cur:
            lines.append(cur)
        return lines

    def section(key, y):
        head_h = 30
        c.setFillColor(ACCENT)
        c.setFont("MonoBold", 7.4)
        c.drawString(M, y, TITLES[key].upper())
        tw = pdfmetrics.stringWidth(TITLES[key].upper(), "MonoBold", 7.4)
        c.setStrokeColor(ACCENT_SOFT)
        c.setLineWidth(1.4)
        c.line(M, y - 5, M + tw + 2, y - 5)
        c.setStrokeColor(RULE)
        c.setLineWidth(0.8)
        c.line(M + tw + 12, y - 4.5, RIGHT, y - 4.5)
        return y - head_h

    def para(text, y, size=9.4, font="Inter", lead=14.4, color=MID, indent=0):
        c.setFillColor(color)
        c.setFont(font, size)
        for ln in wrap(text, font, size, TEXT_W - indent):
            c.drawString(M + indent, y, ln)
            y -= lead
        return y

    y = section("summary", y)
    y = para(CONTENT["summary"], y, lead=15.4) - 12

    y = section("education", y)
    for when, org, title, notes in CONTENT["education"]:
        c.setFillColor(SOFT)
        c.setFont("Mono", 7.4)
        c.drawString(M, y, when.upper())
        c.setFillColor(INK)
        c.setFont("InterMed", 10.4)
        c.drawString(M + 96, y, org)
        y -= 13.5
        c.setFillColor(MID)
        c.setFont("Inter", 9.2)
        c.drawString(M + 96, y, title)
        y -= 12.5
        for n in notes:
            c.setFillColor(SOFT)
            c.setFont("Inter", 8.6)
            c.drawString(M + 96, y, "\u2013  " + n)
            y -= 11.6
        y -= 14

    y = section("skills", y)
    for label, value in CONTENT["skills"]:
        c.setFillColor(INK)
        c.setFont("InterMed", 9.4)
        c.drawString(M, y, label)
        c.setFillColor(MID)
        c.setFont("Inter", 9.4)
        c.drawString(M + 96, y, value)
        y -= 17
    y -= 12

    y = section("activity", y)
    for role, org, note in CONTENT["activity"]:
        c.setFillColor(INK)
        c.setFont("InterMed", 10)
        c.drawString(M, y, role)
        x = M + 96
        if org:
            c.setFillColor(SOFT)
            c.setFont("Inter", 9)
            c.drawString(x, y, org)
            x += pdfmetrics.stringWidth(org, "Inter", 9) + 10
        c.setFillColor(MID)
        c.setFont("Inter", 9)
        c.drawString(x, y, "\u2014  " + note)
        y -= 17

    # ── footer
    c.setStrokeColor(RULE)
    c.setLineWidth(0.8)
    c.line(M, M + 22, RIGHT, M + 22)
    c.setFillColor(SOFT)
    c.setFont("Mono", 7)
    c.drawString(M, M + 10, CONTENT["footer"])
    c.drawRightString(RIGHT, M + 10, "1 / 1")

    c.showPage()
    c.save()
    return path


# ══ DOCX ═══════════════════════════════════════════════════════════════════
def build_docx(path):
    from docx import Document
    from docx.shared import Pt, RGBColor, Cm
    from docx.enum.text import WD_ALIGN_PARAGRAPH
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
    st.font.size = Pt(9.5)
    st.font.color.rgb = rgb(MID)
    st.paragraph_format.space_after = Pt(0)
    st.paragraph_format.line_spacing = 1.25
    st.element.rPr.rFonts.set(qn("w:eastAsia"), "Inter")

    def para(text, size=9.5, color=MID, bold=False, before=0, after=0,
             spacing=1.25, font="Inter"):
        p = d.add_paragraph()
        p.paragraph_format.space_before = Pt(before)
        p.paragraph_format.space_after = Pt(after)
        p.paragraph_format.line_spacing = spacing
        r = p.add_run(text)
        r.font.size = Pt(size)
        r.font.color.rgb = rgb(color)
        r.font.bold = bold
        r.font.name = font
        return p

    def rule(color=RULE, size=6):
        p = d.add_paragraph()
        p.paragraph_format.space_before = Pt(2)
        p.paragraph_format.space_after = Pt(0)
        pPr = p._p.get_or_add_pPr()
        pbdr = OxmlElement("w:pBdr")
        bottom = OxmlElement("w:bottom")
        bottom.set(qn("w:val"), "single")
        bottom.set(qn("w:sz"), str(size))
        bottom.set(qn("w:space"), "1")
        bottom.set(qn("w:color"), color.lstrip("#"))
        pbdr.append(bottom)
        pPr.append(pbdr)

    def heading(text):
        para(text.upper(), size=7.6, color=ACCENT, bold=True, before=14,
             after=5, font="Courier New")
        rule()

    para(CONTENT["name"], size=26, color=INK, bold=True, after=2)
    para(CONTENT["role"], size=11.5, color=MID, after=4)
    para(f"{CONTENT['place'].upper()}   \u00b7   {CONTENT['email']}",
         size=8, color=SOFT, font="Courier New", after=6)
    rule(ACCENT, 12)

    heading(TITLES["summary"])
    para(CONTENT["summary"], after=2)

    heading(TITLES["education"])
    for when, org, title, notes in CONTENT["education"]:
        para(when.upper(), size=7.6, color=SOFT, font="Courier New",
             before=4)
        para(org, size=10.5, color=INK, bold=True)
        para(title, size=9.2, color=MID)
        for n in notes:
            para("\u2013  " + n, size=9, color=SOFT)

    heading(TITLES["skills"])
    for label, value in CONTENT["skills"]:
        p = d.add_paragraph()
        p.paragraph_format.space_after = Pt(2)
        r = p.add_run(f"{label}   ")
        r.font.bold = True
        r.font.size = Pt(9.5)
        r.font.color.rgb = rgb(INK)
        r2 = p.add_run(value)
        r2.font.size = Pt(9.5)
        r2.font.color.rgb = rgb(MID)

    heading(TITLES["activity"])
    for role, org, note in CONTENT["activity"]:
        p = d.add_paragraph()
        p.paragraph_format.space_after = Pt(3)
        r = p.add_run(role)
        r.font.bold = True
        r.font.size = Pt(10)
        r.font.color.rgb = rgb(INK)
        rest = "   " + (org + "   " if org else "") + "\u2014  " + note
        r2 = p.add_run(rest)
        r2.font.size = Pt(9)
        r2.font.color.rgb = rgb(MID)

    para(CONTENT["footer"], size=7.5, color=SOFT, before=16,
         font="Courier New")

    d.core_properties.title = "Mitali Chincholikar \u2014 Curriculum Vitae"
    d.core_properties.author = "Mitali Chincholikar"
    d.save(str(path))
    return path


# ══ TXT ════════════════════════════════════════════════════════════════════
def build_txt(path):
    def rule(ch="=", n=74):
        return ch * n

    L = []
    a = L.append
    a(CONTENT["name"].upper())
    a(CONTENT["role"])
    a(f"{CONTENT['place']}  |  {CONTENT['email']}")
    a(rule("="))
    a("")

    a(TITLES["summary"].upper())
    a(rule("-"))
    import textwrap
    for line in textwrap.wrap(CONTENT["summary"], 74):
        a(line)
    a("")

    a(TITLES["education"].upper())
    a(rule("-"))
    for when, org, title, notes in CONTENT["education"]:
        a(f"{when}")
        a(f"  {org}")
        a(f"  {title}")
        for n in notes:
            a(f"    - {n}")
        a("")

    a(TITLES["skills"].upper())
    a(rule("-"))
    for label, value in CONTENT["skills"]:
        a(f"{label}:")
        for line in textwrap.wrap(value, 68):
            a(f"    {line}")
    a("")

    a(TITLES["activity"].upper())
    a(rule("-"))
    for role, org, note in CONTENT["activity"]:
        head = role + (f"  |  {org}" if org else "")
        a(head)
        a(f"    {note}")
    a("")
    a(rule("="))
    a(CONTENT["footer"])

    text = "\n".join(L)
    # pure ASCII, CRLF, so Notepad on any Windows box shows it correctly
    ascii_text = (text.replace("\u2014", "-").replace("\u00b7", "|")
                      .replace("\u2019", "'").replace("\u2013", "-"))
    ascii_text = ascii_text.encode("ascii", "replace").decode("ascii")
    path.write_bytes(ascii_text.replace("\n", "\r\n").encode("ascii"))
    return path


def main():
    OUT.mkdir(exist_ok=True)
    for name, fn in (("resume.pdf", build_pdf),
                     ("resume.docx", build_docx),
                     ("resume.txt", build_txt)):
        p = fn(OUT / name)
        print(f"  {name:<14}{p.stat().st_size / 1024:7.1f} KB")


if __name__ == "__main__":
    main()
