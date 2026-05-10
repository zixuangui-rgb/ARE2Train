# ARE2Train 教程目录

这个目录用于存放 ARE2Train 的教程章节。

教程目标不是直接假设读者已经懂 RL 或 agent infra，而是带着基础较弱的学习者，从 0 开始理解并搭建一套工业级 agentic RL infrastructure。

> 基于 ARE/Gaia2-style environments 构建工业级 agentic RL infrastructure。

## 适合谁

- 想系统学习 agentic RL 的同学。
- 想理解 ARE/Gaia2 如何从 benchmark 变成 training environment 的同学。
- 想做一个可以用于申请、论文或工业实践的 agent training 项目的同学。
- 有基础编程能力，但还不熟悉 rollout、trajectory、verifier、RLVR/GRPO 的同学。

## 学习方式

每章都按同一套结构组织：

```text
本章目标
需要先懂什么
核心概念
我们要做什么
输入和输出
实现步骤
验收标准
常见坑
最终产物
```

读者可以按顺序学习，也可以根据项目进度跳到具体章节。

## 章节规划

| 章节 | 文件 | 这一章解决什么问题 |
|---|---|---|
| 00 | [00-overview-learning-path.md](00-overview-learning-path.md) | 从整体上理解 ARE2Train 要做什么 |
| 01 | [01-research-question-and-protocol.md](01-research-question-and-protocol.md) | 定义研究问题、实验边界和防止 benchmark leakage |
| 02 | [02-environment-and-repo-setup.md](02-environment-and-repo-setup.md) | 搭建代码仓库、环境和运行基础 |
| 03 | [03-are-gaia2-primer.md](03-are-gaia2-primer.md) | 用通俗语言理解 ARE/Gaia2/OpenClaw |
| 04 | [04-baseline-runner.md](04-baseline-runner.md) | 先跑通原始模型 baseline |
| 05 | [05-trajectory-schema.md](05-trajectory-schema.md) | 设计统一 trajectory / trace 数据格式 |
| 06 | [06-trace-store-and-failure-taxonomy.md](06-trace-store-and-failure-taxonomy.md) | 保存、分析和分类失败案例 |
| 07 | [07-scenario-factory.md](07-scenario-factory.md) | 生成可训练的 Gaia2-style scenarios |
| 08 | [08-verifier-and-reward.md](08-verifier-and-reward.md) | 把 verifier 变成 reward 信号 |
| 09 | [09-teacher-trajectories.md](09-teacher-trajectories.md) | 用强模型生成 teacher trajectories |
| 10 | [10-sft-data-and-lora.md](10-sft-data-and-lora.md) | 用成功轨迹做 SFT / LoRA |
| 11 | [11-preference-data-and-training.md](11-preference-data-and-training.md) | 构造 preference data 并训练 |
| 12 | [12-rlvr-grpo.md](12-rlvr-grpo.md) | 做 verifier-based RLVR / GRPO |
| 13 | [13-evaluation-and-ablation.md](13-evaluation-and-ablation.md) | 做 held-out evaluation 和 ablation |
| 14 | [14-industrialization.md](14-industrialization.md) | 把系统做成工业可用的 infra |
| 15 | [15-paper-and-release.md](15-paper-and-release.md) | 整理论文、教程和开源发布 |
| 16 | [16-glossary.md](16-glossary.md) | 术语表，帮助基础较弱的读者查概念 |

## 教程写作原则

- 先解释“为什么”，再解释“怎么做”。
- 每章只引入少量新概念。
- 对 `agent`、`rollout`、`trajectory`、`verifier`、`reward` 等核心术语保留英文。
- 每章都必须有明确的输入、输出和验收标准。
- 每章都要记录常见错误，因为这些错误是学习的一部分。
