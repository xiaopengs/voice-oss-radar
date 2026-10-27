# 02 · TTS 语音合成

> 2026 年 TTS 的竞争轴已经不在"像不像人"，而在三件事：**零样本克隆的一致性**、**自然语言可控性（声音设计）**、**单位成本与 RTF**。
> 选型时最常被忽略的是**权重许可**——代码 Apache-2.0、权重 CC-BY-NC 的组合非常常见。

## 主表

| 项目 | 地址 | 代码许可 | 权重许可 | 语言 | 关键能力 | 核实 |
|---|---|---|---|---|---|---|
| Qwen3-TTS | [QwenLM/Qwen3-TTS](https://github.com/QwenLM/Qwen3-TTS) | Apache-2.0 | Apache-2.0 | 10 语言 | 流式 / 声音设计 / 克隆 | 2026-10 |
| OmniVoice | [k2-fsa/OmniVoice](https://github.com/k2-fsa/OmniVoice) | Apache-2.0 | **CC-BY-NC** | 600+ | 零样本克隆 / 指令化声音设计 | 2026-10 |
| CosyVoice | [FunAudioLLM/CosyVoice](https://github.com/FunAudioLLM/CosyVoice) | Apache-2.0 | 见模型页 | 中/英/日/粤/韩 | 中文强 / 流式 / 指令控制 | 2026-10 |
| IndexTTS | [index-tts/index-tts](https://github.com/index-tts/index-tts) | Apache-2.0 | 见模型页 | 中/英 | 零样本 / 情感与时长控制 | 2026-10 |
| GPT-SoVITS | [RVC-Boss/GPT-SoVITS](https://github.com/RVC-Boss/GPT-SoVITS) | MIT | MIT | 中/英/日/韩/粤 | 1 分钟数据少样本微调 | 2026-10 |
| F5-TTS | [SWivid/F5-TTS](https://github.com/SWivid/F5-TTS) | MIT | CC-BY-NC（基座数据） | 中/英 | 长文本、低幻觉 | 2026-10 |
| OpenVoice v2 | [myshell-ai/OpenVoice](https://github.com/myshell-ai/OpenVoice) | MIT | MIT | 多语（跨语言克隆） | 音色转换器，~100ms | 2026-10 |
| Coqui TTS / XTTS-v2 | [coqui-ai/TTS](https://github.com/coqui-ai/TTS) | MPL-2.0 | **CPML（非商用）** | 17 语言 | 生态最全的经典工具包 | 2026-10 |
| Kokoro | [hexgrad/kokoro](https://github.com/hexgrad/kokoro) | Apache-2.0 | Apache-2.0 | 多语 | 82M 超轻量，质量/体积比高 | 2026-10 |
| Piper | [rhasspy/piper](https://github.com/rhasspy/piper) | MIT | 各 voice 单独 | 30+ | 端侧/树莓派，极快 | 2026-10 |
| MeloTTS | [myshell-ai/MeloTTS](https://github.com/myshell-ai/MeloTTS) | MIT | MIT | 中/英/日/韩/西/法 | 轻量多语，常作克隆基座 | 2026-10 |
| Chatterbox | [resemble-ai/chatterbox](https://github.com/resemble-ai/chatterbox) | MIT | MIT | 多语（V3） | 0.5B，情绪夸张度可调 | 2026-10 |
| Fish-Speech | [fishaudio/fish-speech](https://github.com/fishaudio/fish-speech) | 见仓库 | 见仓库 | 多语 | 零样本克隆，社区活跃 | 2026-10 |
| Spark-TTS | [SparkAudio/Spark-TTS](https://github.com/SparkAudio/Spark-TTS) | 见仓库 | 见仓库 | 中/英 | 基于 LLM 的简洁架构 | 2026-10 |
| Pocket TTS | [kyutai-labs](https://github.com/kyutai-labs) | 见仓库 | 见仓库 | 多语 | 100M，**CPU 实时**，一行调用 | 2026-10 |
| Kyutai TTS 1.6B | [kyutai-labs](https://github.com/kyutai-labs) | 见仓库 | 见仓库 | 多语 | 低延迟流式，配套 Unmute | 2026-10 |

---

## 重点条目

### Qwen3-TTS — 目前最"全"的开放权重 TTS

- **地址**：[QwenLM/Qwen3-TTS](https://github.com/QwenLM/Qwen3-TTS)
- **定位**：阿里 Qwen 团队开放权重 TTS 系列，同时覆盖**流式合成、自由声音设计、语音克隆**
- **能力范围**
  - 10 语言；表达力与韵律控制优于多数开源模型
  - **声音设计**：用自然语言描述生成音色（性别/年龄/音高/口音），不需要参考音频
  - **克隆**：短音频零样本复刻
  - 工程：Python 包 + 本地 Web UI + vLLM 推理 + 微调工具
  - 生态位置：与 Qwen3-ASR 配对，可组成"同一家模型"的语音链路
- **规模**：约 13.5k stars（2026-09 观测），Apache-2.0 对商用最友好
- **坑**：GPU 依赖重，不适合 CPU-only 或边缘设备；语言只有 10 种，小语种不行
- **适合**：要自托管、要商用、要"设计音色 + 克隆"两条路都走的团队

### OmniVoice（k2-fsa）— 语言覆盖最广的零样本克隆

- **地址**：[k2-fsa/OmniVoice](https://github.com/k2-fsa/OmniVoice)（2026-03-31 首发）
- **定位**：扩散语言模型架构的多语种零样本 TTS，主打 **600+ 语言覆盖**与**指令化声音设计**
- **能力范围**
  - 三种模式：克隆（参考音频）/ 设计（自然语言描述）/ 自动（随机音色）
  - 细粒度控制：行内非言语符号（`[laughter]` 等）、中文带声调拼音、英文 CMU 音标纠音
  - 性能：RTF 最低 **0.025**（约 40 倍实时），批量 CLI 支持 FlashInfer
  - 工程：`pip install omnivoice`，CLI + Web UI，HuggingFace 权重
- **增长**：约 2.1k（4 月）→ 8.3k（7 月）→ 10.8k+ stars（9 月）
- **⚠️ 许可陷阱**：**代码 Apache-2.0，预训练权重 CC-BY-NC（非商用）**，因训练数据（含 Emilia）受限。要做商业产品，要么重训，要么走法务确认
- **衍生生态**：VoiceStudio 把它作为默认 TTS 引擎之一（14 个引擎里选一个），说明工程可用性已被下游验证
- **适合**：多语种研究、内部工具、非商业内容生产

### CosyVoice（阿里 FunAudioLLM）— 中文听感的第一梯队

- **地址**：[FunAudioLLM/CosyVoice](https://github.com/FunAudioLLM/CosyVoice)
- **定位**：面向中文优化的零样本 TTS，支持流式合成与**自然语言指令控制**（"用四川话说""语速快一点"）
- **能力范围**：中/英/日/粤/韩；零样本克隆；流式低延迟；情感/方言/语速指令
- **注意**：模型版本迭代快，接口在版本间有破坏性变更，锁版本
- **适合**：中文有声内容、虚拟人、需要方言的中文 TTS

### IndexTTS（B 站开源）— 中文 + 时长可控

- **地址**：[index-tts/index-tts](https://github.com/index-tts/index-tts)
- **定位**：中文零样本 TTS，第二代加入**精确时长控制**与更强情感迁移
- **能力范围**：中/英；零样本克隆；按目标时长生成（配音对齐的关键能力）；情感参考音频迁移
- **适合**：视频配音（需要严格对齐口型/字幕时间轴）、有声书

### GPT-SoVITS — 少样本微调的老牌实用派

- **地址**：[RVC-Boss/GPT-SoVITS](https://github.com/RVC-Boss/GPT-SoVITS)
- **定位**：**用 1 分钟数据微调**出高相似度音色的 TTS，中文社区生态最成熟
- **能力范围**：中/英/日/韩/粤；零样本 + 少样本微调；WebUI 全流程（切分/标注/训练/推理）
- **注意**：微调路线意味着**每个音色都要训练**，规模化场景成本高；推理不是流式
- **适合**：固定几个音色的长期内容生产（主播、IP 角色）

### OpenVoice v2 — 只做"音色转换"的那一半

- **地址**：[myshell-ai/OpenVoice](https://github.com/myshell-ai/OpenVoice)（约 37.6k stars，MIT）
- **定位**：把 TTS 拆成两段——MeloTTS 生成中性语音，再用**音色转换器**把音色换成目标人
- **优势**：转换器仅约 300M、单次 **<100ms**，与音频长度无关；预注册音色库场景成本极低
- **限制**：依赖 MeloTTS 作为基座（`pip install MeloTTS` 必须装，否则装完没声音）；原生语言覆盖窄，跨语言能力靠参考音频
- **适合**：音色库固定、请求量大的产品（客服、播报）

### 轻量端侧三件套：Kokoro / Piper / Pocket TTS

| 项目 | 规模 | 特点 | 场景 |
|---|---|---|---|
| Kokoro | 82M | Apache-2.0，质量/体积比极高 | 本地朗读、App 内播报 |
| Piper | 依 voice | MIT，30+ 语言，树莓派可跑 | 智能家居、离线设备 |
| Pocket TTS | 100M | CPU 上快于实时，一行代码接入 | 低资源设备的语音能力 |

**共性取舍**：轻量模型能给你"清楚、稳定、便宜"，但给不了"情感丰富、长文本韵律自然"。有声书/广告配音别用它们。

---

## 选型检查清单

1. **先确认商用**：读**权重**页，不是代码页。CC-BY-NC / CPML 都不等于可商用
2. **再确认是否需要克隆**：固定音色选 GPT-SoVITS 微调；任意音色选 Qwen3-TTS / CosyVoice
3. **再确认延迟**：要流式（<300ms 首包）只有 Qwen3-TTS、CosyVoice、Kyutai TTS、Pocket TTS 这条路
4. **再确认语言**：600+ 语言只有 OmniVoice 一家，但它是非商用权重
5. **最后试听**：同一段中文长句 + 一段中英混排 + 一段数字/单位，三个样本足够判断真实水平

## 常见坑

- **"支持 N 语言"是模型卡自报**，很多语言的训练数据只有几十小时（例：OmniVoice 葡萄牙语 16.9k 小时 vs 英语 206k 小时，比例差 12 倍）
- **中文 TTS 的数字/单位/多音字**是最容易翻车的地方，测试集里必须放进去
- **声音克隆的合规风险**：几乎所有模型卡都禁止未授权克隆与 impersonation，产品侧需要留同意凭证
