# 06 · 端侧与推理运行时

> 端侧的选型标准和服务端完全不同：不看榜单，看**包体积、内存峰值、首字延迟、CPU 单核能不能跑、有没有你要的平台绑定**。
> 一个残酷现实：绝大多数"开源 SOTA 模型"在手机/桌面上跑不动，能跑的是**特定导出的量化版本**。

## 主表

| 项目 | 地址 | 许可 | 运行时 | 覆盖能力 | 核实 |
|---|---|---|---|---|---|
| sherpa-onnx | [k2-fsa/sherpa-onnx](https://github.com/k2-fsa/sherpa-onnx) | Apache-2.0 | ONNX Runtime（C++ 核心） | ASR / TTS / VAD / 说话人分离 / 声纹 / 音频事件 | 2026-10 |
| whisper.cpp | [ggml-org/whisper.cpp](https://github.com/ggml-org/whisper.cpp) | MIT | GGML（GGUF） | Whisper 全系列 ASR | 2026-10 |
| llama.cpp（音频多模态） | [ggml-org/llama.cpp](https://github.com/ggml-org/llama.cpp) | MIT | GGML | 语音 LLM（Qwen-Audio/Voxtral 类，需 mmproj） | 2026-10 |
| CTranslate2 | [OpenNMT/CTranslate2](https://github.com/OpenNMT/CTranslate2) | MIT | 自研 C++ | faster-whisper 的推理引擎 | 2026-10 |
| ONNX Runtime | [microsoft/onnxruntime](https://github.com/microsoft/onnxruntime) | MIT | ONNX | 通用推理后端（几乎所有端侧方案的地基） | 2026-10 |
| Moonshine | [usefulsensors/moonshine](https://github.com/usefulsensors/moonshine) | MIT | ONNX | 短音频端侧 ASR | 2026-10 |
| Vosk | [alphacep/vosk-api](https://github.com/alphacep/vosk-api) | Apache-2.0 | Kaldi 派生 | 轻量离线 ASR，多语言绑定 | 2026-10 |
| TEN VAD | [TEN-framework/ten-vad](https://github.com/TEN-framework/ten-vad) | Apache-2.0 | 轻量 C | 端侧 VAD | 2026-10 |

---

## 重点条目

### sherpa-onnx — 端侧语音的"全家桶"

- **地址**：[k2-fsa/sherpa-onnx](https://github.com/k2-fsa/sherpa-onnx)
- **定位**：C++ 核心 + 全平台绑定的**离线语音推理框架**，把 ASR / TTS / VAD / 说话人分离 / 声纹 / 音频事件打成一个包
- **版本节奏**：v1.13.6（2026-08-18）补 Flutter 的 VAD+ASR 示例与 Dart CLI；**v2.0.0（2026-10-23）** 修 Dart 包发布、支持离线示例里的 NeMo transducer、Kotlin API 加 `OfflineDiacritization`、流式 NeMo transducer 支持 `modified_beam_search + hotwords`、`SpeakerEmbeddingManager` 加 `GetEmbedding`
- **支持的模型族**（持续增加）：Zipformer / Paraformer / SenseVoice / Whisper / Moonshine / Qwen3-ASR（0.6B、1.7B 的 int8 导出）/ FireRedASR / NeMo transducer / Supertonic(TTS) 等
- **平台绑定**：Python、C#、Java/Kotlin、Swift、Go、Dart/Flutter、Rust、WASM、Node
- **为什么值得关注**：它把"模型下载 → 麦克风采集 → VAD 切分 → 推理 → 结果回调"的**工程路径**补齐了，尤其是移动端。Flutter 一套代码跨 Android/iOS 这件事，在语音场景里最容易卡在原生绑定上
- **适合**：本地会议 App、手机端语音输入、离线字幕、嵌入式设备

### whisper.cpp — 端侧 Whisper 的标准答案

- **地址**：[ggml-org/whisper.cpp](https://github.com/ggml-org/whisper.cpp)
- **定位**：Whisper 的 C/C++ 重实现，GGUF 量化，无 Python 依赖
- **能力范围**：全系列 Whisper 模型；Metal / CUDA / Vulkan / Core ML 加速；流式伪实时；VAD 可选
- **取舍**：中文仍弱（模型本身限制，不是实现问题）；量化到 Q5/Q8 后精度有可见下降
- **适合**：macOS/iOS 桌面 App、Windows 本地转写、离线字幕工具

### llama.cpp 的音频路径

- **定位**：通过 `mmproj` 多模态投影加载**语音 LLM**（如 Qwen-Audio、Voxtral 类），在 CPU/端侧做"语音理解 + 生成"
- **现状**：支持度随模型而异，量化后精度损失明显；适合实验，不适合直接上生产
- **价值**：FunASR v1.4.0 的 Release 里已经附带 **9 个自包含的 llama.cpp/GGUF 运行时**，说明"语音模型 + GGUF"这条路正在被主流项目正式接纳

### Moonshine / Vosk — 老派但可靠

| 项目 | 优势 | 局限 |
|---|---|---|
| Moonshine | 针对**短音频**优化，比 Whisper 快很多，ONNX 端侧友好 | 语言覆盖窄，长音频需自己切 |
| Vosk | 模型小（几十 MB）、绑定全（含 Android/iOS/Rust）、离线稳定 | 精度明显落后于新一代模型；中文模型老 |

---

## 端侧落地检查清单

1. **先算内存**：模型 + 运行时 + 音频缓冲，Android 上超过 500MB 就要谨慎
2. **再看首字延迟**：端侧实时字幕要求 <300ms，只有流式模型（Zipformer streaming / Paraformer streaming）能做到；SenseVoice 是非流式的，只能"说完再转"
3. **量化选型**：Q4 省内存、Q8 平衡、F16 精度高但体积翻倍（例：Fun-ASR Nano 的 Q4 0.90GB / Q8 1.27GB / F16 1.98GB）
4. **平台绑定是否现成**：没有你要的语言绑定，等于要自己写 JNI/FFI，工期翻倍
5. **模型许可证**：端侧分发意味着**权重会进入你的安装包**，许可约束比服务端更硬

## 一个常见误区

> "端侧 = 精度差" 这个结论在 2026 年已经不成立。
> SenseVoice-Small Q4 只有 136MB，中文近场识别足够用；Qwen3-ASR 0.6B int8 也能在 CPU 上跑。
> 真正的瓶颈不是精度，而是**流式能力**和**远场/噪声鲁棒性**。
