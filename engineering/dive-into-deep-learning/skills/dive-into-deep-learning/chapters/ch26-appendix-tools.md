# Ch 26 — Appendix: Tools for Deep Learning

Source: `chapter_appendix-tools-for-deep-learning` of d2l-ai/d2l-en (CC BY-SA 4.0).

## Jupyter
The notebook workflow: cells (code/markdown), kernels, `%magic` commands (e.g. `%matplotlib inline`, `%timeit`), `!shell` commands. Keep notebooks small; move reusable code into modules (`%load_ext autoreload` for live reload). JupyterLab is the modern IDE-like front end.

## Colab
Free hosted notebooks with GPU/TPU (`Runtime → Change runtime type`): zero setup, `!pip install`, mount Google Drive, share. Limits: session timeouts, no persistent storage — save artifacts to Drive/cloud. d2l.ai pages link Colab directly.

## Cloud GPUs
- **AWS**: EC2 GPU instances (p3/p4/p5 = V100/A100/H100), SageMaker for managed training, S3 for data, ECR for containers.
- **Selecting servers/GPUs**: match VRAM to model+optimizer+batch (rule of thumb ~12–16 bytes/param with Adam in fp16/bf16); NVLink matters for multi-GPU; spot/preemptible instances cut cost 60–90% for fault-tolerant training (checkpoint often!).

## The `d2l` package & utils
The book's helper library: `d2l` module with `#@save`-marked functions (data loaders, training loops, plotting, GPU helpers). `d2l.utils` etc. Read its source — it's a clean reference implementation of everything in the book.

## Contributing
The book is open source (GitHub + Discourse forum): issues/PRs welcome; style guide in the repo (STYLE_GUIDE.md); every chapter is a Jupyter notebook — edit and PR.

## 2026 delta
- uv/mamba for envs, VS Code + Jupyter extension for local dev, Weights & Biases/MLflow for experiment tracking, Hugging Face Hub for models/datasets, Modal/RunPod/Lambda for cheap on-demand GPUs.
- Colab still the fastest path to a GPU; Kaggle notebooks are the other free option (with internet off by default — enable it).

## Gotchas
- Always checkpoint cloud training (spot instances die without warning).
- Pin versions (`requirements.txt`/`uv.lock`) — notebook code rots fast across framework versions.
- Don't commit large data/weights to git; use DVC or cloud storage.
