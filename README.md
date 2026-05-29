# Model Signature Features

[中文](README_CN.md)

This repository publishes metadata-only, observable outer-format features for reasoning-continuity
signatures emitted by Claude, GPT, Gemini, and Grok-family endpoints.

It is a feature catalog, not a capture pipeline or runtime integration database. Raw signature
values, prompts, tool arguments, request IDs, credentials, and private logs do not belong in the
public catalog.

## Published Layout

```text
features/
  signature-features.json        # family-level feature records and observed outer markers
signatures/
  claude/
  gpt/
  gemini/
  grok/                          # metadata-only observations by trusted endpoint family
schemas/
  signature.schema.json
  signature-features.schema.json
docs/
  signature-outer-formats.md
  classification.md
  schema.md
tools/
  validate_public_catalog.py
```

Internal capture, database, CLIProxyAPI, backlog, staging, and evidence work now lives under
`internal/`. Those files can help maintain the catalog, but they are not the public surface.

## What Counts As A Feature

A published feature describes observable structure, for example:

- native field name: `signature`, `signature_delta`, `encrypted_content`, `thoughtSignature`;
- public encoding: base64 or base64url;
- decoded outer markers: first byte, token envelope shape, channel marker, IV/HMAC presence;
- publication policy: raw value omitted, metadata only;
- replay boundary: same endpoint/family only unless proven otherwise.

Outer-format classification does not prove decryptability, authentication, or replay success. It
only says the value matches a known container shape.

## Current Families

- Claude: `signature` on Anthropic Messages thinking blocks; stream field `signature_delta`.
- GPT: `encrypted_content` on OpenAI Responses reasoning and related opaque items.
- Gemini: `thoughtSignature` / `thought_signature` on content parts.
- Grok/xAI: Responses-compatible `encrypted_content`, tracked separately from GPT.

See [docs/signature-outer-formats.md](docs/signature-outer-formats.md) for the detailed marker
rules.

## Validation

Run the public catalog validator before publishing changes:

```bash
python3 tools/validate_public_catalog.py
```

For a quick JSON parse check:

```bash
jq empty features/*.json schemas/*.json signatures/**/*.json
```

## Publishing Rules

- Publish hashes, lengths, encodings, classifications, and notes only.
- Do not publish raw native signatures or encrypted reasoning blobs.
- Keep low-confidence local routing names out of public endpoint taxonomy.
- Put internal capture artifacts, staging data, runtime exports, and database material in
  `internal/`.
- When a field name is shared across providers, such as GPT and xAI `encrypted_content`, keep the
  families separate until replay compatibility is directly proven.
