# 00 - 总览：从 0 到 ARE2Train

## 本章目标

这一章帮助你先建立全局地图：ARE2Train 到底是什么、为什么要做、完整流程有哪些阶段，以及每个阶段最后会产出什么。

如果你现在还不熟悉 RL、agent、Gaia2 或训练系统，没有关系。本教程会从最基础的概念开始。

## 先用一句话理解项目

ARE2Train 想做的是：

> 把 ARE/Gaia2 这类 agent benchmark 改造成可以训练模型的环境，并用它提升中小模型在真实工作流任务上的表现。

## 为什么这件事有价值

普通 benchmark 像考试卷，只告诉我们模型做对了多少题。

ARE2Train 想进一步做成训练场：

```text
模型尝试完成任务
-> 系统记录每一步
-> verifier 判断哪些动作对、哪些动作错
-> 把这些反馈变成训练数据或 reward
-> 训练模型变强
```

这对工业 agent 很重要，因为真实 agent 不是只回答问题，而是要调用工具、修改状态、处理时间、澄清歧义，并且不能乱操作。

## 完整流程

```text
1. 定义研究问题和评测协议
2. 搭建环境和仓库
3. 理解 ARE/Gaia2/OpenClaw
4. 跑原始模型 baseline
5. 设计 trajectory schema
6. 保存 trace 并分析失败
7. 生成可训练 scenarios
8. 设计 verifier 和 reward
9. 生成 teacher trajectories
10. 做 SFT / LoRA
11. 做 preference tuning
12. 做 RLVR / GRPO
13. 做 held-out evaluation 和 ablation
14. 工业化系统
15. 整理论文和教程
```

## 最终产物

项目最终应该产出：

- 一套可复现的 agentic RL infra。
- 一批可验证的 Gaia2-style training scenarios。
- 一套统一 trajectory / trace 格式。
- Qwen3-14B 等模型的 baseline、SFT、preference、RLVR 对比结果。
- held-out ARE/Gaia2 evaluation 报告。
- failure taxonomy 和可视化分析。
- 论文草稿。
- 一套面向学习者的教程。

## 学习者需要具备什么基础

最低要求：

- 会使用 Python。
- 会使用 Git。
- 理解基本的命令行操作。
- 大概知道 LLM 是什么。

不要求一开始就懂：

- RLVR / GRPO
- agent rollout
- OpenClaw
- Gaia2 verifier
- LoRA 训练

这些会在后续章节逐步解释。

## 本章验收标准

读完这一章后，你应该能回答：

- ARE2Train 想解决什么问题？
- benchmark 和 training environment 有什么区别？
- 为什么要记录 trajectory？
- 为什么 verifier 是训练中的关键？
- 完整项目大概要分成哪些阶段？

