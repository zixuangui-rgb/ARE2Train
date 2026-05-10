# Process Log

这个目录用于记录 ARE2Train 每一个有意义的阶段。

目标有两个：

1. 让研究和工程过程可复现。
2. 为最终公开教程保留原始材料。

每个阶段都应该创建一份新的 Markdown 文件：

```text
001-bootstrap.md
002-baseline-qwen3-14b.md
003-scenario-factory-v0.md
004-rollout-store-v0.md
...
```

每条新记录都使用 `TEMPLATE.md`。

## 写作规则

- 尽可能记录精确命令。
- 链接到配置、commits、run folders 和结果文件。
- 不要只记录成功结果；失败和修复也是教程的一部分。
- 区分 observation 和主观解释。
- 不要把私有 API key、账号凭证、未公开数据写进日志。
- 核心技术术语保留英文，例如 `agent`、`rollout`、`trajectory`、`trace`、`verifier`、`reward`、`scenario`、`checkpoint`、`token usage`。但“工具调用、测试集、训练集、评测指标、成本、延迟、环境状态”等中文表达清楚的词，优先使用中文。
