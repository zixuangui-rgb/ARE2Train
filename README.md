# ARE2Train

**ARE2Train** 是一个面向真实工程和论文产出的研究项目。它的目标是把 ARE/Gaia2 这类动态 agent benchmark，扩展成可以持续采样、记录、打分和训练的 agentic post-training 系统，用来提升中小型开源模型在真实工作流任务中的表现。

项目会从 **Qwen3-14B** 这类原始开源模型出发，搭建完整闭环：

```text
生成 scenarios
-> 收集 rollouts
-> 分析 trace
-> verifier / action-level reward
-> SFT / preference tuning / RLVR
-> held-out ARE/Gaia2 评测
-> tutorial + paper
```

## 为什么做这个项目

ARE/Gaia2 不只是用来测试模型的测试集。它有工具环境、trace 和 write-action verifier，非常适合进一步变成 **agentic post-training** 的基础设施。

这个项目想回答的问题是：

> 能否把动态 agent benchmark 改造成可复现、可扩展的训练基础设施，并让中小型开源模型在真实工作流 agent 任务上显著变强？

目标不是做一个 demo，而是做一套能在真实 agent 开发中使用、并且足以支撑论文结果的系统。

## 研究假设

如果训练围绕以下几个核心设计展开，中小型开源模型可以在 ARE/Gaia2-style 任务上获得显著提升：

1. 按能力拆分的 scenario generation。
2. transition-level 的 rollout 记录，而不是只保存最终对话。
3. action-level 的 verifier reward，而不是只有最终 pass/fail。
4. 高质量 teacher trajectories 和可验证训练数据。
5. 面向成本和效率的 SFT、preference tuning、RLVR/GRPO。
6. 严格使用官方 ARE/Gaia2 任务做 held-out evaluation，避免 benchmark leakage。

## 项目原则

- **禁止 benchmark leakage**：官方 Gaia2 任务只用于最终 held-out evaluation，不直接用于训练。
- **verifier-first**：一个 scenario 如果不能被 verifier 自动检查，就不能作为高质量训练环境。
- **记录一切**：prompt、工具调用、工具返回、环境状态、reward、延迟、token usage、失败类型都必须记录。
- **工程可靠性**：runner 需要支持断点续跑、失败重试、版本化配置和可复现输出。
- **满足论文要求的评测**：必须报告 pass rate、split-wise 结果、成本、延迟、工具调用错误率、ablation 和 failure analysis。
- **教程优先记录**：每一个实现阶段都要留下过程记录，后续整理成公开教程。

## 当前实验协议

项目已经固定第一版实验协议：

- 最终主结果使用官方 ARE/Gaia2 held-out tasks。
- 自建 synthetic scenarios 用于训练和生成 teacher trajectories。
- 自建 validation scenarios 用于开发调试，不作为最终 claim 的主要证据。
- 官方 held-out tasks 不进入训练、调参、checkpoint 选择或 reward 设计。
- 主实验固定官方 OpenClaw / 官方 agent scaffold，只替换模型 checkpoint。
- 本项目主线是模型 post-training，不把改进 agent scaffold 作为研究变量。

正式协议见 `docs/paper/evaluation-protocol.md`，评测配置模板见 `configs/eval/`。

## 术语规范

为了和论文、代码、ARE/Gaia2、OpenClaw 等生态保持一致，少数核心技术术语默认保留英文，不做生硬翻译：

```text
agent
agent scaffold
rollout
trajectory
trace
verifier
reward
scenario
benchmark
post-training
checkpoint
prompt
token usage
RLVR / GRPO
```

正文中优先使用自然中文，例如“工具调用、工具返回、训练集、测试集、数据集、评测指标、成本、延迟、环境状态”。只有在字段名、代码接口、论文固定说法或容易歧义时，才保留英文。

## 系统规划

```text
ARE2Train
├── scenario factory
│   ├── 人工设计的任务模板
│   ├── LLM 生成的 scenario 变体
│   ├── 程序化生成的环境状态
│   └── 自动生成 oracle / verifier
├── rollout engine
│   ├── OpenClaw / ARE adapters
│   ├── 本地模型服务 adapters
│   ├── API teacher model adapters
│   └── 异步、可断点续跑的批量执行
├── trace store
│   ├── full trajectories
│   ├── transition-level 记录
│   ├── reward 标注
│   └── failure taxonomy
├── training pipeline
│   ├── 基于成功的 trajectory 做 SFT
│   ├── 成功/失败 preference data
│   ├── 基于 verifier 的 RLVR / GRPO
│   └── checkpoint 评测
└── reporting
    ├── held-out Gaia2 评测
    ├── ablation 实验
    ├── 成本和延迟分析
    ├── 教程材料
    └── 论文草稿
```

## 初始模型计划

主模型：

```text
Qwen3-14B
```

候选参考模型：

```text
Qwen3-8B
Phi-4 14B
GLM-4.5-Air
MiniMax-M2 / M2.7 as strong references
teacher API models for trajectory generation
```

第一阶段目标是让 Qwen3-14B 在固定官方 OpenClaw scaffold 的前提下，在 held-out ARE/Gaia2-style 任务上获得可衡量提升，同时降低工具调用错误率，并改善每次成功任务的成本。

## 评测指标

项目会持续记录：

- overall pass rate
- 按任务族统计的 pass rate
- 按 Gaia2 split 统计的 pass rate
- 工具调用错误率
- clarification accuracy
- time-reasoning accuracy
- dynamic-event handling accuracy
- 平均工具调用次数
- 单任务延迟
- 每次成功任务的 token usage
- 每次成功任务的成本

## 仓库结构

```text
.
├── README.md
├── docs/
│   ├── process-log/        # 每个阶段的原始记录，后续整理成教程
│   ├── tutorial/           # 打磨后的教程章节
│   └── paper/              # 论文大纲、图表、实验表格和笔记
├── src/
│   └── are2train/          # 项目核心代码
├── scripts/                # 可直接运行的 CLI 脚本
├── configs/                # 模型、rollout、训练、评测配置
│   └── eval/               # baseline、SFT、preference、RLVR、teacher 评测模板
├── experiments/            # 实验清单和报告
└── tests/                  # 单元测试和 smoke tests
```

## 过程记录规范

每一个有意义的阶段都必须在 `docs/process-log/` 下创建一份 Markdown 记录，并使用 `docs/process-log/TEMPLATE.md` 模板。

过程记录不是可选项。它是后续公开教程的原始材料。

每条记录应该包含：

- 目标
- 日期
- 相关 commit 或 run ID
- 实验和开发环境
- 精确命令
- 实现笔记
- 观察到的结果
- 失败和修复
- 下一步计划

## 第一阶段里程碑

1. **Baseline 复现**
   - 用 Qwen3-14B base checkpoint + 官方 OpenClaw scaffold 跑一小批 ARE/Gaia2-compatible 任务。
   - 保存完整 traces 和 failure categories。

2. **Mini scenario factory**
   - 先构建 3 个任务族：calendar rescheduling、email extraction、ambiguity clarification。
   - 生成 300-500 个可验证 scenarios。

3. **Rollout 和 trace store**
   - 标准化 trajectory schema。
   - 增加 transition-level 导出。
   - 增加 resume/retry 支持。

4. **Teacher trajectory generation**
   - 每个 scenario 生成多条 rollouts。
   - 使用 verifier 过滤。
   - 构造 SFT 和 preference data。

5. **Qwen3-14B LoRA SFT**
   - 使用通过 verifier 检查的成功的 trajectory 训练。
   - 在 held-out synthetic validation 和官方 Gaia2 tasks 上评测。

6. **RLVR / GRPO**
   - 使用 verifier rewards。
   - 在同一个官方 OpenClaw scaffold 下，对比 base、SFT、preference、RLVR checkpoints。

7. **满足论文要求的评测**
   - 做 ablation 实验。
   - 报告成本、延迟、工具调用错误、split-wise 结果和 failure analysis。

## 预期贡献

计划形成的论文/教程贡献包括：

1. 一套可复现的 pipeline，用于把 ARE/Gaia2-style benchmark 转化为可训练环境。
2. 一种面向 personal-assistant agents 的按能力拆分的 scenario generation 方法。
3. 一套面向 agentic RL 的 transition-level trace 和 verifier reward schema。
4. 一组关于 SFT、preference tuning、RLVR 在中小型开源模型上的实证研究。
5. 一份关于可用于真实工程的 agentic RL infrastructure 实战教程。

## 当前状态

项目已经完成初始骨架搭建，并完成第 01 章“研究问题与实验协议”的正式化：

- 教程说明：`docs/tutorial/01-research-question-and-protocol.md`
- 正式协议：`docs/paper/evaluation-protocol.md`
- 评测配置模板：`configs/eval/`
- 过程记录：`docs/process-log/003-research-question-and-protocol.md`

下一步进入第 02 章：环境和仓库设置。
