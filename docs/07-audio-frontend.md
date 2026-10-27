# 07 · 音频前端（VAD / 降噪 / 回声消除 / 音源分离）

> 语音系统里最被低估的一层。**上游音频差 3dB，下游模型再强也救不回来**。
> 顺序很重要：AEC（回声消除）→ 降噪/增强 → VAD → ASR。顺序错了，VAD 会被自己的回声和噪声持续触发。

## 主表

| 项目 | 地址 | 许可 | 作用 | 形态 | 核实 |
|---|---|---|---|---|---|
| Silero VAD | [snakers4/silero-vad](https://github.com/snakers4/silero-vad) | MIT | 语音活动检测 | ONNX / JIT，30ms 帧 | 2026-10 |
| TEN VAD | [TEN-framework/ten-vad](https://github.com/TEN-framework/ten-vad) | Apache-2.0 | 轻量 VAD | C，端侧 | 2026-10 |
| FSMN-VAD | FunASR 内置 | MIT | VAD（中文优化） | ONNX | 2026-10 |
| WebRTC VAD | [py-webrtcvad](https://github.com/wiseman/py-webrtcvad) | MIT | 极轻 VAD | C | 2026-10 |
| DeepFilterNet | [Rikorose/DeepFilterNet](https://github.com/Rikorose/DeepFilterNet) | MIT/Apache-2.0 | 实时降噪（48kHz） | Rust/Python | 2026-10 |
| RNNoise | [xiph/rnnoise](https://github.com/xiph/rnnoise) | BSD-3 | 超轻降噪 | C | 2026-10 |
| ClearerVoice-Studio | [modelscope/ClearerVoice-Studio](https://github.com/modelscope/ClearerVoice-Studio) | Apache-2.0 | 增强 / 分离 / 超分 / 去混响 | PyTorch | 2026-10 |
| Demucs | [facebookresearch/demucs](https://github.com/facebookresearch/demucs) | MIT | 音乐音源分离 | PyTorch | 2026-10 |
| MossFormer2 | 见 ClearerVoice-Studio | Apache-2.0 | 语音分离 SOTA 系 | PyTorch | 2026-10 |
| WebRTC AEC / SpeexDSP | [xiph/speexdsp](https://github.com/xiph/speexdsp) | BSD-3 | 回声消除 | C | 2026-10 |

---

## 重点条目

### Silero VAD — 默认选择

- **地址**：[snakers4/silero-vad](https://github.com/snakers4/silero-vad)
- **定位**：目前最广泛使用的开源 VAD，MIT 许可，模型极小（约 1–2MB）
- **能力范围**：16kHz 单声道，30ms 帧；ONNX 与 TorchScript 两种形态；支持 `min_silence_duration` 等参数调优
- **优势**：精度/体积比极高，几乎所有语音 Agent 框架默认接它
- **坑**：对**音乐、键盘声、呼吸声**仍会误判；中文电话窄带（8kHz）要先重采样；参数默认值面向"人声清晰"场景，会议远场需重调

### FSMN-VAD（FunASR 生态）

- **定位**：FunASR 链路里的中文优化 VAD，ONNX 可独立使用
- **优势**：与 FunASR 的 ASR 模型配合时切分策略一致，避免"VAD 切的和 ASR 期望的不一样"
- **适合**：已经用 FunASR 的中文场景，别混搭

### DeepFilterNet — 实时降噪

- **地址**：[Rikorose/DeepFilterNet](https://github.com/Rikorose/DeepFilterNet)
- **定位**：48kHz 实时语音降噪，DeepFilterNet3 可在单核 CPU 上跑实时
- **能力范围**：宽带/超宽带降噪、去混响；提供 Rust 与 Python 接口
- **适合**：通话、录音前处理；**不适合**已经很强的近场录音（过度降噪会吃掉辅音，反而降低 ASR 准确率）

### ClearerVoice-Studio — 一站式语音处理工作台

- **地址**：[modelscope/ClearerVoice-Studio](https://github.com/modelscope/ClearerVoice-Studio)
- **定位**：阿里系语音处理工具箱，覆盖**语音增强、语音分离、语音超分、目标说话人提取、去混响**
- **价值**：把散落在各篇论文里的模型做成可调用流水线；Apache-2.0
- **适合**：会议录音后处理、把"多人混说"先分离再分别转写

### Demucs — 音乐分离，不要拿来分人声

- **定位**：`htdemucs` 系列是音乐音源分离（人声/鼓/贝斯/其他）的事实标准
- **误用警告**：Demucs 分出来的是"唱歌的人声"，对**说话**场景的多人分离效果差，别拿它做会议 diarization。会议分离用 ClearerVoice / MossFormer2 / pyannote

---

## 回声消除（AEC）为什么必须单独说

在"扬声器外放 + 麦克风"的场景（会议、车载、桌面助手），如果不做 AEC：

1. Agent 的 TTS 输出会被麦克风收回 → **自我触发**（以为用户在说话）
2. VAD 持续为真 → 打断逻辑完全失效
3. ASR 转写出自己的话 → 对话循环

**方案**：WebRTC AEC3（成熟、免费、效果够用）或 SpeexDSP；浏览器端可直接用 `getUserMedia({echoCancellation: true})`。
**采集侧更优解**：直接采**系统音频 loopback**（WASAPI loopback / ScreenCaptureKit / PulseAudio monitor），从物理上避免回声——这也是多数会议转写桌面应用的做法（见 [10](10-meeting-desktop.md)）。

## 调试方法

| 问题 | 排查方向 |
|---|---|
| 识别断句奇怪 | VAD 阈值与 `min_silence_duration`；采样率是否匹配（16k vs 48k） |
| 一直不触发 | 增益太低 / 降噪过度 / 声道数不匹配（立体声喂单声道模型） |
| 频繁误触发 | 键盘声、呼吸声；换 TEN VAD 或加能量阈值 |
| 转写丢字 | 降噪过强吃掉辅音；或 VAD 把弱起音切掉 |
| 说话人分离错乱 | 上游有回声或音乐；先分离再 diarization |

**通用建议**：把每一步的中间音频都落盘（原始 / AEC 后 / 降噪后 / VAD 切片），否则线上问题只能猜。
