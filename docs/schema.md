# Public Schemas

[中文](schema_CN.md)

The public catalog keeps two schema families:

- [signature.schema.json](../schemas/signature.schema.json): metadata-only observations under
  `signatures/`.
- [signature-features.schema.json](../schemas/signature-features.schema.json): family-level feature
  records under `features/signature-features.json`.

## Signature Entries

Each signature entry records:

- `model_family`: `claude`, `gpt`, `gemini`, or `grok`;
- `endpoint`: trusted public endpoint bucket and confidence;
- `signature_source`: native field and JSON path;
- `sample`: hash, length, encoding, and raw-publication policy;
- `classification`: observable outer-format metadata;
- `replay_contract`: endpoint-scoped replay boundary;
- `provenance`: non-sensitive source notes.

The schema intentionally preserves provider-native field names. It does not invent a normalized
cross-provider signature kind.

## Feature Records

Feature records summarize the reusable outer-format facts across samples:

- `field`: the native signature field;
- `observable_format`: concise human-readable format description;
- `observable_variants`: marker-level variants, such as first byte or token envelope shape;
- `raw_publication_policy`: usually `metadata_only`;
- `portable_across_endpoints`: false unless directly proven;
- `synthetic_replacement`: allowed only for documented provider-native sentinels.

## Internal Schemas

Schemas for capture manifests, database export, runtime integration, backlog reports, and other
maintenance workflows live in `internal/schemas/`. They are not part of the public catalog surface.
