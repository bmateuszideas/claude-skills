# Ch 6 — Linear Regression: the full loop

Source: `chapter_linear-regression` of d2l-ai/d2l-en (CC BY-SA 4.0).

## The model
$\hat{y} = \mathbf{w}^\top \mathbf{x} + b$ — an **affine transformation** (weighted sum + bias). For a dataset: design matrix $\mathbf{X} \in \mathbb{R}^{n\times d}$, predictions $\hat{\mathbf{y}} = \mathbf{X}\mathbf{w} + b$ (broadcasting over rows). Even if the true relationship is linear, real data has measurement noise — we never fit exactly.

## Loss: squared error
$l^{(i)}(\mathbf{w},b) = \frac{1}{2}(\hat{y}^{(i)} - y^{(i)})^2$; total loss $L = \frac{1}{n}\sum_i l^{(i)}$. The ½ cancels in the derivative. Quadratic ⇒ large errors punished quadratically (also sensitive to outliers).

## Two ways to optimize
- **Analytic (closed form)**: absorb bias as a column of 1s; $\mathbf{w}^* = (\mathbf{X}^\top\mathbf{X})^{-1}\mathbf{X}^\top\mathbf{y}$ — exists uniquely iff $\mathbf{X}^\top\mathbf{X}$ invertible (full column rank). Great for analysis; almost nothing in DL has this luxury.
- **Minibatch SGD** (the workhorse): sample minibatch $\mathcal{B}$ of size $|\mathcal{B}|$ (32–256, power of 2), update
  $(\mathbf{w},b) \leftarrow (\mathbf{w},b) - \frac{\eta}{|\mathcal{B}|}\sum_{i\in\mathcal{B}} \partial_{(\mathbf{w},b)} l^{(i)}$.
  - $\eta$ = **learning rate**, $|\mathcal{B}|$ = batch size: both **hyperparameters** (not learned); parameters $\mathbf{w},b$ are learned. Tune hyperparameters on a **validation set**.
  - Minibatches beat full-batch (slow, redundant) and single-sample SGD (slow on hardware, breaks batch-norm) — the sweet spot is vectorized matrix–vector products.
  - Vectorize everything: no Python for-loops over examples; one matmul per step.
- SGD on quadratic loss converges toward the minimizer but rarely hits it exactly in finite steps; minibatch randomness makes runs non-deterministic.

## Weight decay (L2 regularization)
Add $\frac{\lambda}{2}\|\mathbf{w}\|^2$ to the loss (bias usually not penalized). Effect: shrinks weights toward 0, controls capacity. In PyTorch: `optimizer = torch.optim.SGD(model.parameters(), lr=..., weight_decay=lambda)` — the concise way; from scratch add `lambda * w` to the gradient.

## Generalization
- **Training error** vs **generalization error** (unseen data). The gap is the real target.
- **Model complexity** drives the gap: more parameters ⇒ can memorize. **Underfitting** = too simple (high train error); **overfitting** = too complex (low train, high test). Polynomial curve fitting is the canonical demo.
- More **dataset size** shrinks the gap. **Model selection**: hold out a **validation set**; **k-fold cross-validation** when data is scarce.
- Rule of thumb: if train error is high → more capacity / train longer; if gap is large → more data / regularization / simpler model.

## Code patterns (PyTorch)
- From scratch: linear layer `y = X @ w + b`, MSE `((y - y_hat)**2).mean()` (the ½ is optional), SGD step manual or via `torch.optim.SGD`.
- Concise: `nn.Linear(d, 1)`, `nn.MSELoss()`, `DataLoader` over `TensorDataset` with `batch_size`, loop: `loss = loss_fn(net(Xb), yb); opt.zero_grad(); loss.backward(); opt.step()`.
- OO design (the `d2l` package pattern): `HyperParameters` (save args), `Module` (forward/loss/training step), `DataModule` (train/val dataloaders), `Trainer` (fit loop) — copy this structure for your own projects.

## 2026 delta
- Analytic solution is a teaching device; nobody uses it past tiny problems.
- `DataLoader` + `nn.Linear` + AdamW (see ch. 15) is the modern default; SGD+momentum still wins for some vision training runs.
- Cross-validation is less used in DL (huge datasets); a single large validation split or a fixed test set is standard.

## Gotchas
- Feature scaling matters for SGD conditioning (unscaled features → ill-conditioned $\mathbf{X}^\top\mathbf{X}$).
- Always `opt.zero_grad()` before `backward()` (gradient accumulation pitfall).
- Report train **and** validation error every epoch; watch the gap, not just train loss.
