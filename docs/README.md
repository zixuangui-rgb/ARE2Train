# 文档导览

这个目录保存 ARE2Train 的教程、过程记录和论文材料。

如果你是第一次打开这个项目，建议按下面顺序阅读。

## 推荐阅读顺序

1. `../README.md`
   - 先看项目目标、实验边界和整体路线。

2. `tutorial/README.md`
   - 看完整教程目录，知道每一章要解决什么问题。

3. `tutorial/00-overview-learning-path.md`
   - 从整体上理解 ARE2Train 的学习路径。

4. `tutorial/01-research-question-and-protocol.md`
   - 先明确研究问题、数据边界和最终评测规则。

5. `tutorial/02-environment-and-repo-setup.md`
   - 再搭建最小工程环境，运行 doctor 和 smoke test。

6. `paper/evaluation-protocol.md`
   - 需要写论文或设计正式实验时，回到这里看正式协议。

## 目录说明

```text
docs/
├── tutorial/       # 面向学习者的教程章节
├── process-log/    # 每个阶段的原始过程记录
└── paper/          # 论文协议、草稿、实验表格和笔记
```

## 写作原则

- 教程面向基础较弱的读者，先讲目标，再讲步骤。
- 过程记录保留真实命令、失败和修复，不只写成功结果。
- 论文材料更正式，服务于实验 claim 和可复现性。
- 主实验不修改官方 OpenClaw / 官方 agent，只替换模型 checkpoint。
