# 001 - 项目启动

## 元信息

- 日期：2026-05-10
- 负责人：Zixuan Gui
- 相关 commit：pending
- 相关 config：无
- 相关 run folder：无

## 目标

创建 ARE2Train 仓库结构，并定义项目方向：做一个面向真实工程和论文产出的 RL infrastructure 项目，用来提升中小型开源模型在 ARE/Gaia2-style dynamic agent tasks 上的表现。

## 背景

这个项目有两个用途：

1. 作为面向 Meta MSL-style agentic AI 方向的高质量申请项目和研究项目。
2. 作为现代 RL 教程未来的案例，尤其对应 Agentic RL 和 RLVR 部分。

## 环境

仓库来自：

```text
https://github.com/zixuangui-rgb/ARE2Train
```

本地路径：

```text
/Users/hell/Projects/meta_paris/ARE-GAIA/ARE2Train
```

## 命令

```bash
git clone https://github.com/zixuangui-rgb/ARE2Train.git
```

## 实现笔记

创建了初始 README 和 documentation 目录：

```text
docs/process-log/
docs/tutorial/
docs/paper/
src/are2train/
scripts/
configs/
experiments/
tests/
```

后续每个主要阶段都必须写 process log。这些记录会作为最终教程的原始素材。

## 结果

仓库已经有了项目定位、milestones 和文档记录规范。

## 失败和修复

本阶段没有实现失败。

## 未解决问题

- 第一版 baseline 应该使用哪个具体 Qwen3-14B checkpoint？
- 第一版 runnable environment 应该直接用官方 ARE/Gaia2，还是先做一个更快迭代的 Gaia2-like local environment？
- 第一版 RL stack 应该用 verl、OpenRLHF，还是自写轻量 GRPO loop？

## 下一步

1. 添加 baseline reproduction 的具体项目计划。
2. 定义第一版 trajectory schema。
3. 搭建或改造一个最小 ARE/Gaia2 rollout runner。
4. 用开源模型或 OpenAI-compatible endpoint 跑一个小 baseline。
