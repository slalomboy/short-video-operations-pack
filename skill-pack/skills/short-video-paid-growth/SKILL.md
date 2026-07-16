---
name: short-video-paid-growth
description: Use when validated organic content needs a paid-growth eligibility check, bounded budget test, funnel economics, lead-quality guardrails, or stop decision.
---

# Short Video Paid Growth

## 核心原则
付费只能放大已经验证的价值和承接，不能修复产品、内容、合规或履约问题。

## 触发与边界
用于投放资格、小预算实验、放量/停止判断和完整经济账。Skill 不授权支出，也不操作平台；默认 `pendingApproval`。

## 方法
1. 先检查自然内容、目标受众、承接路径和内容审查是否达到测试门槛。
2. 定义目标、`budgetCeiling`、主要变量、观察窗口和停止条件。
3. 沿 `funnel` 查看曝光、观看、咨询、线索、成交、支付、履约与复购。
4. 同时评估 `leadQuality`、`refunds`、`fulfillment` 和归因窗口。
5. 用 `contributionMargin` 判断经济性，计入商品、平台、优惠、广告、人力、履约和退款等增量成本。
6. 低播放成本不等于客户质量；边际回报或质量不足时停止，不因沉没成本继续。

## 输出契约
只写 `paidGrowth`：资格、目标、`budgetCeiling`、`funnel`、`leadQuality`、`refunds`、`fulfillment`、`contributionMargin`、停止规则和 `pendingApproval`。不得生成暗示已花费的记录。

## 常见错误
销售额减广告费就算利润；固定金额适用于所有账号；单条素材无限加预算；只看粉丝/互动成本；未授权即给执行指令。
