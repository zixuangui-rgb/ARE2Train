# 005 - 仓库整理

## 目标

整理当前仓库入口和目录说明，让新读者更容易理解项目结构，也让常用检查命令更容易运行。

## 日期

2026-05-10

## 相关 commit 或 run ID

本阶段文档和脚本提交，详见 git history。

## 环境

本阶段不运行模型训练，不接入真实 OpenClaw，不下载 Qwen3-14B。

## 命令

```bash
make doctor
make smoke
make check
```

## 实现笔记

整理内容：

- 新增 `docs/README.md`，说明教程、过程记录和论文材料的阅读顺序。
- 新增 `Makefile`，提供 `doctor`、`smoke`、`test`、`bootstrap`、`check` 等常用入口。
- 更新根目录 `README.md` 的仓库结构和快速命令。
- 删除已经不需要的 `.gitkeep`，因为对应目录已经有真实文件。
- 补充 `.gitignore`，忽略常见 Python 构建产物和测试覆盖率产物。

## 观察到的结果

仓库现在有三个主要入口：

- `README.md`：项目总览。
- `docs/README.md`：文档导览。
- `Makefile`：常用命令入口。

本地存在 `.venv/` 和 `__pycache__/`，它们是运行检查脚本产生的本地文件，已经被 `.gitignore` 忽略，不会进入 git。

## 失败和修复

暂无。

## 未解决问题

- 尚未接入真实官方 OpenClaw。
- 尚未建立第 04 章需要的 baseline runner。
- 尚未定义真实 run 输出 schema。

## 下一步计划

进入第 03 章：解释 ARE/Gaia2、官方 OpenClaw、任务、工具、trace 和 verifier 的关系。
