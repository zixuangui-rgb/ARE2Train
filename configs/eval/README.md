# 评测配置说明

这个目录存放 ARE2Train 的评测配置模板。

这些文件现在还不是可直接运行的完整 runner 配置。它们的作用是先固定实验意图：评测哪个模型、处在哪个训练阶段、使用什么数据边界、记录哪些指标。

## 文件说明

- `baseline.yaml`：原始 Qwen3-14B 和基础 agent scaffold 的评测模板。
- `sft.yaml`：SFT 后模型的评测模板。
- `preference.yaml`：SFT + preference tuning 后模型的评测模板。
- `rlvr.yaml`：SFT + preference tuning + RLVR/GRPO 后模型的评测模板。
- `teacher.yaml`：强 teacher model 的参考线评测模板。

## 固定规则

- `final_test` 必须指向官方 ARE/Gaia2 held-out tasks。
- `development` 使用自建 validation scenarios。
- 官方 held-out tasks 不能用于训练、调参或 checkpoint 选择。
- 每次评测都必须保存 trace、verifier result 和 failure analysis。

后续实现 runner 时，代码应该读取这些配置，并把实际 run 的完整配置复制到输出目录中。
