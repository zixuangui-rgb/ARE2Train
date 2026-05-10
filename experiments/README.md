# 实验目录

这个目录记录实验清单和实验报告。

真正运行实验时，建议把每次 run 的输出放到仓库根目录下的 `runs/`。`runs/` 默认不进入 git，因为里面会有大量 trace、日志和模型输出。

## 推荐 run 目录格式

```text
runs/
  20260510_baseline_qwen3_14b_seed0/
    config.snapshot.yaml
    command.txt
    environment.txt
    traces/
    verifier_results.jsonl
    metrics.json
    failure_analysis.md
```

## 每次实验至少记录什么

- 运行时间。
- 使用的模型 checkpoint。
- 使用的评测配置。
- 官方 OpenClaw / 官方 agent 版本。
- 命令行参数。
- 随机种子。
- pass rate、成本、延迟和 token usage。
- 失败案例分类。

这样做的目的很简单：以后看到一个分数时，我们能知道它是怎么跑出来的。
