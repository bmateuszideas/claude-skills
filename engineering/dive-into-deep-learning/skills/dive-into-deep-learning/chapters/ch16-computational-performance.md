# Ch 16 — Computational Performance: hardware, parallelism, compilers

Source: `chapter_computational-performance` of d2l-ai/d2l-en (CC BY-SA 4.0). Making training actually fast.

## Hardware basics
- **CPU**: few powerful cores, big caches, good latency; **GPU**: thousands of small cores, huge memory bandwidth, great for parallel matmul — the reason DL took off. GPU memory (VRAM) is the hard constraint (model + activations + optimizer states ≈ 12–16 bytes/param in mixed precision training with Adam).
- **Memory** (RAM) vs **storage** (SSD/NVMe): dataset must stream from disk fast enough to not starve the GPU; **network** matters in multi-machine training.
- Rule: profile first (`nvidia-smi`, PyTorch profiler) — find the bottleneck (data loading vs compute) before optimizing.

## Asynchronous computation
Frameworks queue ops on the GPU and return control immediately (non-blocking); the Python frontend runs ahead while the backend computes. Pitfall: synchronizing too early (`.item()`, `.cpu()`) stalls the pipeline — keep data on GPU, sync only when needed.

## Data parallelism (multi-GPU)
Split each minibatch across GPUs; each computes gradients locally; **all-reduce** (ring or tree) averages them; all replicas update identically. Scales ~linearly until communication dominates. PyTorch: `DistributedDataParallel` (DDP) with `torchrun`. Parameter-server architecture is the older alternative (key-value store of params, ring synchronization).

## Automatic parallelism
Framework splits a single op (e.g. big matmul) across devices automatically (device mesh / `torch.distributed.tensor`); model parallelism splits layers across GPUs (needed when one model doesn't fit on one GPU — pipeline parallelism, tensor parallelism for LLMs).

## Compilers & interpreters
- Eager mode (default): op-by-op Python dispatch — flexible, overhead per op.
- **Graph/hybrid**: capture the computation graph (TorchScript `torch.jit.script/trace`, **torch.compile** in torch 2.x) → kernel fusion, fewer launches, big speedups. `torch.compile(model)` is the one-line modern win.
- Hybrid programming: compile the hot training loop, keep data loading in eager Python.

## Practical performance checklist
1. Use `DataLoader(num_workers>0, pin_memory=True)` + prefetch; cache preprocessed data.
2. Mixed precision: `torch.autocast` + `GradScaler` (or `bfloat16`) — ~2× speedup, less VRAM.
3. `torch.compile`, cudnn benchmark mode for CNNs.
4. Profile with `torch.profiler` before and after.

## 2026 delta
- `torch.compile` + `bfloat16` + FlashAttention-style kernels are now default expectations, not tricks.
- For LLM-scale training: tensor/pipeline parallelism (Megatron-LM, DeepSpeed) + 3D parallelism (data+tensor+pipeline).
- Inference: KV caching, quantization (AWQ/GPTQ), speculative decoding.

## Gotchas
- DataLoader with num_workers=0 is often the hidden bottleneck — GPU idles waiting for CPU.
- `.item()`/`.tolist()` in the training loop forces sync every step — accumulate and log sparingly.
- VRAM fragmentation over long runs — restart or use memory profiling; activation checkpointing trades compute for memory.
