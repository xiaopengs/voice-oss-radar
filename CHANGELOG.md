# 变更记录

## v0.2.0 - 2026-10-27

- 新增 `docs/index.html`：单文件静态索引页，77 个项目卡片化展示，支持分类筛选、关键词搜索、许可筛选
- 新增 `build_page.py`：从 `data/projects.yaml` 自动生成索引页，改数据即改页面，避免手改 HTML
- 索引页首屏加入许可风险分布条（可商用 55 / 需逐项确认 3 / 禁止商用 2 / 待确认 17）

格式参考 [Keep a Changelog](https://keepachangelog.com/zh-CN/1.1.0/)，版本号遵循 `主.次.修订`。

## [0.1.0] - 2026-10-27

### 新增

**仓库初始化**，建立 11 个分类与结构化登记表：

- `docs/01-asr.md` — ASR：FunASR、SenseVoice、Qwen3-ASR、GLM-ASR、Whisper 系（whisper / faster-whisper / WhisperX / whisper.cpp）、Parakeet、Moonshine、Vosk、WeNet、Voxtral、CocktailASR-1、MOSS-Transcribe-Diarize
- `docs/02-tts.md` — TTS：Qwen3-TTS、OmniVoice、CosyVoice、IndexTTS、GPT-SoVITS、F5-TTS、OpenVoice v2、Coqui/XTTS、Kokoro、Piper、MeloTTS、Chatterbox、Fish-Speech、Spark-TTS、Pocket TTS
- `docs/03-speech-to-speech.md` — 全双工 / 端到端：Moshi、Hibiki、Unmute、Qwen-Omni、GLM-4-Voice、Step-Audio 2、Ultravox、MiniCPM-o
- `docs/04-voice-agent.md` — 编排：LiveKit Agents、Pipecat、Vocode、Bolna、TEN Framework、Rasa
- `docs/05-diarization.md` — 说话人：pyannote.audio、3D-Speaker、DiariZen、sherpa-onnx、NeMo、WeSpeaker、MOSS-Transcribe-Diarize
- `docs/06-on-device.md` — 端侧：sherpa-onnx（v2.0.0）、whisper.cpp、llama.cpp、CTranslate2、ONNX Runtime、Moonshine、Vosk、TEN VAD
- `docs/07-audio-frontend.md` — 音频前端：Silero VAD、TEN VAD、FSMN-VAD、WebRTC VAD、DeepFilterNet、RNNoise、ClearerVoice-Studio、Demucs、SpeexDSP
- `docs/08-voice-conversion.md` — 变声：RVC、Seed-VC、so-vits-svc、kNN-VC、Step-Audio-EditX
- `docs/09-speech-translation.md` — 翻译：SeamlessM4T / SeamlessStreaming、Hibiki、Whisper+NLLB 级联
- `docs/10-meeting-desktop.md` — 会议桌面应用：Meetily、Liberty、Talktrace、Conversationaly、Auricle、meeting-summarizer、Whisper Meeting Assistant、meeting_transcript、Handy，以及 VoiceStudio（debpalash / mjlzz）辨析
- `docs/11-datasets-eval.md` — 数据集与评测口径，含"自建 30–50 条评测集"的分层构造方法

### 说明

- `data/projects.yaml` 收录 80+ 条结构化条目，代码许可与权重许可分列
- 初始版本的会议应用部分来自 2026-10 的一份专项梳理（见 `docs/00-原始梳理-会议转写与VoiceStudio.txt`），已重组为可维护的表格与条目
- 所有条目 `verified` 为 `2026-10`，星数与版本号仅在有来源时记录

### 待办

- [ ] 补充 `docs/` 中标注 `unknown` 的许可证信息
- [ ] 增加"语音数据标注工具"分类（Label Studio、Praat、ELAN）
- [ ] 增加"语音评测/测试工具"分类（如自动 WER 计算脚本）
- [ ] 建立每周自动扫描新项目的流程
