# Ch 4 — Introduction: ML in one chapter

Source: `chapter_introduction` of d2l-ai/d2l-en (CC BY-SA 4.0).

## The core idea: programming with data
You rarely write a rule that maps inputs→outputs explicitly. Instead you define a **flexible program whose behavior is set by parameters (knobs)**; a **learning algorithm** uses a **labeled dataset** to find the knob settings; the fixed result is the **model**. The set of all programs reachable by turning knobs = the **model family**.

Training loop: start random → grab labeled batch → tweak knobs to reduce loss on that batch → repeat until good.

## The four components of every ML problem
1. **Data** — a collection of *examples*; each example = *features* (inputs) + in supervised learning a *label* (target). Fixed-length vectors have constant *dimensionality*; images/text are variable-length — a key advantage of deep nets is handling variable-length inputs gracefully. More data ⇒ more powerful models, less reliance on assumptions. **Garbage in, garbage out** — and beware bias: underrepresented groups (e.g. skin-cancer models never trained on dark skin) and labels reflecting historical prejudice (hiring data) get automated silently.
2. **Model** — machinery ingesting one data type, emitting predictions of another. Deep learning = many chained transformations ("deep"), learned **jointly from data**.
3. **Objective function (loss)** — formal "how good" measure; by convention **lower is better** (flip the sign of anything where higher is better). Squared error for regression; error rate for classification — but error rate is non-differentiable, so in practice we optimize a **surrogate** (e.g. cross-entropy). Split data into **training set** (fit parameters) and **test set** (held-out evaluation). Good on train + bad on test = **overfitting** (memorizing practice questions).
4. **Optimization algorithm** — searches for parameters minimizing the loss; for DL, **gradient descent** family: perturb each parameter slightly, see how train loss changes, step in the reducing direction.

## Kinds of ML problems
- **Supervised** (majority of industrial ML): predict label from features; probabilistically, estimate $P(\text{label} \mid \text{features})$. Forms:
  - **Regression** — target is any real number ("how much/how many": price, rainfall, surgery hours). Loss: squared error.
  - **Classification** — discrete classes; multi-class, multi-label (**tagging**), hierarchical.
  - **Search & ranking**, **recommender systems** (implicit feedback), **sequence learning** (variable-length input and/or output; e.g. time series, translation — note outputs may depend on each other).
- **Unsupervised / self-supervised**: no labels — **clustering**, **subspace estimation/PCA**, **embeddings** (Rome−Italy+France≈Paris), **causality/graphical models**, **deep generative models** (VAE, GAN, normalizing flows, diffusion). **Self-supervised**: supervision from the data itself (masked-word prediction = BERT; relative position/occlusion in images) → pretrain, then fine-tune downstream.
- **Offline vs online**: supervised/unsupervised are *offline* (grab data once, learn, done). **Reinforcement learning** = agent interacts with an environment over time steps: observation → action → reward. Policy = map from observations to actions. Hard parts: **credit assignment** (chess: only win/lose at the end), **partial observability**, **explore vs exploit**. Special cases: fully observed → **MDP**; state independent of past actions → **contextual bandit**; stateless → **multi-armed bandit**. Classic wins: DQN (Atari), AlphaGo. Key failure mode shared with supervised: **distribution shift** (train ≠ test environment).

## The essence of deep learning
- Multi-layer representation learning: each layer's operations are **learned jointly from data**.
- Excels on **low-level perceptual data** (raw pixels, raw audio, arbitrary-length sentences) where classical methods needed hand-crafted features.
- **End-to-end training** replaces feature engineering: Canny edges + SIFT used to be the front end of CV; now automatically tuned filters outperform them. This unified CV, speech, NLP, medicine — one toolkit.
- Shift from parametric to **nonparametric** models as data grows; acceptance of **nonconvex** optimization, suboptimal solutions, and empiricism ("try before proving").
- Open-source ethos: libraries, models, and this book's notebooks are free.

## 2026 delta
- The "essence" paragraph has only grown truer: transformers (ch. 14) now dominate not just NLP but vision (ViT), speech, and RL; diffusion models are the standard generative backbone; self-supervised pretraining is the default starting point, not an exotic extra.
- Distribution shift is now a first-class production concern (dataset datasheets, monitoring, retraining) — the book's exam/homework analogy maps directly to train-serving skew.
- The nonconvex-empiricism stance is now mainstream: nobody waits for proofs before deploying.

## Gotchas
- Don't optimize the metric you can't differentiate (error rate) — pick a surrogate loss and track the real metric separately.
- Always hold out a test set before you start tuning; report both train and test.
- In RL, reward hacking and credit assignment bite hard — design reward shaping carefully.
