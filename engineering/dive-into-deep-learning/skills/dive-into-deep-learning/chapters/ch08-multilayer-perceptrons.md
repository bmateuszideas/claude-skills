# Ch 8 — Multilayer Perceptrons: the first deep model

Source: `chapter_multilayer-perceptrons` of d2l-ai/d2l-en (CC BY-SA 4.0).

## Why linear models aren't enough
A linear model can only carve the input space with hyperplanes: XOR is the canonical non-linearly-separable example. Stacking linear layers without nonlinearity collapses to one linear layer.

## The MLP
$\mathbf{h} = \sigma(\mathbf{W}^{(1)}\mathbf{x} + \mathbf{b}^{(1)})$, $\hat{\mathbf{y}} = \mathbf{W}^{(2)}\mathbf{h} + \mathbf{b}^{(2)}$ — **hidden layer** with nonlinear **activation** $\sigma$, then output layer. In PyTorch: `nn.Sequential(nn.Flatten(), nn.Linear(784, 256), nn.ReLU(), nn.Linear(256, 10))`.

## Activation functions
- **ReLU**: $f(x) = \max(0, x)$ — the default. Cheap, mitigates vanishing gradients for x>0; "dead ReLU" problem for x<0 (use LeakyReLU/ELU/GELU if units die).
- **Sigmoid**: $\sigma(x) = 1/(1+e^{-x})$ — squashes to (0,1); saturates for large |x| → vanishing gradients; use only at output for binary probability, not hidden layers.
- **Tanh**: squashes to (−1,1), zero-centered — better than sigmoid historically, still saturates.
- Modern defaults: ReLU family (LeakyReLU, GELU in transformers).

## Universal approximation
A single hidden layer with enough units can approximate any continuous function on a compact set (Cybenko). Depth is still preferred in practice: deep nets compose features hierarchically and need far fewer units than a shallow net for the same function.

## Backpropagation
The chain rule applied layer-by-layer in reverse: forward pass builds a computational graph storing intermediates; backward pass computes $\partial L/\partial \mathbf{W}^{(l)}$ from $\partial L/\partial \mathbf{h}^{(l)}$ and the stored activations. PyTorch does this automatically (`loss.backward()`); from scratch it's the chain rule: $\frac{\partial L}{\partial \mathbf{W}^{(1)}} = \frac{\partial L}{\partial \mathbf{h}} \odot \sigma'(\cdot) \cdot \mathbf{x}^\top$. Cost: forward+backward ≈ 2–3× forward.

## Numerical stability & initialization
- **Vanishing gradients**: with sigmoid/tanh and many layers, products of small derivatives → early layers barely train. **Exploding gradients**: large weights × many layers → overflow (watch for NaN loss).
- **Breaking symmetry**: never init all weights to the same value (all units learn identically) — random init required.
- **Xavier/Glorot init**: scale variance to keep signal variance stable across layers: $W \sim \mathcal{N}(0, \frac{2}{n_{in}+n_{out}})$ (for tanh); **He init** for ReLU: $\mathcal{N}(0, 2/n_{in})$. PyTorch default (Kaiming) is fine — never set all-zero or constant weights.

## Dropout (regularization for deep nets)
During training, zero each hidden unit with probability $p$ (e.g. 0.5) and **rescale survivors by $1/(1-p)$** (inverted dropout — done automatically in `nn.Dropout`). At inference: no dropout (`model.eval()`). Effect: ensemble-like robustness, prevents co-adaptation of units. Modern nets often prefer weight decay + data augmentation over heavy dropout.

## The Kaggle recipe (house prices)
The chapter's capstone: preprocess (log-transform skewed features, standardize, one-hot categories, handle NaNs), MLP with ReLU + dropout, MSE loss (on log prices), k-fold CV, submit. Lessons: log-transform targets with heavy tails, standardize features, CV for small data.

## 2026 delta
- ReLU → GELU/SwiGLU in transformers; MLP blocks there are "FFN" with expansion factor 4.
- Init: default Kaiming/He is fine; never custom-tune init in modern deep nets.
- Dropout is often replaced by stochastic depth / label smoothing in large-scale training; still standard for small MLPs.
- Backprop is still autograd — the math matters for debugging (gradient flow checks).

## Gotchas
- NaN loss early in training ⇒ exploding gradients (lower lr, check init, consider grad clipping `nn.utils.clip_grad_norm_`).
- Dead ReLUs (all-zero row) ⇒ try LeakyReLU or lower lr.
- Always `model.train()` / `model.eval()` to toggle dropout & batchnorm behavior.
