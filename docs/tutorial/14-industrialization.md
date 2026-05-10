# 14 - 工业化：把研究代码变成可用 infra

## 本章目标

把实验系统整理成可以在真实团队中使用的 agentic RL infra。

## 什么叫工业可用

工业可用不只是能跑一次，而是：

- 可配置。
- 可复现。
- 可监控。
- 可断点续跑。
- 可扩展。
- 错误可诊断。
- 结果可审计。

## 需要补齐的能力

```text
config management
async rollout
resume / retry
trace database
dashboard
experiment registry
model registry
data versioning
cost tracking
access control
```

## 输入

- 已经跑通的训练和评测流程。
- 多次实验产生的 runs。
- 用户或研究团队的实际需求。

## 输出

- 稳定 CLI。
- 配置模板。
- 实验 registry。
- trace viewer 或 dashboard。
- 文档和部署说明。

## 验收标准

- 新人能按文档复现 baseline。
- 实验失败后能 resume。
- 每个结果都能追溯到 config、commit 和 run ID。
- 可以并发跑多个任务。
- 费用和延迟可统计。

## 常见坑

- 研究代码和生产代码完全混在一起。
- 配置散落在脚本里。
- trace 太大但没有索引。
- 没有 experiment registry。
- 没有处理并发失败和部分失败。

