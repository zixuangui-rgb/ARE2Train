# 01 - 研究问题与实验协议

## 这一章能带来什么

这一章不会训练模型，也不会跑 benchmark。它的作用是先把“游戏规则”写清楚。

如果没有这一步，后面很容易出现一个问题：模型分数变高了，但别人不知道这个分数是不是真的可信。比如你可能不小心用测试题选择 checkpoint，或者不同模型用了不同任务集合，最后结果看起来提升了，但其实不能说明模型真的变强。

完成这一章之后，你会得到三样东西：

- 一个清楚的研究目标：我们到底想证明什么。
- 一套数据使用规则：哪些数据能训练，哪些数据只能最终测试。
- 一套评测协议：后面每次实验都按同一把尺子比较。

简单说，这一章是在给整个项目定标准。后面所有代码、训练和论文结果，都要回到这个标准上检查。

## 本章目标

本章要回答一个核心问题：

> 我们如何证明 Qwen3-14B 这类中小型开源模型，经过 ARE/Gaia2-style 训练后，在官方 ARE/Gaia2 held-out tasks 上真的变强？

注意这里有两个关键词：

- **官方 held-out tasks**：最终结果必须用官方保留测试任务证明。
- **真的变强**：不能只是记住题目，也不能只是换了评测设置后刚好撞对。

## 先用通俗语言理解实验协议

实验协议可以理解成考试规则。

训练模型像备考。你可以做练习题，可以做模拟题，也可以看老师讲解。但正式考试题不能提前拿来看，更不能拿正式考试题反复练。

在 ARE2Train 里：

```text
自建 synthetic scenarios = 练习题
自建 validation scenarios = 模拟题
官方 ARE/Gaia2 held-out tasks = 正式考试
```

我们最终要向外展示的是正式考试成绩，也就是官方 held-out 结果。自建数据只用来训练、调试和理解失败原因，不作为最终 claim 的主要证据。

## 核心概念

### 什么是 benchmark leakage

benchmark leakage 指测试题进入了训练或调参过程。

最直接的泄漏是：拿官方 Gaia2 测试题训练模型。这样分数再高也没有意义，因为模型可能只是记住了题。

更隐蔽的泄漏是：虽然没有直接训练测试题，但你反复看官方测试集错误，然后不断改数据生成器、改 reward、改 checkpoint 选择规则。这样也会慢慢针对测试集优化，最后结果同样不够可信。

### 什么是 held-out evaluation

held-out evaluation 指有一批任务在训练过程中完全不使用，只在最后评测时使用。

本项目里，最终 held-out evaluation 使用官方 ARE/Gaia2 held-out tasks。它的作用是判断模型有没有学到能迁移的能力，而不是只适应我们自己生成的数据。

### 为什么还需要自建 validation

因为训练过程中一定需要调试。

你会调整数据过滤规则、LoRA 参数、RLVR 参数，也会选择不同 checkpoint。如果每次调整都去看官方 held-out 分数，就等于反复偷看正式考试。

所以我们用自建 validation scenarios 做内部调试。它们不代表最终成绩，只帮助我们决定下一步怎么改。

### 本项目不改 agent

本项目的主线很明确：**固定官方 OpenClaw / 官方 agent，只调整模型 checkpoint**。

也就是说，我们不是要证明自己写了一个更好的 agent，而是要证明在官方 agent 完全不变的情况下，模型经过 SFT、preference tuning、RLVR 后真的变强。

## 我们最终要证明什么

主研究问题：

> 能否把 ARE/Gaia2-style benchmark 扩展成可训练环境，并通过 SFT、preference tuning、RLVR 提升 Qwen3-14B 在官方 ARE/Gaia2 held-out tasks 上的表现？

这个问题可以拆成四个小问题：

1. 自建 scenarios 训练出来的能力，能不能迁移到官方 held-out tasks？
2. verifier 提供的 reward，能不能减少工具调用错误？
3. SFT、preference tuning、RLVR 分别带来了多少提升？
4. 分数提升的代价是什么：成本、延迟、token usage 有没有明显变差？

## 数据使用规则

本项目采用下面的数据边界：

| 数据类型 | 来源 | 用途 | 能不能训练 |
|---|---|---|---|
| 训练集 | 自建 synthetic scenarios | 训练模型、生成 teacher trajectories | 可以 |
| 开发集 | 自建 validation scenarios | 调训练参数、排查 runner 问题、选择 checkpoint | 不直接训练 |
| 最终测试集 | 官方 ARE/Gaia2 held-out tasks | 最终评测和论文主结果 | 绝对不能训练 |

官方 ARE/Gaia2 held-out tasks 只能用于最终评测。不能用于训练，不能用于选择 checkpoint，也不能用于反复调训练策略。

## baseline 怎么设

baseline 是比较对象。没有 baseline，就不知道模型到底有没有进步。

第一版所有对比都使用同一个官方 OpenClaw / 官方 agent。需要比较的是这些模型 checkpoint：

- Qwen3-14B base。
- Qwen3-14B SFT。
- Qwen3-14B SFT + preference。
- Qwen3-14B SFT + preference + RLVR。
- teacher model，作为参考线。

主 baseline 应该是：

```text
Qwen3-14B base checkpoint
```

官方 OpenClaw / 官方 agent 是默认评测环境，不需要在每个对比项里重复写。后面所有训练后的 checkpoint 都放进这个相同环境里评测。这样变量才干净：如果分数提升，主要原因就是模型 checkpoint 变了。

## 评测指标

最终不能只看一个总分。agent 任务里，模型可能最后答对了，但过程很差；也可能最后失败了，但某些中间能力其实进步了。

本项目主要记录：

- overall pass rate：总体通过率。
- 按任务族统计的 pass rate：看 calendar、email、clarification 等能力分别如何。
- 按 Gaia2 split 统计的 pass rate：看不同官方 split 上是否稳定。
- 工具调用错误率：工具名、参数、调用顺序有没有错。
- clarification accuracy：该问清楚时有没有问清楚。
- time-reasoning accuracy：时间推理是否正确。
- dynamic-event handling accuracy：环境变化后是否能正确处理。
- 平均工具调用次数：是否过度调用工具。
- 单任务延迟：跑一个任务要多久。
- 每次成功任务的 token usage：成功一次要消耗多少 token。
- 每次成功任务的成本：成功率提升是否值得。

## 什么结果才算可信

一个实验结果要被接受，至少满足这些条件：

- 使用同一批官方 held-out tasks。
- 保存完整 trace。
- 记录模型版本、scenario 版本、checkpoint 版本和官方 OpenClaw 配置版本。
- 记录运行配置和随机种子。
- 报告失败类型，不只报告成功率。
- 不根据官方 held-out 错误反复调整训练数据、reward 或 checkpoint 选择规则。

如果一个结果无法复现，或者不知道用了什么配置，那它不能作为论文主结果。

## 本章要产出的文件

这一章完成后，仓库里应该有：

```text
docs/paper/evaluation-protocol.md
configs/eval/baseline.yaml
configs/eval/sft.yaml
configs/eval/preference.yaml
configs/eval/rlvr.yaml
configs/eval/teacher.yaml
docs/process-log/003-research-question-and-protocol.md
```

`evaluation-protocol.md` 是正式协议。教程负责解释为什么这么做，协议文件负责让后续实验有章可循。

## 验收标准

完成本章后，你应该能回答：

- 我们最终要证明什么？
- 哪些数据可以训练？
- 哪些数据只能最终测试？
- 为什么官方 held-out 不能用来调参？
- baseline 有哪些？
- 主要评测指标有哪些？
- 一个实验结果怎样才算可信？

如果这些问题都能回答清楚，就可以进入下一章：环境和仓库设置。

## 常见坑

- 过早看官方 held-out 结果，然后根据错误反复调整训练策略。
- 只报告总体 pass rate，不分析失败类型。
- 不同 checkpoint 使用了不同版本的官方 agent。
- 不记录模型、数据、checkpoint 和官方 OpenClaw 配置版本。
- 用不同任务集合比较不同模型。
- 自建 validation 分数很好，就直接声称官方能力提升。
