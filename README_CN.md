# 模型 Signature 特征

本仓库发布 Claude、GPT、Gemini、Grok 系列端点产生的 reasoning-continuity signature 的
**metadata-only 可观察外层特征**。

它是一个特征目录，不是采集流水线、运行时集成数据库，也不是内部日志归档。公开目录中不应出现
raw signature、prompt、tool 参数、request id、凭据或私有日志。

## 发布目录

```text
features/
  signature-features.json        # family 级特征记录和外层 marker
signatures/
  claude/
  gpt/
  gemini/
  grok/                          # 按可信 endpoint family 存放 metadata-only 观测
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

内部采集、数据库、CLIProxyAPI、backlog、staging、evidence 等维护材料放在 `internal/`。
它们可以辅助维护目录，但不是公开发布面。

## 什么算特征

公开 feature 描述的是可观察结构，例如：

- 原生字段名：`signature`、`signature_delta`、`encrypted_content`、`thoughtSignature`；
- 公开编码：base64 或 base64url；
- decode 后的外层 marker：首字节、token envelope、channel marker、IV/HMAC 是否存在；
- 发布策略：只发布 metadata，不发布 raw value；
- replay 边界：除非直接证明，否则只限同 endpoint 或同 family。

外层格式分类不证明可解密、可认证或可 replay；它只说明这个值看起来符合某个已知容器形状。

## 当前 Family

- Claude：Anthropic Messages thinking block 上的 `signature`，流式字段为 `signature_delta`。
- GPT：OpenAI Responses reasoning item 及相关 opaque item 上的 `encrypted_content`。
- Gemini：content part 上的 `thoughtSignature` / `thought_signature`。
- Grok/xAI：Responses-compatible `encrypted_content`，但和 GPT 分开跟踪。

详细 marker 规则见 [docs/signature-outer-formats_CN.md](docs/signature-outer-formats_CN.md)。

## 验证

发布前运行：

```bash
python3 tools/validate_public_catalog.py
```

快速 JSON 解析检查：

```bash
jq empty features/*.json schemas/*.json signatures/**/*.json
```

## 发布规则

- 只发布 hash、length、encoding、classification 和非敏感 notes。
- 不发布 raw native signature 或 encrypted reasoning blob。
- 低可信本地路由名不要进入 public endpoint taxonomy。
- 内部采集产物、staging 数据、运行时导出和数据库材料放进 `internal/`。
- 不同 provider 共享字段名时，例如 GPT 和 xAI 都有 `encrypted_content`，在 replay 兼容性被直接证明前必须分开建模。
