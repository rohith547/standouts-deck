#!/usr/bin/env python3
"""One-page rehearsal cue cards (PDF) for the standout-projects speaker deck.

Just the spoken essentials \u2014 the 30-second pitch, each project's hook + the
one hard-part beat + the landing line, and the closing \u2014 so you can rehearse
without the laptop.
"""
from reportlab.lib.pagesizes import LETTER
from reportlab.lib.units import inch
from reportlab.lib.enums import TA_LEFT
from reportlab.lib.colors import HexColor
from reportlab.platypus import (
    BaseDocTemplate, PageTemplate, Frame, Paragraph, Spacer, HRFlowable,
)
from reportlab.lib.styles import ParagraphStyle

INK   = HexColor("#111827")
HEAD  = HexColor("#047857")
BAR   = HexColor("#10B981")
ACC2  = HexColor("#0369A1")
MUTED = HexColor("#6B7280")
RULE  = HexColor("#E5E7EB")

OUT = "Standout-Speaker-Cue-Cards.pdf"


def st(name, **kw):
    base = dict(fontName="Helvetica", fontSize=9.3, leading=12.6, textColor=INK,
                alignment=TA_LEFT, spaceBefore=0, spaceAfter=0)
    base.update(kw); return ParagraphStyle(name, **base)

S = {
    "title": st("title", fontName="Helvetica-Bold", fontSize=17, leading=19, textColor=INK),
    "sub":   st("sub", fontSize=9, leading=12, textColor=MUTED),
    "h":     st("h", fontName="Helvetica-Bold", fontSize=10, leading=12, textColor=HEAD,
                spaceBefore=7, spaceAfter=2),
    "proj":  st("proj", fontName="Helvetica-Bold", fontSize=10.5, leading=13, textColor=INK,
                spaceBefore=6, spaceAfter=1),
    "body":  st("body", fontSize=9.3, leading=12.8, textColor=INK),
    "mut":   st("mut", fontSize=8.8, leading=12, textColor=MUTED),
}


def hr():
    return HRFlowable(width="100%", thickness=0.7, color=RULE, spaceBefore=4, spaceAfter=2)


def on_page(c, d):
    c.saveState(); c.setFillColor(BAR)
    c.rect(0, 0, 0.16 * inch, LETTER[1], stroke=0, fill=1); c.restoreState()


LM, RM, TM, BM = 0.62 * inch, 0.55 * inch, 0.5 * inch, 0.45 * inch
doc = BaseDocTemplate(OUT, pagesize=LETTER, leftMargin=LM, rightMargin=RM,
                      topMargin=TM, bottomMargin=BM)
frame = Frame(LM, BM, LETTER[0] - LM - RM, LETTER[1] - TM - BM, id="m",
              leftPadding=0, rightPadding=0, topPadding=0, bottomPadding=0)
doc.addPageTemplates([PageTemplate(id="t", frames=[frame], onPage=on_page)])

E = []
E.append(Paragraph("Speaker Cue Cards \u2014 Standout Projects", S["title"]))
E.append(Paragraph("Rehearse out loud. Hook \u2192 pause \u2192 story \u2192 the hard part \u2192 landing line \u2192 stop.", S["sub"]))
E.append(hr())

E.append(Paragraph("OPEN \u2014 30-second pitch", S["h"]))
E.append(Paragraph(
    "\u201CI'm an AI Application Engineer \u2014 I use AI to turn ideas into production apps fast. I've shipped 75-plus "
    "across five domains. Today: five standouts \u2014 an agent control center, an autonomous video pipeline, my own "
    "reusable-skills system, financial-intelligence dashboards, and a bank-automation bot in production. The "
    "thread through all of them: real, working systems \u2014 not demos.\u201D", S["body"]))

cards = [
    ("01 \u00b7 CommandCore",
     "One chat window that understands what you want \u2014 and quietly dispatches the right specialist to do it.",
     "Hard part: orchestration \u2014 typed tools, persisted memory, restart-safe at 3am.",
     "That's the difference between a demo you show once and a system you can depend on."),
    ("02 \u00b7 Beacon",
     "Every morning a fresh AI news video gets made \u2014 and I barely touch it.",
     "Hard part: trust \u2014 fact-check BEFORE generate, checkpoint every stage, cost cap, human approves the publish.",
     "Automation people trust isn't about removing the human \u2014 it's putting the human in exactly the right place."),
    ("03 \u00b7 Skills Hub",
     "Here's how I build 75 apps without reinventing the wheel 75 times.",
     "Why it matters: 25 reusable skills wired into my AI CLI \u2014 compounding leverage, each project speeds up the next.",
     "Most engineers ship code. I also ship the system that ships the code."),
    ("04 \u00b7 Financial Intelligence",
     "I turn raw market filings into signals a person can act on in seconds.",
     "Hard part: messy, noisy data \u2014 normalize filings into a glanceable, trustworthy view (loading/error/empty/full).",
     "Data is everywhere. The value is in making it decision-ready."),
    ("05 \u00b7 Rent-tracker",
     "I had a boring monthly question \u2014 who actually paid rent? \u2014 so I automated the whole answer.",
     "Hard part: the bank fights automation \u2014 sessions die headless; fresh visible-browser logins + idempotent runs. "
     "(Private \u2014 offer a live 2-min walkthrough.)",
     "Unglamorous, real-world engineering that saves time every month \u2014 running in production right now."),
]
E.append(Paragraph("THE FIVE \u2014 hook / hard part / land it", S["h"]))
for name, hook, hard, land in cards:
    E.append(Paragraph(name, S["proj"]))
    E.append(Paragraph(f'<b>Hook:</b> \u201C{hook}\u201D', S["body"]))
    E.append(Paragraph(f'<font color="#047857"><b>Hard part:</b></font> {hard}', S["mut"]))
    E.append(Paragraph(f'<font color="#0369A1"><b>Land it:</b></font> \u201C{land}\u201D', S["body"]))

E.append(hr())
E.append(Paragraph("CLOSE \u2014 deliver slower, then stop", S["h"]))
E.append(Paragraph(
    "\u201CAcross all five, it's the same engineer working the same way: range across five domains, depth in agents "
    "and automation, and the discipline to make it reliable. I use AI as a multiplier \u2014 but verifying before "
    "generating, capping cost, keeping a human where it matters, that's the engineering.\u201D", S["body"]))
E.append(Spacer(1, 3))
E.append(Paragraph(
    "<b>Final line (look up, pause):</b> \u201CPoint me at a problem, and I\u2019ll turn it into a dependable, "
    "AI-powered product \u2014 fast, tested, and in production. That\u2019s what I do.\u201D", S["body"]))
E.append(Spacer(1, 4))
E.append(Paragraph(
    "Delivery reminders: smile on the open \u00b7 pause after every bold claim \u00b7 don't read bullets aloud \u00b7 "
    "end each project on the landing line and stop talking.", S["mut"]))

doc.build(E)
print(f"Wrote {OUT}")
