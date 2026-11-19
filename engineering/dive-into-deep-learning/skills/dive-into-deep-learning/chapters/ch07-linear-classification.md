# Ch 7 — Linear Classification: softmax regression, metrics, distribution shift

Source: `chapter_linear-classification` of d2l-ai/d2l-en (CC BY-SA 4.0).

## From regression to classification
Labels are **categories**, not numbers. Store them as integers, but represent them for training as **one-hot vectors**: $y \in \{(1,0,0),(0,1,0),(0,0,1)\}$. (Ordinal labels with a natural order can stay numeric — ordinal regression.)

## Softmax regression = single fully-connected layer
- Model: one affine function per class, $\mathbf{o} = \mathbf{W}\mathbf{x} + \mathbf{b}$, $\mathbf{W} \in \mathbb{R}^{d\times q}$, $\mathbf{b}\in\mathbb{R}^{q}$; vectorized over minibatch: $\mathbf{O} = \mathbf{X}\mathbf{W} + \mathbf{b}$.
- **Softmax** turns logits into probabilities: $\hat{y}_i = \frac{\exp(o_i)}{\sum_j \exp(o_j)}$ — nonnegative, sums to 1, monotonic.
- Prediction = `argmax` — and `argmax_j ŷ_j = argmax_j o_j`, so you never need to compute softmax to predict.
- **Loss: cross-entropy** (negative log-likelihood under one-hot labels): $l(\mathbf{y},\hat{\mathbf{y}}) = -\sum_j y_j \log \hat{y}_j = -\log \hat{y}_{\text{true class}}$. PyTorch: `nn.CrossEntropyLoss()` takes **raw logits** (applies log-softmax internally — numerically stable; never apply softmax yourself before it).
- Numerical note: compute softmax stably (subtract max before exp) — frameworks do this for you.

## Metrics: accuracy
Accuracy = fraction of correct predictions. Fine for balanced classes; misleading under **class imbalance** — then use precision/recall/F1, confusion matrix.

## The dataset pattern: Fashion-MNIST
`torchvision.datasets.FashionMNIST(root, train=True, transform=..., download=True)` → wrap in `DataLoader(dataset, batch_size=256, shuffle=True)`; images are 28×28 grayscale → flatten to 784 features for a linear model. Always visualize a few minibatches first.

## Distribution shift (the silent killer)
Training assumes test data ~ training distribution. In reality:
- **Covariate shift**: $P(x)$ changes, $P(y\mid x)$ doesn't (e.g. train on sunny photos, test on night).
- **Label shift**: $P(y)$ changes, $P(x\mid y)$ doesn't (e.g. disease prevalence changes).
- **Concept shift**: $P(y\mid x)$ itself changes (e.g. "spam" definition evolves).
Fixes: importance weighting, retraining, domain adaptation — detect it by monitoring input/output statistics in production.

## Generalization in classification
- **Never reuse the test set** for model selection — that leaks and inflates reported accuracy (test-set reuse is a classic benchmark-science sin).
- Statistical learning theory bounds generalization error via model complexity + dataset size (VC dimension / Rademacher complexity) — intuition: capacity must match data size.

## 2026 delta
- `CrossEntropyLoss` on logits is still exactly right; label smoothing (`label_smoothing=0.1`) is a cheap modern add-on against overconfidence.
- Class imbalance is ubiquitous (fraud, rare disease): use weighted loss / focal loss, and report PR-AUC, not just accuracy.
- Distribution shift monitoring (Evidently, WhyLabs) is standard MLOps practice now — the chapter's covariate/label/concept taxonomy maps directly onto production drift detectors.

## Gotchas
- One-hot + MSE works but is the wrong loss — use cross-entropy (proper likelihood, better gradients).
- `argmax` on logits ≡ argmax on softmax — skip softmax at inference.
- Accuracy on an imbalanced test set can look great while the model is useless.
