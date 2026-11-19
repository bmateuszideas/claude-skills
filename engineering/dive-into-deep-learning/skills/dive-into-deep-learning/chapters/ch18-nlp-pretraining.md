# Ch 18 — NLP Pretraining: word2vec → subwords → GloVe → BERT

Source: `chapter_natural-language-processing-pretraining` of d2l-ai/d2l-en (CC BY-SA 4.0).

## Word embeddings
One-hot vectors are huge and uninformative. **Word2vec (2013)** learns dense vectors from co-occurrence:
- **Skip-gram**: predict context words from center word.
- **CBOW**: predict center from context.
- Training trick: **negative sampling** — instead of softmax over the whole vocab, sample k negative words and do binary logistic classification (fast; the "approx-training" section).
- Result: vector arithmetic works — `king − man + woman ≈ queen` (similarity & analogy demos). Vectors capture semantic/syntactic regularities.

## Subword embeddings
Words like "newest"/"newest-looking" explode the vocab. **Byte-pair encoding (BPE)** merges frequent character pairs iteratively → subword units shared across words; handles OOV naturally. (WordPiece/SentencePiece are variants — the tokenizers used by BERT/GPT.)

## GloVe (2014)
Global vectors from the **co-occurrence matrix** X (word–context counts): factorize log X ≈ word·contextᵀ via least squares with weighting f(X_ij). Combines global statistics with local context; vectors comparable to/complementary with word2vec.

## BERT (2018) — pretraining transformers
Pretrain a **bidirectional** transformer encoder on raw text with two self-supervised tasks:
- **Masked language model (MLM)**: mask 15% of tokens, predict them from both sides (bidirectional context — the key difference from GPT).
- **Next sentence prediction (NSP)**: is sentence B the actual next sentence of A? (Later models dropped NSP — it's weak signal.)
Then **fine-tune** the pretrained model on downstream tasks by adding a small head (ch. 19). BERT dataset: BooksCorpus + Wikipedia.

## 2026 delta
- word2vec/GloVe are legacy for most NLP — subword-tokenized transformers (BERT/RoBERTa for encoding, GPT-family for generation) dominate. Static embeddings still useful for tiny/edge setups.
- BERT-style encoder-only models remain the workhorse for classification/NER/embedding (sentence-transformers); decoder-only LLMs for generation.
- Pretraining data scale grew from BooksCorpus+Wikipedia (~3B words) to trillions of tokens; data quality/filtering (dedup, quality classifiers) now matters more than raw size.

## Gotchas
- Cosine similarity (not dot product) for comparing embedding vectors after normalization.
- Negative sampling k≈5–20; more negatives ≈ better approximation of softmax.
- MLM masks: 80% [MASK], 10% random token, 10% unchanged (BERT's recipe) — keeps fine-tuning consistent.
