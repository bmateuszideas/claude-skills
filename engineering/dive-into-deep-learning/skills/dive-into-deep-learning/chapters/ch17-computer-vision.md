# Ch 17 — Computer Vision applications

Source: `chapter_computer-vision` of d2l-ai/d2l-en (CC BY-SA 4.0).

## Bounding boxes & anchors
- Bounding box: (x_min, y_min, x_max, y_max) or center+width/height. IoU (intersection over union) measures overlap — the detection metric (mAP@IoU thresholds).
- **Anchor boxes**: at each pixel, multiple boxes of predefined scales/aspect ratios; the model predicts (a) class and (b) offset from each anchor. Generating multiscale anchors across feature-map levels is the basis of modern detectors.

## Object detection
- **SSD (Single Shot Multiscale Detector)**: predict class+offsets at multiple feature-map scales in one forward pass; NMS (non-maximum suppression) removes duplicate boxes.
- **R-CNN family**: two-stage — region proposals (R-CNN/selective search → Fast R-CNN → Faster R-CNN with a learned RPN) → per-region classification. Accurate, slower.
- Modern practice: one-stage detectors (YOLO, RetinaNet) are fast; transformers (DETR) removed anchors/NMS entirely — predict boxes directly with bipartite matching loss.

## Semantic segmentation
Every pixel gets a class label. **FCN**: replace FC layers with 1×1 convs → per-pixel class scores; **transposed convolution** (learned upsampling) restores resolution; skip connections (U-Net) preserve fine detail. Datasets: Pascal VOC/COCO-seg.

## Image augmentation
Random crop/resize, horizontal flip, color jitter, Cutout/CutMix, RandAugment/AutoAugment, mixup. Augmentation is often the single biggest accuracy lever on small datasets — use `torchvision.transforms` v2.

## Fine-tuning / transfer learning
Pretrained backbone (ImageNet) → replace head → (a) train head only (frozen backbone), (b) fine-tune all with small lr, (c) discriminative lr (lower lr for early layers). Kaggle CIFAR-10/dogs demos show the recipe.

## Neural style transfer
Content image + style image → optimize an output image whose **content loss** (deep feature distance) and **style loss** (Gram-matrix statistics of features) match — Gatys et al. Modern: real-time arbitrary style transfer with transformer-based models.

## 2026 delta
- Detection/segmentation: use pretrained YOLO11/SegFormer/DINOv2 rather than training from scratch; DETR-family (DINO, RT-DETR) is now competitive with YOLO.
- Diffusion models (ch. 23-era) power generation/editing (inpainting, ControlNet); classification backbones are ViT/ConvNeXt (ch. 11/14).
- Augmentation is built into dataloaders (albumentations, torchvision v2); mixup/CutMix standard in supervised training.

## Gotchas
- NMS threshold and IoU threshold change mAP a lot — report the full curve, not one point.
- Always fine-tune with ImageNet normalization stats matching the backbone's weights.
- Small datasets: heavy augmentation + strong backbone + early stopping beats custom architectures.
