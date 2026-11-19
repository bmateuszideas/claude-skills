# Ch 11 — Modern CNNs: AlexNet → ResNet/DenseNet + BatchNorm

Source: `chapter_convolutional-modern` of d2l-ai/d2l-en (CC BY-SA 4.0). The architecture zoo, in historical order.

## The lineage
- **AlexNet (2012)** — the deep-learning breakthrough on ImageNet: 5 conv + 3 FC, ReLU, dropout, data augmentation, GPU training. Bigger kernels (11×11, 5×5), stride 4.
- **VGG (2014)** — small 3×3 kernels stacked deep (16/19 layers), in repeated blocks: conv-conv-pool. Lesson: depth with small kernels beats one big kernel; but many params in FC head.
- **NiN (2014)** — Network-in-Network: 1×1 convs after conv layers for per-pixel nonlinearity, then **global average pooling** instead of big FC layers → far fewer params, less overfitting.
- **GoogLeNet/Inception (2014)** — parallel branches with 1×1, 3×3, 5×5 convs + pooling, concatenated ("Inception module"); 1×1 convs reduce channels before expensive 3×3/5×5. 22 layers but efficient.
- **BatchNorm (2015)** — normalize each layer's activations per minibatch: $\hat{x} = (x-\mu_B)/\sqrt{\sigma_B^2+\epsilon}$, then scale/shift with learned $\gamma,\beta$. Effects: allows higher learning rates, reduces internal covariate shift, mild regularization. At inference use running averages. **Still in nearly every CNN.** PyTorch: `nn.BatchNorm2d(ch)` after conv, before activation (or after — both used).
- **ResNet (2015)** — **residual blocks**: $y = F(x) + x$ where $F$ is conv-BN-ReLU-conv-BN; the identity shortcut lets gradients flow directly (solves vanishing in very deep nets), and the net learns *residual* corrections. With BN, 152+ layers train fine. Bottleneck blocks (1×1→3×3→1×1) for efficiency. PyTorch: `torchvision.models.resnet50(weights=...)`.
- **DenseNet (2016)** — **dense connections**: each layer receives the feature maps of *all* preceding layers (concatenated) — maximal information flow, small feature maps, strong on small datasets; downside: memory grows with depth.

## Design heuristics
- Start from a known backbone (ResNet-50, EfficientNet) + transfer learning; train from scratch only with lots of data.
- Channels usually double as spatial size halves (compute stays ~constant): 64→128→256→512.
- cnn-design section: scaling width/depth/resolution together (compound scaling, à la EfficientNet) beats scaling one axis.

## 2026 delta
- ResNet-50 is still a solid baseline; EfficientNet/ConvNeXt (modernized ResNet with large kernels, LayerNorm, GELU) beat it on accuracy-per-FLOP.
- Vision Transformers (ch. 14) have displaced CNNs for large-scale vision, but CNNs remain best for small data / edge / real-time (mobile) due to inductive biases and efficiency.
- BatchNorm is being replaced by LayerNorm/GroupNorm in some modern designs (transformers, ConvNeXt), but BN is still standard in classic CNNs.

## Gotchas
- BN behaves differently in train vs eval — `model.eval()` at inference or metrics collapse.
- BN with batch size 1 is meaningless — use GroupNorm/LayerNorm for tiny batches.
- Pretrained backbones expect ImageNet normalization (mean/std) — reuse their transforms.
