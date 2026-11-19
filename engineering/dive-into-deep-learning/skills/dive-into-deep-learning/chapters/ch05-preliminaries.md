# Ch 5 — Preliminaries: tensors, pandas, linear algebra, calculus, autograd, probability

Source: `chapter_preliminaries` of d2l-ai/d2l-en (CC BY-SA 4.0). This is the crash course that makes the rest of the book runnable.

## 5.1 Data manipulation (ndarray)
- A **tensor** = (possibly multi-dimensional) array of numbers: 1-D = vector, 2-D = matrix, k-D = k-th order tensor.
- Create: `torch.arange(12, dtype=torch.float32)`, `torch.zeros((2,3,4))`, `torch.ones(...)`, `torch.randn(3,4)` (standard normal), `torch.tensor([[...], ...])`.
- Inspect: `x.numel()` (element count), `x.shape`.
- **Reshape** without changing values: `x.reshape(3,4)`; infer one dim with `-1`: `x.reshape(-1,4)`. Elements laid out row-major: `x[3] == X[0,3]`.
- Indexing/slicing like Python lists: 0-based, negative indices from the end, `X[start:stop]` — stop **exclusive**.
- Elementwise ops: `+ - * / **`; broadcasting lets shapes like `(3,1)` and `(1,4)` combine to `(3,4)` — the mechanism behind most shape bugs and most concise code.
- **In-place memory**: `X[:] = ...` / `X += Y` avoid new allocations (matters in training loops). JAX arrays are immutable — use `x.at[i].set(v)`.
- Conversion: `X.numpy()` (torch, CPU only) / `torch.tensor(np_array)`.

## 5.2 Data preprocessing (pandas)
- Load CSV: `pd.read_csv(path)`; missing entries become `NaN`.
- Split inputs/targets by position: `inputs, targets = data.iloc[:, 0:2], data.iloc[:, 2]`.
- Handle missing values:
  - Categorical: `pd.get_dummies(inputs, dummy_na=True)` — `NaN` becomes its own category (one-hot).
  - Numeric: `inputs.fillna(inputs.mean())` — impute with column mean. (Deletion is the alternative: drop rows/cols with NaN.)
- To tensors: `torch.tensor(inputs.to_numpy(dtype=float))`.

## 5.3 Linear algebra
- Ladder: scalar → vector $\mathbf{x}$ → matrix $\mathbf{X}$ → tensor $\mathsf{X}$.
- Key products: dot $\langle\mathbf{x},\mathbf{y}\rangle$ (`torch.dot`), matrix–vector $\mathbf{Xv}$ (`X @ v`), matrix–matrix `X @ Y` (`torch.matmul`), elementwise/Hadamard `X * Y` (`⊙`), transpose `X.T`.
- **Reduction**: `X.sum()`, sum over axes: `X.sum(axis=0)` (keeps dims with `keepdims=True` — avoids shape bugs), mean `X.mean()`.
- **Norms**: ℓ2 `‖x‖₂ = √(Σxᵢ²)` = `torch.norm(x)` (Euclidean length); ℓ1 `‖x‖₁ = Σ|xᵢ|` (Manhattan, robust to outliers); general ℓp; matrix **Frobenius** `‖X‖_F = √(Σxᵢⱼ²)` = ℓ2 of flattened matrix. Norm axioms: positive-definite, homogeneous, triangle inequality. Frobenius is what weight decay (L2 regularization) penalizes.
- Eigenvalues/eigenvectors (`torch.linalg.eigh` for symmetric) come up with PCA and spectral analysis.

## 5.4 Calculus
- Derivative $dy/dx$; **gradient** $\nabla_{\mathbf{x}} y$ = vector of partial derivatives, same shape as $\mathbf{x}$, points in direction of steepest ascent.
- **Chain rule** for compositions — the mathematical backbone of backpropagation: $\frac{dy}{dz} = \frac{dy}{dx}\frac{dx}{dz}$.

## 5.5 Automatic differentiation (autograd)
- PyTorch: `x = torch.arange(4.0, requires_grad=True)` → compute `y = 2 * torch.dot(x, x)` → `y.backward()` → read `x.grad` (should be `4*x`). The computation graph ("tape") is built during the forward pass; `backward()` walks it in reverse.
- Non-scalar `y`: `y.backward()` implicitly sums gradients over `y`'s components (vector-Jacobian product with all-ones vector) — same shape as `x`.
- **Pitfall**: PyTorch **accumulates** gradients across `backward()` calls — always `optimizer.zero_grad()` (or `x.grad.zero_()`) before each training step, otherwise gradients from all previous steps pile up.
- Detach from graph when you need a constant: `x.detach()`.

## 5.6 Probability & statistics
- Sample space $\mathcal{S}$, events = subsets; **Kolmogorov axioms**: $P(\mathcal{A}) \ge 0$, $P(\mathcal{S})=1$, countable additivity for mutually exclusive events.
- **Random variable** $X$: mapping from sample space to values; $P(X{=}v)$ is the probability of the event. Discrete (coin) vs **continuous** (height): for continuous, $P(X{=}x)=0$ — use **density** $p(x)$ and integrate over intervals.
- Multiple variables: joint $P(X,Y)$, conditional $P(X\mid Y)$, **marginalization** $P(X)=\sum_Y P(X,Y)$; **independence** $P(X,Y)=P(X)P(Y)$; **Bayes' rule** $P(X\mid Y) = P(Y\mid X)P(X)/P(Y)$.
- **Expectation** $E[X]$ = probability-weighted average; linearity $E[aX+bY]=aE[X]+bE[Y]$ holds without independence. Variance $\mathrm{Var}(X)=E[(X-E[X])^2]$. These are what loss functions estimate on finite data.

## 5.7 Looking up API docs
- `dir(module)`, `dir(torch)`, `help(torch.matmul)` — read signatures *in the installed version*; docstrings are the ground truth.

## 2026 delta
- Prefer `torch` over NumPy for anything on GPU; NumPy stays fine for data prep.
- `pandas` 2.x: `get_dummies`/`fillna` unchanged; watch `CoW` (copy-on-write) default changes in pandas 3.
- Modern torch idiom: `with torch.no_grad():` for inference, `torch.inference_mode()` is faster; `model.eval()` + `no_grad` is the standard eval pattern.
- Autograd pitfall (gradient accumulation) is still the #1 beginner bug — `optimizer.zero_grad()` every step.

## Gotchas
- `*` is elementwise, `@` is matmul — never mix them up.
- `sum(axis=0)` without `keepdims` changes rank — broadcasting then silently misaligns.
- NaN handling: decide impute vs delete **before** converting to tensors; NaN propagates through training and poisons gradients.
