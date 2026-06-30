#!/usr/bin/env python3
"""Render the standout deck as a viewable landscape PDF (no GUI / Keynote needed).

Mirrors the on-screen slides (not the speaker notes) so the deck can be flipped
through on a phone. Same brand + content as build_standouts.py.
"""
from reportlab.pdfgen import canvas
from reportlab.lib.colors import HexColor
from reportlab.pdfbase.pdfmetrics import stringWidth

IN = 72.0
W, H = 13.333 * IN, 7.5 * IN

INK    = HexColor("#0B0E14")
PANEL  = HexColor("#11151F")
EDGE   = HexColor("#1E2533")
ACCENT = HexColor("#6EE7B7")
ACCENT2= HexColor("#38BDF8")
WHITE  = HexColor("#F3F4F6")
GRAY   = HexColor("#9CA3AF")
DIM    = HexColor("#6B7280")

OUT = "Standout-Projects-Speaker-Deck.pdf"
c = canvas.Canvas(OUT, pagesize=(W, H))

BOLD = "Helvetica-Bold"
REG = "Helvetica"


def Y(top_in):
    return H - top_in * IN


def rect(x, y, w, h, fill=None, stroke=None, sw=1.0, r=8):
    if fill is not None:
        c.setFillColor(fill)
    if stroke is not None:
        c.setStrokeColor(stroke); c.setLineWidth(sw)
    c.roundRect(x * IN, Y(y) - h * IN, w * IN, h * IN, r,
                fill=1 if fill is not None else 0,
                stroke=1 if stroke is not None else 0)


def srect(x, y, w, h, fill):
    c.setFillColor(fill)
    c.rect(x * IN, Y(y) - h * IN, w * IN, h * IN, fill=1, stroke=0)


def wrap(text, font, size, max_w_in):
    max_w = max_w_in * IN
    words = text.split(" ")
    lines, cur = [], ""
    for w in words:
        trial = (cur + " " + w).strip()
        if stringWidth(trial, font, size) <= max_w or not cur:
            cur = trial
        else:
            lines.append(cur); cur = w
    if cur:
        lines.append(cur)
    return lines


def para(x_in, top_in, max_w_in, runs, leading=1.15, gap=0.06):
    """runs: list of (text, size, color, bold). Each is a wrapped paragraph."""
    y = top_in
    for txt, size, color, bold in runs:
        font = BOLD if bold else REG
        c.setFillColor(color); c.setFont(font, size)
        lh = size * leading / IN
        for ln in wrap(txt, font, size, max_w_in):
            c.drawString(x_in * IN, Y(y) - size, ln)
            y += lh
        y += gap
    return y


def header(kicker, title):
    srect(0.6, 0.62, 0.09, 0.62, ACCENT)
    c.setFillColor(ACCENT); c.setFont(BOLD, 12)
    c.drawString(0.85 * IN, Y(0.5) - 12, kicker.upper())
    c.setFillColor(WHITE); c.setFont(BOLD, 30)
    c.drawString(0.85 * IN, Y(0.78) - 30, title)


def footer(n):
    c.setFillColor(DIM); c.setFont(REG, 9)
    c.drawString(0.6 * IN, Y(7.02) - 9, "Rohith Shabad  \u2022  AI Application Engineer")
    c.drawRightString(12.7 * IN, Y(7.02) - 9, f"{n:02d}")


def chips(x0, y0, items, max_w, color=WHITE, gap=0.12, line_h=0.44):
    cx, cy = x0, y0
    for it in items:
        w = 0.20 + 0.092 * len(it)
        if cx + w > x0 + max_w:
            cx = x0; cy += line_h
        rect(cx, cy, w, 0.34, fill=PANEL, stroke=EDGE, sw=0.75, r=5)
        c.setFillColor(color); c.setFont(REG, 10.5)
        c.drawCentredString((cx + w / 2) * IN, Y(cy + 0.17) - 5, it)
        cx += w + gap
    return cy + line_h


def bg():
    c.setFillColor(INK); c.rect(0, 0, W, H, fill=1, stroke=0)


# ---------------- 1. TITLE ----------------
bg()
srect(0, 0, 0.18, 7.5, ACCENT)
c.setFillColor(ACCENT); c.setFont(BOLD, 14)
c.drawString(1.0 * IN, Y(2.0) - 14, "STANDOUT PROJECTS  \u2022  SPEAKER DECK")
c.setFillColor(WHITE); c.setFont(BOLD, 50)
c.drawString(0.95 * IN, Y(2.45) - 50, "Rohith Shabad")
c.setFillColor(GRAY); c.setFont(REG, 20)
c.drawString(1.0 * IN, Y(3.55) - 20, "The five projects I lead with \u2014 and how to talk about them.")
c.setFillColor(GRAY); c.setFont(REG, 15)
c.drawString(1.0 * IN, Y(4.7) - 15, "Speaker scripts live in the .pptx Notes pane; cue cards in the companion PDF.")
c.showPage()

# ---------------- 2. LINEUP ----------------
bg(); header("Agenda", "The five standouts")
rows = [
    ("01  CommandCore", "Agent orchestration", "One chat that routes intent to specialized AI agents."),
    ("02  Beacon", "Content automation", "An AI news-video pipeline that ships itself daily."),
    ("03  Skills Hub", "Force-multiplier", "25 reusable skills wired into my AI command line."),
    ("04  Financial Intelligence", "Live data products", "Dashboards that turn market filings into signals."),
    ("05  Rent-tracker", "Production automation", "A bank-scraping bot that tracks who paid rent."),
]
y = 1.95
for tag, cat, d in rows:
    rect(0.85, y, 11.6, 0.86, fill=PANEL, stroke=EDGE)
    c.setFillColor(ACCENT); c.setFont(BOLD, 15)
    c.drawString(1.15 * IN, Y(y + 0.43) - 6, tag)
    c.setFillColor(ACCENT2); c.setFont(BOLD, 12)
    c.drawString(4.5 * IN, Y(y + 0.43) - 5, cat)
    c.setFillColor(GRAY); c.setFont(REG, 12.5)
    c.drawString(7.2 * IN, Y(y + 0.43) - 5, d)
    y += 1.0
footer(2)
c.showPage()


# ---------------- deep dives ----------------
def deep_dive(n, kicker, title, repo, hook, what, how, hard, tags):
    bg(); header(kicker, title)
    rect(0.85, 1.78, 11.6, 0.92, fill=PANEL, stroke=ACCENT, sw=1.25)
    c.setFillColor(WHITE); c.setFont(BOLD, 16)
    hk = wrap("\u201C" + hook + "\u201D", BOLD, 16, 11.0)
    hy = 2.05 if len(hk) > 1 else 2.18
    for ln in hk:
        c.drawString(1.15 * IN, Y(hy) - 16, ln); hy += 16 * 1.04 / IN
    cards = [("What it does", what, ACCENT), ("How it works", how, ACCENT2), ("Why it's hard", hard, ACCENT)]
    xs = [0.85, 4.92, 8.99]
    for (t, d, col), x in zip(cards, xs):
        rect(x, 2.95, 3.78, 2.55, fill=PANEL, stroke=EDGE)
        para(x + 0.28, 3.22, 3.25, [(t, 14, col, True), (d, 12, GRAY, False)], leading=1.1, gap=0.1)
    c.setFillColor(ACCENT2); c.setFont(BOLD, 12)
    c.drawString(0.85 * IN, Y(5.85) - 12, "Code  \u2192  ")
    c.setFillColor(GRAY); c.setFont(REG, 12)
    c.drawString((0.85 + 0.75) * IN, Y(5.85) - 12, repo)
    chips(0.85, 6.12, tags, max_w=11.6, color=WHITE)
    footer(n)
    c.showPage()


deep_dive(3, "Standout \u00b7 01", "CommandCore", "github.com/rohith547/commandcore",
    "Imagine one chat window that understands what you want \u2014 and quietly dispatches the right specialist to do it.",
    "A control center where you type a request and it routes that intent to the right specialized AI agent \u2014 each with its own tools and memory. Telegram + inline keyboards, zero learning curve.",
    "A router reads intent and hands off to an agent. State is persisted in a database, so it's restart-safe \u2014 reboot and it resumes exactly where it left off.",
    "Orchestration: typed tools, persisted memory, and getting multiple agents to cooperate without stepping on each other. That separates a system from a demo.",
    ["Node/TS", "Prisma", "OpenAI", "Telegram", "Agents", "Docker"])

deep_dive(4, "Standout \u00b7 02", "Beacon", "github.com/rohith547/beacon",
    "Every morning a fresh AI news video gets made \u2014 and I barely touch it.",
    "An end-to-end content pipeline: fetch the day's stories, verify them, write the script, generate a voice, render the video, publish. The one human step is a single approval tap.",
    "Stages run in sequence \u2014 fetch, verify, script, voice, video, publish \u2014 each checkpointed so a failure never burns the whole run. Cost is capped per run.",
    "Trust. LLMs hallucinate, so I fact-check BEFORE generating, checkpoint every stage, and keep a human at the one decision that matters \u2014 the publish.",
    ["Python", "OpenAI", "TTS", "ffmpeg", "cron", "Human-in-loop"])

deep_dive(5, "Standout \u00b7 03", "Skills Hub", "github.com/rohith547/skills-hub",
    "Here's how I build 75 apps without reinventing the wheel 75 times.",
    "25 reusable engineering 'skills' \u2014 my best patterns \u2014 distilled from across my projects, plus a browsable React app to explore them, with tests.",
    "Each skill is a documented folder wired into my AI command line, so every new build automatically follows my proven conventions instead of starting from scratch.",
    "Compounding leverage: every project makes the next one faster. It externalizes how I think, not just what I shipped \u2014 a system that builds systems.",
    ["React", "TypeScript", "Vite", "Vitest", "CLI", "Single-source"])

deep_dive(6, "Standout \u00b7 04", "Financial Intelligence", "github.com/rohith547/smart-money-13f",
    "I turn raw market filings into signals a person can act on in seconds.",
    "A family of live dashboards: smart-money-13f tracks what institutions buy, insider-tracker watches executives buying their own stock, macro-pulse scores the economy, fed-watch follows policy.",
    "Each pulls live financial data, normalizes messy filings, and renders a glanceable view \u2014 every component handles loading, error, empty and populated states.",
    "Financial data is messy and noisy. The value is distilling it into something trustworthy and decision-ready a human reads in seconds.",
    ["React", "TypeScript", "Tailwind", "Live data", "Dashboards", "Vercel"])

deep_dive(7, "Standout \u00b7 05", "Rent-tracker", "private repo \u2014 live walkthrough on request",
    "I had a boring monthly question \u2014 who actually paid rent? \u2014 so I automated the whole answer.",
    "A Telegram bot logs into the bank, reads transactions, fuzzy-matches each deposit to the right tenant, and reports \u20187 of 7 tenants paid\u2019 every cycle. No spreadsheets.",
    "It scrapes the bank, matches deposits to tenants by name and amount, and pings me on Telegram \u2014 counting unique tenants, not raw transactions.",
    "The bank fights automation \u2014 sessions expire instantly headless. Solved with fresh visible-browser logins, careful session handling, and idempotent runs so it never double-counts.",
    ["Python", "Playwright", "Telegram", "Fuzzy-match", "Idempotent", "Production"])

# ---------------- 8. THROUGH-LINE ----------------
bg()
srect(0, 0, 0.18, 7.5, ACCENT)
c.setFillColor(WHITE); c.setFont(BOLD, 40)
c.drawString(1.0 * IN, Y(1.55) - 40, "The through-line")
c.setFillColor(GRAY); c.setFont(REG, 18)
c.drawString(1.0 * IN, Y(2.55) - 18, "Five projects, one engineer, one consistent way of working.")
pillars = [
    ("Range + depth", "Agents, automation, tooling, live-data products, real-world reliability."),
    ("Systems, not demos", "Restart-safe, idempotent, checkpointed, tested \u2014 built to run unattended."),
    ("AI as a multiplier", "LLMs inside real products, with verification, cost caps and a human where it counts."),
]
x = 1.0
for t, d in pillars:
    rect(x, 3.5, 3.7, 1.7, fill=PANEL, stroke=EDGE)
    para(x + 0.3, 3.78, 3.15, [(t, 15, ACCENT, True), (d, 12, GRAY, False)], leading=1.1, gap=0.1)
    x += 3.9
rect(1.0, 5.5, 11.3, 1.0, fill=PANEL, stroke=ACCENT, sw=1.25)
c.setFillColor(ACCENT); c.setFont(BOLD, 14)
c.drawString(1.35 * IN, Y(6.0) - 6, "So what?")
c.setFillColor(WHITE); c.setFont(REG, 14)
msg = "Point me at a problem and I'll turn it into a dependable, AI-powered product \u2014 fast, tested, and in production."
c.drawString(2.35 * IN, Y(6.0) - 6, msg)
footer(8)
c.showPage()

c.save()
print(f"Wrote {OUT}")
