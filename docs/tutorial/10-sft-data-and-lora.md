# 10 - SFT / LoRA：先让模型学会正确 trajectory

## 本章目标

把通过 verifier 检查的成功的 trajectory 转成 SFT 数据，并用 LoRA 训练 Qwen3-14B。

## SFT 是什么

SFT 是 supervised fine-tuning。简单说，就是给模型看正确示范，让它模仿。

在 ARE2Train 中，正确示范不是普通问答，而是包含工具调用过程的 trajectory。

## LoRA 是什么

LoRA 是一种高效训练方法。它不更新模型所有参数，而是在部分层上训练小矩阵，降低显存和训练成本。

## 我们要做什么

- 把成功的 trajectory 转成训练样本。
- 控制上下文长度。
- 保留工具调用格式。
- 训练 LoRA adapter。
- 在 validation scenarios 上评测。

## 输入

- 通过 verifier 检查的成功的 trajectory。
- Qwen3-14B。
- tokenizer 和 chat template。
- 训练配置。

## 输出

- SFT 数据集。
- LoRA checkpoint。
- validation report。

## 验收标准

- SFT 后工具调用格式的错误率下降。
- validation pass rate 高于 baseline。
- 没有明显过拟合训练 scenarios。
- 训练配置和 checkpoint 可复现。

## 常见坑

- 把失败的 trajectory 当作成功样本训练。
- 打乱 trajectory，导致上下文断裂。
- 忽略工具调用的结构化格式。
- 只看训练 loss，不跑任务评测。
