# 03 · 全双工语音对话 / 端到端语音 LLM

> 这一层的核心分歧是 **级联（ASR → LLM → TTS） vs 端到端（speech-in, speech-out）**。
> 级联工程可控、可替换、可观测，但延迟天花板约 600–800ms，且**丢掉副语言信息**（语气、情绪、犹豫、被打断的意图）。
> 端到端模型把延迟压到 200ms 级、能"听见情绪"，代价是**可控性差、难调试、生态工具少**。

## 主表

| 项目 | 地址 | 许可 | 形态 | 语言 | 关键点 | 核实 |
|---|---|---|---|---|---|---|
| Moshi | [kyutai-labs/moshi](https://github.com/kyutai-labs/moshi) | Apache-2.0 / MIT（代码），CC-BY 4.0（权重） | 全双工语音对话 | 英（多语实验性） | 首个真·全双工开源，Mimi codec | 2026-10 |
| Hibiki / Hibiki-Zero | [kyutai-labs](https://github.com/kyutai-labs) | 见仓库 | 实时语音翻译（S2ST） | 4 语言 | 无需对齐数据的同传 | 2026-10 |
| Unmute | [kyutai-labs/unmute](https://github.com/kyutai-labs/unmute) | 见仓库 | 给任意文本 LLM 加"听说" | 多语 | STT + TTS 低延迟串联 | 2026-10 |
| Qwen-Omni（2.5/3） | [QwenLM/Qwen2.5-Omni](https://github.com/QwenLM/Qwen2.5-Omni) | Apache-2.0 | 端到端多模态（听/说/看） | 多语 | 语音输入 + 语音输出 + 视觉 | 2026-10 |
| GLM-4-Voice | [THUDM/GLM-4-Voice](https://github.com/THUDM/GLM-4-Voice) | Apache-2.0 | 端到端中文语音对话 | 中/英 | 中文情绪与语速可控 | 2026-10 |
| Step-Audio 2 | [stepfun-ai/Step-Audio2](https://github.com/stepfun-ai/Step-Audio2) | Apache-2.0 | 端到端语音理解+生成 | 中/英 | 工具调用、副语言理解 | 2026-10 |
| Ultravox | [fixie-ai/ultravox](https://github.com/fixie-ai/ultravox) | MIT | 语音 LLM（语音进文本出） | 多语 | 轻量、易微调 | 2026-10 |
| MiniCPM-o | [OpenBMB/MiniCPM-o](https://github.com/OpenBMB/MiniCPM-o) | 见仓库 | 端侧多模态实时对话 | 中/英 | 手机端可跑 | 2026-10 |

---

## 重点条目

### Moshi（Kyutai）— 全双工的开山之作

- **地址**：[kyutai-labs/moshi](https://github.com/kyutai-labs/moshi)
- **定位**：第一个真正意义上的**端到端全双工**语音对话系统（2024-07 发布，比 GPT-4o 语音模式早一个月）
- **架构**：直接在语音 token 层建模，**跳过 ASR→LLM→TTS**；底层用 **Mimi** 流式神经音频编解码器；多流（multi-stream）范式同时处理"自己说"和"对方说"
- **能力范围**
  - 全双工：可被打断、可同时听与说、能感知情绪与非语言信息
  - 三套推理栈：**PyTorch / MLX（Apple Silicon）/ Rust + Candle（生产服务，NVIDIA GPU）**
  - 微调走独立仓库 `kyutai-labs/moshi-finetune`
- **许可**：代码 Apache-2.0 + MIT 双许可；**模型权重 CC-BY 4.0**
- **衍生**：Hibiki-Zero（同传）、Unmute（给文本 LLM 加语音）、Muscriptor
- **坑**：输出是**音频 + 并行文本流**，不是纯文本模型，接入方式要重写；英文为主，中文能力弱
- **适合**：研究级全双工 loop、低延迟语音陪伴、需要"打断"体验的产品原型

### Qwen-Omni 系列 — 中文生态里最实用的端到端

- **地址**：[QwenLM/Qwen2.5-Omni](https://github.com/QwenLM/Qwen2.5-Omni)
- **定位**：Thinker-Talker 双塔架构，输入语音/图像/文本，输出**语音 + 文本**双流
- **能力范围**：多语种语音对话、语音理解（情绪/事件）、与 Qwen 生态（ASR/TTS）打通
- **优势**：中文表现明显好于 Moshi 系；Apache-2.0 商用友好；社区部署方案多
- **坑**：不是严格意义的"全双工"（更接近流式轮次对话），打断体验要自己补

### GLM-4-Voice（智谱）

- **地址**：[THUDM/GLM-4-Voice](https://github.com/THUDM/GLM-4-Voice)
- **定位**：端到端中文语音对话模型，语音 tokenizer + LLM + 声码器一体
- **能力范围**：中/英；**语速、情绪、方言**可用自然语言指令调节；支持低延迟流式
- **适合**：中文语音助手、需要"情绪可控"的对话场景
- **坑**：生态与工具链不如 Qwen 系成熟，部署文档以研究为主

### Step-Audio 2（阶跃星辰）

- **地址**：[stepfun-ai/Step-Audio2](https://github.com/stepfun-ai/Step-Audio2)
- **定位**：面向"真实业务"的端到端语音大模型，强调**副语言理解**（笑、叹气、犹豫）与**工具调用**
- **能力范围**：中/英；语音问答、语音检索、工具调用；可做 RAG 语音助手
- **注意**：模型体积大，推理成本高；对标场景是企业级语音 Agent 而不是消费级 App

---

## 级联 vs 端到端：怎么选

| 维度 | 级联（ASR→LLM→TTS） | 端到端（S2S） |
|---|---|---|
| 首响延迟 | 600–800ms 起 | 200ms 级 |
| 打断/重叠 | 需自己做 VAD + barge-in，容易误判 | 原生支持 |
| 副语言（情绪/语气） | 丢失（文本瓶颈） | 保留 |
| 可控性/可观测 | 每段可替换、可日志、可回放 | 黑盒，调试困难 |
| 工具调用/知识注入 | 成熟（就是 LLM） | 弱，需额外适配 |
| 成本 | 三段分别计费，但可选便宜模型 | 单模型大算力 |
| 生态 | 极丰富（LiveKit/Pipecat 等） | 稀少 |

**实践结论**：做**业务型语音 Agent**（客服、预约、工单）→ 级联，可控性和工具调用是命脉。
做**体验型语音产品**（陪伴、口语练习、实时翻译）→ 端到端，延迟和自然度是命脉。
两者可以混：端到端做"门面"（接话、打断、情绪），关键业务动作交回级联链路执行。

## 坑

- **"全双工"是个被滥用的词**。判断标准：能否在模型说话时持续接收输入并即时反应，而不是"支持流式输入"。
- 端到端模型的**中文能力普遍弱于英文**，选型必须用中文样本实测。
- 端到端模型通常**无法直接复用你的 prompt 工程与 RAG**，接入成本被严重低估。
