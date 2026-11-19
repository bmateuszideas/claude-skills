# Ch 10 — CNNs: convolutions, channels, pooling, LeNet

Source: `chapter_convolutional-neural-networks` of d2l-ai/d2l-en (CC BY-SA 4.0).

## Why convolutions (from FC layers)
Two structural priors for images:
1. **Translation invariance** — a cat is a cat anywhere in the image; FC layers must relearn each position.
2. **Locality** — nearby pixels are related; a pixel's meaning depends on its neighborhood, not the whole image.
Convolution = local weighted sum (kernel) slid over the input — sparse interactions + shared parameters.

## The 2-D cross-correlation (what "convolution" means in DL)
Output $Y[i,j] = \sum_{a,b} X[i+a, j+b] \, W[a,b]$ (in practice cross-correlation, no kernel flip). In PyTorch: `nn.Conv2d(in_ch, out_ch, kernel_size, stride=1, padding=0)`.
- **Padding** (usually same, e.g. 1 for 3×3) preserves spatial size: out = ⌊(n + 2p − k)/s⌋ + 1.
- **Stride** downsamples.
- Edge detection demo: a learned 1×2 kernel `[1,-1]` highlights vertical edges.

## Channels
- **Multiple input channels**: sum the per-channel convolutions (e.g. RGB: 3 kernels summed).
- **Multiple output channels**: one kernel per output channel → output has `out_ch` channels. Params: `out_ch × in_ch × k × k`.
- **1×1 conv**: a per-pixel linear projection across channels — used to mix channels cheaply (NiN, ResNet bottlenecks).

## Pooling
`nn.MaxPool2d(2)` / `nn.AvgPool2d(2)` — downsample by taking max/mean over windows (typically 2×2, stride 2). No parameters, adds translation robustness, reduces compute. Modern nets often replace pooling with strided convs.

## LeNet (1998) — the template
`conv(6, 5×5) → sigmoid → avgpool → conv(16, 5×5) → sigmoid → avgpool → flatten → fc(120) → fc(84) → fc(10)` on MNIST/Fashion-MNIST. The pattern — conv-pool blocks → FC head — dominated CV for 20 years. Modern version: ReLU instead of sigmoid, max-pool, more channels, dropout.

## 2026 delta
- Sigmoid/tanh activations and avg-pool are out; ReLU-family + max-pool or stride-2 convs are standard.
- LeNet itself is a toy; the *pattern* (conv blocks + global pooling + linear head) survives in ResNet/ViT.
- `nn.Conv2d` is implemented as highly optimized GEMM (im2col) — always prefer it over manual loops.

## Gotchas
- Output size formula: ⌊(n + 2p − k)/s⌋ + 1 — off-by-one here breaks every downstream shape.
- Channels-first in PyTorch: `NCHW` (batch, channels, H, W) — permute images accordingly.
- Kernel size is usually 3×3 (two 3×3 > one 5×5 in receptive field with fewer params).
