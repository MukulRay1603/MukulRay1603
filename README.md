<div align="center">
  
  <!-- REPLACE with your own banner — a custom-made one or a screenshot from your Nemesis project would be ideal -->
  <img src="https://capsule-render.vercel.app/api?type=waving&color=0:0d1117,50:161b22,100:1f6feb&height=220&section=header&text=Mukul%20Rayana&fontSize=42&fontColor=ffffff&animation=fadeIn&fontAlignY=35&desc=AI/ML%20Engineer%20·%20Game%20AI%20·%20LLMOps%20·%20Reinforcement%20Learning&descSize=16&descAlignY=55&descColor=8b949e" width="100%"/>

</div>

<p align="center">
  <a href="https://linkedin.com/in/mukul-rayana"><img src="https://img.shields.io/badge/LinkedIn-0A66C2?style=for-the-badge&logo=linkedin&logoColor=white" /></a>&nbsp;
  <a href="mailto:mukulray@umd.edu"><img src="https://img.shields.io/badge/Email-EA4335?style=for-the-badge&logo=gmail&logoColor=white" /></a>&nbsp;
  <a href="https://huggingface.co/spaces/MukulRay"><img src="https://img.shields.io/badge/🤗%20HuggingFace-FFD21E?style=for-the-badge&logoColor=black" /></a>&nbsp;
  <a href="https://ieeexplore.ieee.org/document/10467441"><img src="https://img.shields.io/badge/IEEE%20Published-00629B?style=for-the-badge&logo=ieee&logoColor=white" /></a>
</p>

<p align="center">
  <b>M.S. Applied Machine Learning</b> · University of Maryland, College Park (May 2026)<br>
  Building end-to-end ML systems — from distributed training to production inference.<br>
  Every project below has <b>real eval metrics</b>, <b>public repos</b>, and <b>live deployments</b>.
</p>

---

### ⚡ Tech Stack

<div align="center">

| Domain | Technologies |
|:---|:---|
| **Languages** | `Python` `SQL` `C++` `C#` `Bash` |
| **ML & DL** | `PyTorch` `TensorFlow` `Reinforcement Learning` `Scikit-learn` `OpenCV` |
| **GenAI & LLMs** | `LangChain` `LangGraph` `LoRA / QLoRA` `RAG` `Agentic AI` `Multi-Agent Systems` `vLLM` `Pinecone` `Guardrails` |
| **MLOps & Infra** | `MLflow` `FastAPI` `Docker` `AWS` `Azure` `GitHub Actions CI/CD` `ONNX` `Unity Sentis` `Ray RLlib` `CUDA` |

</div>

---

### 🏗️ Featured Projects

<table>
<tr>
<td width="50%" valign="top">

#### ⚔️ [Nemesis](https://github.com/MukulRay1603/nemesis-boss-ai)
**Distributed RL Boss AI + Real-Time LLM Narration**

| | |
|:--|:--|
| Training | PPO · 300K steps · reward −2.4 → 13.2 |
| Scaling | Ray RLlib · 8 workers · **2.6× speedup** |
| Runtime | ONNX → Unity Sentis · **<2 ms/frame · 60 fps** |
| LLM Layer | Groq LLaMA-3.3-70B + NeMo Guardrails · 114–352 ms |
| Eval | RL boss outlasts FSM baseline by **85%** (50 episodes) |

`PPO` `Ray RLlib` `Unity Sentis` `ONNX` `Groq` `NeMo` `MLflow` `C#`

</td>
<td width="50%" valign="top">

#### 🛡️ [EmpathRAG](https://github.com/MukulRay1603/Empath-RAG)
**NLI Safety Guardrail & Emotion-Conditioned RAG**

| | |
|:--|:--|
| Safety | DeBERTa NLI · **0.9629 crisis recall** · 30 adversarial probes |
| XAI | captum Integrated Gradients on every intercept |
| Retrieval | **1.67M-vector FAISS** · RoBERTa + LoRA (0.7127 F1) |
| Ablation | Emotion alignment **0.88** vs 0.30 BM25 baseline |
| Significance | Wilcoxon p = **3.62 × 10⁻⁸** |

`DeBERTa` `RoBERTa` `LoRA` `FAISS` `captum` `Mistral 7B` `PyTorch`

</td>
</tr>

<tr>
<td width="50%" valign="top">

#### 🔍 [RECON](https://github.com/MukulRay1603/project-recon) · [Live Demo ↗](https://huggingface.co/spaces/MukulRay/recon)
**Agentic ML Research Navigator (LangGraph)**

| | |
|:--|:--|
| Architecture | 4-agent LangGraph state machine + retry loop |
| Critic | 4-verdict taxonomy: PASS / STALE / CONTRADICTED / INSUFFICIENT |
| Staleness | Catches **52%** superseded claims vs **0%** single-pass RAG |
| Decay Ablation | Linear optimal (52% vs 42% no-decay, 38% log-decay) |
| Position Acc. | **43.9%** vs 32.3% baseline (130-question eval) |

`LangGraph` `Groq` `Semantic Scholar` `Tavily` `Gradio` `HF Spaces`

</td>
<td width="50%" valign="top">

#### 🌳 [Irminsul](https://github.com/MukulRay1603/Irminsul) · [Live Demo ↗](https://huggingface.co/spaces/MukulRay/Irminsul)
**Production LLMOps System**

| | |
|:--|:--|
| Fine-tuning | Llama 3.1 8B · QLoRA (rank 16, lr 2e-4) |
| Tracking | 3 MLflow experiments · best by sim **0.826** / ROUGE-L 0.466 |
| Serving | FastAPI + LangChain + Pinecone RAG + guardrails |
| Corpus | [Auto-pipeline](https://github.com/MukulRay1603/irminsul-corpus) · 840 docs · 6,876 vectors · 3 tiers |
| CI/CD | GitHub Actions weekly ingest → Pinecone upsert |

`QLoRA` `LangChain` `Pinecone` `FastAPI` `Docker` `MLflow` `GitHub Actions`

</td>
</tr>
</table>

---

### 📄 Publication

> **Voice-Driven Panoramic VR Generation** — *IEEE IDCIoT 2024*  
> Speech → 360° image pipeline (Whisper · GPT-Neo · Stable Diffusion) · 2.3× throughput via attention slicing on 10 GB VRAM  
> [DOI: 10.1109/IDCIoT59759.2024.10467441](https://ieeexplore.ieee.org/document/10467441)

---

### 🎯 Currently

```
🔭  Wrapping up Nemesis (LLM-as-judge eval + demo recording)
🎓  Graduating May 2026 — STEM OPT eligible
🎯  Seeking: AI/ML Engineer · GenAI · Game AI · LLMOps · RL Engineer
🧗  Off-hours: climbing walls, Genshin theory-crafting, houseplants
```

<div align="center">
  <img src="https://capsule-render.vercel.app/api?type=waving&color=0:0d1117,50:161b22,100:1f6feb&height=100&section=footer" width="100%"/>
</div>
