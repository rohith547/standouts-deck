# Standout Projects — Speaker Deck

A focused, present-it-out-loud deck of my five flagship projects. Every slide
carries a full **orator script in the speaker-notes pane**: hook → story →
the hard part → a line to land it, plus likely Q&A.

- **Output:** [`Standout-Projects-Speaker-Deck.pptx`](./Standout-Projects-Speaker-Deck.pptx) (8 slides)
- Projects: CommandCore · Beacon · Skills Hub · Financial Intelligence · Rent-tracker
- Branding matches the [portfolio deck](https://github.com/rohith547/ai-portfolio-deck).

> **Tip:** Present in PowerPoint/Keynote with *Presenter View* so the speaker
> notes show on your screen while the audience sees only the slide.

## Build

```bash
python3 -m venv .venv
.venv/bin/pip install python-pptx
.venv/bin/python build_standouts.py
```

Edit `build_standouts.py` (single source of truth) and re-run to regenerate.
