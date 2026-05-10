# 01 - 研究问题与实验协议

## 本章目标

在动手写代码前，先定义清楚项目要证明什么，以及哪些数据能用来训练，哪些数据只能用于最终测试。

这一步很重要。如果实验协议不清楚，后面就容易出现 benchmark leakage，导致结果没有说服力。

## 核心概念

### 什么是 benchmark leakage

benchmark leakage 指模型在训练阶段接触到了本来应该只用于测试的题目。

如果你用官方 Gaia2 测试题训练模型，然后又用同一批题评测，分数即使提升也不可信。

### 什么是 held-out evaluation

held-out evaluation 指最终 test set 在训练过程中完全不使用。它用来检验模型是否真的学会了能力，而不是记住了训练题。

## 我们要做什么

这一阶段要写清楚：

- 主研究问题是什么。
- 训练数据从哪里来。
- 官方 ARE/Gaia2 数据如何使用。
- baseline 模型有哪些。
- 最终 metrics 有哪些。
- 哪些实验算有效，哪些实验不算。

## 输入

- ARE/Gaia2 官方任务说明。
- 项目目标模型，例如 Qwen3-14B。
- 可用算力，例如 8xA100。
- 计划生成的 synthetic scenarios。

## 输出

- `docs/paper/evaluation-protocol.md`
- `configs/eval/*.yaml`
- train / dev / test 数据使用规则。

## 推荐协议

```text
training set：
  自建 Gaia2-style synthetic scenarios

dev set：
  自建 validation scenarios
  少量官方任务只用于调试 runner，不用于训练

最终 test set：
  官方 Gaia2 held-out tasks
```

## 关键决策

1. 官方 Gaia2 不直接进入训练。
2. 训练主要依赖自建 scenarios 和 teacher trajectories。
3. 每个模型都在同一批 held-out tasks 上评测。
4. 每个结果都保存 trace，方便复查。

## 验收标准

本阶段完成后，应该能明确回答：

- 哪些数据用于训练？
- 哪些数据用于最终测试？
- baseline 是什么？
- 主要 metrics 是什么？
- 如何避免 benchmark leakage？

## 常见坑

- 先跑 test set，再根据 test set 错误不断调 prompt。
- 只报告总体 pass rate，不报告分类型结果。
- 没有记录模型版本、prompt 版本和环境版本。
- 用不同任务集合比较不同模型。
