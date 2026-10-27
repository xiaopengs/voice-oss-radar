# 09 · 语音翻译（同传 / S2ST）

> 三条技术路线，延迟与质量成反比：
> **级联（ASR → MT → TTS）**：质量最好、可控、可插入术语表，延迟 2–5 秒
> **端到端 S2ST**：直接语音到语音，延迟 500ms–1.5 秒，但音质与忠实度打折
> **流式同传（simultaneous）**：边听边译，延迟 <1 秒，需要"读/写策略"（何时开始译）

## 主表

| 项目 | 地址 | 许可 | 覆盖 | 形态 | 核实 |
|---|---|---|---|---|---|
| SeamlessM4T / SeamlessStreaming | [facebookresearch/seamless_communication](https://github.com/facebookresearch/seamless_communication) | **CC-BY-NC 4.0** | 约 100 语言（文本/语音） | S2ST / S2TT / 流式 | 2026-10 |
| Hibiki / Hibiki-Zero | [kyutai-labs/hibiki](https://github.com/kyutai-labs/hibiki) | CC-BY 4.0（权重） | 4 语言 | 实时 S2ST | 2026-10 |
| Whisper + NLLB 级联 | [openai/whisper](https://github.com/openai/whisper) + [facebookresearch/nllb](https://github.com/facebookresearch/fairseq/tree/nllb) | MIT / CC-BY-NC | 多语 | 级联 | 2026-10 |
| Qwen-Omni | [QwenLM/Qwen2.5-Omni](https://github.com/QwenLM/Qwen2.5-Omni) | Apache-2.0 | 多语 | 语音理解 + 翻译 | 2026-10 |

---

## 重点条目

### SeamlessM4T v2 / SeamlessStreaming — 覆盖最广

- **地址**：[facebookresearch/seamless_communication](https://github.com/facebookresearch/seamless_communication)
- **定位**：Meta 的统一语音翻译模型族，一个模型覆盖 **S2ST / S2TT / T2ST / T2TT / ASR**
- **能力范围**：约 100 种语言（语音输入/输出各 36–100 种不等）；SeamlessStreaming 支持**流式同传**与读写策略（EMMA）
- **⚠️ 许可**：**CC-BY-NC 4.0，禁止商用**。这是它最大的现实障碍
- **坑**：模型大、推理慢；语言对质量差异极大（欧洲语言远好于亚洲语言）；中文方向明显弱于专门的中文模型

### Hibiki（Kyutai）— 实时同传的体验标杆

- **地址**：[kyutai-labs/hibiki](https://github.com/kyutai-labs/hibiki)
- **定位**：基于 Moshi 架构的**流式语音到语音翻译**，输出目标语言语音 + 文本
- **能力范围**：法语→英语为主，扩展至 4 语言；**边听边译**，延迟低；音色保持原说话人特征（voice preservation）
- **Hibiki-Zero**：**不需要词级对齐数据**训练同传模型的方法，意义大于模型本身——对齐数据是同传的最大瓶颈
- **适合**：实时字幕/同传 demo、低延迟跨语言通话

### 级联方案（工程上最常用）

```
麦克风 → VAD → ASR（Whisper/FunASR/SenseVoice） → MT（NLLB/GPT/DeepL） → TTS
```

- **优势**：每段可换、可加**术语表/领域词典**（这是端到端做不到的）、可输出双语字幕、可人工校对
- **延迟来源**：ASR 等一句话说完（1–3s）+ MT（0.3–1s）+ TTS 首包（0.2–0.5s）
- **优化**：ASR 用流式模型（Zipformer streaming）；MT 用增量翻译；TTS 用流式首包
- **适合**：会议同传、课程字幕、需要术语准确的专业场景

---

## 选型建议

| 场景 | 方案 |
|---|---|
| 会议字幕（双语、要术语准确） | 级联，ASR 用流式 + 术语表注入 MT |
| 实时通话同传（体验优先） | Hibiki 类端到端，或 SeamlessStreaming（仅研究） |
| 商用产品 | **避开 CC-BY-NC 的 Seamless**；级联 + 商用友好模型（Qwen3-ASR + 自建 MT + Qwen3-TTS） |
| 视频字幕批处理 | Whisper 系 + MT + 人工校对，成本最低 |

## 坑

- **"支持 100 语言"是模型卡口径**，实际可用语言对少得多，必须用你的目标语言对实测
- **同传的读写策略**比模型更重要：什么时候开始译、遇到没说完的句子怎么办，决定了可用性
- **数字、专名、缩略语**是翻译质量的黑洞，级联方案里加术语表能救回来，端到端救不回来
- 语音翻译的**评测集（如 FLEURS）与真实口音差距大**，别只看 BLEU
