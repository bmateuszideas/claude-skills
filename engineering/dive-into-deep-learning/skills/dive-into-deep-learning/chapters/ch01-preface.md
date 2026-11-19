# Ch 1 — Preface: what D2L is and how to read it

Source: `chapter_preface` of d2l-ai/d2l-en (CC BY-SA 4.0).

## The book's promise
One unified, freely available resource that teaches deep learning through **concepts + context + runnable code** — updated continuously (unlike print textbooks), with a forum (discuss.d2l.ai) for discussion.

## The five disciplines every DL application needs
1. Motivations for casting a problem a particular way (problem formulation)
2. The mathematical form of the model
3. Optimization algorithms for fitting models to data
4. Statistical principles for generalization (when to expect it, how to certify it)
5. Engineering for efficient training (numerical computing, hardware)

D2L interleaves all five; most other resources cover only one.

## Learning philosophy: just-in-time, learning by doing
- Concepts are taught **just in time** — you train your first model before meeting esoteric theory.
- **One working example per notebook** — copy a notebook, modify it, start your own project.
- **Two versions of examples**: from-scratch (NumPy-level, to understand what happens inside a layer/optimizer) and high-level framework API (what you actually use later).
- SGD is used *before* it is fully explained — tools before theory, intuition by tweaking code.

## Book structure (three parts)
- **Part 1 — Basics**: introduction, preliminaries (data ops, linear algebra, calculus, probability), regression, classification, MLPs, overfitting/regularization.
- **Part 2 — Modern techniques**: computation (autograd, layers, init), CNNs + modern CNNs, RNNs + modern RNNs, attention & transformers.
- **Part 3 — Scalability & applications** (online): optimization, computational performance, computer vision, NLP pretraining/applications, RL, Gaussian processes, hyperparameter optimization, GANs, recommender systems, appendices.

## Tooling conventions
- All book code lives in the **`d2l` package** (`pip install d2l`); reusable blocks are marked `#@save` in notebooks and importable as `d2l.<name>`.
- Code is **framework-tabbed**: PyTorch (default), TensorFlow, JAX, MXNet (legacy). Pick one tab and stay on it.
- Source on GitHub, notebooks via Jupyter, rendered by Sphinx — community-editable.

## 2026 delta
- The online edition (d2l.ai) is the living version; print/pinned versions age. Always read d2l.ai, not a stale PDF.
- PyTorch is by far the dominant tab now; MXNet is effectively legacy — ignore its tab.
- The "two versions" pattern (from scratch vs high-level) still holds and is the best way to actually understand layers/optimizers.
- Colab links on every d2l.ai page give instant GPU environments — the fastest "installation" path today.

## Gotchas
- Framework versions pinned in the book (torch 2.0.0 etc.) are 2023-era; the online notebooks track current releases. If a notebook breaks, check the online version first.
- "From scratch" examples use only NumPy-like ops + autograd — deliberately minimal, not production code.
