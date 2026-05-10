# 论文笔记

这个目录用于存放论文计划、实验表格、图、草稿和相关笔记。

初始工作标题：

> ARE2Train: Turning Dynamic Agent Benchmarks into Verifiable Post-Training
> Environments for Efficient Workflow Agents

初始论文主张：

1. ARE/Gaia2-style environments 可以通过 verifier-based rewards 和 transition-level traces 转化为可规模化使用的训练环境。
2. Capability-factorized synthetic scenarios 可以提升中小型 agentic models 的样本效率。
3. 在不改官方 OpenClaw / 官方 agent 的前提下，SFT、preference tuning 和 RLVR 能更稳定地提升 held-out personal-assistant task 表现。
4. 成本感知评测可以揭示 pass rate、延迟、工具使用和每次成功任务的 token usage 之间的取舍。

## 当前文件

- `evaluation-protocol.md`：第一版正式评测协议，定义研究问题、数据边界、baseline、评测指标和结果有效性标准。
