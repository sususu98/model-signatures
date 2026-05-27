# Contributing

Please keep entries factual and reproducible.

Before adding a signature:

1. Remove secrets, tokens, cookies, request IDs, private prompts, and user content.
2. Keep only fields needed to identify the signature.
3. Prefer normalized JSON over raw logs.
4. Include the observed model name, source, signature type, and observation time.
5. Keep one logical observation per entry.

If an observation depends on a specific client, endpoint, or protocol version, add that detail
under `evidence.notes`.

