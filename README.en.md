# Short Video Operations Pack

[中文主入口](README.md) · [English documentation index](docs/en/README.md)

Short Video Operations Pack is an open Agent Skills suite for creators and content teams that need a repeatable way to plan, review, and learn from short-video work. It turns disconnected prompts into a shared job record with evidence, approval gates, experiments, and review.

**Current status:** `v0.1.0-alpha.3` is a fixed prerelease source version. The suite structure and deterministic checks are verified. **Next step:** install the fixed Tag, run one planning-only request, and keep publishing, spending, and live-stream actions behind explicit human approval.

## What problem does it solve?

Short-video work often breaks between positioning, topic selection, scripting, evidence, production, publishing experiments, and performance review. This suite keeps those decisions in one `ShortVideoOpsJob`, so another person or Agent can continue without rebuilding the full context.

## Install and make the first call

```bash
git clone --branch v0.1.0-alpha.3 --depth 1 https://github.com/slalomboy/short-video-operations-pack.git
cd short-video-operations-pack
python3 skill-pack/scripts/validate_pack.py skill-pack
```

Place `skill-pack/` in a Skill directory supported by your Agent runtime. For flat discovery, install managed entrypoints with:

```bash
python3 skill-pack/scripts/install_runtime_entrypoints.py skill-pack <skill-root>
```

Then ask: “Use `short-video-operations` to define positioning and propose the first topic batch for this new account. Stop at planning; do not publish.”

## Skill map and routing

The suite contains one router, [`short-video-operations`](https://github.com/slalomboy/short-video-operations-pack/tree/v0.1.0-alpha.3/skill-pack/skills/short-video-operations), and twelve specialist Skills for positioning, audience insight, materials, topics, scripts, evidence, shots, content review, publishing experiments, paid-growth decisions, live conversion, and performance review. They share one repository version and are not separate releases.

Use the router when a request crosses more than one stage or resumes an existing job. Call a specialist Skill directly when the task has one clear boundary.

## Real output

The first useful output is not a published video. It is a versioned `ShortVideoOpsJob` with the current stage, evidence gaps, owner, approval state, and `nextActions`. That record lets the workflow continue safely across people and sessions.

## Verified scope

- 13/13 Skill packages pass structural validation.
- 31/31 deterministic tests pass.
- Managed entrypoints were installed and read back in a temporary directory.

These checks do not prove account access, platform publishing, audience growth, conversion, or advertising returns.

## Limitations, privacy, and third-party boundaries

The suite does not log in to platforms, publish automatically, authorize spending, or start a live stream. `short-video-paid-growth` and `short-video-live-conversion` are bounded decision aids, not outcome guarantees. Public files exclude credentials, customer information, source videos, transcripts, and private operating data.

## License and provenance

Original code and documentation use the [Apache License 2.0](https://github.com/slalomboy/short-video-operations-pack/blob/v0.1.0-alpha.3/LICENSE), SPDX identifier `Apache-2.0`. Platform content, accounts, APIs, media, and third-party tools remain under their own terms.

Continue with the [English quick start](docs/en/quickstart.md), [usage guide](docs/en/usage.md), or [limitations](docs/en/limitations.md).
