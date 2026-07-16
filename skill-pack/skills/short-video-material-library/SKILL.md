---
name: short-video-material-library
description: Use when short-video source material needs classification, provenance, rights, retrieval fields, migration notes, or reuse history.
---

# Short Video Material Library

## 核心原则
素材库不是收藏夹，而是保留来源、权利、功能和使用历史的外部记忆系统。

## 触发与边界
用于素材分类、来源整理、版权链、拆片记录、跨行业迁移和历史使用追踪。只做素材治理，不决定最终选题或公开复制研究样本。

## 方法
1. 为每条素材设置 `materialId`、`type`、`source`、日期与原作者。
2. 记录 `rights`、隐私/肖像状态、允许用途和保存限制。
3. 按选题、结构、开篇、表现、镜头、证据、承接等功能分类。
4. 写清可迁移机制、不可复制事实、适用条件和风险。
5. 每次使用追加 `usageHistory`、版本和结果，不覆盖旧记录。

禁止直接复制、去水印丢来源、逐句换词；跨行业迁移必须重新核验事实、用户、证据和权利，不能只替换名词。

## 输出契约
只写 `materials`：记录数组、分类索引、权利状态、迁移说明、风险、`usageHistory`。权利不明进入 `reviewItems`。

## 常见错误
以收藏数量衡量能力；用单个爆款证明机制；把公开可见误认为可自由使用；清理素材时丢失旧版本和引用链。
