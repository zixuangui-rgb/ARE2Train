# 12 - RLVR / GRPO：用 verifier reward 训练

## 本章目标

在 SFT checkpoint 基础上，使用 verifier reward 做 RLVR / GRPO。

## RLVR 是什么

RLVR 是 reinforcement learning from verifiable rewards。意思是用 verifier 可以自动检查的结果作为 reward。

在 ARE2Train 中，verifier 能检查 agent 是否正确完成任务，因此可以作为 reward 来源。

## GRPO 是什么

GRPO 是一种常用于大模型 RL 的方法。它通常会对同一个问题采样多条输出，然后比较它们的相对好坏。

通俗理解：

```text
同一个 scenario 采样多条 trajectories
-> verifier 给每条打分
-> 好的 trajectory 被强化，差的 trajectory 被压低
```

## 为什么不要一开始就做 RL

原始模型如果连 tool-call format 都不稳定，RL 会很难训练。推荐顺序是：

```text
baseline
-> SFT
-> preference tuning
-> RLVR / GRPO
```

## 输入

- SFT 或 preference checkpoint。
- training scenarios。
- verifier reward。
- rollout engine。
- RL 框架，例如 verl / OpenRLHF / 自定义轻量实现。

## 输出

- RL checkpoint。
- reward curve。
- validation report。
- failure analysis。

## 验收标准

- RL 后 held-out validation 有提升。
- 没有明显 reward hacking。
- tool-call error 没有恶化。
- 与 SFT-only、preference-only 做对比。

## 常见坑

- reward 太稀疏，训练信号很弱。
- rollout 成本过高。
- 模型学会利用 verifier 漏洞。
- KL 约束太弱导致模型漂移。
- 只看 reward curve，不跑真实任务评测。
