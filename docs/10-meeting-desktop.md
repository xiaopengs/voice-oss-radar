# 10 · 会议转写桌面应用（本地化 / 隐私优先）

> 这一类的共同诉求：**音频不出本机**、能采**系统音频 + 麦克风**双轨、能出**结构化纪要**。
> 技术上分成两个流派：**Tauri + Rust 系**（体积小、原生性能）与 **Electron / Qt 系**（UI 开发快、包体大）。
> 转写内核的选择才是决定中文效果的关键——**Whisper 系在中文会议上是明显短板，FunASR 系才有保障**。

> 本页为仓库初始条目（v0.1，2026-10 梳理），星数与版本迭代快，引用前请复核仓库最新状态。

## 主表

| 项目 | 地址 | 桌面栈 | 转写内核 | 跨平台 | 中文 |
|---|---|---|---|---|---|
| Meetily | [zackriya-solutions/meetily](https://github.com/zackriya-solutions/meetily) | Tauri 2 + Rust + Next.js | whisper.cpp / Parakeet | Win / macOS | ⚠️ 弱 |
| Liberty | [whalesky-labs/Liberty](https://github.com/whalesky-labs/Liberty) | Tauri 2 + React + Python | **FunASR** | Windows 为主 | ✅ 强 |
| 言迹 Talktrace | [luguochang/meeting-copilot](https://github.com/luguochang/meeting-copilot) | Tauri 2 + Rust + FastAPI | **FunASR**（在线/离线分层） | Windows | ✅ 强 |
| Conversationaly | [bykof/conversationaly](https://github.com/bykof/conversationaly) | Tauri / Rust | transcribe.cpp（85 模型） | Win / macOS / Linux | 取决于模型 |
| Auricle | [ManeeshJupalle/Auricle](https://github.com/ManeeshJupalle/Auricle) | **纯 Rust 单二进制** | 可插拔，默认本地 Whisper | Windows | 取决于后端 |
| meeting-summarizer | [john7ross/meeting-summarizer](https://github.com/john7ross/meeting-summarizer) | PySide6（Qt） | 7 引擎可选 | Windows 为主 | 取决于引擎 |
| Whisper Meeting Assistant | [bishoku/whisper-meeting-assistant](https://github.com/bishoku/whisper-meeting-assistant) | Tauri v2 | whisper.cpp + pyannote | macOS 专用 | ⚠️ |
| meeting_transcript | [yoshi-bbb/meeting_transcript](https://github.com/yoshi-bbb/meeting_transcript) | 极简本地 | faster-whisper（CPU int8） | Win / Linux / macOS | ⚠️ |
| Handy | [cjpais/handy](https://github.com/cjpais/handy) | Tauri + Rust | Whisper / Parakeet | 跨平台 | ⚠️ |

---

## 能力对照

| 能力 | Meetily | Liberty | Talktrace | Conversationaly | Auricle | meeting-summarizer |
|---|---|---|---|---|---|---|
| 中文优化 | ⚠️ 实测约 18.7% | ✅ FunASR | ✅ FunASR 优先 | 取决于模型 | 取决于后端 | 取决于引擎 |
| 实时流式 | ✅ 2–4s 延迟 | 偏文件/队列 | ✅ partial + final 双阶段 | ✅ 流式模型 | ✅ | ✅ 实时/录音后 |
| 说话人分离 | ✅ 基础（Pro 完整） | ✅ 失败不编造 | 未强调 | 未强调 | 双人 | ✅ sherpa-onnx / pyannote |
| 系统音频采集 | ✅ | 文件导入为主 | ✅ WASAPI 双轨 | ✅ | ✅ loopback | ✅ WASAPI loopback |
| 结构化纪要 | ✅ 摘要 | ✅ DOCX 纪要 | ✅ 证据/复盘工作流 | ✅ Markdown | ✅ Markdown | ✅ 最丰富 |
| 本地 LLM 摘要 | ✅ Ollama/BYO | ✅ OpenAI 兼容 | ✅ 可选 | ✅ 捆绑 Gemma 4 | ✅ 可选 | ✅ 9 provider + MCP |
| 跨平台 | Win/macOS | Windows 为主 | Windows | **三平台** | Windows | Windows 为主 |
| 社区体量 | **最大（约 19K stars，305K+ 下载）** | 中等 | 小众 | 中等（Meetily fork） | 小众但架构独特 | 小众但功能密度高 |

---

## 逐个项目

### Meetily — 赛道体量最大

- **栈**：Tauri 2（Rust 后端）+ Next.js/React；约 8.6 万行代码，Rust 占约 40%
- **转写**：whisper.cpp 为主，Parakeet-tdt-0.6b-v3（ONNX）作默认模型；摘要走 Ollama 或 BYO LLM（Claude/Groq/OpenAI 同接口）
- **加速**：Apple Metal / NVIDIA CUDA / AMD-Intel Vulkan 全覆盖
- **真实短板**：**中文实测准确率约 18.7%**，专业术语常错；背景噪声下说话人识别从约 80% 掉到 30%；完整说话人分离在 Pro 付费档
- **结论**：英语场景 + Windows 企业桌面 + 要生态成熟度，选它；中文会议谨慎

### Liberty — 中文会议的产品化标杆

- **栈**：Tauri 2 壳 + React/TS 前端 + **托管 Python 3.10.17 运行时跑 FunASR runner**（"Tauri 壳 + Python 内核"混合架构）
- **转写**：FunASR，中/中英混合/方言；中文普通话字准确率实测 95%+；标点与数字规范化好（"三点二十"→"3:20"）
- **设计亮点**：**区分"ASR 成功但 diarization 失败"**，不强行编造说话人标签，只把验证过的结果投影到说话人视图——这是本仓库最欣赏的一个产品决策
- **导出**：TXT / Markdown / bundled Markdown / DOCX 会议纪要
- **代价**：Windows 为主；混合运行时的安装与依赖较重；界面有游戏化元素（等级/钱包），风格见仁见智

### 言迹 Talktrace — 分层转写架构

- **栈**：Tauri 2 + Rust（音频/进程生命周期）+ React/TS + FastAPI（本地编排）+ SQLite
- **转写分层**：
  - 在线阶段：FunASR Paraformer + ONNX Runtime → 低延迟 partial，供实时预览
  - 离线阶段：SeACo Paraformer + FSMN VAD + CT-Transformer 标点 → 权威 final
  - LLM 只做文本校正，**不承担转写**
- **采集**：WASAPI 麦克风 + 系统音频，16kHz 单声道 PCM
- **价值**：明确承认"一个模型扛不了两个目标"，把实时性和准确率拆开——这是工程上正确的取舍
- **风险**：公开评测与社区体量少，选型前必须用真实中文会议样本验证终稿质量

### Conversationaly — 跨平台 + 模型最宽

- **定位**：**Meetily 的 fork**，转写底座从 whisper.cpp 换成 **transcribe.cpp**，内置 Gemma 4 本地 LLM 做摘要（无需另装 Ollama）
- **模型库**：85 个模型 / 16 个家族——Whisper、Parakeet、Nemotron、Canary、Voxtral、Qwen3-ASR、SenseVoice、Moonshine、GigaAM 等
- **默认模型**：parakeet-tdt-0.6b-v3-q8，官方标称 1.94% WER，覆盖 25 个欧洲语言 locale
- **流式**：nemotron-3.5-asr-streaming-0.6b-q8 可做逐词实时
- **加速**：Metal / CUDA / Vulkan / ROCm
- **优势**：macOS/Windows/Linux 三平台预构建包，**不想被单一模型锁定的最佳选择**

### Auricle — 单二进制 + API-first

- **形态**：**约 39MB 单一 Rust 二进制**，不依赖 Tauri/Electron/Node；采集、STT 调度、REST/WS/SSE API、内嵌 dashboard、always-on-top overlay 全在一个进程
- **特色 copilot 模式**：`Ctrl+Shift+A` 截当前窗口做本地 OCR + 取最近 10 分钟转录，流式输出答案到覆盖层
- **MCP**：暴露 MCP server，Claude Code 类 agent 可直接读当前会议内容
- **注意**：安装包未签名，首装触发 SmartScreen；多人会议说话人分离未在 README 强调

### meeting-summarizer — 功能密度最高

- **栈**：PySide6（Qt），原 Electron UI 重写为 Qt，Python 后端以 CLI 子进程复用
- **7 个引擎**：Whisper / Faster-Whisper / WhisperX（带分离）/ Vosk / sherpa-onnx / whisper.cpp / FunASR
- **说话人分离**：默认 **sherpa-onnx（开箱即用，无 token 门槛）**，可选 pyannote（需 HF token）
- **导出**：txt / md / json / html / pdf / docx，支持 Obsidian vault、按说话人拆分文件、Google Sheets webhook
- **MCP**：内置 MCP server，可让 agent 检索会议档案
- **代价**：跨平台与 UI 现代感不如 Tauri 系；包体与资源占用更高

### 三个轻量选项

| 项目 | 特征 |
|---|---|
| Whisper Meeting Assistant | macOS 专用；ScreenCaptureKit 直采系统音频；pyannote + Silero VAD；Metal 加速；说话人持久化 voice profile |
| meeting_transcript | 极简录音 + CPU int8 faster-whisper（**无需 GPU**）；Windows/Linux loopback，macOS 需 BlackHole |
| Handy | 快捷键触发 + VAD + 剪贴板粘贴；MIT；跨平台 |

---

## 易混淆：VoiceStudio 不是会议转写工具

很多人把 **VoiceStudio** 当成会议转写项目，其实它是**语音创作工作台**（本地 ElevenLabs 替代品）。

### debpalash/VoiceStudio

- **地址**：[debpalash/VoiceStudio](https://github.com/debpalash/VoiceStudio)｜中文镜像 [bayshier/voicestudio-zh](https://github.com/bayshier/voicestudio-zh)
- **定位**：开源、完全本地的语音克隆 / 声音设计 / 视频配音 / 有声书制作，**AGPL-3.0**，约 1.2 万+ stars
- **规模**：运行 **16 个本地 TTS 引擎**，覆盖 646 种语言
- **栈**：Electron + Python 后端，本机端口 3900，带 OpenAI 兼容 API 与 MCP
- **听写能力**：系统级实时听写，全局快捷键任意应用触发，转文字自动粘贴；可选本地 LLM 润色标点、可选回声消除
- **为什么不适合会议**：**没有会议级说话人分离、没有系统音频采集、没有会议工作流与结构化纪要导出**
- **已知限制**：Intel Mac 不支持本地后端（issue #889）
- **适合**：语音克隆 + 配音 + 顺带个人口述，**不建议作为会议转写主工具**

### mjlzz/voice-studio

- **地址**：[mjlzz/voice-studio](https://github.com/mjlzz/voice-studio)
- **定位**：轻量 ASR & TTS 工具箱（名字相近，容易与上面混淆）
- **栈**：Python FastAPI + Web UI；STT 用 faster-whisper，TTS 支持 edge-tts / Piper / ONNX 中英混合；支持 CPU、离线
- **形态**：**桌面悬浮话筒** + 系统托盘 + Web UI + CLI
- **能力**：中/英/日三语，实时流式与录音后转写，词级时间戳，导出 TXT/SRT/JSON
- **缺什么**：会议级说话人分离、系统音频采集工作流

---

## 按场景选型

| 场景 | 首选 | 理由 |
|---|---|---|
| 中文会议 + Windows + 本地 | **Liberty** 或 **Talktrace** | 都基于 FunASR，中文基础好；Liberty 更产品化，Talktrace 分层架构更精细 |
| 英语/多语言 + 最大生态 | **Meetily** | 体量最大、Windows 覆盖最好；但中文是硬短板 |
| 跨平台 + 不想被模型锁定 | **Conversationaly** | 三平台安装包 + 85 模型 + 默认 Parakeet |
| 开发者 / API-first / 轻量 | **Auricle** | 39MB 单二进制，REST/WS/SSE + MCP |
| 多引擎对比 + 极致导出 | **meeting-summarizer** | 功能密度最高，Obsidian/Sheets/MCP 全有 |
| 只要个人听写 | mjlzz/voice-studio | 悬浮话筒，够用且轻 |

## 自建会议转写的关键决策（比选现成项目更重要）

1. **采集方式**：能采**系统 loopback** 就别用麦克风录外放（避免回声 + 音质更好）。Windows WASAPI loopback / macOS ScreenCaptureKit / Linux PulseAudio monitor
2. **中文内核**：FunASR（SenseVoice / Paraformer）是当前中文会议的最优解；Whisper 系不要用于中文正式会议
3. **双阶段转写**：实时用流式小模型出 partial，结束后用大模型 + VAD + 标点重跑出 final（Talktrace 的思路）
4. **diarization 要能降级**：分离失败时输出"未识别说话人"，不要编造标签
5. **本地 LLM 摘要**：Ollama + 7B 级模型足够做会议纪要，不必上云
6. **导出格式是产品力**：Markdown / DOCX / SRT / JSON 至少给三种，接 Obsidian 是加分项
