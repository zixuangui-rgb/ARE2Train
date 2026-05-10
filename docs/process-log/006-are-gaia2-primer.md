# 006 - ARE/Gaia2/OpenClaw 入门

## 目标

完成第 03 章教程，让基础较弱的读者先理解 ARE、Gaia2、官方 agent、scenario、trace 和 verifier 的关系，再进入 baseline runner。

## 日期

2026-05-10

## 相关 commit 或 run ID

本阶段文档和配置提交，详见 git history。

## 环境

本阶段不运行模型训练，不正式跑 Gaia2 分数。

参考公开资料：

- Meta Research 的 ARE 论文页面。
- Hugging Face 的 Gaia2 博客。
- Hugging Face 的 Gaia2 dataset card。
- PyPI 的 `meta-agents-research-environments` 页面。

## 命令

```bash
make doctor
make smoke
```

## 实现笔记

新增和修改内容：

- 重写 `docs/tutorial/03-are-gaia2-primer.md`。
- 新增 `configs/are.example.yaml`，作为第 04 章 baseline runner 的前置配置模板。
- 更新教程索引和 README 当前状态。

核心写作原则：

- 用“模拟手机 + 个人助手任务”的方式解释 Gaia2。
- 强调 Gaia2 不是普通问答数据集，而是动态交互 benchmark。
- 解释 scenario、trace、verifier 与 post-training 的关系。
- 保持项目边界：主实验不修改官方 OpenClaw / 官方 agent，只替换模型 checkpoint。

## 观察到的结果

第 03 章现在承担从概念到 baseline runner 的过渡作用。第 04 章可以直接从 `configs/are.example.yaml` 继续扩展实际运行配置。

## 失败和修复

暂无。

## 未解决问题

- 尚未安装 `meta-agents-research-environments`。
- 尚未运行 `are-benchmark`。
- 尚未接入 Qwen3-14B 模型服务。

这些问题留到第 04 章处理。

## 下一步计划

进入第 04 章：实现 baseline runner，先用官方 agent 运行少量 Gaia2 mini tasks，并保存 trace 和 summary。
