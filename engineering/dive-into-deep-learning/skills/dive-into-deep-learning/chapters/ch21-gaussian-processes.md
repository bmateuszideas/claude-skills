# Ch 21 — Gaussian Processes: Bayesian nonparametrics

Source: `chapter_gaussian-processes` of d2l-ai/d2l-en (CC BY-SA 4.0).

## From distributions over variables to distributions over functions
A **Gaussian process** is a distribution over functions: any finite set of function values has a **joint Gaussian distribution**. Defined by a **mean function** $m(x)$ (usually 0) and a **kernel/covariance function** $k(x, x')$ that encodes smoothness/similarity (e.g. **RBF/Squared-Exponential**: $k(x,x') = \sigma^2 \exp(-(x-x')^2/2\ell^2)$ — $\ell$ = length-scale, $\sigma^2$ = signal variance).

## GP priors
Sampling functions from a GP prior = drawing smooth (or rough, depending on kernel) curves. Kernel choice = prior over function properties (periodic kernel → periodic functions, etc.).

## GP inference (regression)
Given noisy observations $y = f(x) + \epsilon$, the GP posterior at new points is **analytic**: posterior mean $m_* + K_{*x}(K_{xx}+\sigma_n^2 I)^{-1}(y - m)$ and covariance $K_{**} - K_{*x}(K_{xx}+\sigma_n^2 I)^{-1}K_{x*}$. You get **predictive means and uncertainty** for free — GPs are the gold standard for calibrated uncertainty in the small-data regime.

## GPs vs neural networks
An infinitely wide NN with Gaussian weights is exactly a GP (Neural Tangent Kernel / NNGP correspondence). Practical difference: NNs are trained by SGD (scalable, less calibrated), GPs by exact linear algebra (O(n³) — limited to ~10⁴ points; sparse/inducing-point approximations scale further).

## 2026 delta
- GPs are used for **Bayesian optimization** (ch. 22), surrogate modeling, and uncertainty estimation where data is scarce (robotics, materials, hyperparameter tuning).
- Deep kernel learning (NN feature extractor + GP head) combines both worlds; scalable via variational inference (SVGP) in GPyTorch.
- For large data, ensembles / MC-dropout are cheaper uncertainty proxies.

## Gotchas
- Kernel hyperparameters (length-scale, noise) are usually learned by maximizing the **marginal likelihood** — can overfit with few points.
- Naive GP is O(n³) time, O(n²) memory — never use on big data without inducing points.
- Always add a small **jitter** ($10^{-6}I$) to the covariance matrix for numerical stability (Cholesky).
