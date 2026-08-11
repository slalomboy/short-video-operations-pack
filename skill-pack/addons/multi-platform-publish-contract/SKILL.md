---
name: multi-platform-publish-contract
description: Use when approved videos, covers, captions, accounts, platforms, times, authorization gates, and platform receipts must be assembled into a local publishing batch without logging in or claiming that upload means publication.
---

# Multi-Platform Publish Contract

Build and validate a portable `PublishJob` before an operator or authorized platform adapter performs any external action.

## Minimum input

Provide a unique job ID, asset-package ID and owner, plus exactly one account key, platform, video reference, cover reference, caption, authorization map, and current evidence state.

## Output

The validator returns a list of contract errors. A valid local job can reach `ready_for_operator`. `uploaded`, `submitted`, and `scheduled` remain distinct evidence states. `published_verified` requires both a public URL and the platform content ID.

## Boundary

This public add-on does not log in, upload, submit, schedule, publish, store credentials, select accounts, or call platform APIs. Asset references are portable relative references, not customer files. External actions still require explicit authorization and an account-to-asset one-to-one mapping.
