# Text-Image-GenAI — Evaluation (1‑page summary)

Purpose
- Describe metrics and procedures used to measure model fidelity, semantic alignment, and caption quality in the text↔image pipeline.

Evaluation Strategy
- Round‑trip evaluation: prompt → generate image → caption image → compare caption to original prompt.
- Quantitative metrics:
  - FID: image quality (lower is better).
  - CLIPScore: semantic alignment between image and text (higher is better).
  - BLEU / METEOR / ROUGE / CIDEr: caption/text similarity metrics.
  - Perceptual metrics: LPIPS, human eval scores.

Design of Experiments
- Ablation studies: vary guidance scale, model size, captioner architecture, and data augmentation.
- Round‑trip consistency: measure semantic drift between prompt and caption (CLIP distance).
- Robustness: evaluate across prompt styles, object composition, and out‑of‑distribution prompts.

Statistical Reporting
- Report mean ± std over multiple seeds; provide significance testing for ablation differences.
- Use precision/recall for object presence and retrieval tasks where applicable.

Practical Notes
- Use balanced datasets and sampled prompts to avoid metric bias.
- Complement automatic metrics with human rating studies for realism and alignment.

---
One‑page evaluation summary suitable for exam prep and quick reference.
