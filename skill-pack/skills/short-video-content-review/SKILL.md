---
name: short-video-content-review
description: Use when a short-video script, shot plan, or cut needs fact, evidence, rights, disclosure, privacy, clarity, platform, or conversion review before release.
---

# Short Video Content Review

## 核心原则
先判断任务、事实、人声、主体与证据，再检查呈现；每轮只修最影响理解或风险最高的一到两个变量。

## 触发与边界
用于脚本、分镜或成片审查，不用于直接重写整稿、剪辑或发布。审查通过只代表内容门通过，不代表外部行动授权。

## 方法
1. 按 `severity` 标记 blocker、major、minor、note。
2. 依次检查业务任务、事实主张、证据、权利/隐私、披露、平台时效、声音语义、主体、字幕和承接。
3. 禁止虚构场景、假顾客/假订单/假销量、未经同意的隐藏拍摄，以及把情景还原冒充真实记录。
4. 不用复杂效果修复弱内容；优先提出可重拍、可核验的动作。
5. 给出本轮一到两个变量的修订优先级，避免同时改变全部条件。

## 输出契约
只写 `review`：`severity`、问题、证据、修改动作、优先级、复核状态、是否具备 `publish-ready` 内容条件。所有待核验项进入 `reviewItems`。

## 常见错误
用“高级感”替代诊断；只查错字不查证据；忽略退款/履约承诺；把低播放归因于画面参数；审查通过后直接发布。
