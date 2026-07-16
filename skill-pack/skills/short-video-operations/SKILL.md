---
name: short-video-operations
description: Use when a request needs an end-to-end short-video operations plan, coordinated specialist decisions, or continuation from an existing ShortVideoOpsJob.
---

# Short Video Operations

## 总则
把短视频当作从定位、内容、证据、制作、实验到履约复盘的经营系统。JSON 任务单是事实源；本 Skill 只负责路由、状态、门槛和补丁合并。

## 何时使用
- “帮我做一套短视频运营方案”“从定位到复盘跑完整流程”。
- 用户说“继续这个短视频任务单”或提供 `ShortVideoOpsJob`。
- 一个请求跨越两个以上专业环节，需要统一依赖、状态与授权。

不用于只润色口播或“只帮我改这段文案”；交给 `content-voiceover-copywriter`。不用于“剪掉口误”或直接剪片；交给 `talking-head-video-production` 或 `video-use`。总控不得代替这些专业能力。

## 执行顺序
1. 读取 `../../shared/short-video-ops-job.schema.json`、字段所有权和公共规则。
2. 读取或新建任务单，识别当前入口阶段；JSON 优先于 Markdown。
3. 检查必需字段、证据、规则时效和授权，不确定项写入 `reviewItems`。
4. 按 `references/routing.md` 选择能完成目标的最小 Skill 链，不机械跑全流程。
5. 仅合并版本匹配且符合字段所有权的补丁；每次合并后重新验证并刷新 Markdown。
6. 缺证据、规则过期、结论冲突或外部行动未授权时停止，按 `references/state-and-gates.md` 标记状态。
7. 返回当前状态、已产出物、缺口、下一动作和授权门，不把计划描述成已执行。

## 输出契约
- 路由：按依赖顺序列出 Skill 名和理由。
- 补丁：`jobId`、`baseVersion`、`skill`、`writes`、`reviewItems`。
- 总控只写 `meta`、`governance`、`nextActions`。
- 发布、支出、开播、全局安装和外部写入均保持 `pendingApproval`，直到获得明确授权。

## 常见错误
- 用户只要单项服务却启动整包。
- Markdown 与 JSON 冲突时修改 Markdown。
- 用单条数据改长期定位或规则。
- 把审查通过当作发布授权。
