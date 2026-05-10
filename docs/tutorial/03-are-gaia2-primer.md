# 03 - ARE/Gaia2/OpenClaw 入门

## 这一章能带来什么

这一章不训练模型，也不正式跑分。它的目标是让你看懂后面实验里反复出现的几个东西：

- ARE 是什么。
- Gaia2 是什么。
- 官方 OpenClaw / 官方 agent 在评测中做什么。
- 一个 scenario 里有什么。
- 为什么 trace 和 verifier 对训练很重要。
- 为什么本项目可以把 Gaia2-style benchmark 变成 post-training 环境。

完成这一章之后，你应该能看懂第 04 章 baseline runner 的输入和输出，不会把 Gaia2 误解成普通问答数据集。

## 本章目标

本章要建立一个简单心智模型：

```text
ARE = 提供可交互任务世界的环境平台
Gaia2 = 用 ARE 构建的一套 agent benchmark
官方 OpenClaw / 官方 agent = 官方评测时运行模型和工具交互的默认执行方式
ARE2Train = 在不改官方 agent 的前提下，收集 trace、构造训练数据、训练模型、评测 checkpoint
```

一句话概括：

> Gaia2 不是让模型回答选择题，而是让模型在一个会变化的模拟世界里完成任务。

## 需要先懂什么

如果你是初学者，只需要先理解下面这几个词。

- **任务世界**：一个模拟出来的环境，里面有邮件、日历、联系人、文件、购物信息等数据。
- **工具**：模型不能直接改世界，需要通过工具 API 查数据、改日历、发消息等。
- **scenario**：一条完整任务，包括用户请求、初始状态、可能发生的事件和检查规则。
- **trace**：模型执行任务时留下的完整过程记录。
- **verifier**：自动检查任务有没有完成的程序。

你可以把 Gaia2 想成一个“模拟手机 + 个人助手任务”的考试场。模型不是写作文，而是要真的查东西、做决定、调用工具、修改状态，并被自动检查。

## ARE 是什么

ARE 全称是 Meta Agents Research Environments。

通俗地说，ARE 是一个用来搭建 agent 任务环境的平台。它负责提供：

- 模拟应用，比如 Email、Calendar、Contacts、FileSystem、Shopping。
- 初始数据，比如联系人列表、邮件历史、日历事件。
- 可调用工具，比如查邮件、查联系人、创建日历事件、修改文件。
- 动态事件，比如任务运行到一半突然来了新邮件，或者环境状态发生变化。
- verifier，用来自动判断 agent 是否真的完成任务。
- trace 记录，用来保存 agent 每一步做了什么。

普通 benchmark 往往只问：

```text
模型最后答案对不对？
```

ARE 更关心：

```text
模型是不是在正确的环境里，用正确的工具，以正确的顺序完成了任务？
```

这也是它对我们有价值的地方。因为 post-training 不只需要最终对错，还需要知道模型中间哪里做对、哪里做错。

## Gaia2 是什么

Gaia2 是基于 ARE 构建的 agent benchmark。

它测试的是 personal assistant agent 的真实工作流能力。也就是说，模型要像一个个人助手一样处理任务，而不是只回答一句自然语言。

公开数据集目前主要提供 validation split，并按能力分成 `mini`、`execution`、`search`、`adaptability`、`time`、`ambiguity` 等配置。后面第 04 章先用 `mini` 做小规模 baseline，是为了快速确认环境和 runner 能跑通。

Gaia2 里常见的任务包括：

- 查邮件，找出关键信息。
- 修改日历事件。
- 根据联系人信息发消息。
- 在多个应用之间综合信息。
- 遇到歧义时向用户追问。
- 在时间变化或新事件出现后重新调整计划。
- 在环境有噪声或工具失败时保持稳定。

一个简单例子：

```text
用户：把我和 Alex 的会议改到周五下午。

agent 需要：
1. 查联系人，确认 Alex 是谁。
2. 查日历，找到对应会议。
3. 判断“周五下午”对应哪个时间段。
4. 修改正确的日历事件。
5. 不要误改别人的会议。
6. 如果有多个 Alex 或多个会议，先向用户问清楚。
```

这个任务看起来很自然，但对模型很难。因为它需要同时做好搜索、计划、工具调用、时间推理、歧义处理和状态修改。

## 官方 OpenClaw / 官方 agent 是什么

在本项目里，我们把官方评测入口统一称为官方 OpenClaw / 官方 agent。落到公开命令上，最关键的是使用官方 ARE CLI，并选择官方默认 agent。

你可以把它理解成“官方提供的运行方式”：它负责把模型接到 Gaia2 环境里，让模型能看任务、调用工具、读取工具返回，并把整个过程记录下来。

公开命令里常见的形式是：

```bash
uvx --from meta-agents-research-environments \
  are-benchmark run \
  --hf meta-agents-research-environments/Gaia2 \
  --split validation \
  --config mini \
  --model YOUR_MODEL \
  --model_provider YOUR_MODEL_PROVIDER \
  --agent default \
  --max_concurrent_scenarios 2 \
  --scenario_timeout 300 \
  --output_dir ./runs/example_gaia2_mini
```

这里最重要的是：

```text
--agent default
```

本项目主实验不修改这个官方 agent。我们要比较的是不同模型 checkpoint：

```text
Qwen3-14B base
Qwen3-14B SFT
Qwen3-14B SFT + preference
Qwen3-14B SFT + preference + RLVR
```

这样做的好处是变量很干净。如果分数提升，主要原因应该是模型 checkpoint 变了，而不是我们改了官方 agent。

## 三者关系

可以用下面这张图理解：

```text
用户任务
  |
  v
Gaia2 scenario
  |
  v
ARE 环境
  |-- 应用数据：邮件、日历、联系人、文件
  |-- 工具 API：搜索、读取、写入、修改
  |-- 动态事件：新邮件、时间流逝、环境变化
  |-- verifier：自动检查是否完成任务
  |
  v
官方 OpenClaw / 官方 agent
  |
  v
模型 checkpoint
  |
  v
trace + verifier result + metrics
```

ARE2Train 要做的事情，是把最后这些结果整理成训练和评测闭环：

```text
trace
-> failure analysis
-> teacher trajectory
-> SFT data
-> preference data
-> RLVR reward
-> 新 checkpoint
-> 再放回同一个官方 agent 中评测
```

## 一个 scenario 里通常有什么

你可以把 scenario 理解成“一道完整的动态任务题”。

它通常包含：

- 用户请求：agent 要完成什么。
- 初始环境状态：邮件、日历、联系人、文件等内容。
- 可用工具：agent 可以调用哪些 API。
- 时间设置：当前时间是什么，任务中时间如何流动。
- 动态事件：运行过程中可能出现什么变化。
- verifier rule：最后如何判断任务是否完成。

普通问答题只需要题目和答案。Gaia2-style scenario 更像一个小型模拟世界，所以它的数据结构会复杂得多。

## trace 为什么重要

trace 是 agent 执行任务时留下的过程记录。

它可能包含：

- 用户请求。
- prompt。
- 模型输出。
- 工具调用。
- 工具返回。
- 环境状态变化。
- 错误信息。
- 延迟。
- token usage。
- verifier 结果。

如果只看最终 pass/fail，我们只能知道任务成没成功。但看 trace 后，我们能知道失败原因：

```text
是联系人找错了？
是时间推理错了？
是工具参数写错了？
是没有处理新事件？
是该问用户时没有问？
是最后答案对了，但误改了环境？
```

这对训练非常关键。因为我们不是只想知道模型弱，而是要知道它弱在哪里。

## verifier 为什么重要

verifier 是自动检查任务是否完成的程序。

它不像人工评分那样只看大概意思，而是可以检查环境里真实发生了什么。

例如，用户要求：

```text
把和 Alex 的会议改到周五下午 3 点。
```

verifier 可以检查：

- 是否找到了正确的 Alex。
- 是否修改了正确的日历事件。
- 新时间是否是周五下午 3 点。
- 是否没有误删或误改其他事件。
- 如果任务有歧义，agent 是否先向用户追问。

这就是为什么 Gaia2-style 环境适合训练。因为 verifier 的结果可以进一步变成 reward。

## Gaia2 主要评测哪些能力

结合官方资料，Gaia2 关注的能力大致可以分成几类。

### Execution

执行能力。模型能不能把一个多步骤任务真正做完。

例子：

```text
找到某个会议 -> 修改时间 -> 发消息通知相关人
```

### Search

搜索和信息整合能力。模型能不能从邮件、联系人、文件等地方找到需要的信息。

### Adaptability

适应动态变化的能力。任务运行到一半环境变了，模型能不能重新调整。

### Time

时间推理能力。模型能不能处理“明天下午”“下周五”“会议前一小时”这类表达。

### Ambiguity

歧义处理能力。信息不够时，模型是否知道先问清楚，而不是乱猜。

### Agent2Agent

多 agent 协作能力。agent 可能需要和其他模拟 agent 或应用交互。

### Noise

抗干扰能力。环境里可能有噪声、失败、无关信息或不稳定因素，模型不能被轻易带偏。

## 为什么它适合做 post-training

Gaia2-style 任务对训练有三个很有价值的特征。

第一，它不是静态问答，而是有过程。

这意味着我们能从 trace 里提取训练样本，不只是拿最终答案训练。

第二，它有 verifier。

这意味着我们可以自动过滤成功 trajectory，也可以把 verifier 结果转成 reward。

第三，它覆盖多个真实工作流能力。

这意味着训练不是只提高某一种题型，而是有机会提升工具调用、时间推理、歧义处理、动态适应等组合能力。

所以本项目的主线是：

```text
用 Gaia2-style scenarios 产生可验证交互数据
-> 用成功 trajectory 做 SFT
-> 用成功/失败对比做 preference tuning
-> 用 verifier reward 做 RLVR
-> 在官方 agent 不变的情况下评测 checkpoint
```

## 本章新增配置

本章新增：

```text
configs/are.example.yaml
```

它不是最终 runner 配置，而是帮助我们提前固定几个关键选择：

- 使用 Gaia2 数据集。
- 默认先跑 `mini` 配置。
- 使用官方 `default` agent。
- 输出到 `runs/`。
- 保存 trace 和 verifier result。

第 04 章写 baseline runner 时，会基于这个配置继续扩展。

## 资料来源

本章参考了这些公开资料：

- [Meta Research: ARE: Scaling Up Agent Environments and Evaluations](https://ai.meta.com/research/publications/are-scaling-up-agent-environments-and-evaluations/)
- [Hugging Face Blog: Gaia2 and ARE](https://huggingface.co/blog/gaia2)
- [Hugging Face Dataset: meta-agents-research-environments/gaia2](https://huggingface.co/datasets/meta-agents-research-environments/gaia2)
- [PyPI: meta-agents-research-environments](https://pypi.org/project/meta-agents-research-environments/)

## 本章完成后应该能回答

- ARE 和 Gaia2 的区别是什么？
- 为什么 Gaia2 不是普通问答数据集？
- 官方 agent 在评测里承担什么作用？
- scenario 里通常包含哪些东西？
- trace 为什么比最终答案更重要？
- verifier 为什么可以变成训练 reward？
- 本项目为什么坚持不修改官方 agent？

如果这些问题都能回答，就可以进入第 04 章：用官方 agent 跑 Qwen3-14B base checkpoint，得到 baseline。
