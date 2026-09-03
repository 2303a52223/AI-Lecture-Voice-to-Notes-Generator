# Text-Image-GenAI — Methods (1‑page summary)

Purpose
- Build a modular pipeline that performs text→image generation and image→text captioning, enabling round‑trip evaluation and iterative improvement.

Pipeline Overview
- Components: (1) Text encoder, (2) Latent diffusion model (text→image), (3) Vision–language encoder/captioner (image→text), (4) Evaluation & API layer.
- Data flow: Prompt → text embedding → diffusion sampling → generated image → vision encoder → caption → compare to prompt.

Modeling Details
- Latent diffusion: operates in a compressed latent space to iteratively denoise a noise tensor conditioned on text embeddings. Advantages: high fidelity, controllable via classifier‑free guidance.
- Vision–language encoders: BLIP/BLIP‑2 or similar transformer‑based models map images and text into a shared embedding space for captioning and semantic comparison.
- Conditioning & control: use guidance scale and temperature parameters; classifier‑free guidance mixes conditional/unconditional denoising to trade fidelity vs diversity.

Training & Objectives
- Multi‑objective loss: L(Θ) = α·L_text + β·L_img + γ·L_perc + λ·R(Θ).
  - L_text: CLIP‑style contrastive loss to align text↔image embeddings.
  - L_img: diffusion reconstruction/denoising loss (mean squared error in latent/noise prediction).
  - L_perc: perceptual loss (VGG features) to preserve visual quality.
  - R(Θ): regularization (weight decay, priors).

Evaluation & Round‑Trip
- Round‑trip: generate image from prompt, caption image, then compute semantic alignment between original prompt and generated caption.
- Metrics: FID (image quality), CLIPScore (semantic alignment), BLEU/METEOR/ROUGE/CIDEr (caption quality).
- Ablations: vary model sizes, guidance scales, and captioner architectures to measure tradeoffs.

Engineering & Deployment
- Modular design: decouple diffusion model, captioner, and API service (FastAPI). Allows swapping components and offline vs cloud runtimes.
- Efficiency: use latent-space sampling, mixed precision and caching of embeddings; batch captioning during evaluation.
- Scalability: expose endpoints for text→image and captioning; worker queue for heavy generation jobs.

Practical Notes
- Compute: diffusion sampling is CPU/GPU heavy; consider smaller checkpoints or low‑rank adapters for constrained environments.
- Ethics & Safety (brief): add watermarking, content filters, and human review for sensitive outputs.

References (key models)
- Latent diffusion / Stable Diffusion family; BLIP / BLIP‑2 for captioning; CLIP for embedding alignment.

---
Generated as a concise, one‑page methods summary for exam prep and quick reference.
