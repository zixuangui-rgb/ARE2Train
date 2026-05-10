# 002 - 教程流程拆解

## 元信息

- 日期：2026-05-10
- 负责人：Zixuan Gui
- 相关 commit：pending
- 相关 config：无
- 相关 run folder：无

## 目标

在正式实现 ARE2Train 之前，先把从 0 开始做训练的完整流程拆解成教程章节，并为每个流程初始化 Markdown 文件。

## 背景

ARE2Train 不只是研究项目，也要作为教程案例发布。考虑到目标用户基础可能较弱，教程不能只写工程步骤，还需要解释概念、输入输出、验收标准和常见坑。

## 环境

本阶段只涉及文档初始化。

## 命令

```bash
# 文档由人工初始化，后续每章会随着实现进展持续补充。
```

## 实现笔记

教程被拆成 17 个文件：

```text
00-overview-learning-path.md
01-research-question-and-protocol.md
02-environment-and-repo-setup.md
03-are-gaia2-primer.md
04-baseline-runner.md
05-trajectory-schema.md
06-trace-store-and-failure-taxonomy.md
07-scenario-factory.md
08-verifier-and-reward.md
09-teacher-trajectories.md
10-sft-data-and-lora.md
11-preference-data-and-training.md
12-rlvr-grpo.md
13-evaluation-and-ablation.md
14-industrialization.md
15-paper-and-release.md
16-glossary.md
```

每章都优先面向学习者，避免默认读者已经理解 RL 或 agent infra。

## 结果

完成教程目录和每章初始骨架。

## 失败和修复

无。

## 未解决问题

- 后续是否需要把每章配套 notebook？
- 是否需要设计 Mini-Gaia2 local demo，作为教程中不依赖完整 Gaia2 的轻量版本？
- 每章是否需要加入练习题和自测题？

## 下一步

1. 先实现 baseline runner 相关章节。
2. 同步定义 trajectory schema。
3. 给每章补充对应代码链接和运行结果。

