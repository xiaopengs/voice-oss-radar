# 语音开源雷达 · Voice OSS Radar

持续收集、持续核实的**语音方向开源项目索引**：ASR、TTS、全双工语音、语音 Agent 编排、说话人分离、端侧推理、音频前端、变声、语音翻译、会议转写应用。

不只列仓库地址，每个项目都记四件事：**它能干什么、它不能干什么、许可证能不能商用、什么时候核实的**。

> 语音赛道的模型迭代以周计，"我记得它很强"是最危险的选型依据。本仓库所有条目都带核实日期，过期即视为待复核。

---

## 为什么做这个

语音项目选型有三类高频踩坑：

1. **许可陷阱**：代码 Apache-2.0，权重 CC-BY-NC。商用直接踩雷（OmniVoice、F5-TTS、Seamless 都是）
2. **榜单幻觉**：LibriSpeech / AISHELL 上很强的模型，到了真实会议（远场、重叠、术语）掉 20 个点
3. **能力错配**：拿音乐分离模型做会议人声分离、拿 VoiceStudio 当会议转写工具、拿非流式模型做实时字幕

这个仓库的存在意义就是把这些坑提前标出来。

---

## 分类导航

| # | 分类 | 内容 | 入口 |
|---|---|---|---|
| 01 | **ASR 语音识别** | FunASR、SenseVoice、Qwen3-ASR、Whisper 系、Parakeet、目标说话人识别 | [docs/01-asr.md](docs/01-asr.md) |
| 02 | **TTS 语音合成** | Qwen3-TTS、OmniVoice、CosyVoice、IndexTTS、GPT-SoVITS、轻量端侧三件套 | [docs/02-tts.md](docs/02-tts.md) |
| 03 | **全双工 / 端到端语音 LLM** | Moshi、Qwen-Omni、GLM-4-Voice、Step-Audio 2 | [docs/03-speech-to-speech.md](docs/03-speech-to-speech.md) |
| 04 | **语音 Agent 编排** | LiveKit Agents、Pipecat、Vocode、Bolna、TEN | [docs/04-voice-agent.md](docs/04-voice-agent.md) |
| 05 | **说话人分离与声纹** | pyannote、3D-Speaker、DiariZen、sherpa-onnx | [docs/05-diarization.md](docs/05-diarization.md) |
| 06 | **端侧与推理运行时** | sherpa-onnx、whisper.cpp、CTranslate2、llama.cpp | [docs/06-on-device.md](docs/06-on-device.md) |
| 07 | **音频前端** | Silero VAD、DeepFilterNet、ClearerVoice、AEC | [docs/07-audio-frontend.md](docs/07-audio-frontend.md) |
| 08 | **变声与语音编辑** | RVC、Seed-VC、so-vits-svc、Step-Audio-EditX | [docs/08-voice-conversion.md](docs/08-voice-conversion.md) |
| 09 | **语音翻译 / 同传** | SeamlessM4T、Hibiki、级联方案 | [docs/09-speech-translation.md](docs/09-speech-translation.md) |
| 10 | **会议转写桌面应用** | Meetily、Liberty、Talktrace、Conversationaly、Auricle、VoiceStudio | [docs/10-meeting-desktop.md](docs/10-meeting-desktop.md) |
| 11 | **数据集与评测** | 数据集清单、指标口径、自建评测集方法 | [docs/11-datasets-eval.md](docs/11-datasets-eval.md) |

结构化登记表（机器可读）：[`data/projects.yaml`](data/projects.yaml)

---

## 按需求速查

| 我要做什么 | 先看这些 |
|---|---|
| **中文会议转写，本地部署** | [Liberty](https://github.com/whalesky-labs/Liberty)、[Talktrace](https://github.com/luguochang/meeting-copilot)（FunASR 内核）＋ [sherpa-onnx](https://github.com/k2-fsa/sherpa-onnx) 做分离 |
| **中文 ASR 服务端** | [FunASR](https://github.com/modelscope/FunASR)、[SenseVoice](https://github.com/FunAudioLLM/SenseVoice)、[Qwen3-ASR](https://github.com/QwenLM/Qwen3-ASR) |
| **手机/桌面端离线 ASR** | [sherpa-onnx](https://github.com/k2-fsa/sherpa-onnx)、[whisper.cpp](https://github.com/ggml-org/whisper.cpp) |
| **TTS 要能商用** | [Qwen3-TTS](https://github.com/QwenLM/Qwen3-TTS)（Apache-2.0 权重）、[CosyVoice](https://github.com/FunAudioLLM/CosyVoice) |
| **TTS 要多语种克隆（非商用可）** | [OmniVoice](https://github.com/k2-fsa/OmniVoice)（600+ 语言，权重 CC-BY-NC） |
| **中文配音要卡时长** | [IndexTTS](https://github.com/index-tts/index-tts) |
| **固定几个音色、长期量产** | [GPT-SoVITS](https://github.com/RVC-Boss/GPT-SoVITS)（1 分钟数据微调） |
| **搭电话/浏览器语音 Agent** | [LiveKit Agents](https://github.com/livekit/agents)（要 SIP）、[Pipecat](https://github.com/pipecat-ai/pipecat)（要灵活） |
| **低延迟"能打断"的语音对话** | [Moshi](https://github.com/kyutai-labs/moshi)、[Qwen-Omni](https://github.com/QwenLM/Qwen2.5-Omni)、[GLM-4-Voice](https://github.com/THUDM/GLM-4-Voice) |
| **说话人分离（中文）** | [3D-Speaker](https://github.com/modelscope/3D-Speaker)；精度优先且能过授权就 [pyannote](https://github.com/pyannote/pyannote-audio) |
| **VAD** | [Silero VAD](https://github.com/snakers4/silero-vad)（默认）、[TEN VAD](https://github.com/TEN-framework/ten-vad)（端侧） |
| **变声/换音色** | [RVC](https://github.com/RVC-Project/Retrieval-based-Voice-Conversion-WebUI)（微调最强）、[Seed-VC](https://github.com/Plachtaa/seed-vc)（零样本） |
| **实时同传** | [Hibiki](https://github.com/kyutai-labs/hibiki)（体验）；商用走级联 |

---

## 三条贯穿全仓库的结论

**1. 中文语音的默认答案在 FunASR 系，不在 Whisper 系。**
Whisper 的中文弱不是实现问题，是训练数据问题。会议场景里 Meetily 的中文实测约 18.7%，而 FunASR 系普通话字准确率 95%+——差了一个量级。

**2. 许可证要看权重，不是看代码。**
`license: Apache-2.0` + `weights_license: CC-BY-NC` 是本领域最常见的组合。端侧分发时权重会进安装包，约束比服务端更硬。

**3. 上游音频决定上限。**
AEC → 降噪 → VAD → ASR 的顺序错了，后面全是徒劳。VAD 切错，ASR 再准也只是把错误切分转录得更清楚。

---

## 维护规则

- **更新节奏**：每周扫一次新项目与重大版本；每月复核全部条目的活跃度与许可证变更
- **核实口径**：`verified` 字段 = 最后人工核实日期；星数、版本只写有来源的，没核实就写 `unknown`
- **准入标准**：① 有公开可访问的仓库或权重 ② 能说清它解决什么问题 ③ 至少有一个真实用户/下游项目在用，或作者持续维护
- **不收录**：纯云端 API（无开源权重）、已归档/停更超过 18 个月、只发论文不给代码

## 贡献

见 [CONTRIBUTING.md](CONTRIBUTING.md)。提 PR 请务必带上**许可证**与**核实日期**，缺这两项的 PR 会被打回。

## 变更记录

见 [CHANGELOG.md](CHANGELOG.md)。

## 声明

本仓库为信息索引，不构成对任何项目的推荐或担保。所有项目的许可证与商用条款请以各自仓库的最新 LICENSE 与模型卡为准。条目中的性能数据来自项目方自报或第三方实测，使用前请用自己的评测集验证。
