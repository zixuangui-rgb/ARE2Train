# 08 - Verifier 与 Reward

## 本章目标

把 verifier 输出转成可训练的 reward 信号。

## verifier 是什么

verifier 是自动检查系统。它判断 agent 是否真的完成了任务。

例如：

```text
用户要求把会议改到明天下午 3 点
verifier 检查日历中对应 event 是否真的被改到正确时间
```

## reward 是什么

reward 是训练时给模型的反馈分数。

最简单的 reward：

```text
成功 = 1
失败 = 0
```

但 agent 任务通常需要更细的 reward。

## 为什么需要 action-level reward

如果一个任务有 20 步，最后失败了，仅仅知道失败并不够。我们还想知道哪一步错了。

action-level reward 可以奖励正确的中间动作：

```text
找对联系人 +0.2
选对 calendar event +0.2
时间转换正确 +0.2
该问澄清时问了 +0.3
误改无关 event -0.5
```

## 输入

- scenario oracle。
- tool call records。
- environment final state。
- verifier result。

## 输出

- final reward。
- action-level rewards。
- reward breakdown。

## 验收标准

- 每个任务都有 final reward。
- 能解释 reward 来自哪些动作。
- reward 不鼓励投机行为。
- reward 能用于 SFT 过滤、preference 构造和 RLVR。

## 常见坑

- reward 太稀疏。
- reward 设计鼓励多余工具调用。
- 只奖励最后答案，不奖励状态修改。
- reward 和 verifier 逻辑不一致。

