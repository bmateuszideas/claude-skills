# Patterns — Dive into Deep Learning

Recurring techniques and design patterns from the book, with trade-offs. (Original synthesis.)

## The universal training loop
`for epoch: for batch in loader: loss = criterion(model(x), y); opt.zero_grad(); loss.backward(); opt.step()` — everything in the book reduces to this shape. Add: validation each epoch, checkpointing, early stopping, logging.

## Two-version pedagogy
Every core component is shown **from scratch** (NumPy-level, to see the mechanics) and **concise** (framework API, for real use). Pattern for your own code: implement once manually to understand, then use the library.

## Vectorize everything
No Python loops over examples — one matmul per minibatch. 10,000-element vector adds show 10–100× speedup vs loops. Pattern: think in whole-tensor ops; broadcasting is your friend (and your bug source — check shapes).

## Design-matrix thinking
Batch of n examples with d features = matrix X ∈ R^{n×d}; model = XW + b. Most "per-example" code is one matrix op.

## Loss selection by task
Regression → squared error (Gaussian MLE). Classification → cross-entropy on logits (never softmax+MSE). Ranking → sampled-softmax / pairwise losses. Each loss = an MLE under a noise model — pick the noise model that matches your data.

## Regularization ladder (in order of cheapness)
More data → augmentation → weight decay (AdamW) → dropout → early stopping → smaller model. In the overparameterized regime, prefer data/regularization over shrinking the model (ch06).

## Architecture selection
- Tabular → MLP (or gradient boosting outside this book).
- Images → CNN (ResNet/ConvNeXt) if data small; ViT if lots of data/pretraining.
- Sequences → transformer (ch14); RNN/LSTM only for tiny/edge cases.
- Generation → diffusion (2026 default), GAN for real-time/style.

## Optimization recipe (2026 default)
AdamW (lr 1e-3 to 3e-4 for big models, 1e-3 small), warmup + cosine decay, grad clipping, bf16 mixed precision, batch 32–256+, weight decay 0.01–0.1 decoupled. SGD+momentum+step decay still wins some vision baselines.

## Debugging ladder for training failures
1. Loss NaN early → lr too high / bad init / exploding grads → lower lr, check init, `clip_grad_norm_`.
2. Loss flat → lr too low / dead ReLUs / wrong loss / data pipeline bug → check data first (visualize batch), then lr.
3. Train ↓, val ↑ → overfitting → augmentation, dropout, weight decay, more data, early stopping.
4. Train ↓ slowly → underfitting / ill-conditioning → scale features, more capacity, longer training, better lr schedule.
5. Model fine but production bad → distribution shift (ch07) → monitor input stats, retrain.

## Data pipeline pattern
pandas: read CSV → split inputs/targets (iloc) → one-hot categoricals (`get_dummies(dummy_na=True)`) → impute numerics (`fillna(mean)`) → `to_numpy(dtype=float)` → `torch.tensor` → `TensorDataset` → `DataLoader(batch_size, shuffle=True, num_workers>0, pin_memory=True)`.

## Pretraining → fine-tuning pattern
Pretrain on large unlabeled data (MLM / next-token) → freeze or low-lr fine-tune on task data with task head → small lr (2e-5–5e-5 for BERT), few epochs, early stopping.

## Reproducibility pattern
Fix seeds (`torch.manual_seed`, `np.random.seed`, `random.seed`), `cudnn.deterministic=True`, log config + metrics (W&B/MLflow), save `state_dict` checkpoints, record env (`pip freeze`).

## Anti-patterns
- Optimizing accuracy directly (non-differentiable) — use surrogate loss, track metric separately.
- Reusing the test set for decisions — leaks, inflates results.
- Comparing models on train loss — compare on held-out validation.
- `*` vs `@` confusion; axis-sum without `keepdims`; forgetting `opt.zero_grad()`; train/eval mode confusion (dropout/BN).
