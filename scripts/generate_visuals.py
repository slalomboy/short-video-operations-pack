#!/usr/bin/env python3
"""Regenerate the five core SVG illustrations without external dependencies."""

from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
SPECS = {
    "operations-loop.svg": ("短视频运营闭环", "从定位到复盘，经验持续回流", ["定位与受众", "素材与选题", "脚本与证据", "拍摄与审查", "实验与增长", "复盘与回流"]),
    "capability-map.svg": ("能力地图", "13 个 Skill 覆盖四层经营问题", ["战略层", "内容层", "执行层", "增长层"]),
    "orchestrator-specialists.svg": ("总控 + 专业 Skill", "总控路由，专家判断，共享任务单协作", ["目标与状态", "最小 Skill 链", "专业补丁", "验证与下一步"]),
    "shared-job.svg": ("共享任务单", "JSON 是事实源，Markdown 是阅读视图", ["任务身份", "版本控制", "字段所有权", "证据与缺口", "权限状态", "下一动作"]),
    "approval-gates.svg": ("人工权限门", "有现实影响的动作必须明确授权", ["发布内容", "支付预算", "开始直播", "全局安装", "外部写入"]),
}


def render(title: str, subtitle: str, items: list[str]) -> str:
    boxes = []
    for index, item in enumerate(items):
        row, col = divmod(index, 3)
        x, y = 70 + col * 370, 250 + row * 115
        boxes.append(f'<rect x="{x}" y="{y}" width="330" height="78" rx="18" fill="#182338" stroke="#33445f"/><text x="{x+165}" y="{y+48}" text-anchor="middle" fill="#f7f2e8" font-size="24">{item}</text>')
    return f'<svg xmlns="http://www.w3.org/2000/svg" width="1200" height="675" viewBox="0 0 1200 675" role="img" aria-label="{title}"><rect width="1200" height="675" fill="#0b1220"/><circle cx="1080" cy="90" r="160" fill="#ff6b35" opacity=".13"/><text x="70" y="95" fill="#ff6b35" font-size="24" font-weight="700">SHORT VIDEO OPS</text><text x="70" y="158" fill="#f7f2e8" font-size="46" font-weight="800">{title}</text><text x="70" y="200" fill="#a8b3c7" font-size="22">{subtitle}</text>{"".join(boxes)}</svg>'


if __name__ == "__main__":
    target = ROOT / "assets" / "illustrations"
    target.mkdir(parents=True, exist_ok=True)
    for filename, spec in SPECS.items():
        (target / filename).write_text(render(*spec) + "\n", encoding="utf-8")
    print(f"generated {len(SPECS)} illustrations")
