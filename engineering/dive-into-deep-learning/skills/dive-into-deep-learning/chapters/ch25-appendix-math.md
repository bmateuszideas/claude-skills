# Ch 25 — Appendix: Mathematics for Deep Learning

Source: `chapter_appendix-mathematics-for-deep-learning` of d2l-ai/d2l-en (CC BY-SA 4.0). Reference math used across the book.

## Calculus
- Single-variable: derivatives, rules (product/chain/quotient), partial derivatives, gradients $\nabla f$, Jacobian/Hessian; multi-variable chain rule (the backprop math).
- Integrals: definite/indefinite, change of variables, integration by parts — appear in probability (expectations over continuous r.v.s) and variational methods.

## Linear algebra
- Scalars→vectors→matrices→tensors; arithmetic, broadcasting; dot/matrix products; norms (ℓp, Frobenius); **eigendecomposition** $A = Q\Lambda Q^{-1}$ (symmetric: orthogonal Q), SVD $A = U\Sigma V^\top$ — power iteration, PCA, low-rank approximation.
- Geometric view: linear maps as rotations/scalings/shears; vector spaces, subspaces, basis, rank, linear independence.

## Probability & statistics
- Random variables (discrete/continuous), distributions (Bernoulli, uniform, Gaussian, exponential family...), joint/marginal/conditional, Bayes' rule, independence, expectation/variance/covariance, **maximum likelihood estimation** (why squared error = Gaussian MLE, cross-entropy = categorical MLE), **naive Bayes** classifier, **information theory**: entropy $H(X)$, cross-entropy, KL divergence $D_{KL}(P\|Q)$ (asymmetric! nonneg by Gibbs' inequality) — the loss functions of ML are KL/cross-entropy in disguise.

## How it all connects
- MLE → loss functions; KL → regularization and variational inference; eigendecomposition/SVD → PCA and recommender systems; gradients/Hessian → optimization and second-order methods; Bayes → uncertainty (and GPs, ch. 21).

## 2026 delta
- The math hasn't changed; the scale has. Modern practice leans on automatic differentiation for all gradient math and on probabilistic programming (NumPyro/Pyro) for Bayesian work.
