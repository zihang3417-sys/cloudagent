# CloudAgent Resume Rewrite Plan

## Overall Strategy

The current resume uses one page for both CloudAgent and the SAR segmentation
research project. After the enterprise refactor, CloudAgent is strong enough to
become the entire first page. The SAR/deep-learning project should move to page
two, where it can support your original deep-learning strength.

Recommended positioning:

```text
Page 1: AI Agent application engineering / enterprise AI assistant MVP
Page 2: Deep learning and SAR segmentation research / model optimization
```

This is more coherent than squeezing both into one page. Page one tells the
employer: "I can build a real AI Agent application." Page two tells them:
"I also have solid Python, PyTorch, experiment, and model-evaluation skills."

## Page 1 Layout

### Header

Keep the current name, phone, email, city, education summary, and GitHub link.
Do not let education consume too much space. Use a compact two-line format.

### Project Title

```text
CloudAgent Enterprise: Cloud Platform Multi-Agent Assistant MVP
GitHub: github.com/zihang3417-sys/cloudagent
Role: Core developer / independent engineering refactor
Time: 2026.04 - Present
```

### Technology Stack

```text
Python, FastAPI, Vue3, LangGraph, LangChain, SSE, MCP-style Tool Calling,
Redis, Milvus, Neo4j, MySQL, Docker Compose, Ollama/Qwen, pytest, GitHub Actions
```

### One-Sentence Project Summary

```text
Built a cloud-service AI assistant MVP that combines LangGraph multi-agent
orchestration, RAG/GraphRAG, business tool calling, memory, semantic cache,
streaming chat, and enterprise-oriented reliability controls for internal pilot
usage.
```

### Recommended Resume Bullets

Use 5 to 7 bullets. The first 5 are enough for most resumes; add the last 2
only if space allows.

1. Built an end-to-end FastAPI + Vue3 cloud-service assistant with SSE
   streaming responses, LangGraph multi-agent orchestration, and specialist
   agents for billing, product Q&A, recommendation, promotion, and FinOps
   scenarios.

2. Designed the core request path from `/api/chat` to semantic cache, memory
   context, LangGraph workflow, MCP-style business tools, RAG/GraphRAG, and
   streamed frontend response.

3. Integrated Redis short-term memory, Milvus long-term memory and semantic
   cache, Milvus document RAG, and Neo4j GraphRAG to support product-document
   Q&A, instance-spec relationship queries, and user preference context.

4. Encapsulated order, instance, monitoring, product-catalog, and promotion
   operations as MCP-style tools, and added backend-trusted user identity plus
   cross-user access blocking to reduce prompt-injection driven data leakage.

5. Added enterprise-oriented trust foundations including trace IDs, structured
   JSON logs, health/readiness endpoints, request metrics, stable error
   contracts, golden eval regression cases, and GitHub Actions CI.

6. Improved runtime resilience with SQLite LangGraph checkpointing, structured
   log PII redaction, per-user rate limiting, configurable workflow timeout
   handling, and safe SSE error payloads.

7. Added backend deployment readiness with Dockerfile, enterprise Compose
   override, container env template, compose-config release gate, and
   documentation for small-company internal pilot deployment.

## Page 1 Interview Keywords

Place these near the project or skills section:

```text
Multi-Agent orchestration, AgentState, Tool Calling, RAG, GraphRAG, semantic
cache, memory, SSE streaming, observability, guardrails, CI/eval, Docker Compose
```

## Page 2 Layout

### SAR Project Title

```text
SAR Remote Sensing Sea-Land/Water Segmentation and Lightweight Model Optimization
Role: Project owner
Time: 2025.09 - Present
```

### SAR Resume Bullets

1. Built a unified SAR segmentation dataset from multiple data sources, covering
   label mapping, train/test split, grayscale-image and mask processing,
   polygon conversion, 512x512 preprocessing, and evaluation pipeline setup.

2. Reproduced traditional SAR sea-land segmentation methods and compared them
   with deep-learning baselines; traditional method reached IoU 0.8357, while
   YOLO11s-Seg reached IoU 0.9771 and Accuracy 0.9887 on the test set.

3. Built PyTorch training and evaluation workflows for DeepLabV3+, YOLO11/26,
   SegFormer, UPerNet, and EfficientViT, standardizing mIoU, Accuracy, IoU,
   Precision, and Recall reporting.

4. Compared lightweight backbones and segmentation models; DeepLabV3+ +
   ResNet18 reached mIoU 0.9686 and Water IoU 0.9747, while EfficientNet-B0
   reached mIoU 0.9613 with 4.91M parameters.

5. Introduced EfficientViT-B1 with CNN pyramid features and LiteMLA attention,
   reaching mIoU 0.9825 and Accuracy 0.9916 with about 4.78M parameters, and
   completed inference, visualization, and ONNX export validation.

6. Explored SAR-specific features such as grayscale, local variance, GLCM
   contrast/homogeneity, Feature Gate, Channel Attention, Spatial Attention,
   and CBAM for ablation experiments.

## Skills Section Rewrite

Use four compact skill groups:

```text
AI Agent Engineering: LangGraph, LangChain, RAG, GraphRAG, Tool Calling,
MCP-style tools, AgentState, memory, semantic cache, prompt-injection defense.

Backend and AI Application: Python, FastAPI, SSE, Pydantic, pytest,
structured logging, metrics, GitHub Actions, Docker Compose.

Data and Infra: MySQL, Redis, Milvus, Neo4j, Ollama/Qwen, DashScope embedding,
local deployment and demo environment setup.

Deep Learning: PyTorch, OpenCV, NumPy, semantic segmentation, lightweight
models, attention modules, ONNX export, experiment evaluation and visualization.
```

## Important Boundary

Do not write:

```text
production-grade SaaS
real OAuth/JWT authentication
large-scale distributed deployment
full enterprise multi-tenant platform
```

Safer wording:

```text
enterprise-oriented AI assistant MVP
small-company internal pilot
local reproducible demo
production-readiness scaffolding
```
