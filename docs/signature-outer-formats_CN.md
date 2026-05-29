# Signature 外层格式

本文描述 native reasoning-continuity signature 的可观察外层容器。这里不声明可解密性、语义等价性，
也不声明它能在其他 endpoint 上 replay 成功。

## 范围

外层格式分类是结构检查：解码公开编码，观察容器形状，并记录 length、首字节、channel marker、
token envelope 字段等 metadata。除非 schema 明确允许，raw signature value 都必须保持私有。

`valid_outer_format = true` 的含义是：“这个值符合该 family 预期的公开容器形状。”它不表示这个值能被
其他账号、session、model 或 endpoint 解密、认证或 replay。

本地网关名和从文件名推出来的路由标签不能作为外层格式的 endpoint evidence。不要用它们推断 channel
class、backend class、endpoint 支持范围或 replay 可移植性。

## Claude `signature`

Claude signature 是 Anthropic Messages `thinking` block 上的 base64 protobuf-like 值。
流式响应使用 `signature_delta`，需要组装回当前 active thinking block 后再存入 history。

有用的外层 marker：

- `top_level_first_byte = 0x12`：普通 compact signature。
- `channel_id = 12`：已观测到的 direct Anthropic 样本。
- `channel_id = 11`：Claude-compatible shared marker；单独看这个 marker 不能证明 endpoint 身份。
- `infra_id = 1` 或 `infra_id = 2`：已观测到的 cloud backend marker。
- `channel_block_length = 70` 或 `72`，并且 `ecdsa_length = 64`：compact-schema 样本。
- Claude Code 可能有外层 wrapper；需要 unwrap 后分类内部 signature。

Replay 仍然是 Claude endpoint scoped。外来 signature 应该连同 thinking block 一起 drop，而不是转换或合成。

## GPT `encrypted_content`

GPT Responses reasoning state 使用 base64url `encrypted_content`。当前有效 OpenAI-family 样本呈
Fernet-like envelope：

- `version_byte = 0x80`。
- decoded length 至少 `57` bytes。
- version byte 后有 8-byte timestamp。
- 存在 16-byte IV。
- ciphertext length 为正数，并且按 16-byte 对齐。
- 末尾存在 32-byte HMAC。

这些 marker 只证明外层 envelope 形状，不证明可解密或 replay 成功。需要保留完整 reasoning item graph，
包括 item id 和顺序。

## Gemini `thoughtSignature`

Gemini signature 位于 content part 上，字段为 `thoughtSignature` 或 `thought_signature`。分类是
part-level，不是 message-level。

已观测外层类别：

- `top_level_first_byte = 0x0a`，常见 base64 prefix 为 `Ci`、`Ck`、`Cl`、`Cm`：protobuf-like 值。
- `top_level_first_byte = 0x12`：wrapped protobuf-like，但尚未完全分类。
- decode 后是 UTF-8 UUID 形状：legacy 或 malformed function-call 样本。
- `skip_thought_signature_validator`：唯一接受的 synthetic sentinel。

Replay 前要保留 part identity、function-call pairing 和 provider metadata namespace。

## Grok/xAI `encrypted_content`

Grok 使用 Responses-compatible `encrypted_content` surface，但它不是 OpenAI `encrypted_content`。
当前 xAI 样本不满足 OpenAI Fernet-like envelope 检查，必须保持 xAI scoped。

有用的 xAI state 包括 `providerMetadata.xai.reasoningEncryptedContent`、
`providerMetadata.xai.itemId`，以及兼容的 `previous_response_id` 行为。只有在 direct native samples
和 public adapter evidence 对 replay contract 达成一致后，profile 才能从 provisional 升级。
