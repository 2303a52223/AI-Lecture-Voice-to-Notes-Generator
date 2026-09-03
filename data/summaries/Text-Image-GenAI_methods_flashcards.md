# Flashcards — Text-Image-GenAI (Methods)

- Q: What are the main components of the Text‑Image‑GenAI pipeline?
  A: Text encoder, latent diffusion model (text→image), vision–language captioner (image→text), evaluation/API.

- Q: What advantage do latent diffusion models provide?
  A: Operate in compressed latent space for high fidelity sampling and computational efficiency compared to pixel‑space diffusion.

- Q: What is classifier‑free guidance?
  A: A technique that mixes conditional and unconditional denoising to trade fidelity vs diversity via a guidance scale.

- Q: Name the multi‑objective loss components used.
  A: L_text (CLIP contrastive), L_img (diffusion reconstruction), L_perc (perceptual), R(Θ) (regularization).

- Q: What metric measures semantic alignment of image and text?
  A: CLIPScore.

- Q: Which metric evaluates image quality?
  A: FID (Fréchet Inception Distance).

- Q: How is round‑trip evaluation performed?
  A: Generate image from prompt → caption the image → compare caption to original prompt (semantic metrics).

- Q: Two engineering strategies to reduce compute cost?
  A: Use latent‑space sampling, mixed precision, caching embeddings, and smaller checkpoints or adapters.

- Q: Name one safety control to add in deployment.
  A: Content filters, watermarking, and human review.
