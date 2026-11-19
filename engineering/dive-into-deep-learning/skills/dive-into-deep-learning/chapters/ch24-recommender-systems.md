# Ch 24 — Recommender Systems

Source: `chapter_recommender-systems` of d2l-ai/d2l-en (CC BY-SA 4.0). MovieLens demo throughout.

## The problem
Predict user–item interactions (ratings/clicks) from sparse explicit or implicit feedback. Core tension: **exploration vs exploitation** (also ch. 20's RL theme).

## Matrix factorization (MF)
User matrix $P \in \mathbb{R}^{m\times k}$, item matrix $Q \in \mathbb{R}^{n\times k}$; predict $\hat{r}_{ui} = p_u^\top q_i$ (+ biases $b_u + b_i$). Train with squared error on observed entries (+ L2). Latent factors capture taste/genre. Limitation: no side features.

## Factorization machines (FM)
$\hat{y} = w_0 + \sum w_i x_i + \sum_{i<j} \langle v_i, v_j\rangle x_i x_j$ — captures **pairwise feature interactions** with O(k·n) params instead of O(n²). Good for sparse one-hot features (user id, item id, context).

## Neural approaches
- **NeuMF**: combine MF's linear dot product with an MLP over concatenated embeddings (generalized matrix factorization).
- **DeepFM / CTR models**: FM + deep net for click-through-rate prediction — industry standard for ads/recs.
- **AutoRec**: autoencoder over the user–item interaction vector (like MF but neural).
- **Sequence-aware rec (seqrec)**: model the user's session as a sequence (RNN/transformer, ch. 12/14) to predict the next item — captures temporal intent.

## Ranking
Training on implicit feedback with negative sampling; ranking metrics: Precision@k, Recall@k, NDCG@k, MAP — better than RMSE for top-k recommendations.

## 2026 delta
- Two-tower architectures (separate user tower and item tower, dot-product scoring) are the scalable industry pattern — enables ANN retrieval (FAISS/ScaNN) over millions of items, then a reranker (cross-encoder) on top-k.
- LLMs are now used for zero-shot/explainable recommendations and as rerankers.
- Cold start: content-based features + exploration bandits.

## Gotchas
- RMSE on observed ratings is misleading for ranking — optimize ranking metrics with sampled negatives.
- Popularity bias: MF without correction recommends popular items; add item-bias correction or downsample popular items.
- Data leakage: split by **time** (last interaction as test), not random — random splits leak the future.
