# Model Signatures

This repository collects observable signatures for LLM model families and client surfaces.

Current scope:

- Claude
  - API
  - Claude Code
- GPT
  - API
  - Codex
- Gemini
  - AI Studio
  - Vertex AI
  - Antigravity
  - Gemini CLI

The goal is to keep the data small, reviewable, and safe to publish. Do not commit API keys,
authorization headers, cookies, private prompts, user content, or raw logs that may contain
secrets.

## Layout

```text
signatures/
  claude/
    api/
      signatures.json
    claude-code/
      signatures.json
  gpt/
    api/
      signatures.json
    codex/
      signatures.json
  gemini/
    aistudio/
      signatures.json
    vertex/
      signatures.json
    antigravity/
      signatures.json
    gemini-cli/
      signatures.json
schemas/
  signature.schema.json
```

## Entry Format

Each `signatures.json` file is an array of entries matching
[`schemas/signature.schema.json`](schemas/signature.schema.json).

Minimal example:

```json
{
  "provider": "claude",
  "source": "api",
  "model": "claude-example-model",
  "signature_type": "response_shape",
  "signature": {
    "example_key": "example_value"
  },
  "evidence": {
    "captured_from": "redacted request/response sample",
    "notes": "Only non-sensitive fields are included."
  },
  "observed_at": "2026-05-27T00:00:00Z",
  "redactions": ["authorization", "user_content"]
}
```

## Validate

Basic JSON validation:

```bash
jq empty signatures/**/*.json schemas/*.json
```
