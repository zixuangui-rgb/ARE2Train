# 003 - 研究问题与实验协议

## 目标

把 ARE2Train 的研究问题、数据边界和评测规则写清楚，避免后续训练和评测出现 benchmark leakage。

## 日期

2026-05-10

## 相关 commit 或 run ID

本阶段文档提交，详见 git history。

## 环境

本阶段只修改文档和配置模板，不运行训练或评测。

## 命令

```text
无实验命令。
```

## 实现笔记

本阶段新增正式评测协议，并把教程第 01 章改写成面向初学者的说明。

核心决策：

- 最终评测使用官方 ARE/Gaia2 held-out tasks。
- 自建 synthetic scenarios 用于训练。
- 自建 validation scenarios 用于开发调试。
- 官方 held-out tasks 不进入训练、调参或 checkpoint 选择。
- 主实验固定官方 OpenClaw / 官方 agent scaffold，只替换模型 checkpoint。
- 裸模型不作为正式 agent baseline，只能作为工具调用格式 sanity check。
- 教程和术语表需要解释 agent scaffold，避免初学者误以为本项目要改 agent 外壳。

新增文件：

- `docs/paper/evaluation-protocol.md`
- `configs/eval/baseline.yaml`
- `configs/eval/sft.yaml`
- `configs/eval/preference.yaml`
- `configs/eval/rlvr.yaml`
- `configs/eval/teacher.yaml`

修改文件：

- `docs/tutorial/01-research-question-and-protocol.md`

## 观察到的结果

项目现在有了第一版实验协议。后续章节可以基于这份协议继续做环境搭建、baseline runner、trace schema 和训练流程。

## 失败和修复

暂无。

## 下一步计划

进入第 02 章：环境和仓库设置。
