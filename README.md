<h1 align="center">Mukul Rayana</h1>
<h3 align="center">AI/ML Engineer · Game AI · LLMOps · Reinforcement Learning</h3>

<p align="center">
  M.S. Applied Machine Learning · University of Maryland, College Park (May 2026)<br>
  IEEE-published · Production deployments on HuggingFace Spaces, AWS, Azure
</p>

<p align="center">
  <a href="https://linkedin.com/in/mukul-rayana">
    <img src="https://img.shields.io/badge/LinkedIn-0A66C2?style=flat-square&logo=linkedin&logoColor=white" />
  </a>
  <a href="mailto:mukulray@umd.edu">
    <img src="https://img.shields.io/badge/Email-EA4335?style=flat-square&logo=gmail&logoColor=white" />
  </a>
  <a href="https://huggingface.co/spaces/MukulRay">
    <img src="https://img.shields.io/badge/HuggingFace-FFD21E?style=flat-square&logo=huggingface&logoColor=black" />
  </a>
  <a href="https://ieeexplore.ieee.org/document/10467441">
    <img src="https://img.shields.io/badge/IEEE_Publication-00629B?style=flat-square&logo=ieee&logoColor=white" />
  </a>
</p>

---

### What I Build

I build end-to-end ML systems — from training to production inference — with a focus on **LLMOps pipelines**, **agentic AI architectures**, **reinforcement learning in game engines**, and **safety-critical AI guardrails**. Every project below has real eval metrics, public repos, and live deployments.

---

### Featured Projects

#### ⚔️ [Nemesis — Distributed RL Boss AI with Real-Time LLM Narration](https://github.com/MukulRay1603/nemesis-boss-ai)
PPO agent trained with 3-stage curriculum learning (300K steps, reward −2.4 → 13.2) via **Ray RLlib** across 8 parallel workers (2.6× speedup). Exported to ONNX, deployed via **Unity Sentis** at <2 ms/frame — 60 fps, zero Python runtime. Real-time LLM narration layer (Groq LLaMA-3.3-70B + NeMo Guardrails, 114–352 ms) over TCP. RL boss outlasted scripted FSM baseline by 85% across 50 episodes.

`PPO` `Ray RLlib` `Unity ML-Agents` `ONNX` `Unity Sentis` `Groq` `NeMo Guardrails` `MLflow` `C#`

---

#### 🛡️ [EmpathRAG — NLI Safety Guardrail & Emotion-Conditioned RAG](https://github.com/MukulRay1603/Empath-RAG)
Fine-tuned DeBERTa-v3-base on 232K NLI pairs for crisis detection — **0.9629 recall** on 30 adversarial probes across 6 attack categories. **captum Integrated Gradients** on every safety intercept for auditable token-level XAI. 5-stage emotion-conditioned RAG over a **1.67M-vector FAISS index** (RoBERTa + LoRA, 0.7127 F1). Ablation: emotion alignment 0.88 vs. 0.30 BM25 baseline — Wilcoxon p = 3.62 × 10⁻⁸.

`DeBERTa` `RoBERTa` `LoRA` `FAISS` `captum` `NLI` `Mistral 7B (GGUF)` `PyTorch`

---

#### 🔍 [RECON — Agentic ML Research Navigator](https://github.com/MukulRay1603/project-recon) · [Live Demo](https://huggingface.co/spaces/MukulRay/recon)
Four-agent **LangGraph** state machine with a retry loop and 4-verdict critic taxonomy (PASS / STALE / CONTRADICTED / INSUFFICIENT). Catches **52% of superseded ML claims** vs. 0% for single-pass RAG on a 130-question ground-truth eval. Ablated 3 recency-decay formulas — linear decay optimal (52% vs. 42% no-decay, 38% log-decay). Position accuracy 43.9% vs. 32.3% baseline.

`LangGraph` `Groq` `Semantic Scholar API` `Tavily` `Gradio` `HuggingFace Spaces`

---

#### 🌳 [Irminsul — Production LLMOps System](https://github.com/MukulRay1603/Irminsul) · [Live Demo](https://huggingface.co/spaces/MukulRay/Irminsul)
Fine-tuned Llama 3.1 8B with **QLoRA** (rank 16, lr 2e-4); selected winning checkpoint from 3 MLflow-tracked experiments by semantic similarity (0.826) and ROUGE-L (0.466). FastAPI + LangChain + Pinecone RAG with guardrails and confidence-gated web fallback. Companion [corpus pipeline](https://github.com/MukulRay1603/irminsul-corpus) autonomously ingests 840 documents across 3 trust tiers and upserts 6,876 vectors to Pinecone weekly via **GitHub Actions CI/CD**.

`QLoRA` `LangChain` `Pinecone` `FastAPI` `Docker` `MLflow` `HuggingFace Spaces` `GitHub Actions`

---

### Publication

**Voice-Driven Panoramic VR Generation** — IEEE IDCIoT 2024  
Speech-to-360° image pipeline (Whisper → GPT-Neo → Stable Diffusion). 2.3× throughput via attention slicing on 10 GB VRAM.  
[DOI: 10.1109/IDCIoT59759.2024.10467441](https://ieeexplore.ieee.org/document/10467441)

---

### Technical Skills

**Languages:** Python, SQL, C++, C#, Bash

**ML & DL:** PyTorch · TensorFlow · Reinforcement Learning · Scikit-learn · OpenCV · NumPy · Pandas

**GenAI & LLMs:** LangChain · LangGraph · PEFT / LoRA / QLoRA · RAG · Agentic AI · Multi-Agent Systems · Prompt Engineering · Fine-tuning · vLLM · Pinecone · Guardrails · Ragas

**MLOps & Infra:** MLflow · FastAPI · Docker · AWS (EC2/S3) · Azure (ACR/ACI) · GitHub Actions CI/CD · ONNX · Unity Sentis · Ray RLlib · HuggingFace · CUDA · Linux

---

### Currently

- 🔭 Wrapping up Nemesis (LLM-as-judge eval + demo recording) and actively job hunting
- 🎯 Targeting: **AI/ML Engineer · GenAI Engineer · Game AI · LLMOps · RL Engineer**
- 🎓 Graduating May 2026 — STEM OPT eligible
- 🧗 Off-hours: climbing walls, Genshin Impact theory-crafting, keeping houseplants alive
