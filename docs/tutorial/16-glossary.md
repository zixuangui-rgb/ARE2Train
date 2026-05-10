# 16 - 术语表

## 本章目标

帮助基础较弱的读者快速查阅本项目中反复出现的术语。

## agent

能根据目标采取行动的模型系统。它不只是生成文字，还可能调用工具、读取环境、修改状态、等待反馈。

## agent scaffold

包在模型外面的工作流程。它负责组织 prompt、工具调用、工具返回、停止条件、错误处理和 trace 记录。

模型负责生成下一步动作，agent scaffold 负责把这一步动作接到真实环境里执行。

如果只改 scaffold，模型参数没有变；如果做 SFT 或 RLVR，模型本身才发生了训练变化。实验里必须区分这两种提升。

## benchmark

用于评测模型能力的任务集合。benchmark 主要回答“模型现在有多强”。

## training environment

用于训练模型的环境。它不只是打分，还能提供 trajectory、反馈和 reward。

## scenario

一个完整任务场景，包括用户请求、初始状态、可用工具和 verifier rule。

## rollout

模型在一个 scenario 中实际执行一次任务的过程。

## trajectory

一次 rollout 的完整记录，包含每一步 state、action、observation 和结果。

## trace

偏工程日志的记录，包含 prompt、模型输出、工具调用、错误、时间、token 等信息。

## verifier

自动检查 agent 是否完成任务的程序。

## reward

训练时给模型的反馈分数。reward 越高，表示行为越应该被强化。

## RLVR

Reinforcement Learning from Verifiable Rewards。使用 verifier 可以自动检查的 reward 做强化学习。

## GRPO

一种大模型强化学习方法，常用于同一任务采样多条输出后做相对比较。

## SFT

Supervised Fine-Tuning。用正确示范训练模型模仿。

## LoRA

一种高效 fine-tuning 方法，只训练少量新增参数，降低显存和算力需求。

## preference data

preference data 通常包含一条更好的回答或 trajectory，以及一条较差的回答或 trajectory。

## held-out evaluation

把一批任务完全留到最终测试阶段，不参与训练和调参。

## benchmark leakage

benchmark leakage 指测试集内容进入训练过程，导致评测结果不可信。
