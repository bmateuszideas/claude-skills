---
name: dive-into-deep-learning
description: "Knowledge base compiled from Dive into Deep Learning (d2l.ai, Zhang/Lipton/Li/Smola, CC BY-SA 4.0, open source at d2l-ai/d2l-en). 26 chapter files covering the full modern DL stack: linear models, MLPs, CNNs (LeNet to ResNet/DenseNet), RNNs/LSTM/GRU, attention and transformers (incl. ViT and BERT pretraining), optimization (SGD to AdamW, LR schedules), computational performance and multi-GPU training, computer vision, NLP, RL, Gaussian processes, hyperparameter optimization, GANs, and recommender systems — each chapter file adds a 2026 delta section on what changed since the book. Use when studying or teaching D2L, choosing an architecture/optimizer for a task, debugging training (vanishing gradients, NaN, overfitting), planning a reading path, or checking whether the book's advice is still current. Original synthesis throughout; it indexes the source, never reproduces it."
license: CC-BY-SA-4.0
metadata:
  version: 1.0.0
  author: Mateusz Baranowicz
  category: engineering
  updated: 2026-11-19
---

# Dive into Deep Learning — Knowledge Base

**Source**: *Dive into Deep Learning* (Aston Zhang, Zachary C. Lipton, Mu Li, Alexander J. Smola),
free online at [d2l.ai](https://d2l.ai) · source repo `d2l-ai/d2l-en` · license **CC BY-SA 4.0** (code MIT) ·
compiled 2026-11-19 from the online edition.

**This is a compilation of original synthesis, not a copy of the book.** Every chapter file is
restructured notes (concepts, formulas, code patterns, gotchas, 2026 delta) — it indexes the
source and never reproduces its text at length. See `references/rights_and_provenance.md`.

## How to use this skill
- **No argument** — load this core: frameworks, chapter index, topic index
- **A topic** — e.g. "attention", "AdamW", "ResNet" — resolve via Topic Index, read that chapter file
- **`chNN`** — load that chapter file directly (see index below)
- **"what changed since the book?"** — every chapter file has a **2026 delta** section

## Core frameworks of the book
1. **Learning = fitting a parametric model to data** — data, model, loss, optimizer (ch. 4)
2. **Linear models** are the Rosetta stone: regression (squared loss, analytic solution, minibatch SGD) and softmax classification (cross-entropy) (ch. 6–7)
3. **MLPs** = linear layers + nonlinear activations (ReLU); trained by backprop; need proper init (Xavier/He) and regularization (dropout, weight decay) (ch. 8)
4. **CNNs** encode locality + translation invariance via convolutions; modern stacks = ResNet/DenseNet + BatchNorm (ch. 10–11)
5. **Sequences**: RNN/LSTM/GRU for temporal data; encoder–decoder seq2seq for translation (ch. 12–13)
6. **Attention & transformers**: soft QKV lookup replaced recurrence as the universal sequence architecture; pretraining (BERT/GPT/T5) + fine-tuning is the paradigm (ch. 14, 18–19)
7. **Optimization**: minibatch SGD + momentum → Adam/AdamW; lr schedules with warmup; train/val/test discipline (ch. 6, 15)
8. **Generalization**: the gap between train and test error drives everything — capacity, data size, regularization, augmentation (ch. 6–8, 17)

## Chapter Index

| # | Title | One-liner |
|---|-------|-----------|
| [ch01](chapters/ch01-preface.md) | Preface | What D2L is; just-in-time learning; book structure |
| [ch02](chapters/ch02-installation.md) | Installation | conda env, frameworks, d2l package, notebooks (+2026 delta) |
| [ch03](chapters/ch03-notation.md) | Notation | Symbol conventions; `*` vs `@` |
| [ch04](chapters/ch04-introduction.md) | Introduction | ML = programming with data; 4 components; problem kinds; essence of DL |
| [ch05](chapters/ch05-preliminaries.md) | Preliminaries | tensors, pandas, linear algebra, autograd, probability |
| [ch06](chapters/ch06-linear-regression.md) | Linear regression | model, squared loss, analytic solution, minibatch SGD, weight decay, generalization |
| [ch07](chapters/ch07-linear-classification.md) | Classification | softmax, cross-entropy, accuracy, distribution shift |
| [ch08](chapters/ch08-multilayer-perceptrons.md) | MLPs | hidden layers, ReLU, backprop, init, dropout |
| [ch09](chapters/ch09-builders-guide.md) | Builders' guide | nn.Module/Sequential, params, init, save/load, GPUs |
| [ch10](chapters/ch10-cnn.md) | CNNs | why conv, conv layer, channels, pooling, LeNet |
| [ch11](chapters/ch11-modern-cnn.md) | Modern CNNs | AlexNet→VGG→NiN→GoogLeNet→BatchNorm→ResNet→DenseNet |
| [ch12](chapters/ch12-rnn.md) | RNNs | hidden state, language models, BPTT |
| [ch13](chapters/ch13-rnn-modern.md) | LSTM/GRU/seq2seq | gates, encoder–decoder, attention, beam search |
| [ch14](chapters/ch14-attention-transformers.md) | Attention & transformers | QKV, multi-head, self-attention+pos-enc, transformer, ViT, BERT/GPT/T5 |
| [ch15](chapters/ch15-optimization.md) | Optimization | GD→momentum→AdaGrad→RMSProp→Adam(W), convexity, LR schedules |
| [ch16](chapters/ch16-computational-performance.md) | Performance | hardware, async, data parallelism, DDP, compilers |
| [ch17](chapters/ch17-computer-vision.md) | Computer vision | anchors, SSD/R-CNN, segmentation, augmentation, fine-tuning, style transfer |
| [ch18](chapters/ch18-nlp-pretraining.md) | NLP pretraining | word2vec, BPE, GloVe, BERT MLM |
| [ch19](chapters/ch19-nlp-applications.md) | NLP applications | sentiment, NLI, BERT fine-tuning |
| [ch20](chapters/ch20-reinforcement-learning.md) | RL | MDP, Bellman, value/policy iteration, Q-learning, DQN |
| [ch21](chapters/ch21-gaussian-processes.md) | Gaussian processes | kernels, GP regression, GP↔NN connection |
| [ch22](chapters/ch22-hyperparameter-optimization.md) | Hyperopt | random search, Bayesian BO, successive halving |
| [ch23](chapters/ch23-gans.md) | GANs | minimax game, DCGAN, stability tricks |
| [ch24](chapters/ch24-recommender-systems.md) | Recommender systems | MF, FM, NeuMF/DeepFM, seq-aware rec, ranking metrics |
| [ch25](chapters/ch25-appendix-math.md) | Appendix: math | calculus, linear algebra, probability, MLE, information theory |
| [ch26](chapters/ch26-appendix-tools.md) | Appendix: tools | Jupyter, Colab, cloud GPUs, d2l package |

## Topic Index
- **Training loop / debugging**: ch05 (autograd), ch06 (SGD), ch08 (init, dropout), ch15 (optimizers, schedules), ch16 (performance) · `patterns.md`
- **Architecture choice**: ch08 (MLP), ch10–11 (CNN), ch12–13 (RNN), ch14 (transformer/ViT), ch17 (detection/segmentation)
- **NLP**: ch12–14 (sequences/attention), ch18 (embeddings/BERT), ch19 (tasks)
- **Generative models**: ch18 (BERT), ch21 (GP), ch23 (GANs) — diffusion in ch23's 2026 delta
- **RL**: ch04 (intro), ch20 (MDP/Q-learning), ch24 (exploration in recsys)
- **Math foundations**: ch03 (notation), ch05 (preliminaries), ch25 (appendix)
- **Practical ML engineering**: ch06–7 (generalization, shift), ch09 (PyTorch patterns), ch16 (scaling), ch17 (augmentation/fine-tuning), ch22 (HPO), ch24 (recsys), ch26 (tools)

## Scope
Covers the d2l.ai online edition (v1.0.3, 2023-era pins; read the living site for current code).
Does **not** cover: production MLOps at depth, specific framework APIs beyond PyTorch-style examples,
domain-specific applications beyond the chapters listed, or post-2023 research (see each chapter's 2026 delta).

## Provenance
Compiled from `github.com/d2l-ai/d2l-en` @ main (CC BY-SA 4.0; sample code MIT).
Full license text in `../../LICENSE`. Details: `references/rights_and_provenance.md`.
