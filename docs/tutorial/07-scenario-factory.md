# 07 - Scenario Factory：生成可训练任务

## 本章目标

构建一套生成 Gaia2-style training scenarios 的系统。

## 为什么不能直接用官方 Gaia2 训练

官方 Gaia2 应该用于 held-out evaluation。如果直接用官方测试题训练，结果会有 benchmark leakage。

所以我们需要自己生成训练任务。

## 什么是 scenario

一个 scenario 包含：

- 用户请求。
- 初始环境状态。
- 可用工具。
- 期望结果。
- oracle actions 或 verifier。

## 推荐生成方式

不要完全手写，也不要完全让 LLM 自由发挥。推荐：

```text
人设计任务模板
-> LLM 生成自然语言变体
-> 程序生成环境状态
-> 程序生成 oracle / verifier
-> 自动 sanity check
```

## 第一批任务族

```text
calendar_rescheduling
email_extraction
ambiguity_clarification
time_sensitive_task
dynamic_event_handling
contact_disambiguation
```

## 输入

- seed templates。
- 人名、时间、邮件、日历事件等数据池。
- LLM 生成器。

## 输出

```text
data/scenarios/
  train/
  validation/
  metadata.json
```

## 验收标准

- 每个 scenario 都能自动验证。
- 每个 scenario 有唯一正确目标。
- scenario 难度有 easy / medium / hard。
- scenario 覆盖多个 failure modes。

## 常见坑

- 只生成自然语言，不生成环境状态。
- scenario 无法验证。
- 任务太简单，baseline 已经全对。
- 任务太难，所有模型都失败。
- 训练集和测试集分布完全不一致。

