# 安装、升级与卸载

## macOS / Linux

克隆仓库后，将 `skill-pack` 复制或链接到工具规定的 Skill 目录。需要扁平入口时使用自带安装器，并先指定一个空的临时目录验证结果。

## Windows

使用 Git 克隆仓库，确保 Python 3 可用。路径参数使用 Windows 实际目录；脚本基于 `pathlib`，不依赖 Unix shell。若工具支持直接扫描嵌套 Skill，无需创建扁平入口。

## 升级

阅读 CHANGELOG，备份正在进行的任务单，先在副本上运行 schema 验证。预发布版本可能调整契约；不要用新版本脚本直接覆盖未迁移的数据。

## 卸载

删除你复制的 `short-video-operations-pack` 目录和由安装器生成且带有 managed marker 的扁平入口。安装器不会授权你删除同名非托管目录。
