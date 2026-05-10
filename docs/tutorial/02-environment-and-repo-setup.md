# 02 - 环境与仓库搭建

## 本章目标

这一章搭建项目的工程基础。目标不是立刻训练模型，而是让后续每一步都能可复现地运行。

## 为什么环境搭建很重要

agentic RL 项目会同时涉及：

- ARE/Gaia2 环境。
- OpenClaw 或其他 agent runtime。
- 本地模型服务。
- teacher API 模型。
- rollout runner。
- 训练框架。
- 评测脚本。

如果版本和配置不固定，后面很难判断分数变化是模型变强，还是环境变了。

## 我们要做什么

- 固定 Python 版本。
- 固定依赖。
- 固定 ARE/Gaia2 commit。
- 固定模型服务方式。
- 建立 configs 目录。
- 建立 logs / runs / experiments 约定。

## 输入

- 项目仓库。
- 本地开发机。
- 训练服务器。
- Docker / conda / uv / pip 等环境管理工具。

## 输出

- 可复现的安装脚本。
- 环境检查脚本。
- 第一版 `configs/`。
- 第一版 `scripts/doctor.py` 或 smoke test。

## 最小验收标准

```text
1. 新机器能按 README 安装环境。
2. 能运行 smoke test。
3. 能打印当前依赖、模型服务地址、ARE/Gaia2 路径。
4. 能发现缺失依赖并给出明确错误信息。
```

## 推荐目录

```text
configs/
  env.local.yaml
  env.cluster.yaml
scripts/
  bootstrap_env.sh
  doctor.py
experiments/
  README.md
```

## 常见坑

- 没有固定依赖版本。
- 本地和服务器路径写死。
- API key 写进代码或日志。
- Docker 镜像更新后结果不可复现。
