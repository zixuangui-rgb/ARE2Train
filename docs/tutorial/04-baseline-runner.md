# 04 - Baseline Runner：先跑官方 OpenClaw baseline

## 本章目标

在训练之前，先让 Qwen3-14B base checkpoint 在官方 OpenClaw scaffold 里跑通一批任务，得到 baseline。

baseline 是后续所有提升的参照物。没有 baseline，就不知道训练是否真的有效。

## 什么是 baseline

baseline 就是“不训练模型”的初始表现。

例如：

```text
Qwen3-14B base checkpoint
```

默认评测环境是官方 OpenClaw scaffold。裸的 Qwen3-14B 不能作为正式 agent baseline，因为没有 OpenClaw scaffold，它不会真正执行工具，也不会修改环境或保存 trace。

这里的官方 OpenClaw scaffold 是固定外壳。它把用户请求交给模型，解析模型想调用什么工具，执行工具，再把工具返回交回模型。

本项目主线只比较模型 checkpoint：

```text
base checkpoint
SFT checkpoint
preference checkpoint
RLVR checkpoint
```

这些 checkpoint 都必须放进同一个官方 OpenClaw scaffold 里评测。这样后面如果分数提升，变量就是模型本身，而不是外面的 agent 流程变了。

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
- 官方 OpenClaw 配置。
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
- 官方 OpenClaw 配置和模型版本没有记录。
