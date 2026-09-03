# 📝 Study Notes: Milestone2_TextImageGenAI

## 📋 Summary
Text-Image-GenAI
A Practical Pipeline for Text-to-Image and Image-to-Text
MILESTONE 2 REVIEW
Methodology Implementation & Results
Mani Sharan Deep Reddy Gade  ·  Shashidhar Mushike
Department of Computer Science  ·  SR University, Warangal, India
40
MARKS

MILESTONE 2
Milestone 2 — Evaluation Criteria
What is assessed in this review  ·  40 Marks total
1
Appropriateness of Methodology
Whether the chosen techniques (Stable Diffusion + BLIP) suit the problem objectives
8 pts
2
Correct Implementation / Experimentation
End-to-end pipeline execution: text→image and image→text with working code
8 pts
3
Data Generation and Analysis
Dataset sourcing (COCO, LAION, Kaggle), embedding storage, and processed outputs
8 pts
4
Interim Results and Observations
Quantitative metrics (FID, CLIPScore, BLEU) and qualitative caption evaluation
8 pts
5
Short Presentation Delivery
Clarity, completeness of methodology, validity of results, reproducibility
8 pts

MILESTONE 2
Methodology — Pipeline Architecture
Three primary functional blocks with modular, loosely-coupled design
BLOCK 1
Dataset Acquisition
KaggleHub integration
COCO Captions dataset
LAION subset (scale + diversity)
Independent of generative modules
Requirements.txt install
BLOCK 2
Generative Modeling
Stable Diffusion (LDM)
BLIP & BLIP-2 captioning
CLIP vision-language encoder
Latent diffusion denoising
Transformer-based decoding
BLOCK 3
Deployment Services
FastAPI microservice
JSON REST endpoints
Standalone modular execution
Google Colab compatible
NumPy embedding caching

MILESTONE 2
Mathematical Formulation
Core equations governing the generative pipeline
Compositional Pipeline
f(xT; Θ)  =  gN(·;θN) ∘ gN−1 ∘ … ∘ g1(·;θ1)
N modules composed in sequence — encoder → diffusion → decoder
Multi-Objective Loss
L(Θ)  =  α·Ltext  +  β·Limg  +  γ·Lperc  +  λR(Θ)
CLIP contrastive + diffusion reconstruction + perceptual + regularisation
CLIP Contrastive Loss
Ltext  =  −(1/B) Σ log exp(sim(uj,vj)/τ) / Σ exp(sim(uj,vk)/τ)
Aligns text embeddings uj and image embeddings vj via temperature τ
Diffusion Denoising Loss
Limg  =  E[  ‖ε − εθ(xt, t)‖²  ]
Predicts noise ε at timestep t to progressively denoise towards target image
Evaluation Score
Score  =  w₁·CLIPscore − w₂·FID + w₃·IS + w₄·BLEU
Unified scoring combining semantic alignment, fidelity, diversity, and caption quality

MILESTONE 2
Implementation Details
Correct experimentation: tools, models, and deployment
Text Encoder
CLIP Vision Tower — maps prompt to dense embedding space
Diffusion Model
Stable Diffusion (LDM) — iterative denoising from Gaussian noise to image
Image Decoder
VAE Decoder — reconstructs pixel image from latent representation
Caption Generator
BLIP / BLIP-2 — transformer decoder outputs fluent captions
IMPLEMENTATION HIGHLIGHTS
Framework:
PyTorch + Hugging Face Diffusers
Dataset:
KaggleHub / COCO / LAION subset
API Server:
FastAPI microservice (JSON endpoints)
Embedding Storage:
NumPy arrays (reusable across sessions)
Cloud Tested:
Google Colab with pre-installed GPU drivers
Guidance:
Classifier-free guidance for fidelity/diversity
Preview Mode:
Low-res → full-res progressive rendering
Model Swap:
BLIP replaceable with BLIP-2 via config

MILESTONE 2
Evaluation Metrics
Comprehensive quantitative assessment across image quality, semantic alignment, and caption accuracy
FID
Fréchet Inception Distance
Lower is Better
Image Quality
IS
Inception Score
Higher is Better
Image Quality
CLIPScore
CLIP Similarity
Higher is Better
Semantic Alignment
BLEU
Bilingual Eval Understudy
Higher is Better
Caption Quality
SSIM
Structural Similarity Index
0 → 1 scale
Image Fidelity
PSNR
Peak Signal-to-Noise Ratio
Higher is Better
Reconstruction

MILESTONE 2
Data Generation & Analysis
Dataset selection, embedding pipeline, and output samples
DATASETS USED
Dataset
Strength
Limitation
COCO Captions
High annotation quality
Limited domain diversity
LAION Subset
Large scale + diversity
Noisy captions
Kaggle GenAI
Controlled reproducibility
Limited size
BIDIRECTIONAL PIPELINE FLOW
Text Prompt
CLIP Encoding → Latent z
LDM Denoising → Image
BLIP Encoder → Caption
KEY OBSERVATION:
Embeddings stored as NumPy arrays eliminate redundant computation across sessions. MILESTONE 2
Interim Results & Observations
Quantitative metrics and qualitative analysis of generated outputs
>80%
Round-trip
Consistency
Low
FID
vs GAN
baselines
High
BLEU
METEOR &
CIDEr verified
Fluent
Captions
Semantically
accurate
Text-to-Image Quality
Stable Diffusion outperforms GAN baselines: lower FID scores confirm greater image fidelity; CLIPScore values confirm stronger semantic adherence to input prompts. MILESTONE 2
Completeness · Validity · Reproducibility
Measurable indicators for Milestone 2 assessment
Completeness of Methodology
✔
Full bidirectional pipeline implemented (text↔image)
Mathematical formulation defined (5 core equations)
Three functional modules operational independently
FastAPI deployment layer tested and documented
Validity of Results
✔
7 quantitative metrics applied (FID, IS, CLIP, BLEU, SSIM, PSNR, F1)
Round-trip consistency >80% on test prompts
Human-aligned captions confirmed via BLEU + METEOR + CIDEr
Comparison vs. GAN baselines shows diffusion superiority
Reproducibility of Outcomes
✔
requirements.txt single-command install
Pre-validated on Google Colab GPU environment
NumPy embedding cache enables session reuse
KaggleHub dataset module works independently; model checkpoints swappable

MILESTONE 2
Challenges & Future Directions
Known limitations and planned research extensions
CURRENT CHALLENGES
Computational cost — iterative denoising is GPU-intensive; limits real-time edge deployment
Caption hallucinations on ambiguous or complex scenes generate unsupported information
Training data bias reflected in generated images (gender, occupation stereotypes)
Fine-grained attribute control (exact counts, spatial relations, text rendering) under-performs
Interpretability — transformer + diffusion attention maps provide partial insight only
Closed-loop evaluation still relies on embedding similarity, not human contextual judgment
FUTURE DIRECTIONS
RLHF — Reinforcement Learning from Human Feedback for improved alignment and hallucination reduction
Cross-domain fine-tuning: medical imaging annotation, remote sensing, cultural heritage
Model efficiency — DDIM speedup, quantization, distillation for real-time deployment
Ethical guards — bias detection, fairness-aware training, dataset curation pipelines
Multimodal extension — incorporate audio, video, haptic feedback for richer closed loops
Watermarking generated outputs + adversarial robustness testing for safe deployment

Milestone 2 — Summary
1
Closed-loop pipeline fully implemented: Stable Diffusion (text→image) + BLIP (image→text)
2
Round-trip evaluation confirmed >80% semantic preservation across test prompts
3
Seven evaluation metrics applied: FID, IS, CLIPScore, BLEU, METEOR, SSIM, PSNR
4
Modular architecture: each component deployable and testable in isolation via FastAPI
5
Reproducibility ensured: single-command install, Colab-validated, swappable model checkpoints
6
Ethical considerations addressed: bias documented; watermarking and fairness included in roadmap
Text-Image-GenAI  ·  SR University  ·  Milestone 2 Review  ·  40 Marks

## 🔑 Key Concepts
- **Text Image**: A key concept in the lecture: text image...
- **Text Image Image**: A key concept in the lecture: text image image...
- **Text Image Image Text**: A key concept in the lecture: text image image text...
- **Image Image**: A key concept in the lecture: image image...
- **Image Image Text**: A key concept in the lecture: image image text...

## 📌 Key Points
• Text-Image-GenAI
A Practical Pipeline for Text-to-Image and Image-to-Text
MILESTONE 2 REVIEW
Methodology Implementation & Results
Mani Sharan Deep Reddy Gade  ·  Shashidhar Mushike
Department of Computer Science  ·  SR University, Warangal, India
40
MARKS

MILESTONE 2
Milestone 2 — Evaluation Criteria
What is assessed in this review  ·  40 Marks total
1
Appropriateness of Methodology
Whether the chosen techniques (Stable Diffusion + BLIP) suit the problem objectives
8 pts
2
Correct Implementation / Experimentation
End-to-end pipeline execution: text→image and image→text with working code
8 pts
3
Data Generation and Analysis
Dataset sourcing (COCO, LAION, Kaggle), embedding storage, and processed outputs
8 pts
4
Interim Results and Observations
Quantitative metrics (FID, CLIPScore, BLEU) and qualitative caption evaluation
8 pts
5
Short Presentation Delivery
Clarity, completeness of methodology, validity of results, reproducibility
8 pts

MILESTONE 2
Methodology — Pipeline Architecture
Three primary functional blocks with modular, loosely-coupled design
BLOCK 1
Dataset Acquisition
KaggleHub integration
COCO Captions dataset
LAION subset (scale + diversity)
Independent of generative modules
Requirements.txt install
BLOCK 2
Generative Modeling
Stable Diffusion (LDM)
BLIP & BLIP-2 captioning
CLIP vision-language encoder
Latent diffusion denoising
Transformer-based decoding
BLOCK 3
Deployment Services
FastAPI microservice
JSON REST endpoints
Standalone modular execution
Google Colab compatible
NumPy embedding caching

MILESTONE 2
Mathematical Formulation
Core equations governing the generative pipeline
Compositional Pipeline
f(xT; Θ)  =  gN(·;θN) ∘ gN−1 ∘ … ∘ g1(·;θ1)
N modules composed in sequence — encoder → diffusion → decoder
Multi-Objective Loss
L(Θ)  =  α·Ltext  +  β·Limg  +  γ·Lperc  +  λR(Θ)
CLIP contrastive + diffusion reconstruction + perceptual + regularisation
CLIP Contrastive Loss
Ltext  =  −(1/B) Σ log exp(sim(uj,vj)/τ) / Σ exp(sim(uj,vk)/τ)
Aligns text embeddings uj and image embeddings vj via temperature τ
Diffusion Denoising Loss
Limg  =  E[  ‖ε − εθ(xt, t)‖²  ]
Predicts noise ε at timestep t to progressively denoise towards target image
Evaluation Score
Score  =  w₁·CLIPscore − w₂·FID + w₃·IS + w₄·BLEU
Unified scoring combining semantic alignment, fidelity, diversity, and caption quality

MILESTONE 2
Implementation Details
Correct experimentation: tools, models, and deployment
Text Encoder
CLIP Vision Tower — maps prompt to dense embedding space
Diffusion Model
Stable Diffusion (LDM) — iterative denoising from Gaussian noise to image
Image Decoder
VAE Decoder — reconstructs pixel image from latent representation
Caption Generator
BLIP / BLIP-2 — transformer decoder outputs fluent captions
IMPLEMENTATION HIGHLIGHTS
Framework:
PyTorch + Hugging Face Diffusers
Dataset:
KaggleHub / COCO / LAION subset
API Server:
FastAPI microservice (JSON endpoints)
Embedding Storage:
NumPy arrays (reusable across sessions)
Cloud Tested:
Google Colab with pre-installed GPU drivers
Guidance:
Classifier-free guidance for fidelity/diversity
Preview Mode:
Low-res → full-res progressive rendering
Model Swap:
BLIP replaceable with BLIP-2 via config

MILESTONE 2
Evaluation Metrics
Comprehensive quantitative assessment across image quality, semantic alignment, and caption accuracy
FID
Fréchet Inception Distance
Lower is Better
Image Quality
IS
Inception Score
Higher is Better
Image Quality
CLIPScore
CLIP Similarity
Higher is Better
Semantic Alignment
BLEU
Bilingual Eval Understudy
Higher is Better
Caption Quality
SSIM
Structural Similarity Index
0 → 1 scale
Image Fidelity
PSNR
Peak Signal-to-Noise Ratio
Higher is Better
Reconstruction

MILESTONE 2
Data Generation & Analysis
Dataset selection, embedding pipeline, and output samples
DATASETS USED
Dataset
Strength
Limitation
COCO Captions
High annotation quality
Limited domain diversity
LAION Subset
Large scale + diversity
Noisy captions
Kaggle GenAI
Controlled reproducibility
Limited size
BIDIRECTIONAL PIPELINE FLOW
Text Prompt
CLIP Encoding → Latent z
LDM Denoising → Image
BLIP Encoder → Caption
KEY OBSERVATION:
Embeddings stored as NumPy arrays eliminate redundant computation across sessions.
• MILESTONE 2
Interim Results & Observations
Quantitative metrics and qualitative analysis of generated outputs
>80%
Round-trip
Consistency
Low
FID
vs GAN
baselines
High
BLEU
METEOR &
CIDEr verified
Fluent
Captions
Semantically
accurate
Text-to-Image Quality
Stable Diffusion outperforms GAN baselines: lower FID scores confirm greater image fidelity; CLIPScore values confirm stronger semantic adherence to input prompts.
• MILESTONE 2
Completeness · Validity · Reproducibility
Measurable indicators for Milestone 2 assessment
Completeness of Methodology
✔
Full bidirectional pipeline implemented (text↔image)
Mathematical formulation defined (5 core equations)
Three functional modules operational independently
FastAPI deployment layer tested and documented
Validity of Results
✔
7 quantitative metrics applied (FID, IS, CLIP, BLEU, SSIM, PSNR, F1)
Round-trip consistency >80% on test prompts
Human-aligned captions confirmed via BLEU + METEOR + CIDEr
Comparison vs. GAN baselines shows diffusion superiority
Reproducibility of Outcomes
✔
requirements.txt single-command install
Pre-validated on Google Colab GPU environment
NumPy embedding cache enables session reuse
KaggleHub dataset module works independently; model checkpoints swappable

MILESTONE 2
Challenges & Future Directions
Known limitations and planned research extensions
CURRENT CHALLENGES
Computational cost — iterative denoising is GPU-intensive; limits real-time edge deployment
Caption hallucinations on ambiguous or complex scenes generate unsupported information
Training data bias reflected in generated images (gender, occupation stereotypes)
Fine-grained attribute control (exact counts, spatial relations, text rendering) under-performs
Interpretability — transformer + diffusion attention maps provide partial insight only
Closed-loop evaluation still relies on embedding similarity, not human contextual judgment
FUTURE DIRECTIONS
RLHF — Reinforcement Learning from Human Feedback for improved alignment and hallucination reduction
Cross-domain fine-tuning: medical imaging annotation, remote sensing, cultural heritage
Model efficiency — DDIM speedup, quantization, distillation for real-time deployment
Ethical guards — bias detection, fairness-aware training, dataset curation pipelines
Multimodal extension — incorporate audio, video, haptic feedback for richer closed loops
Watermarking generated outputs + adversarial robustness testing for safe deployment

Milestone 2 — Summary
1
Closed-loop pipeline fully implemented: Stable Diffusion (text→image) + BLIP (image→text)
2
Round-trip evaluation confirmed >80% semantic preservation across test prompts
3
Seven evaluation metrics applied: FID, IS, CLIPScore, BLEU, METEOR, SSIM, PSNR
4
Modular architecture: each component deployable and testable in isolation via FastAPI
5
Reproducibility ensured: single-command install, Colab-validated, swappable model checkpoints
6
Ethical considerations addressed: bias documented; watermarking and fairness included in roadmap
Text-Image-GenAI  ·  SR University  ·  Milestone 2 Review  ·  40 Marks

## 📊 Statistics
- Original text length: 8220 characters
- Summary length: 7275 characters
- Compression ratio: 88.5%
- Method: extractive

---
*Generated automatically from lecture transcript*
