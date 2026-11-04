"""Canonical source-text decoding and hashing for CTI Evidence Lab.

The annotation text is decoded as strict UTF-8. A leading UTF-8 BOM is treated
as an encoding marker and removed; all other bytes are preserved through UTF-8
decoding, including CRLF/LF line endings. No Unicode normalization is applied.
Offsets are Python Unicode code-point indices into this exact decoded string.
"""
from __future__ import annotations

import hashlib
from pathlib import Path

UTF8_BOM = b"\xef\xbb\xbf"


def decode_frozen_source(raw: bytes) -> str:
    """Decode UTF-8, removing only an optional leading UTF-8 BOM."""
    if raw.startswith(UTF8_BOM):
        raw = raw[len(UTF8_BOM):]
    return raw.decode("utf-8", errors="strict")


def read_frozen_source(path: str | Path) -> str:
    """Read source bytes without universal-newline translation."""
    return decode_frozen_source(Path(path).read_bytes())


def frozen_source_sha256(text: str) -> str:
    """Hash the UTF-8 bytes of the exact decoded annotation text."""
    return hashlib.sha256(text.encode("utf-8")).hexdigest()


def frozen_source_metadata(path: str | Path) -> dict[str, int | str]:
    """Return the canonical text hash and code-point count without source text."""
    text = read_frozen_source(path)
    return {
        "source_text_sha256": frozen_source_sha256(text),
        "source_text_char_count": len(text),
    }
