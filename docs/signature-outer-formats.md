# Signature Outer Formats

[中文](signature-outer-formats_CN.md)

This document describes observable outer containers for native reasoning-continuity signatures. It
does not claim decryptability, semantic equivalence, or successful replay on another endpoint.

## Scope

Outer-format classification is a structural check: decode the published encoding, inspect the
container shape, and store metadata such as length, first byte, channel marker, or token envelope
fields. Raw signature values remain private unless a schema explicitly allows publication.

`valid_outer_format = true` means "this value matches the expected public container shape for this
family." It does not mean the value can be decrypted, authenticated, or replayed by a different
account, session, model, or endpoint.

Local gateway names and filename-derived route labels are excluded from outer-format endpoint
evidence. Do not use them to infer channel classes, backend classes, endpoint support, or replay
portability.

## Claude `signature`

Claude signatures are base64 protobuf-like values on Anthropic Messages `thinking` blocks. Streaming
uses `signature_delta`, which must be assembled onto the active thinking block before history is
stored.

Useful outer markers:

- `top_level_first_byte = 0x12` for normal compact signatures.
- `channel_id = 12` for observed direct Anthropic samples.
- `channel_id = 11` for shared-marker Claude-compatible samples; this marker alone is not an
  endpoint identity.
- `infra_id = 1` or `infra_id = 2` for observed cloud backend markers.
- `channel_block_length = 70` or `72`, plus `ecdsa_length = 64`, for compact-schema samples.
- Claude Code may add an outer wrapper; classify the inner signature after unwrap.

Replay remains Claude-endpoint scoped. Foreign signatures should be dropped with their thinking
block rather than converted or synthesized.

## GPT `encrypted_content`

GPT Responses reasoning state uses base64url `encrypted_content` values. Current valid OpenAI-family
samples are Fernet-like envelopes:

- `version_byte = 0x80`.
- decoded length is at least `57` bytes.
- an 8-byte timestamp follows the version byte.
- a 16-byte IV is present.
- ciphertext length is positive and 16-byte aligned.
- a 32-byte trailing HMAC is present.

These markers prove only the outer envelope. They do not prove decryptability or replay success.
Preserve the whole reasoning item graph, including item ids and ordering.

## Gemini `thoughtSignature`

Gemini signatures live on content parts as `thoughtSignature` or `thought_signature`. Classification
is part-level, not message-level.

Observed outer classes:

- `top_level_first_byte = 0x0a`, often with base64 prefixes such as `Ci`, `Ck`, `Cl`, or `Cm`, for
  protobuf-like values.
- `top_level_first_byte = 0x12` for wrapped protobuf-like values that are not fully classified.
- decoded UTF-8 UUID-shaped values for legacy or malformed function-call samples.
- `skip_thought_signature_validator` as the only accepted synthetic sentinel.

Preserve part identity, function-call pairing, and provider metadata namespaces before replay.

## Grok/xAI `encrypted_content`

Grok uses a Responses-compatible `encrypted_content` surface, but this is not OpenAI
`encrypted_content`. Current xAI samples do not satisfy the OpenAI Fernet-like envelope check and
must remain xAI scoped.

Useful xAI state includes `providerMetadata.xai.reasoningEncryptedContent`,
`providerMetadata.xai.itemId`, and any compatible `previous_response_id` behavior. Keep the profile
provisional until direct native samples and public adapter evidence agree on the replay contract.
