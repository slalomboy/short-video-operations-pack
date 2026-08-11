# Usage

[中文主入口](../../README.md) · [English docs](README.md)

## Choose the entrypoint

- Use `short-video-operations` when the task spans multiple stages or resumes an existing job.
- Use one specialist Skill when the request has a single clear output, such as account positioning, evidence planning, or content review.

## Shared job contract

All Skills read and update the same `ShortVideoOpsJob`. The job stores its version, current stage, evidence, approvals, owner, and next actions. Do not replace the full job with an informal summary when handing work to another Agent.

## Example flow

1. Run positioning and audience analysis.
2. Generate and score topic candidates.
3. Build a script and evidence plan.
4. Stop at the relevant human approval gate.
5. Continue with shots, review, a controlled publishing experiment, or performance review only after the required input exists.

Publishing, paid media, and live-stream operations are never authorized by a planning output.
