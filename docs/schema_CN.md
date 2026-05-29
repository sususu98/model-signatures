# Public Schemas

公开目录保留两类 schema：

- [signature.schema.json](../schemas/signature.schema.json)：`signatures/` 下的 metadata-only 观测。
- [signature-features.schema.json](../schemas/signature-features.schema.json)：`features/signature-features.json`
  下的 family 级 feature records。

## Signature Entries

每个 signature entry 记录：

- `model_family`：`claude`、`gpt`、`gemini` 或 `grok`；
- `endpoint`：可信 public endpoint bucket 和 confidence；
- `signature_source`：原生字段和 JSON path；
- `sample`：hash、length、encoding 和 raw-publication policy；
- `classification`：可观察外层格式 metadata；
- `replay_contract`：endpoint-scoped replay 边界；
- `provenance`：非敏感来源说明。

schema 有意保留 provider-native 字段名，不发明跨 provider 的统一 signature kind。

## Feature Records

Feature record 汇总跨样本可复用的外层格式事实：

- `field`：原生 signature 字段；
- `observable_format`：简短的人类可读格式描述；
- `observable_variants`：marker 级变体，例如首字节或 token envelope shape；
- `raw_publication_policy`：通常是 `metadata_only`；
- `portable_across_endpoints`：除非直接证明，否则为 false；
- `synthetic_replacement`：只允许已文档化的 provider-native sentinel。

## Internal Schemas

capture manifest、database export、runtime integration、backlog report 等维护工作流的 schema 位于
`internal/schemas/`。它们不属于 public catalog surface。
