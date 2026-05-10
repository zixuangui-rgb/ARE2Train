# 05 - Trajectory Schema：统一记录格式

## 本章目标

定义统一的 trajectory / trace 格式。后续 SFT、preference tuning、RLVR、failure analysis 都依赖这一步。

## 为什么 schema 很重要

agent 任务不是单轮问答。一次任务通常包含：

```text
用户请求
模型思考
工具调用
工具返回
环境状态变化
最终回答
verifier 结果
```

如果这些信息格式混乱，后面就很难训练和分析。

## 核心概念

### trajectory

一次完整任务执行过程。

### transition

trajectory 中的一步：

```text
state_t -> action_t -> observation_t+1 -> reward_t
```

### trace

更偏工程日志，记录模型输出、工具调用、错误和时间等信息。

## 推荐字段

```json
{
  "run_id": "...",
  "scenario_id": "...",
  "model": "...",
  "messages": [],
  "steps": [],
  "final_answer": "...",
  "verifier_result": {},
  "reward": 0.0,
  "latency_ms": 0,
  "token_usage": {},
  "failure_type": null
}
```

## 输入

- runner 输出。
- OpenClaw/ARE 原始日志。
- verifier 输出。

## 输出

- `src/are2train/schema.py`
- JSON schema 或 Pydantic models。
- trace 示例文件。

## 验收标准

- 所有 runner 都输出同一种 schema。
- schema 能表示成功和失败任务。
- schema 能表示 tool error。
- schema 能被训练数据转换脚本直接读取。

## 常见坑

- 只保存自然语言，不保存结构化 tool calls。
- 不保存时间戳。
- 不保存 prompt 版本。
- reward 和 verifier 结果混在一起，难以追踪。

