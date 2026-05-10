# 02 - 环境与仓库搭建

## 这一章能带来什么

这一章会让项目从“有想法和文档”变成“可以在机器上稳定运行的工程”。

它不会训练模型，也不会报告 ARE/Gaia2 分数。它要解决的是另一个更基础的问题：

> 以后每一次实验，都能不能在同一套规则下重新跑出来？

很多训练项目最后失败，不是因为模型训练本身太难，而是因为环境一开始没有管好。比如本地能跑，服务器不能跑；今天能跑，下周依赖版本变了就不能跑；分数变了，但不知道是模型变强了，还是配置变了。

完成这一章之后，你会得到：

- 一个标准 Python 项目结构。
- 一个环境配置模板。
- 一个 `doctor` 检查脚本。
- 一个 smoke test。
- 一套实验输出目录约定。
- 一份过程记录，说明这一章做了什么。

简单说，这一章是在给后面的 baseline、rollout、SFT 和 RLVR 准备地基。

## 本章目标

本章目标是搭建最小可用工程环境。

“最小可用”不是说以后只能做到这里，而是先保证仓库具备这些能力：

- 新机器 clone 仓库后，知道怎么初始化环境。
- 可以一条命令检查当前环境是否基本正确。
- 可以发现常见错误，比如目录缺失、配置不一致、API key 被写进文件。
- 后续实验有固定的输出位置和记录方式。

这一章结束后，我们还不会接入真实 OpenClaw，也不会下载 Qwen3-14B。原因是这些步骤依赖更重，适合放到后面的 baseline 章节里做。第 02 章先把项目自身的工程框架跑通。

## 需要先懂什么

如果你是初学者，只需要理解下面几个概念：

- **仓库**：保存代码、文档和配置的项目文件夹。
- **环境**：代码运行时依赖的 Python 版本、库、路径和外部服务。
- **配置文件**：把容易变化的参数写到文件里，而不是写死在代码里。
- **smoke test**：很小的测试，用来快速判断项目是不是基本能跑。
- **API key**：调用外部模型服务的密钥，不能写进 git。

如果这些词还不熟，也没关系。你可以先记住一句话：环境搭建的目标是让项目“换一台机器也能照着跑”。

## 为什么环境搭建很重要

agentic RL 项目会同时涉及：

- ARE/Gaia2 环境。
- 官方 OpenClaw / 官方 agent。
- 本地模型服务。
- teacher API 模型。
- rollout runner。
- 训练框架。
- 评测脚本。

如果版本和配置不固定，后面很难判断分数变化是模型变强，还是环境变了。

本项目尤其要注意一点：**主实验不修改官方 OpenClaw / 官方 agent，只替换模型 checkpoint**。所以环境检查里也会检查评测配置是否保持了这个规则。

## 我们要做什么

本章会完成六件事。

### 1. 固定 Python 项目结构

我们先加入 `pyproject.toml`，说明这个仓库是一个 Python 项目，并要求 Python 版本不低于 3.11。

后续为什么用 Python？因为 ARE/Gaia2、训练数据处理、trace 分析、评测统计和很多训练框架都很容易和 Python 集成。

### 2. 建立环境配置模板

我们新增：

```text
configs/env.example.yaml
```

这个文件不是直接运行的最终配置，而是告诉使用者：哪些路径和服务需要配置。

真正本机使用时，可以复制成：

```text
configs/env.local.yaml
```

`env.local.yaml` 不进入 git，因为它可能包含你的本机路径。API key 也不能写进去，只能通过环境变量传入。

### 3. 建立 doctor 检查脚本

我们新增：

```text
scripts/doctor.py
src/are2train/doctor.py
```

doctor 的作用类似体检。它会检查：

- Python 版本是否满足要求。
- 必要目录是否存在。
- 评测配置是否保持“不改官方 agent”。
- 文档和配置里有没有明显的 API key 泄漏。
- 常用环境变量是否已经设置。

这里要注意：没有设置 OpenClaw 路径或模型服务地址时，doctor 只会给 warning，不会直接失败。因为第 02 章还没有正式跑 baseline。

### 4. 建立 smoke test

我们新增：

```text
scripts/smoke_test.sh
tests/test_doctor.py
```

smoke test 的目标不是证明模型能力，而是快速确认项目没有明显损坏。

现在的 smoke test 会运行 doctor，并跑一个最小单元测试。后面每新增一个核心模块，都可以把最小检查加到 smoke test 里。

### 5. 建立实验输出约定

我们新增：

```text
experiments/README.md
```

它规定后续每次实验应该记录什么，比如：

- 用了哪个 checkpoint。
- 用了哪个配置。
- 命令是什么。
- trace 存在哪里。
- verifier 结果是什么。
- metrics 和 failure analysis 在哪里。

这些记录后面会非常重要。因为论文和申请项目都不只看“你跑出了一个分数”，还会看这个分数是否可复现、可解释。

### 6. 加入 `.gitignore`

我们新增 `.gitignore`，避免把这些内容误提交：

- `.venv/`
- `runs/`
- `logs/`
- `artifacts/`
- `checkpoints/`
- `data/`
- 本机私有配置和 `.env`

这些文件可能很大，也可能包含敏感信息，不应该进入 git。

## 输入

- 项目仓库。
- 本地开发机。
- 训练服务器。
- Python 3.11 或更高版本。
- 后续会用到的 OpenClaw、模型服务和训练服务器信息。

## 输出

- `pyproject.toml`
- `.gitignore`
- `configs/env.example.yaml`
- `configs/README.md`
- `experiments/README.md`
- `src/are2train/doctor.py`
- `scripts/doctor.py`
- `scripts/bootstrap_env.sh`
- `scripts/smoke_test.sh`
- `tests/test_doctor.py`
- `docs/process-log/004-environment-and-repo-setup.md`

## 如何使用

### 第一步：运行 doctor

在仓库根目录运行：

```bash
python3 scripts/doctor.py
```

你会看到类似这样的输出：

```text
[OK] python: Python 3.x.x
[OK] directories: all required directories exist
[OK] eval_configs: all eval configs keep official OpenClaw / official agent unchanged
[OK] secrets: no obvious API key pattern in tracked text files
[WARN] optional_env: not set yet: ARE2TRAIN_OPENCLAW_HOME, ARE2TRAIN_MODEL_ENDPOINT, ARE2TRAIN_RUNS_DIR
```

这里的 warning 是正常的。它表示你还没有配置 OpenClaw 路径、模型服务地址和 runs 目录。第 02 章不要求这些都配置好。

### 第二步：运行 smoke test

```bash
bash scripts/smoke_test.sh
```

如果 smoke test 通过，说明仓库最基础的工程检查是好的。

### 第三步：创建本机配置

复制环境模板：

```bash
cp configs/env.example.yaml configs/env.local.yaml
```

然后在 `configs/env.local.yaml` 里填写本机路径。

注意：不要把 API key 写进这个文件。正确做法是在 shell 里设置环境变量：

```bash
export TEACHER_API_KEY=...
```

后续如果用 DeepSeek、OpenAI、DashScope 等 teacher model，也应该用环境变量，而不是写进配置文件。

### 第四步：可选，创建虚拟环境

如果你希望项目依赖和系统 Python 隔离，可以运行：

```bash
bash scripts/bootstrap_env.sh
```

它会创建 `.venv/`，并运行 doctor。

默认情况下，它不会执行 `pip install -e .`。这样做是为了避免在断网环境或训练服务器上，因为 pip 下载依赖失败而卡住。当前第 02 章没有外部 Python 依赖，所以不安装也能完成检查。

如果你确实想把当前项目安装进虚拟环境，可以运行：

```bash
ARE2TRAIN_INSTALL_EDITABLE=1 bash scripts/bootstrap_env.sh
```

如果你已经在 conda、uv 或服务器镜像里管理 Python，也可以不用这个脚本。关键是最终能运行：

```bash
python3 scripts/doctor.py
```

## 本章新增文件怎么理解

### `pyproject.toml`

这是 Python 项目的说明文件。

它告诉工具：

- 项目名字叫 `are2train`。
- Python 版本至少是 3.11。
- 代码包在 `src/` 下面。
- 安装后可以使用 `are2train-doctor` 这个命令。

### `configs/env.example.yaml`

这是环境配置模板。

它不保存真实 API key，只保存“应该从哪个环境变量读取 key”。这样做更安全，也更适合开源。

### `src/are2train/doctor.py`

这是核心检查逻辑。

它目前做的是基础检查，后面可以继续扩展。例如第 04 章接入 OpenClaw 后，可以让 doctor 检查 OpenClaw 是否存在、版本是否正确、模型 endpoint 是否可访问。

### `scripts/doctor.py`

这是给使用者直接运行的入口。

初学者不需要理解 Python package import 细节，只要运行：

```bash
python3 scripts/doctor.py
```

### `scripts/smoke_test.sh`

这是最小测试入口。

后面每次改代码前后，都可以先跑它，确认没有破坏基础功能。

### `experiments/README.md`

这是实验记录规范。

它告诉我们每次 run 应该保存什么。后面做 baseline、SFT、RLVR 时，都要按这个约定整理结果。

## 本章和正式实验的关系

第 02 章本身不产生模型分数。

它产生的是后续实验必须依赖的工程能力：

- 能检查环境。
- 能检查配置边界。
- 能避免 API key 泄漏。
- 能定义 run 目录结构。
- 能让别人复现实验。

没有这一步，后面就算跑出了 ARE/Gaia2 分数，也很难说服别人相信这个结果。

## 最小验收标准

```text
1. 新机器能按 README 安装环境。
2. 能运行 smoke test。
3. 能检查 Python 版本、目录结构和评测配置。
4. 能发现明显的 API key 泄漏。
5. 没有把本机私有配置、日志、runs、checkpoints 提交进 git。
```

## 推荐实验目录

```text
runs/
  YYYYMMDD_method_model_seed/
    config.snapshot.yaml
    command.txt
    environment.txt
    traces/
    verifier_results.jsonl
    metrics.json
    failure_analysis.md
```

这里的 `runs/` 不进入 git。真正需要公开的是整理后的指标、图表、失败分析和复现实验说明。

## 常见坑

- 没有固定依赖版本。
- 本地和服务器路径写死。
- API key 写进代码或日志。
- Docker 镜像更新后结果不可复现。
- 把 `runs/`、`checkpoints/`、`data/` 这类大文件目录提交进 git。
- doctor 有 warning 就误以为项目坏了。warning 表示“后面正式运行前需要补齐”，不是当前阶段失败。

## 本章完成后应该能回答

- 这个项目最低需要什么 Python 版本？
- 为什么不能把 API key 写进配置文件？
- doctor 检查了哪些内容？
- smoke test 和正式评测有什么区别？
- `configs/env.example.yaml` 和 `configs/env.local.yaml` 有什么区别？
- 后续实验输出应该放在哪里？
- 为什么第 02 章不直接跑 ARE/Gaia2 分数？

如果这些问题都能回答，就可以进入下一章：先理解 ARE/Gaia2 和官方 OpenClaw 的任务形态，然后再进入 baseline runner。
