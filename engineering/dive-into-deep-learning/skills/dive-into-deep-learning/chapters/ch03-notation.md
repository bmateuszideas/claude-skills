# Ch 3 — Notation: the book's symbol conventions

Source: `chapter_notation` of d2l-ai/d2l-en (CC BY-SA 4.0).

## The one rule
Lowercase/italic = placeholder of a type ("a scalar"); blackboard/calligraphic = a specific named object (e.g. $\mathbb{Z}$ is *the* integers, not "a set"). This convention is what lets the book write dense formulas without ambiguity.

## Numerical objects
| Symbol | Meaning |
|---|---|
| $x$ | scalar |
| $\mathbf{x}$ | vector |
| $\mathbf{X}$ | matrix |
| $\mathsf{X}$ | tensor (any rank) |
| $\mathbf{I}$ | identity matrix |
| $x_i$, $[\mathbf{x}]_i$ | i-th element of vector |
| $[\mathbf{X}]_{ij}$ | element of matrix at row $i$, col $j$ |

## Sets
$\mathcal{X}$ set · $\mathbb{Z}, \mathbb{Z}^+, \mathbb{R}, \mathbb{R}^n, \mathbb{R}^{a\times b}$ · $|\mathcal{X}|$ cardinality · $\cup, \cap, \setminus$ set ops.

## Functions & operators
$f(\cdot)$ function · $\log$ natural log (base $e$) · $\log_2$ · $\exp$ · $\mathbf{1}(\cdot)$ indicator · $(\cdot)^\top$ transpose · $\mathbf{X}^{-1}$ inverse · $\odot$ Hadamard (elementwise) product · $[\cdot,\cdot]$ concatenation · $\|\cdot\|_p$ ℓp norm, $\|\cdot\|$ = ℓ2 · $\langle\mathbf{x},\mathbf{y}\rangle$ dot product · $\stackrel{\mathrm{def}}{=}$ "defined as".

## Calculus
$\frac{dy}{dx}$ derivative · $\frac{\partial y}{\partial x}$ partial · $\nabla_{\mathbf{x}} y$ gradient · definite/indefinite integrals.

## Probability & information theory
$X$ random variable · $P$ distribution · $X \sim P$ · $P(X{=}x)$, $P(X\mid Y)$ · $p(\cdot)$ density · $E[X]$ expectation · $X \perp Y$ independence · $X \perp Y \mid Z$ conditional independence · $\sigma_X$, $\mathrm{Var}(X)=\sigma_X^2$ · $\mathrm{Cov}(X,Y)$ · $\rho(X,Y)$ Pearson correlation $= \mathrm{Cov}/(\sigma_X\sigma_Y)$ · $H(X)$ entropy · $D_{\mathrm{KL}}(P\|Q)$ KL divergence (note the book's argument order: from $Q$ to $P$).

## Why it matters when working with the code
- In PyTorch, $\mathbf{X}$ is a `torch.Tensor` of shape `(rows, cols)`; `X[i, j]` is `[X]_{ij}`. A vector $\mathbf{x}$ is 1-D, so a column vector is `x.unsqueeze(1)` — the book is sloppy about row-vs-column vectors and the code resolves it via broadcasting.
- `⊙` = `*` (elementwise) in torch, **not** `@`; matmul is `X @ Y` (or `torch.matmul`). Confusing `*` with `@` is the single most common bug when translating book formulas to code.
- Norms: `torch.norm(x)` is ℓ2 by default; ℓ1 is `torch.norm(x, p=1)`.
