<!-- ============================================================ -->
<!--  ✦  MUKUL RAYANA — GitHub Profile README                     -->
<!--  ✦  Theme: Stellar / Astral (Genshin-inspired cosmic palette) -->
<!-- ============================================================ -->

<div align="center">

  <!-- ✦ HEADER BANNER — deep space gradient (indigo → violet → cosmic blue) -->
  <img src="https://capsule-render.vercel.app/api?type=waving&color=0:0d1117,25:1a1a2e,50:16213e,75:0f3460,100:6a0572&height=230&section=header&text=Mukul%20Rayana&fontSize=48&fontColor=e8e8e8&animation=fadeIn&fontAlignY=32&desc=✦%20AI/ML%20Engineer%20·%20Game%20AI%20·%20LLMOps%20·%20Reinforcement%20Learning%20✦&descSize=16&descAlignY=55&descColor=b8c0e0" width="100%"/>

  <!-- ✦ TYPING SVG — animated role titles -->
  <a href="https://git.io/typing-svg">
    <img src="https://readme-typing-svg.demolab.com?font=Fira+Code&weight=600&size=22&duration=3000&pause=1000&color=A78BFA&center=true&vCenter=true&multiline=true&repeat=true&width=700&height=45&lines=Building+end-to-end+ML+systems+from+training+to+production+inference" alt="Typing SVG" />
  </a>

  <br>

  <!-- ✦ CONTACT BADGES -->
  <a href="https://linkedin.com/in/mukul-rayana"><img src="https://img.shields.io/badge/LinkedIn-0A66C2?style=for-the-badge&logo=linkedin&logoColor=white" /></a>&nbsp;
  <a href="mailto:mukulray@terpmail.umd.edu"><img src="https://img.shields.io/badge/Email-EA4335?style=for-the-badge&logo=gmail&logoColor=white" /></a>&nbsp;
  <a href="https://huggingface.co/spaces/MukulRay"><img src="https://img.shields.io/badge/🤗%20HuggingFace-FFD21E?style=for-the-badge" /></a>&nbsp;
  <a href="https://ieeexplore.ieee.org/document/10467441"><img src="https://img.shields.io/badge/IEEE%20Published-00629B?style=for-the-badge&logo=ieee&logoColor=white" /></a>

  <br><br>

  **M.S. Applied Machine Learning** · University of Maryland, College Park (May 2026)  
  Every project below has **real eval metrics**, **public repos**, and **live deployments**.

</div>

---

<!-- ✦✦✦ TECH STACK — skill-icons ✦✦✦ -->

### ✦ Tech Arsenal

<div align="center">
  <a href="https://skillicons.dev">
    <img src="https://skillicons.dev/icons?i=python,pytorch,tensorflow,cpp,cs,docker,fastapi,aws,azure,git,github,githubactions,linux,unity,vscode&theme=dark&perline=15" />
  </a>
</div>

<div align="center">

| Domain | Stack |
|:---|:---|
| **GenAI & LLMs** | LangChain · LangGraph · LoRA / QLoRA · RAG · Agentic AI · Multi-Agent Systems · vLLM · Pinecone · Guardrails · Ragas |
| **ML & DL** | PyTorch · TensorFlow · Reinforcement Learning · Scikit-learn · OpenCV · NumPy · Pandas |
| **MLOps & Infra** | MLflow · FastAPI · Docker · AWS (EC2/S3) · Azure (ACR/ACI) · GitHub Actions CI/CD · ONNX · Unity Sentis · Ray RLlib · CUDA |
| **Languages** | Python · SQL · C++ · C# · Bash |

</div>

---

<!-- ✦✦✦ FEATURED PROJECTS — stacked full-width cards ✦✦✦ -->

### ✦ Featured Projects

<!-- ───────────── PROJECT 1: NEMESIS ───────────── -->

<table>
<tr><td>

### ⚔️ [Nemesis — Distributed RL Boss AI with Real-Time LLM Narration](https://github.com/MukulRay1603/nemesis-boss-ai)

<div align="center">

| Metric | Result |
|:--|:--|
| **Training** | PPO · 3-stage curriculum · 300K steps · reward −2.4 → 13.2 |
| **Distributed Scaling** | Ray RLlib · 1 → 8 workers · **2.6× wall-clock speedup** |
| **Runtime Inference** | ONNX → Unity Sentis · **<2 ms/frame** · 60 fps · zero Python runtime |
| **LLM Narration** | Groq LLaMA-3.3-70B + NeMo Guardrails over TCP · 114–352 ms |
| **Eval** | RL boss outlasts scripted FSM baseline by **85%** (37s vs 20s avg, 50 episodes) |
| **Phase Escalation** | All 3 difficulty phases reached in **100%** of episodes |

</div>

> `PPO` `Ray RLlib` `Unity ML-Agents` `ONNX` `Unity Sentis` `Groq` `NeMo Guardrails` `MLflow` `C#`

</td></tr>
</table>

<!-- ───────────── PROJECT 2: EMPATHRAG ───────────── -->

<table>
<tr><td>

### 🛡️ [EmpathRAG — NLI Safety Guardrail & Emotion-Conditioned RAG](https://github.com/MukulRay1603/Empath-RAG)

<div align="center">

| Metric | Result |
|:--|:--|
| **Crisis Detection** | DeBERTa-v3-base NLI on 232K pairs · **0.9629 recall** · 30 adversarial probes in 6 attack categories |
| **Explainability** | captum Integrated Gradients on **every** safety intercept · auditable token-level XAI |
| **Retrieval** | 5-stage pipeline · **1.67M-vector FAISS** index · RoBERTa + LoRA (0.7127 F1) |
| **Ablation** | Emotion alignment **0.88** vs 0.30 BM25 baseline |
| **Significance** | Wilcoxon p = **3.62 × 10⁻⁸** (Condition D vs A) |

</div>

> `DeBERTa` `RoBERTa` `LoRA` `FAISS` `captum` `NLI` `Mistral 7B (GGUF)` `PyTorch`

</td></tr>
</table>

<!-- ───────────── PROJECT 3: RECON ───────────── -->

<table>
<tr><td>

### 🔍 [RECON — Agentic ML Research Navigator](https://github.com/MukulRay1603/project-recon) &nbsp;·&nbsp; [🚀 Live Demo](https://huggingface.co/spaces/MukulRay/recon)

<div align="center">

| Metric | Result |
|:--|:--|
| **Architecture** | 4-agent LangGraph state machine (planner → retriever → critic → synthesizer) + retry loop |
| **Critic Taxonomy** | 4 verdicts: PASS / STALE / CONTRADICTED / INSUFFICIENT |
| **Staleness Detection** | Catches **52%** superseded ML claims vs **0%** single-pass RAG (130-question eval) |
| **Decay Ablation** | Linear optimal (52%) vs no-decay (42%) vs log-decay (38%) |
| **Position Accuracy** | **43.9%** vs 32.3% baseline |

</div>

> `LangGraph` `Groq LLaMA-3.3-70B` `Semantic Scholar API` `Tavily` `Gradio` `HuggingFace Spaces`

</td></tr>
</table>

<!-- ───────────── PROJECT 4: IRMINSUL ───────────── -->

<table>
<tr><td>

### 🌳 [Irminsul — Production LLMOps System](https://github.com/MukulRay1603/Irminsul) &nbsp;·&nbsp; [🚀 Live Demo](https://huggingface.co/spaces/MukulRay/Irminsul)

<div align="center">

| Metric | Result |
|:--|:--|
| **Fine-tuning** | Llama 3.1 8B · QLoRA (rank 16, lr 2e-4) · 3 MLflow-tracked experiments |
| **Best Checkpoint** | Semantic similarity **0.826** · ROUGE-L 0.466 |
| **Serving Stack** | FastAPI + LangChain + Pinecone RAG + guardrails + confidence-gated web fallback |
| **Corpus Pipeline** | [irminsul-corpus](https://github.com/MukulRay1603/irminsul-corpus) · **840 docs** · **6,876 vectors** · 3 trust tiers |
| **Automation** | GitHub Actions weekly ingest → Pinecone upsert · zero manual intervention |

</div>

> `QLoRA` `LangChain` `Pinecone` `FastAPI` `Docker` `MLflow` `HuggingFace Spaces` `GitHub Actions CI/CD`

</td></tr>
</table>

---

<!-- ✦✦✦ PUBLICATION ✦✦✦ -->

### ✦ Publication

<table>
<tr><td>

📄 **Voice-Driven Panoramic VR Generation** — *IEEE IDCIoT 2024*  
Speech → 360° image pipeline (Whisper · GPT-Neo · Stable Diffusion) · **2.3× throughput** via attention slicing on 10 GB VRAM  
🔗 [DOI: 10.1109/IDCIoT59759.2024.10467441](https://ieeexplore.ieee.org/document/10467441)

</td></tr>
</table>

---

<!-- ✦✦✦ GITHUB STATS ✦✦✦ -->

### ✦ GitHub Activity

<div align="center">
  <img src="https://github-readme-stats.vercel.app/api?username=MukulRay1603&show_icons=true&theme=tokyonight&hide_border=true&bg_color=0d1117&title_color=a78bfa&icon_color=a78bfa&text_color=b8c0e0&ring_color=a78bfa" height="170" />
  &nbsp;&nbsp;
  <img src="https://github-readme-stats.vercel.app/api/top-langs/?username=MukulRay1603&layout=compact&theme=tokyonight&hide_border=true&bg_color=0d1117&title_color=a78bfa&text_color=b8c0e0" height="170" />
</div>

<div align="center">
  <br>
  <img src="https://github-readme-streak-stats.herokuapp.com?user=MukulRay1603&theme=tokyonight&hide_border=true&background=0D1117&ring=A78BFA&fire=A78BFA&currStreakLabel=A78BFA&sideLabels=B8C0E0&dates=6E7681" />
</div>

---

<!-- ✦✦✦ CURRENTLY ✦✦✦ -->

### ✦ Currently

```
🔭  Wrapping up Nemesis — LLM-as-judge eval + demo recording
🎓  Graduating May 2026 — STEM OPT eligible
🎯  Seeking: AI/ML Engineer · GenAI · Game AI · LLMOps · RL Engineer
🧗  Off-hours: climbing walls, Genshin theory-crafting, houseplants
```

---

<div align="center">

  <!-- ✦ FOOTER — matching cosmic gradient -->
  <img src="https://capsule-render.vercel.app/api?type=waving&color=0:6a0572,25:0f3460,50:16213e,75:1a1a2e,100:0d1117&height=120&section=footer" width="100%"/>

  <br>

  *✦ "The stars, the sky... it's all a gigantic hoax." — Mona, probably ✦*

</div>
