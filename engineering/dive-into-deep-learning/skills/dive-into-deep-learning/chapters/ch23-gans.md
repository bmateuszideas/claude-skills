# Ch 23 — Generative Adversarial Networks

Source: `chapter_generative-adversarial-networks` of d2l-ai/d2l-en (CC BY-SA 4.0).

## The minimax game
Two networks: **generator** G maps noise z → fake sample G(z); **discriminator** D(x) estimates P(x is real). Training objective:
$\min_G \max_D V(D,G) = E_{x\sim p_{data}}[\log D(x)] + E_{z\sim p_z}[\log(1 - D(G(z)))]$.
D learns to tell real from fake; G learns to fool D. At equilibrium, G's output distribution = data distribution (theoretical result under ideal conditions).

## Training in practice
- Alternate: k steps of D, then 1 step of G (k=1 usually fine).
- G's loss trick: instead of $\log(1-D(G(z)))$ (saturates early when D is strong), maximize $\log D(G(z))$ — non-saturating loss, stronger gradients early.
- Labels: real=1, fake=0; use **label smoothing** (real=0.9) for stability.

## DCGAN (2015) — conv GAN that actually trains
Architecture rules that made GANs work: all-conv (no pooling — use strided convs), BatchNorm in both G and D (except G's output and D's input), ReLU in G, LeakyReLU(0.2) in D, tanh output in G, Adam(lr=2e-4, β1=0.5). DCGAN's transposed convs upsample noise → image.

## Instability & remedies
Mode collapse (G produces few varieties), non-convergence. Remedies: label smoothing, noise injection, minibatch discrimination, WGAN (Wasserstein distance with gradient penalty — smoother training), spectral norm.

## 2026 delta
- GANs are largely superseded by **diffusion models** (DDPM/latent diffusion, Stable Diffusion) for image generation — better quality, easier training, but slower sampling.
- GANs still used for: super-resolution, domain translation (CycleGAN), data augmentation, some real-time/edge generation (e.g. StyleGAN for faces remains SOTA for controllable face synthesis).
- Conditional generation: cGAN / classifier-guidance in diffusion.

## Gotchas
- Balance D and G: if D loss → 0, G gets no gradient (use non-saturating loss); if G wins too early, mode collapse.
- Eval GANs with FID/IS (learned-feature statistics), not just eyeballing.
- BatchNorm in D leaks batch statistics — use it anyway (DCGAN trick) but know why (WGAN-GP avoids it).
