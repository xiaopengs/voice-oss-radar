# 04 · 语音 Agent 编排框架

> 这一层不产出"能力"，产出的是**链路工程**：音频采集 → 传输 → VAD/轮次检测 → STT → LLM → TTS → 回放，以及打断、超时、工具调用、观测。
> 判断一个框架好不好，只看四件事：**能不能接电话（SIP）**、**能不能自然打断**、**能不能替换每个组件**、**能不能自托管**。

## 主表

| 项目 | 地址 | 许可 | 语言/栈 | 传输 | 关键能力 | 核实 |
|---|---|---|---|---|---|---|
| LiveKit Agents | [livekit/agents](https://github.com/livekit/agents) | Apache-2.0 | Python / Node | WebRTC、SIP | 生产级实时基础设施，多人房间 | 2026-10 |
| Pipecat | [pipecat-ai/pipecat](https://github.com/pipecat-ai/pipecat) | BSD-2 | Python | WebRTC、WebSocket、本地音频 | 组件可插拔，pipeline 完全可控 | 2026-10 |
| Vocode | [vocodedev/vocode-core](https://github.com/vocodedev/vocode-core) | MIT | Python | 电话、Zoom、浏览器、本地 | 传统语音应用快速组装 | 2026-10 |
| Bolna | [bolna-ai/bolna](https://github.com/bolna-ai/bolna) | 见仓库 | Python | Twilio / Plivo 电话 | 配置驱动的外呼/客服 Agent | 2026-10 |
| TEN Framework | [TEN-framework/ten-framework](https://github.com/TEN-framework/ten-framework) | Apache-2.0 | C++ / Go / Python | WebRTC、RTC | 低延迟实时多模态 Agent 运行时 | 2026-10 |
| Rasa | [RasaHQ/rasa](https://github.com/RasaHQ/rasa) | Apache-2.0 | Python | 文本为主 | 状态机式对话、企业流程 | 2026-10 |

---

## 重点条目

### LiveKit Agents — 生产级首选

- **地址**：[livekit/agents](https://github.com/livekit/agents)（配套 [livekit/livekit](https://github.com/livekit/livekit) 服务端）
- **定位**：基于 LiveKit WebRTC 基础设施的语音 Agent 框架，**把实时传输这层最难的部分做完了**
- **能力范围**
  - 传输：WebRTC（浏览器/移动端）、**SIP/电话接入**、多人房间
  - 链路：STT → LLM → TTS pipeline，同时支持**实时 speech-to-speech 模型**
  - 交互：turn detection、**打断（barge-in）**、静音检测、多 Agent 交接
  - 部署：可自托管 LiveKit Server，K8s 友好，自带可观测性
  - SDK：Python、Node.js
- **适合**：浏览器语音客服、电话机器人、多用户语音房间、需要"能上生产"的项目
- **坑**：整套架构偏重，小 Demo 会觉得过度设计；LiveKit Server 的运维是额外成本

### Pipecat — 灵活性最好

- **地址**：[pipecat-ai/pipecat](https://github.com/pipecat-ai/pipecat)
- **定位**：Python 优先的实时语音/多模态 Agent 框架，**pipeline 的每一段都是可替换的 processor**
- **典型链路**
  ```
  麦克风 → 音频传输 → VAD / Turn Detection → STT → LLM/Agent → TTS → 扬声器或电话
  ```
- **能力范围**：STT/LLM/TTS 全插拔；支持 WebRTC、WebSocket、本地音频；支持 Gemini Multimodal Live、OpenAI Realtime 等实时模型；语音打断、上下文管理、多 Agent handoff
- **与 LiveKit 的关系**：可组合使用（Pipecat 做 pipeline，LiveKit 做传输）
- **适合**：想完全控制语音链路、不想被平台 Agent 生命周期绑住；快速实验多种 Provider 组合
- **坑**：生产级的传输/伸缩要自己解决；生态文档更新快于稳定性

### Vocode — 传统语音应用的快车道

- **地址**：[vocodedev/vocode-core](https://github.com/vocodedev/vocode-core)
- **定位**：把 STT/LLM/TTS 模块化拼起来的 Python 框架，主打电话与呼叫中心场景
- **能力范围**：实时语音流、电话/Zoom/本地音频、对话状态管理
- **注意**：项目热度相比 2024 年高峰期有回落，新项目接入前先看最近提交节奏
- **适合**：快速搭一个电话客服原型

### Bolna — 面向电话业务

- **地址**：[bolna-ai/bolna](https://github.com/bolna-ai/bolna)
- **定位**：端到端电话 Agent，集成 ASR/LLM/TTS/WebSocket/Telephony
- **能力范围**：Twilio/Plivo 接入；**JSON 配置驱动**的对话流程（不用写代码改流程）；外呼、预约、回访、客服
- **适合**：销售外呼、预约提醒这类"流程相对固定、量大"的电话业务

### TEN Framework

- **地址**：[TEN-framework/ten-framework](https://github.com/TEN-framework/ten-framework)
- **定位**：实时多模态 Agent 运行时，C++/Go/Python 混合，主打**低延迟与跨端**
- **适合**：对延迟极敏感、需要跑在端侧的实时语音 Agent

---

## 自己搭 vs 用框架

| 场景 | 建议 |
|---|---|
| 验证想法、3 天内要 demo | Pipecat（最少的脚手架） |
| 要接电话/SIP | LiveKit Agents 或 Bolna（别自己造 SIP） |
| 要多人语音房间 | LiveKit Agents |
| 要极致低延迟/端侧 | TEN Framework，或直接端到端模型 + 自研传输 |
| 只是批处理转写 | 不需要这层，直接用 ASR |

## 这一层的共性坑

1. **VAD 决定体验上限**。ASR 再准，VAD 切错就全是断句和误触发。Silero VAD / TEN VAD / FSMN-VAD 都要实测（见 [07 音频前端](07-audio-frontend.md)）
2. **打断逻辑是最难的部分**，不是"检测到人声就停"。要区分：附和（"嗯""对"）vs 真打断；要处理 TTS 已生成音频的丢弃与重生成
3. **回声消除（AEC）** 在"外放 + 麦克风"场景是刚需，否则 Agent 会听到自己
4. **很多框架开源、但默认接的 STT/LLM/TTS 是收费云服务**，本地化要自己换 Provider
5. **可观测性**：一定要能回放"用户音频 + 各段延迟 + 模型输入输出"，否则线上问题无法定位
