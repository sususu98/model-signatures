# Classification Rules

[中文](classification_CN.md)

Classification is by the trusted endpoint surface that emitted the native signature field. Do not
classify by local gateway name, filename, route label, or access proxy.

## Public Endpoint Buckets

- Claude: `anthropic`, `aws-bedrock`, `azure`, `vertex`, `claude-code`
- GPT: `openai`, `azure-openai`, `codex`
- Gemini: `aistudio`, `vertex`, `antigravity`, `gemini-cli`
- Grok: `xai`

If the emitting endpoint is not known, keep the observation in `internal/` until it can be promoted
with credible endpoint evidence.

## Native Fields

- Claude: `signature` on a thinking block, with stream deltas as `signature_delta`.
- GPT: `encrypted_content` on Responses reasoning or related opaque items.
- Gemini: `thoughtSignature` or `thought_signature` on content parts.
- Grok/xAI: `encrypted_content`, tracked separately from GPT even though the field name overlaps.

`classification.format` describes only the observable outer container, such as `protobuf`,
`fernet_like_token`, `wrapped_protobuf_unclassified`, `uuid`, `sentinel`, or `unknown`.

## Promotion Boundary

A value can be promoted into the public catalog only when:

- it has a trusted model family and endpoint bucket;
- raw signature material is omitted from public files;
- the observation records hash, length, encoding, and outer-format classification;
- replay notes stay scoped to the emitting family or endpoint;
- shared field names are not treated as cross-provider compatibility.
