# 06 - Trace Store 与 Failure Taxonomy

## 本章目标

建立 trace 存储和失败分类体系。训练前先理解模型为什么失败。

## 为什么要分析失败

如果只知道模型错了，但不知道错在哪里，就无法设计有效训练数据和 reward。

例如，同样是失败，原因可能完全不同：

- 没有理解用户意图。
- 找错联系人。
- 时间转换错。
- tool-call parameters 填错。
- 没有处理动态事件。
- 应该问澄清却直接猜。

## 我们要做什么

- 保存所有 trace。
- 自动提取关键统计。
- 给失败任务打标签。
- 建立 failure taxonomy。

## 初始 failure taxonomy

```text
intent_error
time_reasoning_error
ambiguity_handling_error
wrong_tool
wrong_tool_parameters
missing_tool_call
unnecessary_tool_call
missed_dynamic_event
state_update_error
final_answer_error
verifier_mismatch
runtime_error
```

## 输入

- baseline traces。
- verifier result。
- tool logs。

## 输出

- failure summary。
- 按 task type 统计的错误分布。
- 典型 bad cases。

## 验收标准

- 每个失败任务至少有一个 failure_type。
- 能按 failure_type 统计数量。
- 能导出典型失败案例。
- 能把失败原因反馈到 scenario generation 和 reward design。

## 常见坑

- 只看 pass/fail，不看失败原因。
- failure_type 太粗，无法指导下一步。
- failure_type 太细，导致分析不可用。
- 没有把 bad case 和原始 trace 链接起来。
