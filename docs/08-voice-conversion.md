# 08 · 变声与语音编辑

> 和 TTS 克隆的区别：**变声（Voice Conversion, VC）保留原音频的内容、韵律、语速、口音，只换音色**。
> 所以配音演员说一句 → 换 10 个音色，效果远好于让 10 个 TTS 各念一遍。

## 主表

| 项目 | 地址 | 许可 | 数据需求 | 实时 | 核实 |
|---|---|---|---|---|---|
| RVC | [RVC-Project/Retrieval-based-Voice-Conversion-WebUI](https://github.com/RVC-Project/Retrieval-based-Voice-Conversion-WebUI) | MIT | 10 分钟微调 | 支持 | 2026-10 |
| Seed-VC | [Plachtaa/seed-vc](https://github.com/Plachtaa/seed-vc) | 见仓库 | 1–30 秒零样本 | 支持 | 2026-10 |
| so-vits-svc | [svc-develop-team/so-vits-svc](https://github.com/svc-develop-team/so-vits-svc) | AGPL-3.0 | 数十分钟微调 | 有限 | 2026-10 |
| kNN-VC | [bshall/kNN-VC](https://github.com/bshall/kNN-VC) | MIT | 参考音频即用 | 否 | 2026-10 |
| OpenVoice v2 | [myshell-ai/OpenVoice](https://github.com/myshell-ai/OpenVoice) | MIT | 参考音频即用 | 是（~100ms） | 2026-10 |
| Step-Audio-EditX | [stepfun-ai/Step-Audio-EditX](https://github.com/stepfun-ai/Step-Audio-EditX) | 见仓库 | 无需训练 | 否 | 2026-10 |

---

## 重点条目

### RVC — 微调路线的天花板

- **地址**：[RVC-Project/Retrieval-based-Voice-Conversion-WebUI](https://github.com/RVC-Project/Retrieval-based-Voice-Conversion-WebUI)
- **定位**：检索式变声（用特征检索补足音色细节），**10 分钟数据**即可训练出高相似度音色
- **能力范围**：实时变声、离线批量；WebUI 全流程；配套 `rvc-python` 供程序调用；生态里有大量第三方音色模型
- **优势**：相似度和自然度在"微调派"里最强；MIT 许可；社区工具链成熟（含 f0 提取、特征索引）
- **坑**：每个音色都要训练；训练数据质量决定一切（带混响/噪声的数据会污染音色）；对跨语言/跨语种迁移支持弱
- **适合**：固定音色的配音、直播变声、翻唱

### Seed-VC — 零样本 + 实时

- **地址**：[Plachtaa/seed-vc](https://github.com/Plachtaa/seed-vc)
- **定位**：零样本变声，**1–30 秒参考音频**即可，支持实时与歌声转换
- **能力范围**：语音/歌声转换、零样本音色克隆、实时模式（低延迟）
- **优势**：不需要训练，音色切换成本接近零；对源音频的音高/节奏保留好
- **坑**：相似度不如 RVC 微调；参考音频质量差会直接反映在输出上

### kNN-VC — 最简单的思路，最稳的 baseline

- **定位**：用 WavLM 特征 + kNN 检索做变声，**不需要训练任何生成模型**
- **价值**：作为"下限 baseline"极好——如果你的复杂方案打不过 kNN-VC，说明方案有问题
- **限制**：非实时，输出音质一般

### Step-Audio-EditX — 语音的"编辑"而不是"转换"

- **定位**：3B 模型，做**情感、风格、副语言**的再编辑（把"平静"改成"生气"，加笑声/叹气）
- **价值**：这是 2026 年新出现的一类能力——不是换音色，而是**改演绎**
- **适合**：有声内容后期、数据增广（同一句话生成多种情绪版本）

---

## 变声 vs TTS 克隆：决策表

| 需求 | 选 VC | 选 TTS 克隆 |
|---|---|---|
| 已有真人录音，只想换音色 | ✅ | |
| 要让"文本"变成语音 | | ✅ |
| 要保留原始语气、停顿、口音 | ✅ | |
| 要精确控制时长/节奏 | | ✅（IndexTTS 等） |
| 要批量、低成本、任意音色 | | ✅ |
| 配音演员已录好，要一人配多角 | ✅ | |

## 合规红线（必须看）

- RVC / so-vits-svc 的模型卡与社区规范都**明确禁止**未授权模仿真人、冒充、诈骗、政治人物
- so-vits-svc 是 **AGPL-3.0**：网络服务方式使用也会触发开源义务，商用前必须过法务
- 产品化必须留**授权凭证**（同意书/合同），并考虑**音频水印**（如 AudioSeal 类方案）
- 国内合规还要叠加《深度合成规定》的**显著标识**要求
