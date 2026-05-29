#!/usr/bin/env python3
"""Validate the public model-signature feature catalog."""

from __future__ import annotations

import json
import sys
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[1]
PUBLIC_ENDPOINTS = {
    "claude": {"anthropic", "aws-bedrock", "azure", "vertex", "claude-code"},
    "gpt": {"openai", "azure-openai", "codex"},
    "gemini": {"aistudio", "vertex", "antigravity", "gemini-cli", "unknown"},
    "grok": {"xai"},
}
PUBLIC_FIELDS = {
    "claude": {"signature"},
    "gpt": {"encrypted_content"},
    "gemini": {"thoughtSignature", "thought_signature"},
    "grok": {"encrypted_content"},
}
FORBIDDEN_PUBLIC_KEYS = {
    "raw_signature",
    "raw_encrypted_content",
    "raw_value",
    "authorization",
    "cookie",
}
FORBIDDEN_PUBLIC_TEXT = {
    "qianyu",
    "replace-with-captured-model",
    "capture_manifest",
    "draft-",
    "recipe-",
}


def load_json(path: Path) -> Any:
    return json.loads(path.read_text(encoding="utf-8"))


def walk(value: Any) -> list[Any]:
    values = [value]
    if isinstance(value, dict):
        for child in value.values():
            values.extend(walk(child))
    elif isinstance(value, list):
        for child in value:
            values.extend(walk(child))
    return values


def validate_signature_file(path: Path, errors: list[str]) -> None:
    data = load_json(path)
    if not isinstance(data, list):
        errors.append(f"{path}: expected top-level array")
        return
    for index, entry in enumerate(data):
        if not isinstance(entry, dict):
            errors.append(f"{path}[{index}]: expected object")
            continue
        family = entry.get("model_family")
        endpoint = entry.get("endpoint", {}).get("id") if isinstance(entry.get("endpoint"), dict) else None
        field = (
            entry.get("signature_source", {}).get("field")
            if isinstance(entry.get("signature_source"), dict)
            else None
        )
        if family not in PUBLIC_ENDPOINTS:
            errors.append(f"{path}[{index}]: invalid model_family {family!r}")
            continue
        if endpoint not in PUBLIC_ENDPOINTS[family]:
            errors.append(f"{path}[{index}]: non-public endpoint {family}/{endpoint}")
        if field not in PUBLIC_FIELDS[family]:
            errors.append(f"{path}[{index}]: invalid native field {field!r} for {family}")
        sample = entry.get("sample")
        if not isinstance(sample, dict):
            errors.append(f"{path}[{index}]: missing sample metadata")
        elif sample.get("raw_policy") not in {"metadata_only", "redacted", "absent"}:
            errors.append(f"{path}[{index}]: public sample must be metadata-only/redacted/absent")
        classification = entry.get("classification")
        if not isinstance(classification, dict) or not classification.get("format"):
            errors.append(f"{path}[{index}]: missing classification.format")
        for node in walk(entry):
            if isinstance(node, dict):
                forbidden = sorted(FORBIDDEN_PUBLIC_KEYS & set(node))
                if forbidden:
                    errors.append(f"{path}[{index}]: forbidden public keys {forbidden}")
            elif isinstance(node, str):
                lowered = node.lower()
                hits = sorted(token for token in FORBIDDEN_PUBLIC_TEXT if token in lowered)
                if hits:
                    errors.append(f"{path}[{index}]: forbidden public text markers {hits}")


def validate_features(errors: list[str]) -> None:
    data = load_json(ROOT / "features/signature-features.json")
    if not isinstance(data, list):
        errors.append("features/signature-features.json: expected top-level array")
        return
    seen_families: set[str] = set()
    for index, feature in enumerate(data):
        if not isinstance(feature, dict):
            errors.append(f"features/signature-features.json[{index}]: expected object")
            continue
        family = feature.get("model_family")
        seen_families.add(str(family))
        if family not in PUBLIC_FIELDS:
            errors.append(f"features/signature-features.json[{index}]: invalid family {family!r}")
            continue
        if feature.get("field") not in PUBLIC_FIELDS[family]:
            errors.append(
                f"features/signature-features.json[{index}]: invalid feature field {feature.get('field')!r}"
            )
        if feature.get("raw_publication_policy") != "metadata_only":
            errors.append(f"features/signature-features.json[{index}]: expected metadata_only")
        if feature.get("portable_across_endpoints") is not False:
            errors.append(f"features/signature-features.json[{index}]: endpoint portability must be false")
    missing = sorted(set(PUBLIC_FIELDS) - seen_families)
    if missing:
        errors.append(f"features/signature-features.json: missing families {missing}")


def main() -> int:
    errors: list[str] = []
    for path in sorted((ROOT / "signatures").glob("*/*/signatures.json")):
        validate_signature_file(path, errors)
    validate_features(errors)
    for path in sorted((ROOT / "schemas").glob("*.json")):
        load_json(path)
    if errors:
        print("public catalog validation failed:", file=sys.stderr)
        for error in errors:
            print(f"- {error}", file=sys.stderr)
        return 1
    print("public catalog ok")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
