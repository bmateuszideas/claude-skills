# Ch 15 — Optimization: from GD to Adam + LR schedules

Source: `chapter_optimization` of d2l-ai/d2l-en (CC BY-SA 4.0).

## The real goal
Optimization ≠ generalization. We minimize **training loss**; we care about **test error**. Over-optimizing train loss can hurt test (overfitting) — early stopping is regularization.

## Gradient descent in 1-D
$x \leftarrow x - \eta f'(x)$. Learning rate $\eta$ is everything: too small → slow; too large → divergence/oscillation. In higher-D, **ill-conditioned** loss surfaces (elongated valleys) make plain GD zigzag slowly.

## Minibatch SGD
Gradient noise from minibatches is a feature: it helps escape poor regions and implicitly regularizes. Convergence rate typically $O(1/\sqrt{T})$ for convex; DL is nonconvex but SGD works empirically.

## The optimizer zoo (all in `torch.optim`)
- **Momentum**: $v_t = \beta v_{t-1} + g_t$; $w \leftarrow w - \eta v_t$. Averages gradients (leaky average, $\beta$=0.9) — accelerates along consistent directions, damps oscillation. Fixes ill-conditioning.
- **AdaGrad**: per-coordinate adaptive lr: $s_t = s_{t-1} + g_t^2$; $w \leftarrow w - \eta g_t/\sqrt{s_t+\epsilon}$. Great for **sparse features** (NLP embeddings); lr decays monotonically — can stop too early.
- **RMSProp**: fix AdaGrad's decay with exponential moving average of squared grads ($s_t = \gamma s_{t-1} + (1-\gamma)g_t^2$).
- **AdaDelta**: no manual lr at all (units-matched update from RMSProp idea).
- **Adam** (default choice): momentum (first moment $m$) + RMSProp (second moment $v$) + **bias correction** for the zero-initialized moments. `torch.optim.Adam(lr=1e-3, betas=(0.9, 0.999))`. Modern variant: **AdamW** — decouples weight decay from the gradient update (correct L2 regularization; default in most LLM/vision training).

## Convexity
Convex set/function definitions; Jensen's inequality ($f(E[x]) \le E[f(x)]$); in convex problems every local minimum is global — why linear regression/SVM are "easy" and DL is not. DL loss surfaces: saddle points and many minima, but empirically SGD finds good-enough ones.

## Learning-rate schedules
Fixed $\eta$ is suboptimal: large early (fast progress), small late (fine convergence). Schedulers in `torch.optim.lr_scheduler`: **StepLR** (multiply by γ every k epochs), **MultiStepLR**, **ExponentialLR**, **CosineAnnealingLR** (cosine decay — very popular), **OneCycleLR**, plus **warmup** (linear increase for first steps — stabilizes transformer/LLM training). Toy demo: LeNet on Fashion-MNIST with/without schedule.

## 2026 delta
- **AdamW + cosine schedule with warmup** is the standard recipe for transformers/LLMs; for small CNNs, SGD+momentum+step-decay still competitive (and generalizes well).
- lr is the most important hyperparameter: use lr-range test / one-cycle policy to pick it.
- Second-order optimizers (Shampoo, K-FAC) exist for very large models but AdamW dominates in practice.

## Gotchas
- NaN loss ⇒ lr too high or exploding grads — lower lr / clip grads / check init.
- Don't decay lr to exactly 0 too early; keep a small floor.
- BatchNorm + very high lr don't mix; warmup helps both BN and transformers.
