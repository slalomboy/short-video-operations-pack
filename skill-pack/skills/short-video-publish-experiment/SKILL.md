---
name: short-video-publish-experiment
description: Use when reviewed short-video content needs a publish hypothesis, controlled variable, comparable conditions, metrics, stop rules, or an explicit release approval gate.
---

# Short Video Publish Experiment

## 核心原则
平台反馈是实验数据，不是玄学判决；单条结果只能形成观察，不能单独证明因果。

## 触发与边界
用于自然发布实验设计、版本对比、指标与停止条件。发布属于外部行动，本 Skill 只准备计划，默认 `pendingApproval`，不执行发布。

## 方法
1. 写清 `hypothesis` 和要回答的问题。
2. 一轮只指定一个 `primaryVariable`；其他内容形成 `comparableConditions`。
3. 选择与任务匹配的 `metric`，同时记录受众和承接质量。
4. 预先写 `stopRule`、观察窗口、样本要求和版本标识。
5. 行动前核验当前平台官方规则、内容审查和明确授权。

## 输出契约
只写 `publishExperiment`：`hypothesis`、`primaryVariable`、`comparableConditions`、`metric`、`stopRule`、规则核验、版本和 `pendingApproval`。未授权时不得写成已发布。

## 常见错误
用两条不可比视频推断因果；同时改开篇、场景、时长和受众；只看播放；先发布再补授权；把规则经验写成固定事实。
