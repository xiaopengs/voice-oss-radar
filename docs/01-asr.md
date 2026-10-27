# 01 · ASR 语音识别

> 这一层最容易被"榜单 WER"误导。真实会议/通话场景的差距来自：混响、远场、重叠语音、专业术语、方言口音、以及**流式延迟与终稿精度的取舍**。

## 主表

| 项目 | 地址 | 许可 | 语言覆盖 | 部署形态 | 核实 |
|---|---|---|---|---|---|
| FunASR | [modelscope/FunASR](https://github.com/modelscope/FunASR) | MIT | 中/粤/英/日/韩 + 方言 | 服务端 + 端侧（ONNX/GGUF） | 2026-10 |
| SenseVoice | [FunAudioLLM/SenseVoice](https://github.com/FunAudioLLM/SenseVoice) | MIT（代码） | 中/粤/英/日/韩 | 端侧/服务端，ONNX | 2026-10 |
| Fun-ASR-Nano | [FunAudioLLM/Fun-ASR-Nano-2512](https://huggingface.co/FunAudioLLM/Fun-ASR-Nano-2512) | 见模型页 | 中/粤/英/日/韩 | 服务端，vLLM / llama.cpp | 2026-10 |
| Qwen3-ASR | [QwenLM/Qwen3-ASR](https://github.com/QwenLM/Qwen3-ASR) | Apache-2.0 | 52 语言 + 语种识别 | Transformers / vLLM | 2026-10 |
| GLM-ASR | [zai-org/GLM-ASR](https://github.com/zai-org/GLM-ASR) | Apache-2.0 | 中/英/粤 + 方言 | 1.5B，GPU | 2026-10 |
| CocktailASR-1 | [Xiaomi-CocktailASR-1](https://github.com/Xiaomi-CocktailASR-1) | Apache-2.0 | 跟随基座（中英） | GPU，端到端 LLM | 2026-10 |
| Whisper | [openai/whisper](https://github.com/openai/whisper) | MIT | 99 语言 | 服务端，PyTorch | 2026-10 |
| faster-whisper | [SYSTRAN/faster-whisper](https://github.com/SYSTRAN/faster-whisper) | MIT | 同 Whisper | CTranslate2，CPU/GPU | 2026-10 |
| WhisperX | [m-bain/whisperX](https://github.com/m-bain/whisperX) | BSD-2 | 同 Whisper | 批处理 + 对齐 | 2026-10 |
| whisper.cpp | [ggml-org/whisper.cpp](https://github.com/ggml-org/whisper.cpp) | MIT | 同 Whisper | C/C++，全平台端侧 | 2026-10 |
| Parakeet | [NVIDIA/NeMo](https://github.com/NVIDIA/NeMo) | CC-BY-4.0（权重） | 25 欧洲语言 | GPU / ONNX | 2026-10 |
| Moonshine | [usefulsensors/moonshine](https://github.com/usefulsensors/moonshine) | MIT | 以英为主 | 端侧，ONNX | 2026-10 |
| Vosk | [alphacep/vosk-api](https://github.com/alphacep/vosk-api) | Apache-2.0 | 20+ 语言 | 端侧，多语言绑定 | 2026-10 |
| WeNet | [wenet-e2e/wenet](https://github.com/wenet-e2e/wenet) | Apache-2.0 | 中/英 | 生产级流式服务 | 2026-10 |
| Voxtral | [mistralai/Voxtral](https://huggingface.co/mistralai) | Apache-2.0 | 多语种 + 音频理解 | GPU，语音 LLM | 2026-10 |

---

## 重点条目

### FunASR — 中文场景的事实标准

- **地址**：[modelscope/FunASR](https://github.com/modelscope/FunASR)
- **定位**：阿里达摩院开源的工业级语音识别**工具包**（不是一个模型，而是一整套链路）
- **能力范围**
  - 模型族：Paraformer（非自回归，快）、SenseVoice（多语种+情感+事件）、Fun-ASR（LLM 架构）、CAM++（声纹）、FSMN-VAD、CT-Transformer（标点）
  - 一条链路全覆盖：VAD 切分 → ASR → 标点 → 时间戳 → 说话人分离
  - 部署：Python 服务、ONNX、GGUF（llama.cpp）、Docker；社区已做 vLLM 原生服务
  - 训练/微调：支持自定义数据微调，中文社区语料最全
- **技术栈**：PyTorch，v1.4.0（2026-07-31）起提供完整 PyPI wheel + 签名 Release
- **许可**：MIT（代码）；各模型权重在 ModelScope/魔搭单独标注
- **坑**
  - 包体积和依赖比 whisper.cpp 重得多，端侧要裁剪
  - "中文准确率 95%+" 是普通话近场朗读场景，会议远场会明显下降
- **适合**：中文会议、方言、需要说话人+标点+时间戳一体化的本地部署

### SenseVoice — 轻量多语种 + 情感/事件标签

- **地址**：[FunAudioLLM/SenseVoice](https://github.com/FunAudioLLM/SenseVoice)
- **定位**：非自回归多语种 ASR，附带**情感识别**与**音频事件检测**（笑声、掌声、BGM 等）
- **能力范围**：中/粤/英/日/韩自动语种检测；Small 版量化后 **136MB（Q4）**，端侧友好；推理速度远快于同规模自回归模型
- **不适合**：需要极高精度终稿的长会议；复杂重叠语音
- **适合**：端侧语音输入、实时字幕、需要"情绪/事件"信号的场景

### Qwen3-ASR — 多语种 + 强制对齐

- **地址**：[QwenLM/Qwen3-ASR](https://github.com/QwenLM/Qwen3-ASR)
- **定位**：Qwen 团队的开放权重 ASR 系列，**52 语言 + 语种识别 + 时间戳预测**，另有 11 语言的强制对齐模型
- **能力范围**：语音/音乐/歌声识别、流式推理、vLLM 后端、微调工具、长音频批量转写（Qwen3-ASR-Toolkit）
- **注意**：维护节奏偏"稳定但慢"（近一年无正式 release），生产接入前建议锁版本
- **适合**：多语种、需要时间戳/对齐、有 GPU 的服务端

### GLM-ASR（智谱）

- **地址**：[zai-org/GLM-ASR](https://github.com/zai-org/GLM-ASR)
- **定位**：1.5B 开源 ASR，主打**噪声/口音/方言鲁棒性**，官方称多项基准超 Whisper large-v3
- **能力范围**：中/英/粤 + 中文方言；Apache-2.0 可商用；社区已出 CTC 头（40M）与 GGUF/ONNX int4 导出，端侧可行
- **适合**：中文方言、嘈杂环境；想避开 Whisper 中文短板又不想上大模型

### CocktailASR-1（小米）— 目标说话人 ASR

- **地址**：GitHub `Xiaomi-CocktailASR-1`（Apache-2.0）
- **定位**：**改变任务输入**——先给一段参考音频，模型只转录这个人的话，其他人说话一律不输出
- **能力范围 / 关键数据**
  - 架构：D2V2 音频编码器 → Adapter → LLM 解码，单 checkpoint，16kHz 单声道
  - LibriMix 2mix WER **4.11%**、LibriSpeechMix 2mix **2.90%**、LibriMix 3mix **12.29%**
  - 对照组在 3mix 混说场景：Qwen3-ASR 106.04%、Gemini 76.10%、StepAudio 121.08% —— 不是"差一点"，是**做不了这件事**
  - 真实会议：AMI SDM 21.81%、AliMeeting Far 20.63%
  - **负样本拒识**：参考人不在场时输出空文本（LibriSpeech 79.59%），防止智能设备误触发
  - 支持 CoT 推理过程输出（可解释性/调试用）
- **依赖**：torch、torchaudio、transformers、soundfile，从 HuggingFace 加载
- **适合**：多人会议里"只跟某个人"的场景、智能音箱/车机的误触发抑制
- **注意**：拒识会带来虚假拒识（FRR 约 0.01%–0.38%），需要按业务调阈值

### Whisper 系 — 生态最大，但别当万能药

| 变体 | 差异 | 什么时候用 |
|---|---|---|
| openai/whisper | 官方参考实现，PyTorch | 做 baseline、研究 |
| faster-whisper | CTranslate2 重写，同精度下快 4 倍左右，int8 可 CPU 跑 | 服务端首选 |
| WhisperX | 加 VAD + wav2vec2 词级对齐 + pyannote 分离 | 需要**词级时间戳**或字幕 |
| whisper.cpp | C/C++ + GGML，Metal/CUDA/Vulkan/CoreML | 端侧、嵌入式、离线 App |

**共性短板**：中文/方言明显弱于 FunASR 系；长静音容易产生**幻觉重复**；原生不支持真正的流式（只能滑窗伪流式）。

### Parakeet（NVIDIA NeMo）

- **定位**：FastConformer + TDT 架构，`parakeet-tdt-0.6b-v3` 覆盖 25 个欧洲语言 locale，官方标称 WER 约 1.94%
- **优势**：0.6B 规模下精度/速度平衡好，ONNX 可端侧
- **注意**：**中文不在覆盖范围**；CC-BY-4.0 权重需保留署名

---

## 选型检查清单

1. **先定语言**：中文优先 FunASR / GLM-ASR / Qwen3-ASR；纯英文再看 Parakeet、Whisper
2. **再定形态**：端侧（sherpa-onnx / whisper.cpp / SenseVoice-Small）还是服务端（FunASR 服务 / vLLM）
3. **再定延迟**：实时字幕要 <500ms 首字，只有流式模型能满足；批处理场景别为流式付溢价
4. **最后验精度**：用**你自己的 30 分钟真实录音**跑一遍，别信模型卡。重点看：专业术语、人名、数字、中英混说
5. **许可**：代码许可和权重许可分开看；商用务必读权重页

## 评测口径参考

- 传统：WER / CER（LibriSpeech、AISHELL、WenetSpeech、Common Voice）
- 编程/Agent 场景新口径：Terminal-Bench 这类"真实受限环境"任务评测（虽然主要面向 LLM，但语音 Agent 的评测正在向"端到端任务完成率"迁移）
- 真实会议：AMI（SDM/IHM）、AliMeeting（Near/Far）——**这两个数据集的表现比 LibriSpeech 更能预测你的实际体验**
