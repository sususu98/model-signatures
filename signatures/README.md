# Signatures

This directory contains metadata-only observations grouped by model family and trusted endpoint
surface.

Published endpoint buckets:

- `claude/anthropic`
- `claude/aws-bedrock`
- `claude/azure`
- `claude/vertex`
- `claude/claude-code`
- `gpt/openai`
- `gpt/azure-openai`
- `gpt/codex`
- `gemini/aistudio`
- `gemini/vertex`
- `gemini/antigravity`
- `gemini/gemini-cli`
- `grok/xai`

Do not add local gateway names, filename-derived buckets, or unverified routing labels here. Keep
those in `internal/` until a direct endpoint source is credible enough to publish.
