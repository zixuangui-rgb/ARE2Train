# 15 - 论文、教程与开源发布

## 本章目标

把工程结果整理成论文、教程和可复现开源项目。

## 论文要讲清楚什么

论文不是项目日志。它需要清楚回答：

- 问题是什么？
- 现有方法缺什么？
- 我们的方法是什么？
- 为什么方法有效？
- 实验如何证明？
- 局限性是什么？

## 初始论文结构

```text
1. Introduction
2. Related Work
3. ARE2Train Framework
4. Scenario Generation
5. Trace and Reward Design
6. Training Methods
7. Experiments
8. Analysis
9. Limitations
10. Conclusion
```

## 教程要讲清楚什么

教程面向学习者，需要更关注：

- 每一步为什么做。
- 如何复现。
- 常见错误。
- 如何调试。
- 读者应该看到什么结果。

## 开源发布要包含什么

- README。
- 安装说明。
- 最小可运行 demo。
- 数据生成脚本。
- baseline runner。
- 训练脚本。
- evaluation 脚本。
- 示例结果。
- 许可证和引用格式。

## 输入

- 完整实验结果。
- process logs。
- figures 和 tables。
- 代码和配置。

## 输出

- paper draft。
- tutorial chapters。
- release checklist。
- reproducibility package。

## 验收标准

- 论文中的每个数字都能追溯到 run ID。
- 教程中的每条命令都实际跑过。
- 开源仓库能让别人跑通最小 demo。
- 没有泄露私有 API key 或受限数据。

## 常见坑

- 只写结果，不写失败和局限。
- 论文 claim 超过实验能支持的范围。
- 教程命令不可运行。
- 开源仓库缺少最小 demo。

