# 贡献指南

## 收录标准

一个项目要进来，必须同时满足：

1. **有公开仓库或公开权重**（纯云端 API 不收，除非它同时开源了模型）
2. **能说清解决什么问题**——"AI 语音工具"这种描述不收
3. **仍在维护**，或至少有真实下游在用；停更超过 18 个月标注为 `dormant`
4. **许可证明确**，代码与权重分开写

## PR 必须包含的字段

```yaml
- id: example                # 小写短横线，全仓库唯一
  name: Example              # 展示名
  repo: https://github.com/org/repo
  category: asr              # asr | tts | speech-to-speech | voice-agent |
                             # diarization | on-device | audio-frontend |
                             # voice-conversion | speech-translation |
                             # meeting-app | voice-studio
  license: Apache-2.0        # 代码许可证，必须填
  weights_license: CC-BY-NC  # 权重许可证，与代码不同时必须单独写；未知写 unknown
  language: [zh, en]
  form: model                # model | toolkit | framework | runtime | desktop | library
  one_liner: 一句话说清它是什么、强在哪
  capabilities: [能力1, 能力2]
  note: 坑、限制、已知问题（可选但强烈建议）
  verified: "2026-10"        # 你亲自核实仓库状态的日期
```

## 文档更新

新增条目时，同步更新 `docs/<分类>.md` 的主表。如果这个项目属于"重点条目"（有独特取舍、或有必须警告的坑），请补一段说明，写清：

- **它凭什么值得单独说**（架构选择、性能量级、生态位置）
- **它的坑**（延迟、许可、语言覆盖、部署成本）
- **适合谁 / 不适合谁**

## 写作规范

- 不写营销词。"革命性""颠覆""SOTA"这类词一律不用，用**数字和取舍**代替
- 性能数字必须给**口径**：在什么数据集、什么硬件、什么语言上
- 不确定的事标 `unknown` 或"待复核"，**不要猜**
- 中文文档，项目名与许可证保留英文原名

## 拒绝的 PR 类型

- 只贴链接，没有任何说明
- 没有许可证信息
- 星数造假或数据来源不明
- 收录自己的商业产品（可以放 `docs/` 里的生态观察，但不进主表）
- 用 AI 生成的能力描述而未实际验证（能看出来）

## 提交前自查

- [ ] `data/projects.yaml` 能正常解析（`python -c "import yaml;yaml.safe_load(open('data/projects.yaml'))"`）
- [ ] `id` 不与现有条目重复
- [ ] 许可证字段填了，权重许可与代码许可分开
- [ ] `verified` 是今天的日期或最近一次核实日期
- [ ] 对应 `docs/` 页面已同步
