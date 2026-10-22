#!/usr/bin/env python3
"""Profile brief — the questionnaire, as a document.

One source of content, two outputs:

    MITALI-BRIEF.md     markdown, readable anywhere
    MITALI-BRIEF.docx   printable, fillable Word document
    MITALI-BRIEF.txt    plain ASCII, opens in Notepad on any Windows

Run: python3 build_brief.py
"""
import pathlib

from docx import Document
from docx.enum.section import WD_SECTION
from docx.enum.text import WD_ALIGN_PARAGRAPH
from docx.oxml import OxmlElement
from docx.oxml.ns import qn
from docx.shared import Pt, RGBColor, Inches

HERE = pathlib.Path(__file__).parent

INK   = RGBColor(0x07, 0x06, 0x0A)
ASH   = RGBColor(0x6B, 0x64, 0x70)
VERM  = RGBColor(0xC1, 0x27, 0x2D)
CREAM = RGBColor(0x2A, 0x25, 0x30)

TITLE = "PROFILE BRIEF"
SUB   = "Mitali Chincholikar"
HANDLE = "github.com/Mitali-Chincholikar"

INTRO = (
    "Answer these and I can build the whole page without guessing. Nothing gets invented "
    "\u2014 if a question goes unanswered, that line simply comes off the page. Answer with the "
    "numbers, in any order, in any format. Half-answers and \u201cidk\u201d are fine and useful."
)

HOW = [
    ("\u2b25  You can skip anything.",
     "Every question is optional. Skipping one changes what the page says, never whether it works."),
    ("\u2b25  \u201cNone yet\u201d is a real answer.",
     "You are in first year. A page that admits that and then shows what you are reaching for is "
     "stronger than one padded with fake projects."),
    ("\u2b25  The starred questions matter most.",
     "They set the structure. Everything else is decoration on top."),
    ("\u2b25  Answer in your own words.",
     "I would rather use a slightly awkward sentence you actually wrote than a smooth one that "
     "sounds like every other profile."),
]

PARTS = [
    ("PART 0 \u00b7 ALREADY ANSWERED", "Confirm or correct these three. Nothing else in this part.", [
        ("Your GitHub handle is Mitali-Chincholikar.", "Confirm \u2014 username changes break every link we build."),
        ("Your name is Mitali Chincholikar.", "Confirm the exact spelling. One wrong letter is a link that 404s."),
        ("You are heading toward web / app development.", "Confirm, or redirect me."),
    ]),
    ("PART 1 \u00b7 IDENTITY", "The top third of the page. What a stranger reads in ten seconds.", [
        ("\u2605 Full name, exactly as you want it printed \u2014 capitalisation included.", "It becomes the biggest text on the page. \u201cMITALI CHINCHOLIKAR\u201d reads very differently from \u201cMitali\u201d."),
        ("\u2605 One line \u2014 what do you want to be known for? Two to six words.", "This is the only sentence most visitors will read. It replaces \u201cpassionate developer\u201d."),
        ("Three words you would want a stranger to use about you after ten seconds.", "Sets the tone of the whole page: calm, sharp, curious, relentless \u2014 each one designs differently."),
        ("Do you want your age or year level shown?", "You do not have to. First-year is a flex in a scene where everyone pretends to be senior."),
        ("What do you want the very first frame of the page to be \u2014 your name, or a symbol?", "The opening plays before anything is read. It decides whether the page feels like a poster or a document."),
    ]),
    ("PART 2 \u00b7 COLLEGE", "The factual spine. Short answers are perfect.", [
        ("\u2605 College name, exactly as it is written officially.", "It appears on the record card. I will not guess at the spelling."),
        ("\u2605 City.", "City only \u2014 no address, no hostel, nothing that pinpoints you."),
        ("\u2605 Branch \u2014 or \u201cundecided\u201d if that is the truth.", "Undecided is a fine answer and I will write it plainly."),
        ("Which semester or year are you in?", "Used for one line of context, not a countdown."),
        ("Any club, society, team or event you are part of?", "Optional. A club is more interesting than a CGPA."),
    ]),
    ("PART 3 \u00b7 SKILLS & BUILDING", "What is real right now, and what you are reaching for. This is where most profiles lie; we will not.", [
        ("\u2605 What do you actually want to learn next \u2014 in order?", "The page will show this as a live queue. It is honest, it updates, and it reads like momentum."),
        ("Languages you have touched, even once \u2014 Python, C, Java, HTML, anything.", "\u201cTouched\u201d is the honest word. I will present it as exposure, not mastery."),
        ("Tools you can open without fear \u2014 VS Code, Git, Figma, Canva, anything.", "Determines whether the page shows a toolkit strip or stays quiet."),
        ("Can you build anything end-to-end right now? If yes, what?", "If yes, this becomes the one real card on the page."),
        ("A project you are planning, even a vague idea.", "Planned projects can be shown as \u201con the bench\u201d \u2014 labelled as not built yet. Never as finished work."),
        ("Do you want a \u201ccurrently learning\u201d strip on the page?", "Yes / no. It is the single most honest element a first-year profile can have."),
        ("\u2605 Do you want skill meters \u2014 bars with percentages?", "Only if you will give me real numbers. On a first-year profile they usually read as invented. My advice: no bars, say what you are learning instead."),
        ("Which operating system do you use?", "Tiny detail. Sometimes becomes a line in the footer. Sometimes nothing."),
    ]),
    ("PART 4 \u00b7 TASTE", "How it looks and moves. The part most people get wrong on their own profiles.", [
        ("\u2605 Pick a mood: dark and cinematic / clean and light / warm and editorial / loud.", "This changes every colour, every font and every animation on the page."),
        ("\u2605 A colour you genuinely like.", "A name is enough \u2014 \u201cochre\u201d, \u201cdeep green\u201d, \u201cice blue\u201d. It becomes the accent."),
        ("A colour you hate, so I never use it.", "Seriously. One wrong accent ruins a page."),
        ("Serif, sans, or monospace-heavy?", "Serif reads editorial and expensive. Sans reads modern and quiet. Mono reads technical."),
        ("Do you want the page to move \u2014 or sit still and be calm?", "This one is mine to build, yours to choose. Motion is not always better. A short, confident opening beats a busy page."),
        ("Any film, poster, album cover or website whose look you love? A link is enough.", "The fastest way to get the feel right is a reference I can actually look at."),
        ("Should the page have a light version for daytime readers?", "GitHub supports both. Costs me one extra file. Costs you nothing."),
        ("Anything you do NOT want to see \u2014 cartoon, emoji, gradients, glassy cards, anything?", "Name it and it is banned. This is yours, not mine."),
    ]),
    ("PART 5 \u00b7 PRESENCE", "What a visitor can click. Every link must lead somewhere real, or it comes off.", [
        ("Email \u2014 should it be on the page, and which address?", "It will be public and scraped by bots. A dedicated address is safer than your personal one."),
        ("LinkedIn \u2014 paste the link, or say no.", "Optional. But it is the one link recruiters actually use."),
        ("Instagram, X, or any other handle?", "Optional. Only if you want it public."),
        ("Do you have a personal site or portfolio?", "If not, we leave the slot out entirely rather than linking to nothing."),
        ("Discord username, if you want it shown?", "Optional."),
        ("Should the email be a clickable link or drawn as plain text?", "Clickable is friendlier. Plain text resists scrapers. Your call."),
    ]),
    ("PART 6 \u00b7 VOICE", "The words. This is what makes a page sound like a person instead of a template.", [
        ("\u2605 Finish this sentence: \u201cI am in first year, and I am here to \u2026\u201d", "Your ending becomes a line on the page, possibly the best one."),
        ("Write one sentence you would actually say out loud about why you want to build things.", "I will polish it. I will not replace it."),
        ("Do you want a quote on the page? Whose?", "Otherwise we use your own words, which is almost always better."),
        ("Any words you hate seeing on profiles \u2014 \u201cpassionate\u201d, \u201caspiring\u201d, \u201centhusiast\u201d, \u201cgo-getter\u201d?", "Banned list. I take this one personally."),
        ("First person (\u201cI build\u201d) or third person (\u201cshe builds\u201d)?", "First person is warmer. Third person reads like a press release."),
        ("How much writing \u2014 one screen, a short scroll, or a long read?", "Most good profiles are one screen. I will not pad it."),
    ]),
    ("PART 7 \u00b7 BOUNDARIES", "Short part. Important part.", [
        ("\u2605 Anything that must NOT appear \u2014 school name, phone number, photos, marks?", "Hard exclusions. I will build around them."),
        ("Are you comfortable with your college and city being public on the page?", "Yes / no. It is normal, but it is your decision, not mine."),
        ("Do you want a photo, an avatar, or an abstract mark instead?", "A mark is safer and often looks better. A photo makes it personal. Both are valid."),
        ("Anything you want to be credited or tagged for?", "Only if it is real and you would stand behind it."),
    ]),
    ("PART 8 \u00b7 RAPID FIRE", "One word each. No thinking. These decide the small details \u2014 the footer, the opening frame, the footnote.", [
        ("Tea or coffee?", "Ends up somewhere small and true."),
        ("Night or morning?", "Sets whether the page reads as late-night or early-start."),
        ("Headphones or speakers?", "Soundtrack question \u2014 even though the page is silent."),
        ("Dark interface or light interface, when you are the user?", "Not the same as how your profile should look. Useful to know both."),
        ("Tabs or spaces?", "A joke that costs one line. Only if you find it funny."),
        ("One app you could not live without?", "Often becomes a footnote detail."),
        ("One song you would put over a trailer of your life?", "I will not embed audio, but the mood bleeds into the type and motion."),
        ("If your page had a soundtrack, one word for it?", "Sharp? Warm? Fast? Slow? One word."),
    ]),
]

MAPPING = [
    ("Mood + colour", "Every palette, font and motion curve on the page."),
    ("The one-line claim", "The biggest text in the opening frame."),
    ("College + city + branch", "The record card \u2014 the four-line fact block under the title."),
    ("\u201cWant to learn next\u201d", "The learning queue: a live, updating list. Only used if you answer it."),
    ("Planned projects", "An \u201con the bench\u201d strip, clearly labelled as unbuilt."),
    ("Banned words + banned visuals", "A strict filter applied to every string I write."),
    ("Finish-the-sentence answer", "The closing line, in your voice, lightly edited."),
    ("Rapid fire", "The footer. One or two details, no more."),
]

MUST = [
    "Full name (exact spelling)",
    "The one line \u2014 what you want to be known for",
    "College name and city",
    "Branch, or \u201cundecided\u201d",
    "What you want to learn next",
    "Mood, and one colour you like",
    "\u201cI am in first year, and I am here to \u2026\u201d",
    "Anything that must NOT appear",
]

CLOSING = (
    "That is everything. Send back whatever you have \u2014 numbered or unnumbered, "
    "typed or photographed. I will build the page from the answers that exist and cut "
    "the lines that do not."
)


# ── markdown ────────────────────────────────────────────────────────────────
def build_md():
    out = [
        f"# {TITLE}",
        "",
        f"**{SUB}** \u00b7 `{HANDLE}`",
        "",
        INTRO,
        "",
        "---",
        "",
        "## How to use this",
        "",
    ]
    for head, body in HOW:
        out += [f"- **{head}**", f"  {body}", ""]
    out += ["---", ""]

    for part, blurb, qs in PARTS:
        out += [f"## {part}", "", f"_{blurb}_", ""]
        for i, (q, why) in enumerate(qs, 1):
            out += [f"**{i}.** {q}", "", f"> {why}", "", "> `Answer:` ", ""]
        out += ["", ]
    out += ["---", ""]
    out += ["## How the answers turn into the page", ""]
    out += ["| Answer | Becomes |", "|---|---|"]
    out += [f"| {a} | {b} |" for a, b in MAPPING]
    out += ["", "---", ""]
    out += ["## Must have \u2014 the short list", ""]
    out += ["If you answer nothing else, answer these eight:", ""]
    out += [f"{i}. {m}" for i, m in enumerate(MUST, 1)]
    out += ["", "---", "", CLOSING, ""]
    return "\n".join(out)


# ── docx helpers ────────────────────────────────────────────────────────────
def shade(par, hex_fill):
    pPr = par._p.get_or_add_pPr()
    shd = OxmlElement("w:shd")
    shd.set(qn("w:val"), "clear")
    shd.set(qn("w:color"), "auto")
    shd.set(qn("w:fill"), hex_fill)
    pPr.append(shd)


def rule(par):
    pPr = par._p.get_or_add_pPr()
    borders = OxmlElement("w:pBdr")
    bottom = OxmlElement("w:bottom")
    bottom.set(qn("w:val"), "single")
    bottom.set(qn("w:sz"), "6")
    bottom.set(qn("w:space"), "4")
    bottom.set(qn("w:color"), "C1272D")
    borders.append(bottom)
    pPr.append(borders)


def add(par, text, size=10.5, bold=False, italic=False, color=INK, font="Calibri", spacing=None):
    r = par.add_run(text)
    r.font.size = Pt(size)
    r.font.bold = bold
    r.font.italic = italic
    r.font.color.rgb = color
    r.font.name = font
    if spacing:
        rPr = r._element.get_or_add_rPr()
        sp = OxmlElement("w:spacing")
        sp.set(qn("w:val"), str(int(spacing * 20)))
        rPr.append(sp)
    return r


def build_docx():
    doc = Document()

    st = doc.styles["Normal"]
    st.font.name = "Calibri"
    st.font.size = Pt(10.5)
    st.paragraph_format.space_after = Pt(4)
    st.paragraph_format.line_spacing = 1.25

    for s in doc.sections:
        s.top_margin = Inches(0.85)
        s.bottom_margin = Inches(0.85)
        s.left_margin = Inches(0.95)
        s.right_margin = Inches(0.95)

    # cover
    p = doc.add_paragraph()
    p.paragraph_format.space_before = Pt(90)
    add(p, TITLE, size=34, bold=True, color=INK, font="Georgia")

    p = doc.add_paragraph()
    add(p, SUB, size=15, color=VERM, font="Georgia")
    p.paragraph_format.space_after = Pt(2)

    p = doc.add_paragraph()
    add(p, HANDLE, size=9.5, color=ASH, font="Consolas")
    rule(p)
    p.paragraph_format.space_after = Pt(26)

    p = doc.add_paragraph()
    add(p, INTRO, size=11, color=CREAM, font="Georgia")

    p = doc.add_paragraph()
    p.paragraph_format.space_before = Pt(30)
    add(p, "A GitHub profile is read in about eleven seconds. "
           "These questions are the only thing standing between those eleven seconds "
           "and a page that sounds like everybody else.", size=10, italic=True, color=ASH)

    doc.add_page_break()

    # how
    p = doc.add_paragraph()
    add(p, "HOW TO USE THIS", size=11, bold=True, color=VERM, font="Consolas", spacing=2.2)
    rule(p)

    for head, body in HOW:
        p = doc.add_paragraph()
        p.paragraph_format.space_before = Pt(10)
        add(p, head, size=10.5, bold=True, color=INK)
        p = doc.add_paragraph()
        p.paragraph_format.left_indent = Inches(0.18)
        add(p, body, size=9.8, color=CREAM)

    # parts
    for part, blurb, qs in PARTS:
        p = doc.add_paragraph()
        p.paragraph_format.space_before = Pt(26)
        add(p, part, size=11, bold=True, color=VERM, font="Consolas", spacing=2.2)
        rule(p)
        p = doc.add_paragraph()
        add(p, blurb, size=9.5, italic=True, color=ASH)
        p.paragraph_format.space_after = Pt(8)

        for i, (q, why) in enumerate(qs, 1):
            p = doc.add_paragraph()
            p.paragraph_format.space_before = Pt(11)
            p.paragraph_format.keep_together = True
            add(p, f"{i:02d}   ", size=10, bold=True, color=VERM, font="Consolas")
            add(p, q, size=10.5, bold=True, color=INK)

            p = doc.add_paragraph()
            p.paragraph_format.left_indent = Inches(0.34)
            add(p, why, size=9, italic=True, color=ASH)

            p = doc.add_paragraph()
            p.paragraph_format.left_indent = Inches(0.34)
            p.paragraph_format.space_before = Pt(3)
            p.paragraph_format.space_after = Pt(9)
            shade(p, "F6F3EE")
            add(p, "  Answer:  ", size=9, color=ASH, font="Consolas")

    # mapping
    p = doc.add_paragraph()
    p.paragraph_format.space_before = Pt(26)
    add(p, "HOW THE ANSWERS TURN INTO THE PAGE", size=11, bold=True, color=VERM, font="Consolas", spacing=2.2)
    rule(p)
    p = doc.add_paragraph()
    add(p, "Nothing in the build is decorative by accident. Each answer drives a specific element.",
        size=9.5, italic=True, color=ASH)
    p.paragraph_format.space_after = Pt(8)

    table = doc.add_table(rows=1, cols=2)
    table.autofit = True
    hdr = table.rows[0].cells
    for cell, txt in zip(hdr, ("Answer", "Becomes")):
        cell.text = ""
        add(cell.paragraphs[0], txt, size=9, bold=True, color=VERM, font="Consolas", spacing=1.4)
    for a, b in MAPPING:
        row = table.add_row().cells
        row[0].text = ""
        row[1].text = ""
        add(row[0].paragraphs[0], a, size=9.5, color=INK)
        add(row[1].paragraphs[0], b, size=9.5, color=CREAM)

    # must
    p = doc.add_paragraph()
    p.paragraph_format.space_before = Pt(26)
    add(p, "MUST HAVE \u2014 THE SHORT LIST", size=11, bold=True, color=VERM, font="Consolas", spacing=2.2)
    rule(p)
    p = doc.add_paragraph()
    add(p, "If she only answers eight things, it should be these eight.", size=9.5, italic=True, color=ASH)

    for i, m in enumerate(MUST, 1):
        p = doc.add_paragraph()
        p.paragraph_format.left_indent = Inches(0.2)
        p.paragraph_format.space_before = Pt(5)
        add(p, "\u25a1  ", size=11, color=VERM)
        add(p, m, size=10.2, color=INK)

    p = doc.add_paragraph()
    p.paragraph_format.space_before = Pt(30)
    add(p, CLOSING, size=10, italic=True, color=CREAM)
    rule(p)

    p = doc.add_paragraph()
    add(p, "  BUILT IN THE SAME INK AS YOURS \u00b7 NONE OF THE SAME VOCABULARY",
        size=8, color=ASH, font="Consolas", spacing=2.0)

    out = HERE / "MITALI-BRIEF.docx"
    doc.save(out)
    return out


# ── plain text (Notepad-proof) ──────────────────────────────────────────────
ASCII = {
    "\u2b25": "*", "\u2605": "*", "\u00b7": "-", "\u2014": "--", "\u2013": "-",
    "\u2018": "'", "\u2019": "'", "\u201c": '"', "\u201d": '"',
    "\u2026": "...", "\u25a1": "[ ]", "\u2192": "->", "\u00a0": " ",
}


def ascii_only(text):
    for bad, good in ASCII.items():
        text = text.replace(bad, good)
    return (text.encode("ascii", "replace")).decode("ascii")


def wrap(text, width=76, indent=""):
    words, lines, cur = text.split(), [], ""
    for w in words:
        if len(cur) + len(w) + 1 > width:
            lines.append(cur)
            cur = w
        else:
            cur = (cur + " " + w).strip()
    if cur:
        lines.append(cur)
    return "\n".join(indent + ln for ln in lines)


def build_txt():
    BAR = "=" * 78
    THIN = "-" * 78
    out = [
        BAR,
        "  PROFILE BRIEF",
        "  Mitali Chincholikar   github.com/Mitali-Chincholikar",
        BAR,
        "",
        wrap(ascii_only(INTRO)),
        "",
        "  A GitHub profile is read in about eleven seconds. These questions are",
        "  the only thing standing between those eleven seconds and a page that",
        "  sounds like everybody else.",
        "",
        THIN,
        "  HOW TO USE THIS",
        THIN,
        "",
    ]
    for head, body in HOW:
        out += [ascii_only(head), wrap(ascii_only(body), indent="   "), ""]

    out += [THIN, ""]
    for part, blurb, qs in PARTS:
        out += [BAR, "  " + ascii_only(part), BAR, ""]
        out += [wrap(ascii_only(blurb), indent="  "), ""]
        for i, (q, why) in enumerate(qs, 1):
            out += [f"  {i:02d}.  " + ascii_only(q)]
            out += [wrap(ascii_only(why), indent="        ") ]
            out += ["", "        ANSWER:", ""]
        out += [""]

    out += [BAR, "  HOW THE ANSWERS TURN INTO THE PAGE", BAR, ""]
    for a, b in MAPPING:
        out += [f"  {ascii_only(a)}", wrap(ascii_only(b), indent="      "), ""]

    out += [BAR, "  MUST HAVE -- THE SHORT LIST", BAR, ""]
    out += ["  If she only answers eight things, it should be these eight:", ""]
    for m in MUST:
        out += ["  [ ]  " + ascii_only(m)]

    out += ["", BAR, ""]
    out += [wrap(ascii_only(CLOSING)), "", BAR, ""]
    out += ["  BUILT IN THE SAME INK AS YOURS -- NONE OF THE SAME VOCABULARY", ""]

    text = "\n".join(out)
    text = ascii_only(text)
    return text.replace("\n", "\r\n")   # CRLF, so Notepad on Windows is happy


if __name__ == "__main__":
    md = build_md()
    (HERE / "MITALI-BRIEF.md").write_text(md, encoding="utf-8")
    print(f"wrote MITALI-BRIEF.md    {len(md):6d} bytes")
    p = build_docx()
    print(f"wrote {p.name}  {p.stat().st_size:6d} bytes")
    t = build_txt()
    (HERE / "MITALI-BRIEF.txt").write_text(t, encoding="ascii", newline="")
    print(f"wrote MITALI-BRIEF.txt   {len(t):6d} bytes  (ascii, CRLF)")
