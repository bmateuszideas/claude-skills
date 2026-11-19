# Dive into Deep Learning (d2l.ai)

Knowledge-base plugin compiled from **Dive into Deep Learning** by Aston Zhang, Zachary C.
Lipton, Mu Li and Alexander J. Smola — free at [d2l.ai](https://d2l.ai), open source at
[d2l-ai/d2l-en](https://github.com/d2l-ai/d2l-en), licensed **CC BY-SA 4.0** (sample code MIT).
26 chapters indexed.

## What is in here

| File | Contents |
|------|----------|
| `skills/dive-into-deep-learning/SKILL.md` | Core frameworks, chapter index, topic index (resident, under 4k tokens) |
| `skills/dive-into-deep-learning/chapters/` | 26 chapter files, one per book chapter — loaded on demand, each with a **2026 delta** section |
| `skills/dive-into-deep-learning/glossary.md` | Key terms, alphabetized, with chapter |
| `skills/dive-into-deep-learning/patterns.md` | Techniques and design patterns with trade-offs |
| `skills/dive-into-deep-learning/cheatsheet.md` | Decision tables: task→model, loss→task, optimizer→situation, debugging ladder |
| `skills/dive-into-deep-learning/references/rights_and_provenance.md` | License basis (CC BY-SA 4.0) and compilation details |
| `LICENSE`, `LICENSE-SAMPLECODE` | Full CC BY-SA 4.0 / MIT texts from the source repo |

## Use

```
/cs:dive-into-deep-learning                    # core frameworks + chapter index
/cs:dive-into-deep-learning <topic>            # resolve via topic index, read one chapter
/cs:dive-into-deep-learning ch14               # read one chapter file
```

Or invoke the `cs-dive-into-dl-tutor` agent for a working session anchored to this source.

## Provenance and limits

**Source:** d2l.ai online edition (v1.0.3), source repo `d2l-ai/d2l-en` @ main, cloned 2026-11-19.
Compiled with the `engineering/book-to-skill` pipeline shape (extract → synthesize → validate).
This package is **original synthesis**: it indexes the book's structure and concepts and never
reproduces its text at length. Chapter numbering follows the book's TOC; the bibliography chapter
is not compiled. The book's pinned versions (torch 2.0.0 etc.) are 2023-era — every chapter file
carries a 2026 delta; read the living d2l.ai for current code.

**Attribution:** Zhang, A., Lipton, Z. C., Li, M., & Smola, A. J. (2023). *Dive into Deep
Learning*. https://d2l.ai — CC BY-SA 4.0. This package is adapted material under CC BY-SA 4.0 and
is not endorsed by the authors.
