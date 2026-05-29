# 分类规则

分类依据是产生 native signature 字段的可信 endpoint surface。不要按本地网关名、文件名、路由标签或访问代理分类。

## Public Endpoint Buckets

- Claude：`anthropic`、`aws-bedrock`、`azure`、`vertex`、`claude-code`
- GPT：`openai`、`azure-openai`、`codex`
- Gemini：`aistudio`、`vertex`、`antigravity`、`gemini-cli`
- Grok：`xai`

如果 emitting endpoint 不明确，观测应留在 `internal/`，直到有可信 endpoint evidence 后再 promotion。

## Native Fields

- Claude：thinking block 上的 `signature`，流式 delta 为 `signature_delta`。
- GPT：Responses reasoning 或相关 opaque item 上的 `encrypted_content`。
- Gemini：content part 上的 `thoughtSignature` 或 `thought_signature`。
- Grok/xAI：`encrypted_content`，即使字段名和 GPT 重叠，也必须单独跟踪。

`classification.format` 只描述可观察外层容器，例如 `protobuf`、`fernet_like_token`、
`wrapped_protobuf_unclassified`、`uuid`、`sentinel` 或 `unknown`。

## Promotion 边界

一个值只有满足以下条件，才能进入 public catalog：

- 有可信的 model family 和 endpoint bucket；
- public 文件中不包含 raw signature material；
- 记录了 hash、length、encoding 和 outer-format classification；
- replay notes 只声明 emitting family 或 endpoint 范围内的边界；
- 共享字段名不会被解释成跨 provider 兼容性。
