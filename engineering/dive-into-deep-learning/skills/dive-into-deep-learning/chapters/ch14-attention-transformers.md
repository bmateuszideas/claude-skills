# Ch 14 — Attention & Transformers: the architecture that ate NLP

Source: `chapter_attention-mechanisms-and-transformers` of d2l-ai/d2l-en (CC BY-SA 4.0).

## Attention pooling (Nadaraya–Watson)
Given queries $q$ and key–value pairs $(k_i, v_i)$: $\text{Attention}(q, (k_i,v_i)) = \sum_i \alpha(q, k_i)\, v_i$ where $\alpha$ = softmax of a similarity score. Attention = a **differentiable, soft lookup** — the core primitive.

## Scoring functions
- **Dot product**: $\alpha(q,k) = q^\top k$ (scaled: divide by $\sqrt{d}$ to keep softmax gradients healthy — **scaled dot-product attention**).
- **Masked softmax**: for decoder self-attention, mask future positions (−∞ before softmax) to preserve autoregressive property.
- **Additive (Bahdanau)**: $v^\top \tanh(W_q q + W_k k)$ for different q/k dims.

## Queries, Keys, Values
Query = what you're looking for; key = what each item offers; value = what you retrieve. Self-attention: all three are projections of the same sequence: $Q = XW_Q$, $K = XW_K$, $V = XW_V$; output $= \text{softmax}(QK^\top/\sqrt{d_k})V$. Complexity $O(n^2 d)$ in sequence length n — the quadratic cost that limits context length.

## Multi-head attention
Run h parallel attention heads with separate projections, concatenate, project: $\text{MHA}(X) = \text{Concat}(\text{head}_1..\text{head}_h)W_O$. Lets the model attend to different representation subspaces (syntax, coreference, position...).

## Self-attention + positional encoding
Self-attention is **permutation-invariant** — it has no notion of order. Fix: add **positional encodings** to input embeddings: sinusoidal $PE_{pos,2i} = \sin(pos/10000^{2i/d})$ (original) or **learned absolute** embeddings (modern). Comparison: CNN = local receptive field, grows with depth, O(n·k·d); RNN = sequential, O(n·d²) recurrence, hard to parallelize; self-attention = any pair in one step, O(n²·d), fully parallel — wins at scale.

## The Transformer (2017, "Attention Is All You Need")
Encoder–decoder, both stacks of identical layers, each layer = [multi-head self-attention → add & layer-norm] + [positionwise FFN (2-layer MLP, ReLU/GELU) → add & layer-norm].
- Encoder self-attention: Q=K=V from previous encoder layer.
- Decoder: masked self-attention (autoregressive) + **encoder–decoder attention** (queries from decoder, keys/values from encoder output).
- Residual connections keep dims fixed ($d$ model dim everywhere); **LayerNorm** (normalize over feature dim, not batch) is preferred over BatchNorm for sequences (variable length, batch-size independent).
- Training: teacher forcing + label smoothing; inference: autoregressive decoding with beam search or sampling.

## Vision Transformer (ViT, 2020)
Split image into patches (e.g. 16×16), flatten + linear project to embeddings, add learned positional embeddings, prepend [CLS] token, run a standard **encoder-only transformer**, read the [CLS] output for classification. Needs lots of data or pretraining; with pretraining it matches/exceeds CNNs.

## Large-scale pretraining
- **Encoder-only (BERT)**: masked-LM + next-sentence-prediction pretraining → fine-tune with a task head.
- **Encoder–decoder (T5/BART)**: span corruption / text-to-text unified framing.
- **Decoder-only (GPT)**: next-token prediction on raw text → the LLM paradigm (pretrain → SFT → RLHF).

## 2026 delta
- This chapter is the foundation of modern LLMs: decoder-only transformers + BPE tokenization + AdamW + cosine LR + large-scale pretraining.
- Efficiency fixes now standard: FlashAttention (memory-efficient exact attention), GQA/MQA (fewer KV heads), RoPE/ALiBi positional encodings instead of sinusoidal, SwiGLU FFN activations.
- Post-training (SFT/DPO/RLHF) is as important as pretraining — the book's "fine-tuning BERT" section generalizes to this.

## Gotchas
- Always scale dot-product attention by $1/\sqrt{d_k}$ — without it softmax saturates and gradients vanish.
- Decoder self-attention must be masked (causal mask) or the model cheats by looking at future tokens.
- LayerNorm placement (pre-LN vs post-LN) matters for training stability of deep models; pre-LN is the modern default.
- Attention is $O(n^2)$ — long-context models need KV caching at inference (never recompute past keys/values).
