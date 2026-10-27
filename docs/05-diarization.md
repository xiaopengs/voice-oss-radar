# 05 · 说话人分离与声纹

> 三个容易混淆的任务，先分清：
> - **Diarization（说话人分离）**：谁在什么时候说话 → 输出 `[SPEAKER_00] 0.0–3.2s`
> - **Speaker Verification（声纹验证）**：这两段是不是同一个人
> - **Target-Speaker ASR（目标说话人识别）**：只转录指定那个人的话（见 [01 ASR · CocktailASR-1](01-asr.md)）
>
> 会议转写里最影响体验的不是 WER，而是 **diarization 错了导致"张冠李戴"**。

## 主表

| 项目 | 地址 | 许可 | 形态 | 强项 | 核实 |
|---|---|---|---|---|---|
| pyannote.audio | [pyannote/pyannote-audio](https://github.com/pyannote/pyannote-audio) | MIT（代码），权重需 HF 授权 | 服务端，PyTorch | 学术 baseline，精度标杆 | 2026-10 |
| 3D-Speaker | [modelscope/3D-Speaker](https://github.com/modelscope/3D-Speaker) | Apache-2.0 | 服务端 | **中文/方言友好**，CAM++ 声纹 | 2026-10 |
| DiariZen | [BUTSpeechFIT/DiariZen](https://github.com/BUTSpeechFIT/DiariZen) | MIT | 服务端 | 端到端分离，重叠语音处理强 | 2026-10 |
| sherpa-onnx | [k2-fsa/sherpa-onnx](https://github.com/k2-fsa/sherpa-onnx) | Apache-2.0 | **端侧**（ONNX） | 离线分离 + 声纹管理 | 2026-10 |
| NeMo（Sortformer / MSDD） | [NVIDIA/NeMo](https://github.com/NVIDIA/NeMo) | 见仓库 | 服务端 GPU | 固定人数场景精度高 | 2026-10 |
| WeSpeaker | [wenet-e2e/wespeaker](https://github.com/wenet-e2e/wespeaker) | Apache-2.0 | 服务端 | 声纹嵌入训练/评测工具链 | 2026-10 |
| MOSS-Transcribe-Diarize | [OpenMOSS-Team](https://huggingface.co/OpenMOSS-Team) | Apache-2.0 | 服务端 | **一次生成转写+时间戳+说话人** | 2026-10 |

---

## 重点条目

### pyannote.audio — 精度标杆，但要过授权关

- **地址**：[pyannote/pyannote-audio](https://github.com/pyannote/pyannote-audio)
- **定位**：说话人分离的事实标准，`speaker-diarization-3.x` pipeline 是绝大多数论文的对照基线
- **能力范围**：分离 + 说话人嵌入 + 重叠语音检测；支持指定人数（`num_speakers`）或自动估计
- **⚠️ 使用门槛**：模型权重托管在 HuggingFace，**需要接受用户协议 + 提供 HF token** 才能下载；商用条款需逐个模型确认
- **坑**：自动估人数在 3 人以上会议经常估错；长音频需要自己切片拼接；GPU 内存占用不低
- **适合**：追求精度、能接受授权流程、有 GPU 的服务端

### 3D-Speaker（阿里）— 中文场景首选

- **地址**：[modelscope/3D-Speaker](https://github.com/modelscope/3D-Speaker)
- **定位**：一站式说话人技术工具包：声纹验证、说话人识别、分离、以及 **CAM++** 系列嵌入模型
- **优势**：**中文/方言数据训练充分**，中文会议表现优于纯英文训练的 pyannote 权重；Apache-2.0
- **能力范围**：说话人验证、注册/检索、分离、端到端识别；与 FunASR 生态可直接串联
- **适合**：中文会议、需要"注册声纹 → 识别是谁"的场景

### sherpa-onnx 内置分离 — 端侧唯一实用解

- **地址**：[k2-fsa/sherpa-onnx](https://github.com/k2-fsa/sherpa-onnx)
- **能力范围**：离线说话人分离（segmentation + embedding 两段式）、`SpeakerEmbeddingManager` 做声纹注册与匹配、跨平台（Android/iOS/Windows/Linux/Web）
- **优势**：**不依赖 Python、不依赖 GPU**，可以塞进桌面 App 或手机
- **代价**：精度不如服务端大模型，适合 2–4 人、录音质量尚可的场景
- **适合**：本地会议转写 App（见 [10 会议应用](10-meeting-desktop.md)）

### MOSS-Transcribe-Diarize（OpenMOSS）

- **定位**：**一次前向同时输出长音频转写、时间戳和说话人标签**，不需要外挂 VAD/分离模块
- **许可**：Apache-2.0（第三方模型，FunASR 已支持 AutoModel 接入）
- **价值**：把"ASR + 分离"两段式流水线合并，减少级联误差；适合长会议
- **注意**：官方说明"无需外部 VAD"不代表内部没有分块——长音频仍有分段逻辑

---

## 评测口径

- **DER（Diarization Error Rate）** = 漏检（miss）+ 误检（false alarm）+ 说话人混淆（confusion），越低越好。真实会议 DER 15%–25% 很常见
- **重叠语音（overlap）** 单独看：双人会议可忽略，多人讨论必须看
- **"谁是谁"比"分了几段"更重要**：产品侧真正在意的是**跨段一致性**（同一个人不能一会儿 SPK_0 一会儿 SPK_2）

## 实践建议

1. **先做 VAD，再做分离**：VAD 不准，分离必然错
2. **人数先验**能大幅提升精度：会议系统通常知道参会人数，别用自动估计
3. **声纹注册 > 盲分离**：如果能提前采集每人 10 秒音频，用"注册 + 匹配"比盲分离准得多
4. **分离失败要能降级**：不要强行编造说话人标签，宁可输出"未识别说话人"——Liberty 这类产品化项目就明确区分了"ASR 成功但 diarization 失败"的情况
