# Ch 13 — Modern RNNs: LSTM, GRU, seq2seq, beam search

Source: `chapter_recurrent-modern` of d2l-ai/d2l-en (CC BY-SA 4.0).

## LSTM (1997)
Vanilla RNN's hidden state gets overwritten each step — long-range dependencies vanish. LSTM adds a **cell state** $\mathbf{C}_t$ (a conveyor belt) gated by:
- **forget gate** $\mathbf{f}_t = \sigma(\cdot)$ — how much of $\mathbf{C}_{t-1}$ to keep
- **input gate** $\mathbf{i}_t$ — how much new candidate $\tilde{\mathbf{C}}_t$ to write
- **output gate** $\mathbf{o}_t$ — how much of $\tanh(\mathbf{C}_t)$ to expose as $\mathbf{H}_t$
Update: $\mathbf{C}_t = \mathbf{f}_t \odot \mathbf{C}_{t-1} + \mathbf{i}_t \odot \tilde{\mathbf{C}}_t$. PyTorch: `nn.LSTM(input, hidden, num_layers)`.

## GRU (2014)
Lighter LSTM: merges forget+input into a single **update gate** $\mathbf{z}_t$, and merges cell/hidden into one state with a **reset gate** $\mathbf{r}_t$. Fewer params, often similar performance. PyTorch: `nn.GRU(...)`.

## Deep & bidirectional RNNs
- Stack multiple RNN layers (`num_layers>1`) for more capacity.
- **Bidirectional RNN** (`bidirectional=True`): forward + backward passes over the sequence, concatenate — great for encoding a whole sequence (e.g. NER), invalid for autoregressive decoding.

## Encoder–decoder / seq2seq
For machine translation: **encoder** RNN reads source → final hidden state = context vector; **decoder** RNN generates target tokens one by one, conditioned on context. Training uses **teacher forcing** (feed the true previous token). Inference: feed the model's own prediction (exposure bias risk).

## Attention (Bahdanau, 2014)
Instead of one fixed context vector, the decoder **attends** over all encoder hidden states with learned alignment weights (see ch. 14 for the general form). This fixed the bottleneck of seq2seq on long sentences.

## Beam search
Greedy decoding picks the locally-best token and can miss globally-better sequences. Beam search keeps the **k best partial hypotheses** at each step (beam width k≈4–8), scores by cumulative log-prob (with length normalization), returns the best final sequence. Standard for MT/summarization with RNNs.

## 2026 delta
- seq2seq RNNs have been replaced by transformers for MT, but the encoder–decoder concept lives on in T5/BART.
- Beam search is still used, but sampling methods (top-p nucleus) dominate in LLM decoding; length normalization remains important.
- LSTM/GRU still used in small on-device models and time-series forecasting (e.g. N-BEATS-style stacks) where transformers are overkill.

## Gotchas
- Bidirectional encoders can't be used autoregressively in the decoder.
- Teacher forcing at train / free-running at test = exposure bias; scheduled sampling mitigates.
- Beam search with too-large k ≈ greedy; too small = slow. Length penalty matters for long outputs.
