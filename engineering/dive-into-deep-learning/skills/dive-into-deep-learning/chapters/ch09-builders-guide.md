# Ch 9 — Builders' Guide: PyTorch modules, parameters, I/O, GPUs

Source: `chapter_builders-guide` of d2l-ai/d2l-en (CC BY-SA 4.0). How to compose, initialize, save, and run models on hardware.

## Layers and modules
- `nn.Module` is the base class: define layers in `__init__`, the computation in `forward(self, X)`. Submodules register automatically.
- `nn.Sequential(*layers)` chains them; a custom module can do anything in `forward` (control flow, multiple branches — e.g. Inception, ResNet).
- Layers without parameters (ReLU, MaxPool, Flatten) vs with parameters (Linear, Conv2d).

## Parameter management
- Every parameter is a `nn.Parameter`; access via `named_parameters()` (names like `net.0.weight`), `parameters()`, or targeted `net[0].weight`.
- **Tied/shared weights**: assign the same Parameter object to two places (weight tying in embeddings/LM heads).
- Device/dtype: `param.data`, move whole model with `net.to('cuda')`.

## Initialization
- Built-in defaults (Kaiming/He for Linear/Conv) are good — `force_reinit=True` to re-roll.
- Custom init: `nn.init.xavier_uniform_`, `nn.init.normal_`, `nn.init.constant_` applied in `__init__` or via `net.apply(fn)`.
- **Lazy init**: layers can infer input dims on first forward (`nn.LazyLinear`) — handy, but check final shapes.

## File I/O
- Save tensors: `torch.save(tensor, 'file.pt')` / `torch.load`.
- Save model **parameters only** (portable): `torch.save(net.state_dict(), 'mlp.params')`, load with `net.load_state_dict(torch.load(...))` — the standard.
- Saving the whole model pickles the class — brittle across versions; prefer `state_dict`.

## GPUs
- `torch.cuda.is_available()`, `torch.device('cuda' if ... else 'cpu')`.
- Tensors and models must live on the **same device**: `X = X.to(device)`, `net = net.to(device)`.
- Query GPU memory: `torch.cuda.memory_allocated()` / `nvidia-smi`.
- Multi-GPU: `nn.DataParallel` (simple, single-process) or **DDP** (distributed, the production choice for training).

## 2026 delta
- `state_dict` + `torch.load(..., weights_only=True)` is now the default-safe load (weights_only default flipped in torch 2.6).
- DDP (`torchrun`) replaced DataParallel for anything serious; `torch.compile` (2.x) often gives bigger speedups than raw multi-GPU plumbing for inference.
- Hugging Face `safetensors` is the safer serialization format for sharing weights.

## Gotchas
- Forgetting `.to(device)` on the input is the classic "expected all tensors on same device" crash.
- Saving whole models breaks when class definitions move; always ship `state_dict` + code.
- Re-init must happen before `load_state_dict`, or shapes mismatch.
