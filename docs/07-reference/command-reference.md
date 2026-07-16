# 命令参考

- 初始化任务单：`python3 skill-pack/scripts/init_job.py --output job.json`
- 校验任务单：`python3 skill-pack/scripts/validate_job.py job.json`
- 渲染 Markdown：`python3 skill-pack/scripts/render_job_md.py job.json job.md`
- 合并补丁：`python3 skill-pack/scripts/merge_patch.py job.json patch.json`
- 查看工作流：`python3 skill-pack/scripts/workflow.py --help`
- 验证 Skill 包：`python3 skill-pack/scripts/validate_pack.py skill-pack`
- 验证公开仓库：`python3 scripts/validate_repository.py`

具体参数以各脚本的 `--help` 为准。先在副本和临时目录演练写操作。
