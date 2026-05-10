# 09 - Teacher Trajectories：用强模型生成训练 trajectory

## 本章目标

用强模型在自建 scenarios 上生成高质量 trajectories，并用 verifier 过滤。

## 为什么需要 teacher trajectories

中小模型一开始可能不会稳定使用工具。直接做 RL 成本高、噪声大。

更稳妥的做法是：

```text
先让强模型尝试任务
-> 保留成功的 trajectory
-> 让小模型模仿
```

## teacher 可以是谁

- GPT-5.5 / Claude / Kimi / MiniMax 等 API 模型。
- 更大的开源模型。
- multi-agent teacher 系统。

## 我们要保存什么

- 成功的 trajectory。
- 失败的 trajectory。
- verifier result。
- reward breakdown。
- token 和延迟。

## 输入

- training scenarios。
- teacher model endpoint。
- rollout runner。
- verifier。

## 输出

```text
data/trajectories/teacher/
  success/
  failure/
  summary.json
```

## 验收标准

- 每个 scenario 采样多条 rollouts。
- 成功的 trajectory 通过 verifier。
- 失败的 trajectory 保留用于 preference 和 failure analysis。
- teacher prompt 和版本被记录。

## 常见坑

- 不过滤失败的 trajectory 就拿去 SFT。
- teacher trajectory 过长，容易让小模型学会冗长低效的行为。
- teacher 使用了测试题。
- 没有记录 teacher 模型版本。
