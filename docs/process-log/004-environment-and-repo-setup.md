# 004 - 环境与仓库搭建

## 目标

把 ARE2Train 从文档骨架推进到可运行的最小工程环境，为后续 baseline、rollout、SFT 和 RLVR 实验准备基础设施。

## 日期

2026-05-10

## 相关 commit 或 run ID

本阶段文档和脚本提交，详见 git history。

## 环境

本阶段不运行模型训练，不接入真实 OpenClaw，不下载 Qwen3-14B。

当前目标是让仓库自身具备基础环境检查能力：

- Python 项目元信息。
- 环境配置模板。
- doctor 检查脚本。
- smoke test。
- 实验输出目录约定。

## 命令

```bash
python3 scripts/doctor.py
bash scripts/smoke_test.sh
```

可选初始化命令：

```bash
bash scripts/bootstrap_env.sh
```

## 实现笔记

新增工程文件：

- `pyproject.toml`
- `.gitignore`
- `configs/README.md`
- `configs/env.example.yaml`
- `experiments/README.md`
- `src/are2train/doctor.py`
- `scripts/doctor.py`
- `scripts/bootstrap_env.sh`
- `scripts/smoke_test.sh`
- `tests/test_doctor.py`

核心设计：

- 第 02 章不要求真实 OpenClaw 和模型服务已经可用。
- doctor 对缺失的 OpenClaw 路径、模型 endpoint 和 runs 目录给 warning，不直接失败。
- doctor 会检查评测配置是否保持官方 OpenClaw / 官方 agent 不变。
- API key 只能通过环境变量提供，不能写进配置和文档。
- `runs/`、`logs/`、`artifacts/`、`checkpoints/`、`data/` 默认不进入 git。

## 观察到的结果

仓库现在已经具备最小 smoke test。后续每章新增核心代码后，都可以把对应的最小检查接到 `scripts/smoke_test.sh` 中。

## 失败和修复

初版 `bootstrap_env.sh` 默认执行 `pip install -e .`。在当前受限网络环境里，pip 会尝试下载 build dependency，导致初始化失败。

修复方式：

- 默认不执行 editable install，只创建 `.venv` 并运行 doctor。
- 如果确实需要 editable install，再显式设置 `ARE2TRAIN_INSTALL_EDITABLE=1`。

这样第 02 章在没有网络、没有 GPU、没有 OpenClaw 的机器上也可以先完成最小环境检查。

## 未解决问题

- 尚未接入真实官方 OpenClaw。
- 尚未检查 ARE/Gaia2 数据路径。
- 尚未检查模型服务 endpoint 是否可访问。
- 尚未定义真实 baseline runner 的命令行参数。

这些问题会在第 03-04 章继续解决。

## 下一步计划

进入第 03 章：先用通俗语言解释 ARE/Gaia2、官方 OpenClaw、任务、工具、trace 和 verifier 的关系，然后再进入 baseline runner。
