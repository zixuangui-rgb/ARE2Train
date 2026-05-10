# ARE2Train

**ARE2Train** 是一个面向真实工程和论文产出的研究项目。它的目标是把 ARE/Gaia2 这类动态 agent benchmark，扩展成可以持续采样、记录、打分和训练的 agentic post-training 系统，用来提升中小型开源模型在真实工作流任务中的表现。

项目会从 **Qwen3-14B** 这类原始开源模型出发，搭建完整闭环：

```text
scenario generation
-> rollout collection
-> trace analysis
-> verifier/action-level rewards
-> SFT / preference tuning / RLVR
-> held-out ARE/Gaia2 evaluation
-> tutorial + paper
```

## 为什么做这个项目

ARE/Gaia2 不只是用来测试模型的 test set。它有 tool environment、trace 和 write-action verifier，非常适合进一步变成 **agentic post-training** 的基础设施。

这个项目想回答的问题是：

> 能否把动态 agent benchmark 改造成可复现、可扩展的训练基础设施，并让中小型开源模型在真实工作流 agent 任务上显著变强？

目标不是做一个 demo，而是做一套能在真实 agent 开发中使用、并且足以支撑论文结果的系统。

## 研究假设

如果训练围绕以下几个核心设计展开，中小型开源模型可以在 ARE/Gaia2-style 任务上获得显著提升：

1. capability-factorized scenario generation。
2. transition-level 的 rollout 记录，而不是只保存最终对话。
3. action-level 的 verifier reward，而不是只有最终 pass/fail。
4. reflection memory 和 multi-agent teacher trajectories。
5. 面向成本和效率的 SFT、preference tuning、RLVR/GRPO。
6. 严格使用官方 ARE/Gaia2 任务做 held-out evaluation，避免 benchmark leakage。

## 项目原则

- **禁止 benchmark leakage**：官方 Gaia2 任务只用于最终 held-out evaluation，不直接用于训练。
- **verifier-first**：一个 scenario 如果不能被 verifier 自动检查，就不能作为高质量训练环境。
- **记录一切**：prompt、tool call、tool output、environment state、reward、latency、token usage、失败类型都必须记录。
- **工程可靠性**：runner 需要支持断点续跑、失败重试、版本化配置和可复现输出。
- **满足论文要求的评测**：必须报告 pass rate、split-wise 结果、cost、latency、tool-call error rate、ablation 和 failure analysis。
- **教程优先记录**：每一个实现阶段都要留下过程记录，后续整理成公开教程。

## 术语规范

为了和论文、代码、ARE/Gaia2、OpenClaw 等生态保持一致，核心技术术语默认保留英文，不做生硬翻译：

```text
agent
tool use
tool call
rollout
trajectory
trace
verifier
reward
scenario
benchmark
post-training
checkpoint
dataset
prompt
latency
token usage
RLVR / GRPO
```

如果一个词没有稳定、自然的中文说法，就保留英文。中文文档的职责是解释概念，而不是强行翻译术语。

## 系统规划

```text
ARE2Train
├── scenario factory
│   ├── 人工设计的 task templates
│   ├── LLM 生成的 scenario variants
│   ├── 程序化生成的 environment states
│   └── 自动生成 oracle / verifier
├── rollout engine
│   ├── OpenClaw / ARE adapters
│   ├── 本地模型服务 adapters
│   ├── API teacher model adapters
│   └── 异步、可断点续跑的批量执行
├── trace store
│   ├── full trajectories
│   ├── transition-level records
│   ├── reward annotations
│   └── failure taxonomy
├── training pipeline
│   ├── 基于 successful trajectories 的 SFT
│   ├── success-vs-failure preference data
│   ├── verifier-based RLVR / GRPO
│   └── checkpoint evaluation
└── reporting
    ├── held-out Gaia2 evaluation
    ├── ablation 实验
    ├── cost / latency analysis
    ├── 教程材料
    └── 论文草稿
```

## 初始模型计划

主模型：

```text
Qwen3-14B
```

候选 baseline：

```text
Qwen3-8B
Phi-4 14B
GLM-4.5-Air
MiniMax-M2 / M2.7 as strong agent baselines
teacher API models for trajectory generation
```

第一阶段目标是让 Qwen3-14B 在 held-out ARE/Gaia2-style 任务上获得可衡量提升，同时降低 tool-call error，并改善 cost per success。

## Evaluation Metrics

项目会持续记录：

- overall pass rate
- pass rate by task family
- pass rate by Gaia2 split
- tool-call error rate
- clarification accuracy
- time-reasoning accuracy
- dynamic-event handling accuracy
- average number of tool calls
- latency per task
- token usage per successful task
- cost per success

## 仓库结构

```text
.
├── README.md
├── docs/
│   ├── process-log/        # 每个阶段的原始记录，后续整理成教程
│   ├── tutorial/           # 打磨后的教程章节
│   └── paper/              # 论文大纲、figures、tables 和 notes
├── src/
│   └── are2train/          # 项目核心代码
├── scripts/                # 可直接运行的 CLI 脚本
├── configs/                # model、rollout、training、evaluation configs
├── experiments/            # experiment manifests 和 reports
└── tests/                  # 单元测试和 smoke tests
```

## 过程记录规范

每一个有意义的阶段都必须在 `docs/process-log/` 下创建一份 Markdown 记录，并使用 `docs/process-log/TEMPLATE.md` 模板。

过程记录不是可选项。它是后续公开教程的原始材料。

每条记录应该包含：

- 目标
- 日期
- 相关 commit 或 run ID
- setup / environment
- 精确命令
- 实现笔记
- observed results
- 失败和修复
- 下一步计划

## 第一阶段里程碑

1. **Baseline 复现**
   - 用原始 Qwen3-14B 跑一小批 ARE/Gaia2-compatible 任务。
   - 保存完整 traces 和 failure categories。

2. **Mini scenario factory**
   - 先构建 3 个 task families：calendar rescheduling、email extraction、ambiguity clarification。
   - 生成 300-500 个可验证 scenarios。

3. **Rollout and trace store**
   - 标准化 trajectory schema。
   - 增加 transition-level export。
   - 增加 resume/retry 支持。

4. **Teacher trajectory generation**
   - 每个 scenario 生成多条 rollouts。
   - 使用 verifier 过滤。
   - 构造 SFT 和 preference data。

5. **Qwen3-14B LoRA SFT**
   - 使用 verified successful trajectories 训练。
   - 在 held-out synthetic validation 和官方 Gaia2 tasks 上评测。

6. **RLVR / GRPO**
   - 使用 verifier rewards。
   - 对比 SFT-only 和 scaffold-only baselines。

7. **满足论文要求的评测**
   - 做 ablation 实验。
   - 报告 cost、latency、tool-call errors、split-wise results 和 failure analysis。

## 预期贡献

计划形成的论文/教程贡献包括：

1. 一套可复现的 pipeline，用于把 ARE/Gaia2-style benchmark 转化为 post-training environment。
2. 一种面向 personal-assistant agents 的 capability-factorized scenario generation 方法。
3. 一套面向 agentic RL 的 transition-level trace 和 verifier reward schema。
4. 一组关于 SFT、preference tuning、RLVR 在中小型开源模型上的实证研究。
5. 一份关于可用于真实工程的 agentic RL infrastructure 实战教程。

## 当前状态

项目已经完成初始骨架搭建，具体实现尚未开始。
