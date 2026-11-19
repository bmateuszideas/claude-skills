# Cheatsheet — Dive into Deep Learning decision rules

Quick decision tables. (Original synthesis; chapter refs in parentheses.)

## Task → model
| Task | First model | Better |
|---|---|---|
| Tabular prediction | MLP (ch08) | GBM outside book; wide-deep |
| Image classification | ResNet-50 fine-tuned (ch11, 17) | ConvNeXt / ViT with pretraining (ch14) |
| Object detection | YOLO/SSD-style one-stage (ch17) | DETR-family (ch17 delta) |
| Segmentation | FCN/U-Net (ch17) | SegFormer |
| Text classification | BERT fine-tune (ch19) | LLM with LoRA |
| Translation/generation | transformer seq2seq (ch13–14) | decoder-only LLM |
| Time series | LSTM/GRU small (ch13) | transformer (TCN/N TFT) |
| Recommendation | two-tower + cross-encoder rerank (ch24) | LLM reranker |
| RL | PPO (ch20 delta) | PPO + RLHF for LLMs |

## Loss → task
| Loss | Use for | Notes |
|---|---|---|
| MSE (½(ŷ−y)²) | regression | Gaussian MLE; sensitive to outliers (ch06) |
| Cross-entropy on logits | classification | `CrossEntropyLoss` applies log-softmax internally (ch07) |
| BCEWithLogits | multi-label | per-label sigmoid |
| KL / cross-entropy | distillation, RL | asymmetric KL — order matters (ch25) |
| Contrastive (InfoNCE) | self-supervised | (ch18 delta) |

## Optimizer → situation
| Optimizer | When | lr |
|---|---|---|
| AdamW | default for almost everything (2026) | 1e-4…1e-3 |
| SGD+momentum | some vision baselines, best generalization sometimes | 0.01–0.1 + schedule |
| Adam | legacy default | 1e-3 |
| AdaGrad | very sparse features (rare now) | 0.01–0.1 |

Always: warmup + cosine/step decay (ch15); clip grads for RNNs (ch12).

## Regularization → symptom
| Symptom | Fix |
|---|---|
| Train≈val≈high (underfit) | more capacity, train longer, check features |
| Train low, val high (overfit) | augmentation → weight decay → dropout → more data → early stop (ch06, ch08) |
| Val worse in prod | distribution shift — monitor, retrain (ch07) |
| NaN loss | lower lr, grad clip, fix init, check for NaN in data (ch08) |

## Quick formulas
- Conv output: ⌊(n + 2p − k)/s⌋ + 1 (ch10)
- SGD: w ← w − η·∇L (ch06/15) · Adam moments: m=β₁m+(1−β₁)g; v=β₂v+(1−β₂)g², bias-corrected (ch15)
- Softmax: ŷᵢ = e^{oᵢ}/Σe^{oⱼ}; argmax(ŷ)=argmax(o) (ch07)
- Attention: softmax(QKᵀ/√dₖ)V (ch14)
- RNN: Hₜ = tanh(XₜWₓ + Hₜ₋₁Wₕ + b) (ch12)
- Bellman: V(s) = max_a [R + γ Σ P(s'|s,a)V(s')] (ch20)
- Perplexity = exp(−mean log P) (ch12)
- VRAM ≈ params × (4 model + 8 Adam states + activations) bytes; bf16 halves model+grads (ch16)

## Sanity checks before training
- [ ] Visualize one batch (labels aligned!)
- [ ] Loss decreases on a tiny overfit run (10 batches, 1 sample) — pipeline OK
- [ ] `model.eval()` + `no_grad` for evaluation
- [ ] Seeds fixed; config logged; checkpointing on
