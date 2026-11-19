# Rights and Provenance — dive-into-deep-learning

**Not legal advice.** This documents the licensing basis for this package.

## Source
- **Book**: *Dive into Deep Learning*, Aston Zhang, Zachary C. Lipton, Mu Li, Alexander J. Smola.
- **Website**: https://d2l.ai · **Source repository**: https://github.com/d2l-ai/d2l-en (cloned at compile time, `main` branch, depth 1).
- **Text license**: Creative Commons Attribution-ShareAlike 4.0 International (**CC BY-SA 4.0**) — full text in `../../LICENSE`.
- **Sample code license**: MIT — full text in `../../LICENSE-SAMPLECODE`.
- **Authors**: see the source repo's README and `d2l.bib`.

## What this package is
A **compilation of original synthesis**: chapter files restructure the book's concepts,
formulas, code patterns, and gotchas into notes, and each carries a 2026 delta section.
No source text is reproduced at length; no figures or long passages are copied.
Under CC BY-SA 4.0, adapted material must be licensed under CC BY-SA 4.0 (or a compatible
license) with attribution — hence this package's `license: CC-BY-SA-4.0` and the included
LICENSE files.

## Attribution
> Zhang, A., Lipton, Z. C., Li, M., & Smola, A. J. (2023). *Dive into Deep Learning*.
> https://d2l.ai — licensed under CC BY-SA 4.0.

## Compilation details
- Compiled: 2026-11-19, from `d2l-ai/d2l-en` @ main (shallow clone, `chapter_*` sources).
- Pipeline: `engineering/book-to-skill` (extract → synthesize → validate), then
  `scripts/check_frontmatter.py`, `scripts/check_skill_names.py`, `scripts/audit_skills.py`,
  `scripts/smoke_scripts.py` run clean.
- Chapter numbering follows the book's TOC (`index.md`), 26 content chapters; the references
  chapter (bibliography) is not compiled.
