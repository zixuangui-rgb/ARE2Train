# 04 - Baseline Runner：先跑原始模型

## 本章目标

在训练之前，先让原始模型跑通一批任务，得到 baseline。

baseline 是后续所有提升的参照物。没有 baseline，就不知道训练是否真的有效。

## 什么是 baseline

baseline 就是“不做训练、不做特殊优化”的初始表现。

例如：

```text
Qwen3-14B + 初始 prompt + OpenClaw/ReAct loop
```

这里的 `prompt + OpenClaw/ReAct loop` 就属于 agent scaffold。

可以把它理解成模型外面的操作流程：它把用户请求交给模型，解析模型想调用什么工具，执行工具，再把工具返回交回模型。模型负责“想下一步做什么”，scaffold 负责“把这一步真的跑起来”。

baseline runner 要记录 scaffold 版本，因为后面如果分数提升了，我们要知道提升来自哪里：

- 是模型经过训练后更强了。
- 还是 scaffold 更会组织工具调用了。

## 我们要做什么

- 写一个 batch runner。
- 支持选择 split 和任务数量。
- 调用模型。
- 运行任务。
- 保存完整 trace。
- 输出 summary。

## 输入

- 模型 endpoint。
- Gaia2 task 列表。
- prompt/scaffold 配置。
- runner 配置。

## 输出

```text
runs/baseline_qwen3_14b_001/
  config.yaml
  summary.json
  traces/
    task_001.json
    task_002.json
```

## 最小运行目标

第一版不要追求跑完整 benchmark。先跑：

```text
30-50 个任务
```

确认：

- 不崩溃。
- 能保存 trace。
- 能恢复中断任务。
- 能统计 pass/fail。

## 验收标准

- 可以一条命令启动 baseline。
- 中断后可以 resume。
- 每个任务都有 trace。
- summary 里有 pass rate、延迟和工具调用次数。

## 常见坑

- 只保存最终答案，没有保存中间工具调用。
- 失败任务没有保存错误信息。
- runner 不能断点续跑。
- prompt 和模型版本没有记录。
