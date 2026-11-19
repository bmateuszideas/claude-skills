# Ch 12 — Recurrent Neural Networks: sequence models

Source: `chapter_recurrent-neural-networks` of d2l-ai/d2l-en (CC BY-SA 4.0).

## Sequences need memory
Fixed-size vectors can't represent variable-length sequences. An RNN keeps a **hidden state** $\mathbf{H}_t$ that summarizes everything seen so far:
$\mathbf{H}_t = \tanh(\mathbf{X}_t \mathbf{W}_{xh} + \mathbf{H}_{t-1} \mathbf{W}_{hh} + \mathbf{b}_h)$, output $\mathbf{O}_t = \mathbf{H}_t \mathbf{W}_{hq} + \mathbf{b}_q$. Same weights at every time step (parameter sharing) — handles any length.

## Language models & text
- Estimate $P(x_1, ..., x_T)$ via chain rule; **n-grams / Markov models** are the statistical precursor.
- Text preprocessing pipeline: tokenize (words or **characters**), build **vocabulary** (map token→id, with `<unk>` for rare), convert corpus to id sequence. Char-level models avoid OOV but have longer sequences.
- Training a language model = predict next token given previous (self-supervised on raw text). Perplexity = $\exp(-\frac{1}{n}\sum \log P(x_t|x_{<t}))$ — the standard LM metric (lower = better; perplexity 1 = perfect).
- Sampling from an LM: feed prefix, sample next token from softmax (with **temperature** to sharpen/flatten), feed back — autoregressive generation.

## RNN training: BPTT
Backpropagation through time = backprop along the unrolled time axis. Gradients over long sequences → vanishing/exploding (same as deep MLPs). **Truncated BPTT**: unroll only k steps back, treat earlier hidden state as constant — the practical fix.

## Concise implementation
`nn.RNN(input_size, hidden_size, num_layers=1)` → outputs + hidden state; for LMs a Linear head on outputs. PyTorch handles the loop.

## 2026 delta
- Vanilla RNNs are rarely used for real sequence tasks anymore — transformers (ch. 14) dominate NLP; RNNs/LSTMs still appear in small/edge sequence models and as components.
- Tokenization is now **subword** (BPE/WordPiece/SentencePiece via Hugging Face `tokenizers`), not word/char — better vocab efficiency.
- Perplexity is still the LM metric, but downstream task metrics matter more; greedy sampling is replaced by temperature/top-k/top-p sampling in practice.

## Gotchas
- Always clip gradients (`clip_grad_norm_`) when training RNNs — exploding gradients are the default failure.
- Sort/pack batches by length (`pack_padded_sequence`) so padding doesn't waste compute.
- Teacher forcing vs free-running at inference (exposure bias) matters for seq2seq (ch. 13).
