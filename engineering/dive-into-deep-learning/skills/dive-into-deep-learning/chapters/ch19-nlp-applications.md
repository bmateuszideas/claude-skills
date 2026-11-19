# Ch 19 — NLP Applications: sentiment, NLI, fine-tuning BERT

Source: `chapter_natural-language-processing-applications` of d2l-ai/d2l-en (CC BY-SA 4.0).

## Sentiment analysis
Task: classify text (e.g. IMDb reviews) as positive/negative. Approaches in the chapter:
- **TextCNN**: 1-D conv over word embeddings + max-over-time pooling → linear classifier. Fast, strong baseline.
- **RNN**: bidirectional GRU/LSTM over the sequence, take final hidden states → classifier.
- **BERT fine-tuning**: prepend [CLS], feed through BERT, classify the [CLS] representation (or mean-pool). Best accuracy; `transformers` library makes it ~10 lines.

## Natural language inference (NLI)
Given a **premise** and a **hypothesis**, predict entailment / contradiction / neutral (SNLI/MultiNLI datasets). Approaches:
- **Attention-based**: encode premise & hypothesis (BiLSTM), align with attention, aggregate (compare) → MLP classifier. (This is the "decomposable attention" model.)
- **BERT**: feed "[CLS] premise [SEP] hypothesis [SEP]" → classify [CLS]. SOTA for years; still a strong baseline.

## Fine-tuning BERT in practice
- Load `bert-base-uncased` from Hugging Face; add `nn.Linear(hidden, num_labels)`.
- Tokenize with BERT's tokenizer (WordPiece, max_len ~128–512, truncation+padding).
- Train with AdamW + warmup, small lr (2e-5–5e-5), few epochs (2–4) — BERT overfits fast on small datasets; use weight decay 0.01, early stopping.
- For sequence labeling (NER): token-level head, align word-piece labels back to words (BIO scheme).

## 2026 delta
- Encoder models (BERT/RoBERTa/DeBERTa) still strong for classification/embeddings; but decoder-only LLMs with prompting/fine-tuning (LoRA/QLoRA) increasingly replace task-specific heads.
- Sentence embeddings: use sentence-transformers (fine-tuned BERT/SBERT) for semantic search — cosine similarity over embeddings.
- NLI is now subsumed by general LLM reasoning; still useful as an eval task.

## Gotchas
- Always use the matching tokenizer for the checkpoint (vocab mismatch silently ruins everything).
- Fine-tune with small lr and few epochs — catastrophic forgetting/overfitting is immediate at lr 1e-3.
- Truncate long inputs (BERT max 512 tokens); chunk + aggregate for longer docs.
