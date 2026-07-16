# 5 分钟快速开始

## 1. 安装

把仓库中的 `skill-pack/` 放进 Agent 工具可读取的 Skill 目录。若运行时只发现扁平目录，可执行：`python3 skill-pack/scripts/install_runtime_entrypoints.py skill-pack <你的 Skill 根目录>`。先在临时目录演练，不要覆盖同名非托管 Skill。

## 2. 新建任务单

执行：`python3 skill-pack/scripts/init_job.py --output my-job.json`。随后用 `python3 skill-pack/scripts/validate_job.py my-job.json` 检查。

## 3. 发出第一个请求

“使用 `short-video-operations`。目标是为一个面向初学者的家庭收纳账号建立定位并产生 10 个首发选题。只做分析和计划，不发布，不投放。所有未知信息写入 reviewItems。”

## 4. 看懂输出

重点检查路由顺序、每个结论的证据、`reviewItems`、`nextActions` 和授权状态。若输出补丁，先验证 `baseVersion`，再合并；不要直接手改 Markdown 视图。

## 5. 继续任务

下次提供更新后的 JSON 并说“继续这个任务单”。总控会从当前状态开始，不会机械重跑全部 13 个 Skill。
