# CloudAgent 简历两页版改写方案

## 总体策略

你现在的 `简历2.0.pdf` 是一页版，CloudAgent 和 SAR 深度学习项目都挤在同一页。原来的 CloudAgent 更像学习型 Demo 时，这样安排还可以；但现在企业副本已经补了工程化、安全、观测、部署和验证能力，CloudAgent 已经足够作为第一页主项目完整展开。

推荐改成两页：

```text
第 1 页：CloudAgent Enterprise，突出 AI Agent 应用工程能力
第 2 页：SAR 遥感语义分割项目，突出深度学习和实验能力
```

这样逻辑更清楚：第一页告诉面试官“我能做一个完整 AI Agent 应用”，第二页证明“我还有扎实的 Python/PyTorch/实验评估基础”。

## 第 1 页结构

### 个人信息和教育经历

保留姓名、电话、邮箱、城市、GitHub、教育经历，但教育经历要压缩。第一页真正的核心应该是 CloudAgent，不要让教育经历占太多版面。

建议格式：

```text
魏子航 | 15045908718 | 2529427746@qq.com | 西安 | GitHub: github.com/zihang3417-sys/cloudagent
西安电子科技大学 信息与通信工程 硕士 2025.09-2028.06 | 通信工程 本科 2021.09-2025.06
```

### 项目标题

```text
CloudAgent Enterprise：云平台客服 Multi-Agent 智能体系统
GitHub: github.com/zihang3417-sys/cloudagent
角色：核心开发 / 企业级工程化改造
时间：2026.04 - 至今
```

### 技术栈

```text
Python、FastAPI、Vue3、LangGraph、LangChain、SSE、MCP-style Tool Calling、
Redis、Milvus、Neo4j、MySQL、Docker Compose、Ollama/Qwen、pytest、GitHub Actions
```

### 一句话项目描述

```text
面向云平台客服/运维场景，构建一个企业级改造方向的 AI 助手 MVP，融合 LangGraph 多 Agent 编排、MCP 工具调用、RAG/GraphRAG、记忆、语义缓存、流式问答、安全边界、可观测性、CI/Eval 与部署就绪骨架。
```

## CloudAgent 推荐简历 bullet

建议放 5-7 条。空间紧张时保留前 5 条；如果第一页完整给 CloudAgent，可以保留 6-7 条。

1. 基于 FastAPI + Vue3 构建云平台客服智能体系统，实现 `/api/chat` 流式问答链路，并通过 SSE 将多 Agent 处理结果实时返回前端。

2. 基于 LangGraph 设计 Multi-Agent 编排流程，由 Orchestrator 按意图路由至 Billing、Product、Recommendation、Promotion、FinOps 等专家 Agent，并通过 AgentState 传递用户身份、会话、记忆上下文和工具调用状态。

3. 封装订单查询、实例查询、监控分析、商品检索、推广物料等 MCP-style 业务工具，支持账单/实例查询、产品问答、选型推荐、推广物料和资源降本等场景。

4. 集成 Redis 短期记忆、Milvus 长期记忆与语义缓存、Milvus 文档 RAG、Neo4j GraphRAG，支持产品文档问答、规格关系查询、高频问题缓存和用户偏好沉淀。

5. 补齐企业级可信基础设施，包括 trace_id 请求追踪、结构化 JSON 日志、健康/就绪检查、请求指标、稳定错误响应、golden eval 回归集和 GitHub Actions CI。

6. 增强安全和运行韧性，实现后端可信用户身份边界、跨用户访问拦截、Prompt Injection/Secret Exfiltration 规则拦截、日志 PII 脱敏、请求限流和工作流超时保护。

7. 增加 SQLite LangGraph checkpoint、本地后端 Dockerfile、企业版 Docker Compose override、容器环境样例和 Compose 配置发布门禁，形成小公司内部试点级部署骨架。

## 第 1 页关键词

可以放在项目描述或技能区里：

```text
Multi-Agent 编排、AgentState、Tool Calling、RAG、GraphRAG、语义缓存、记忆系统、
SSE 流式响应、可观测性、安全边界、CI/Eval、Docker Compose
```

## 第 2 页结构

第 2 页放 SAR 深度学习项目和专业技能。它不应该被删掉，因为它证明你不是只会调大模型 API，而是有真实深度学习、数据处理、实验评估和模型优化经验。

### SAR 项目标题

```text
SAR 遥感海陆/水体语义分割与轻量化模型优化
角色：项目负责人
时间：2025.09 - 至今
```

### SAR 推荐简历 bullet

1. 整合 sea-land segmentation、FUSAR、Water256 等数据源，构建统一 SAR 二类分割数据集，完成标签映射、数据划分、灰度图/掩膜/Polygon 标签转换、512x512 标准化预处理和评估流程搭建。

2. 复现传统 SAR 海陆分割方法，完成先验约束、区域合并、形态学后处理等流程，并与深度学习方法对比；传统方法测试集 IoU 0.8357，YOLO11s-Seg 测试集 IoU 0.9771、Accuracy 0.9887。

3. 基于 PyTorch 搭建 DeepLabV3+、YOLO11/YOLO26、SegFormer、UPerNet、EfficientViT 等模型训练与评估流程，统一输出 mIoU、Accuracy、IoU、Precision、Recall 等指标。

4. 对比不同主干与轻量化模型效果，其中 DeepLabV3+ + ResNet18 在 323SAR 测试集达到 mIoU 0.9686、Water IoU 0.9747；EfficientNet-B0 在 4.91M 参数量下达到 mIoU 0.9613。

5. 引入 EfficientViT-B1 轻量化分割模型，结合 CNN 金字塔特征与 LiteMLA 轻量多尺度注意力机制进行实验；模型参数量约 4.78M，测试集达到 mIoU 0.9825、Accuracy 0.9916，并完成推理脚本、可视化输出与 ONNX 导出验证。

6. 针对 SAR 图像纹理与散射特性，设计灰度、局部方差、GLCM 对比度/同质性等特征通道，并结合 Feature Gate、Channel Attention、Spatial Attention、CBAM 等模块开展消融实验。

## 技能区改写

建议分成四组，避免一长串堆技术名。

```text
AI Agent 应用工程：LangGraph、LangChain、RAG、GraphRAG、Tool Calling、MCP-style 工具、AgentState、记忆系统、语义缓存、Prompt Injection 防护。

后端与 AI 应用开发：Python、FastAPI、SSE、Pydantic、pytest、结构化日志、指标监控、GitHub Actions、Docker Compose。

数据与基础设施：MySQL、Redis、Milvus、Neo4j、Ollama/Qwen、DashScope Embedding、本地部署与演示环境搭建。

深度学习与遥感：PyTorch、OpenCV、NumPy、语义分割、轻量化模型、注意力机制、ONNX 导出、实验评估与可视化。
```

## 不要过度承诺

不要写：

```text
生产级 SaaS 平台
真实 OAuth/JWT 登录系统
大规模分布式部署
完整企业多租户平台
```

更安全的写法：

```text
企业级改造方向的 AI 助手 MVP
小公司内部试点级系统
本地可复现实验/演示环境
生产就绪骨架
```
