# 配置目录

这个目录保存项目的配置模板。

配置文件的目标不是把所有内容一次写死，而是把后续实验中最容易出错的东西明确下来：

- 路径在哪里。
- 用哪个模型。
- 用哪个评测任务。
- 是否保存 trace。
- 是否允许使用官方 held-out tasks。
- 是否修改官方 agent。

## 当前文件

- `env.example.yaml`：本地和服务器都可以参考的环境配置模板。
- `eval/`：不同 checkpoint 的评测配置模板。

## 重要规则

- API key 只能通过环境变量提供，不能写进配置文件。
- `configs/env.local.yaml` 和 `configs/env.cluster.yaml` 是本机私有配置，默认不会进入 git。
- 主实验不修改官方 OpenClaw / 官方 agent，只替换模型 checkpoint。
- 重要 run 开始前，需要把实际使用的配置复制到 run 目录，作为结果复现依据。
