# 论文笔记

这个目录用于存放论文计划、实验表格、图、草稿和相关笔记。

初始工作标题：

> ARE2Train: Turning Dynamic Agent Benchmarks into Verifiable Post-Training
> Environments for Efficient Workflow Agents

初始论文主张：

1. ARE/Gaia2-style environments 可以通过 verifier-based rewards 和 transition-level traces 转化为可规模化使用的训练环境。
2. Capability-factorized synthetic scenarios 可以提升中小型 agentic models 的样本效率。
3. 相比 scaffold-only prompting，结合 reflection、SFT、preference tuning 和 RLVR 能更稳定地提升 held-out personal-assistant task 表现。
4. 成本感知评测可以揭示 pass rate、延迟、工具使用和每次成功任务的 token usage 之间的取舍。
