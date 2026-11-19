# Ch 2 — Installation: getting a runnable D2L environment

Source: `chapter_installation` of d2l-ai/d2l-en (CC BY-SA 4.0).

## What this chapter gives you
A reproducible environment to run every code block in the book: Python + Jupyter + one deep learning framework + the `d2l` helper package + the book's notebooks.

## The setup, condensed
1. **Miniconda** (Python 3.x required), then init the shell:
   `~/miniconda3/bin/conda init`, close/reopen shell.
2. **Create + activate the env**: `conda create --name d2l python=3.9 -y` then `conda activate d2l` (deactivate with `conda deactivate`).
3. **Pick one framework** (the book is framework-tabbed; PyTorch is the default path):
   - PyTorch: `pip install torch==2.0.0 torchvision==0.15.1` (CPU/GPU wheels both work)
   - TensorFlow: `pip install tensorflow==2.12.0 tensorflow-probability==0.20.0`
   - JAX/Flax: `pip install "jax[cuda11_pip]==0.4.13" flax==0.7.0` (GPU) or `jax[cpu]`
   - MXNet (legacy tab): `mxnet-cu112==1.9.1` / CPU `mxnet==1.9.1`
4. **The book's helper package**: `pip install d2l==1.0.3` — encapsulates functions/classes used throughout the book.
5. **Notebooks**: download from the "Notebooks" tab on d2l.ai, or `curl https://d2l.ai/d2l-en-1.0.3.zip -o d2l-en.zip && unzip`, then pick the subfolder for your framework (`pytorch/`, `tensorflow/`, `jax/`, `mxnet/`).
6. **Run**: `jupyter notebook` → http://localhost:8888.

## GPU reality check
- No NVIDIA GPU/CUDA? Fine for the first chapters — CPU is enough; you only need a GPU for the larger models later.
- Check CUDA with `nvcc --version` or `cat /usr/local/cuda/version.txt`; match the wheel suffix (`cu112`, `cu121`, ...) to it.

## 2026 delta (what changed since the book's pinned versions)
- The pinned versions above are the book's tested pins (2023-era). Today use current stable wheels: `pip install torch torchvision` (2.x), and keep `d2l` current (`pip install -U d2l`) — the package is still maintained and tracks new framework APIs.
- `conda` still works, but `uv`/`mamba` are faster drop-in replacements for env management (`uv venv && uv pip install ...`). Jupyter: `jupyter lab` is now the common front end; `notebook` still runs.
- Colab is a zero-install alternative: d2l.ai pages have "Run in Colab" links that give a GPU-backed notebook with everything preinstalled.

## Gotchas
- Every new shell needs `conda activate d2l` (or your chosen env) before running notebooks.
- Don't mix framework tabs: run each notebook in the folder matching the framework you installed.
- Windows: use cmd/PowerShell; the conda init step differs slightly — follow the Miniconda online instructions.
