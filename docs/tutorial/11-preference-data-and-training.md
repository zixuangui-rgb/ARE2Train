# 11 - Preference Data 与 Preference Tuning

## 本章目标

构造 success-vs-failure preference pairs，让模型更偏好正确 agent 行为。

## preference data 是什么

preference data 通常长这样：

```text
chosen: 成功轨迹
rejected: 失败轨迹
```

它告诉模型：遇到同一个任务时，哪种行为更好。

## 为什么 SFT 后还需要 preference tuning

SFT 教模型模仿成功轨迹，但不一定教会它避开坏行为。

preference tuning 可以帮助模型学会：

- 正确问澄清优于乱猜。
- 少而准的工具调用优于冗长乱试。
- 正确状态修改优于只给自然语言回答。

## 可选方法

- DPO
- ORPO
- KTO

第一版可以从 DPO 或 ORPO 开始。

## 输入

- 同一 scenario 下的成功和失败 trajectories。
- reward 或 verifier result。
- SFT checkpoint。

## 输出

- preference dataset。
- preference-tuned checkpoint。
- 对比评测报告。

## 验收标准

- preference 数据能解释 chosen 为什么比 rejected 好。
- 训练后 validation pass rate 不下降。
- tool-call error rate 或 ambiguity error 有改善。
- 与 SFT-only 做清晰对比。

## 常见坑

- chosen/rejected 差异不清楚。
- 不同任务之间随意配对。
- preference 数据只比较语言风格，不比较任务成功。
- 训练后模型变得保守，不愿调用工具。

