---
name: short-video-evidence-planning
description: Use when a script contains material claims, comparisons, demonstrations, results, disclosures, or evidence gaps that affect production readiness.
---

# Short Video Evidence Planning

## 核心原则
每个重要主张只有五种处理：事实、可观察过程、公平比较、有限结果或删除。

## 触发与边界
用于主张—证据映射、产品演示、案例、测评、知识结论、结果表达和披露规划。不负责制造证据，也不把联想画面、音乐或个人感觉当事实证明。

## 方法
1. 从脚本逐项抽取主张并标注事实、观点、经历、推断或行动建议。
2. 指定证据类型、来源、权利、条件、比较基准和限制。
3. 对比必须条件公平；结果只能表达样本和适用范围内的有限结果。
4. 无证据、来源冲突、权利不明或高风险主张进入 `reviewItems`，选择补证、降级或删除。
5. 所有重要缺口关闭前，不得标记 `production-ready`。

## 输出契约
只写 `evidence`：`claims`、证据类型、来源、条件、限制、权利、披露、缺口和处理决定。只返回补丁，不修改脚本原文。

## 常见错误
用商家详情页当独立证据；只展示成功结果；用不公平演示制造反差；免责声明替代核验；缺证据仍进入制作。
