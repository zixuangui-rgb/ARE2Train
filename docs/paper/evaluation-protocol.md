# ARE2Train 评测协议

## 目的

这份文档定义 ARE2Train 的实验规则。它回答三个问题：

- 我们要证明什么？
- 哪些数据可以使用？
- 什么样的结果才可信？

本项目最终要证明的是：通过 ARE/Gaia2-style 训练流程，Qwen3-14B 这类中小型开源模型可以在官方 ARE/Gaia2 held-out tasks 上获得可验证提升。

## 主研究问题

能否把 ARE/Gaia2-style benchmark 扩展成可训练环境，并通过 SFT、preference tuning、RLVR 提升 Qwen3-14B 在官方 ARE/Gaia2 held-out tasks 上的表现？

## 子问题

1. 自建 scenarios 训练出来的能力，能否迁移到官方 held-out tasks？
2. verifier reward 是否能减少工具调用错误？
3. SFT、preference tuning、RLVR 分别贡献多少提升？
4. 分数提升是否带来额外成本、延迟或 token usage？

## 数据使用规则

| 数据集合 | 来源 | 用途 | 是否可训练 |
|---|---|---|---|
| 训练集 | 自建 synthetic scenarios | SFT、preference tuning、RLVR、teacher trajectories | 可以 |
| 开发集 | 自建 validation scenarios | 调试 runner、选择 checkpoint、调整训练参数 | 不直接训练 |
| 最终测试集 | 官方 ARE/Gaia2 held-out tasks | 最终评测和论文主结果 | 不可以 |

官方 ARE/Gaia2 held-out tasks 只能用于最终评测。不得用于训练、数据生成、checkpoint 选择、训练策略调整或 reward 设计。

## benchmark leakage 防护规则

- 不把官方 held-out tasks 加入训练集。
- 不根据官方 held-out 错误反复修改训练策略或评测配置。
- 不根据官方 held-out 选择 checkpoint。
- 不把官方 held-out 的答案、trace 或 verifier 结果用于生成训练数据。
- 官方 held-out 结果必须和 run ID、配置、模型版本一起保存。

## 模型与方法

主模型：

```text
Qwen3-14B
```

训练路线：

```text
base checkpoint
-> SFT checkpoint
-> preference checkpoint
-> RLVR / GRPO checkpoint
```

评测路线：

```text
固定官方 OpenClaw / 官方 agent scaffold
-> 替换不同模型 checkpoint
-> 比较官方 held-out 结果
```

本项目主线只调整模型，不把 agent scaffold 作为研究变量。这里的 agent scaffold 指模型外层的执行流程，包括 prompt 组织、工具调用解析、工具执行、工具返回处理、停止条件、错误恢复和 trace 记录。

## baseline

所有对比必须使用同一套官方 OpenClaw scaffold、同一套评测任务和同一套结果记录格式。

第一版比较以下模型 checkpoint：

- Qwen3-14B base。
- Qwen3-14B SFT。
- Qwen3-14B SFT + preference。
- Qwen3-14B SFT + preference + RLVR。
- teacher model。

裸模型不作为正式 agent baseline。它没有官方 scaffold 时无法完成工具执行和环境交互，只能作为工具调用格式的辅助 sanity check。

## 评测指标

主指标：

- overall pass rate。
- 官方 held-out pass rate。

能力指标：

- 按任务族统计的 pass rate。
- 按 Gaia2 split 统计的 pass rate。
- 工具调用错误率。
- clarification accuracy。
- time-reasoning accuracy。
- dynamic-event handling accuracy。

效率指标：

- 平均工具调用次数。
- 单任务延迟。
- 每次成功任务的 token usage。
- 每次成功任务的成本。

分析指标：

- failure taxonomy。
- verifier reward breakdown。
- error trace examples。

## ablation 规则

ablation 用来判断每个模块到底有没有贡献。一次只移除或替换一个模块。

第一版 ablation：

- 不使用 SFT。
- 不使用 preference tuning。
- 不使用 RLVR。
- 不使用 action-level reward，只用最终 pass/fail。
- 使用不同规模或不同过滤规则的训练数据。

每个 ablation 都必须记录和完整方法的差异。

## 结果记录规则

每次 run 必须记录：

- run ID。
- 日期。
- git commit。
- 模型名称和 checkpoint。
- 官方 OpenClaw 配置版本。
- scenario 版本。
- eval config。
- 随机种子。
- pass rate。
- 成本、延迟、token usage。
- failure analysis。
- 完整 trace 路径。

推荐 run ID 格式：

```text
YYYYMMDD_method_model_split_seed
```

示例：

```text
20260510_sft_qwen3-14b_official-heldout_s42
```

## 有效结果标准

一个结果只有满足以下条件，才可以进入论文主表：

- 使用官方 ARE/Gaia2 held-out tasks。
- 评测前模型、checkpoint 和官方 OpenClaw 配置已经冻结。
- 没有根据官方 held-out 错误做后续调参。
- 保存完整 trace。
- 可以用同一配置重新运行。
- 报告成功和失败，不只报告最好数字。

## 当前默认决策

- 主模型：Qwen3-14B。
- 最终评测：官方 ARE/Gaia2 held-out tasks。
- 训练数据：自建 synthetic scenarios 和 teacher trajectories。
- 开发验证：自建 validation scenarios。
- 训练方法：SFT + preference tuning + RLVR/GRPO。
- agent scaffold：固定官方 OpenClaw / 官方 scaffold，不作为研究变量。
- 主要 claim：在固定官方 OpenClaw scaffold 下，训练后的 Qwen3-14B checkpoints 在官方 ARE/Gaia2 held-out tasks 上获得可验证提升。
