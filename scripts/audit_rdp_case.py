"""Verify the purposive RDP case against a locally saved publisher HTML page.

The command exports hashes and offsets only. It does not assign semantic labels.
Source paragraphs are HTML <p> text with entities decoded, Unicode whitespace
collapsed to single spaces, empty paragraphs removed, then joined by LF.
"""
from __future__ import annotations

import argparse
import hashlib
import json
from html.parser import HTMLParser
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
CASE = ROOT / "research/case_studies/dfir_rdp_v0.1/case.json"


def digest(value):
    return hashlib.sha256(value if isinstance(value, bytes) else value.encode("utf-8")).hexdigest()


class ParagraphParser(HTMLParser):
    def __init__(self):
        super().__init__(convert_charrefs=True)
        self.paragraphs = []
        self.current = None
        self.hidden = 0

    def flush(self):
        if self.current is not None:
            text = " ".join("".join(self.current).split())
            if text:
                self.paragraphs.append(text)
        self.current = None

    def handle_starttag(self, tag, attrs):
        if tag in {"script", "style"}:
            self.hidden += 1
        if self.hidden:
            return
        if tag == "p":
            self.flush()
            self.current = []
        elif tag == "br" and self.current is not None:
            self.current.append(" ")

    def handle_endtag(self, tag):
        if tag in {"script", "style"}:
            self.hidden = max(0, self.hidden - 1)
        elif tag == "p" and not self.hidden:
            self.flush()

    def handle_data(self, data):
        if self.current is not None and not self.hidden:
            self.current.append(data)


def canonical_text(raw):
    parser = ParagraphParser()
    parser.feed(raw.decode("utf-8-sig", errors="strict"))
    parser.flush()
    return "\n".join(parser.paragraphs) + "\n"


def verify(raw, case):
    text = canonical_text(raw)
    source = case["source"]
    if digest(text) != source["paragraph_text_sha256"]:
        raise ValueError("Publisher paragraph snapshot differs from the recorded case; do not silently refresh evidence")
    checked = []
    for span in case["evidence"]:
        start, end = span["char_start"], span["char_end"]
        if not 0 <= start < end <= len(text):
            raise ValueError("Evidence offsets outside canonical text")
        if digest(text[start:end]) != span["span_sha256"]:
            raise ValueError("Evidence passage hash mismatch")
        if text.count("\n", 0, start) + 1 != span["paragraph_number"]:
            raise ValueError("Evidence paragraph mismatch")
        checked.append(span["evidence_id"])
    return {"status": "SOURCE_BINDINGS_VERIFIED_NOT_SEMANTIC_VALIDATION",
            "raw_html_sha256": digest(raw),
            "raw_html_matches_retrieval": digest(raw) == source["raw_html_sha256"],
            "paragraph_text_sha256": digest(text), "evidence_verified": checked}


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--source-html", type=Path, required=True)
    parser.add_argument("--case", type=Path, default=CASE)
    parser.add_argument("--output", type=Path)
    args = parser.parse_args()
    result = verify(args.source_html.read_bytes(), json.loads(args.case.read_text(encoding="utf-8")))
    serialized = json.dumps(result, indent=2, sort_keys=True) + "\n"
    if args.output:
        args.output.parent.mkdir(parents=True, exist_ok=True)
        args.output.write_text(serialized, encoding="utf-8", newline="")
    else:
        print(serialized)
