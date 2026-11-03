# 02 · TTS 语音合成

> 2026 年 TTS 的竞争轴已经不在"像不像人"，而在三件事：**零样本克隆的一致性**、**自然语言可控性（声音设计）**、**单位成本与 RTF**。
> 选型时最常被忽略的是**权重许可**——代码 Apache-2.0、权重 CC-BY-NC 的组合非常常见。

## 主表

| 项目 | 地址 | 代码许可 | 权重许可 | 语言 | 关键能力 | 核实 |
|---|---|---|---|---|---|---|
| Qwen3-TTS | [QwenLM/Qwen3-TTS](https://github.com/QwenLM/Qwen3-TTS) | Apache-2.0 | Apache-2.0 | 10 语言 | 流式 / 声音设计 / 克隆 | 2026-10 |
| OmniVoice | [k2-fsa/OmniVoice](https://github.com/k2-fsa/OmniVoice) | Apache-2.0 | **CC-BY-NC** | 600+ | 零样本克隆 / 指令化声音设计 | 2026-10 |
| Open-OmniVoice-TTS | [hypersniper05/Open-OmniVoice-TTS](https://github.com/hypersniper05/Open-OmniVoice-TTS) | 待核实 | **CC-BY-NC**（继承 OmniVoice） | 646 | OpenAI 兼容 `/v1/audio/speech` 自托管服务，Docker 一条命令 | 2026-11 |
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
| Fish-Speech / Drama 3 | [fishaudio/fish-speech](https://github.com/fishaudio/fish-speech) | 见仓库 | **Community License v1.0** | 83 语种 | 零样本克隆；Drama 3 为 35B MoE，16 角色群戏 | 2026-11 |
| Ming-3.0-tts | [inclusionAI/Ming-3.0-tts](https://github.com/inclusionAI/Ming-3.0-tts) | MIT | MIT | 中/英 | 0.5B，导演模式（情绪/重读/停顿） | 2026-11 |
| Audio8-TTS-Realistic | [Audio8-AI/Audio8_TTS](https://github.com/Audio8-AI/Audio8_TTS) | Apache-2.0 | Apache-2.0 | 23 语种 | 0.6B DualAR，realism critic 强化学习 | 2026-11 |
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

### Ming-3.0-tts — 0.5B 就能"演"

不是"念得更像"，是"按指令演"：指定情绪走向、重读位置、停顿，句中可以插笑声和叹息。Voice Design 还能用文字直接设定音色。

0.5B 是 Qwen2.5-0.5B 稠密骨干 + DiT head，BF16 包 2.96GB；另有 tiny 版 7.9B/A1.3B MoE 做多说话人长文本。**但官方测试环境是 80GB H800，消费级显存数据没公开**——小参数量不等于小显存，先自己实测。

### Fish Audio Drama 3 — 专为群戏设计

35B MoE，一份剧本最多 16 个角色，括号里的舞台指示会被念出来。这是把"有声书/短剧配音"当第一场景在做，而不是把 TTS 当单句合成器。

**许可要格外小心**：Fish Audio Community License v1.0，年收入低于 50 万美元可免费商用；超出该门槛、或作为 TTS/克隆/推理服务对外提供，需单独授权；且禁止未经同意克隆真人声音。权重约 40GB，8GB 显存能跑但要把专家放系统内存。

### Audio8-TTS-Realistic — 治"念得准但听着假"

用真人录音当评分基准训练 realism critic，再上 GRPO 强化学习。CV3 九语种平均错误率 4.86%，优于 Qwen3-TTS-1.7B 的 7.73%。

**短板很具体**：泰语 WER 48.57%、粤语 CER 31.35%。多语种宣传和单语种可用是两件事——部署前先跑你的目标语种。需 PyTorch 2.5+ / Transformers 4.57+，且要 `trust_remote_code`。

### Open-OmniVoice-TTS — 把模型变成"能直接接"的服务

模型和服务的区别在于接入成本。Open-OmniVoice-TTS 把 OmniVoice 包成一个标准的 `/v1/audio/speech` 端点，**现有任何 OpenAI 客户端改个 base URL 就能用**，不用写一行适配代码；Open WebUI、LibreChat、SillyTavern 这类现成前端也能直接指过来。

默认带齐 13 个 OpenAI 音色名，其中 12 个是从 LibriVox 朗读者录音克隆来的开放许可音色。克隆用 3–20 秒录音，也能用文字描述造音色（性别/年龄/音高/口音）。Docker 部署，NVIDIA 或 AMD GPU，约 4GB 显存；一句话在 RTX 3080 上约 0.34 秒、RTX 5090 上 0.17 秒。

**两个必须注意的点**：一是**底层 OmniVoice 权重是 CC-BY-NC 非商用**，套个服务壳不改变这个约束，商用前要自己取得授权；二是**默认没有 API key 且监听所有网卡**，作者自己都提示暴露公网前要加鉴权或挂 VPN，直接对外开放等于送人一个免费 TTS。

> 仓库地址据作者 `hypersniper05` 与项目名推定，GitHub 禁止自动访问，本次未能直连验证；代码许可待确认。入库前建议自行点开确认。

## 常见坑

- **"支持 N 语言"是模型卡自报**，很多语言的训练数据只有几十小时（例：OmniVoice 葡萄牙语 16.9k 小时 vs 英语 206k 小时，比例差 12 倍）
- **中文 TTS 的数字/单位/多音字**是最容易翻车的地方，测试集里必须放进去
- **声音克隆的合规风险**：几乎所有模型卡都禁止未授权克隆与 impersonation，产品侧需要留同意凭证
