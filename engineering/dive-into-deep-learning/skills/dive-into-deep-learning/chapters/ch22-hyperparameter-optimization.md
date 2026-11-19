# Ch 22 — Hyperparameter Optimization

Source: `chapter_hyperparameter-optimization` of d2l-ai/d2l-en (CC BY-SA 4.0).

## Manual → automatic
Manual tuning (grid over a few params) doesn't scale. HPO automates search over lr, batch size, depth, regularization, etc. Key principle: **each trial is a full training run evaluated on validation**; the search method decides what to try next.

## Random search (async)
Sample hyperparameters from prior distributions (log-uniform for lr and weight decay!), train in parallel, keep the best. Beats grid search in high dimensions — most hyperparameters don't matter equally, and random search explores each dimension densely. **Asynchronous** scheduling (don't wait for slow trials to finish before launching new ones) improves wall-clock throughput.

## Bayesian optimization
Build a **surrogate model** (usually a GP, ch. 21) of validation error as a function of hyperparameters, pick the next point by an **acquisition function** (Expected Improvement, UCB, Probability of Improvement) balancing exploration/exploitation. Much more sample-efficient than random search when each trial is expensive. Libraries: Optuna, Ray Tune, Hyperopt, BoTorch.

## Successive halving (and Hyperband)
Train many configs for a small budget (few epochs), kill the worst half, double the budget of survivors, repeat. Allocates budget to promising configs early. **ASHA** = asynchronous successive halving (no waiting). Ray Tune implements this.

## The HPO API pattern (the chapter's `d2l` style)
A tunable function `train(config) → metric`, a searcher (random / Bayesian / ASHA), and a scheduler. Modern equivalent: Optuna's `study.optimize(objective, n_trials=...)` with pruning (`MedianPruner` = successive halving).

## 2026 delta
- Optuna / Ray Tune are the standard tools; for LLMs, evaluation is expensive so low-fidelity proxies (small model, subset of data, fewer steps) + scaling laws guide the search.
- Multi-fidelity methods (ASHA/Hyperband) and Bayesian BO are often combined (BOHB).
- Always log everything (MLflow/W&B) — HPO without tracking is guesswork.

## Gotchas
- Optimize on **validation**, never on test (test-set reuse inflates results — ch. 7).
- Sample lr/weight-decay log-uniformly, batch size from powers of 2.
- Fix random seeds per trial for comparability, but report variance across seeds for the final config.
