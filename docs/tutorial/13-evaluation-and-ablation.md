# 13 - Evaluation 与 Ablation

## 本章目标

建立满足论文要求的评测流程，证明模型提升是真实、稳定、可解释的。

## evaluation 要回答什么

- 模型总体是否变强？
- 哪些 task type 提升最大？
- 哪些错误减少了？
- 成本和延迟是否可接受？
- 在固定官方 OpenClaw scaffold 的前提下，提升来自 SFT、preference 还是 RLVR？

## 主要评测指标

```text
overall pass rate
split-wise pass rate
scenario-family pass rate
工具调用错误率
clarification accuracy
time-reasoning accuracy
单任务延迟
tokens per success
每次成功任务的成本
```

## 推荐对比

默认评测环境：官方 OpenClaw scaffold。

```text
Qwen3-14B base checkpoint
SFT checkpoint
SFT + preference checkpoint
SFT + preference + RLVR checkpoint
teacher model
```

## ablation 是什么

ablation 是拆掉某个模块，看效果变化。

例如：

- 去掉 ambiguity scenarios。
- 去掉 action-level reward。
- 只用 final reward。
- 只用 500 个 scenarios。
- 只用 SFT，不做 preference tuning。
- 只用 SFT + preference，不做 RLVR。

## 输入

- 所有模型 checkpoint。
- held-out validation。
- 官方 Gaia2 held-out tasks。
- trace store。

## 输出

- evaluation report。
- ablation table。
- failure analysis。
- 论文图表。

## 验收标准

- 每个模型在同一批任务上评测。
- 每个结果能追溯到 run ID。
- 每个提升都有统计和案例支持。
- 能解释哪些能力提升、哪些能力没有提升。

## 常见坑

- 不同模型跑不同任务集合。
- 不同 checkpoint 使用了不同 agent scaffold。
- 只报告最好一次结果。
- 没有记录失败案例。
- 没有成本和延迟评测指标。
