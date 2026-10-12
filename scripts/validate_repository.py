#!/usr/bin/env python3
"""Offline integrity checks for this reading companion, not research validation."""
from __future__ import annotations
import json
import re
import sys
from pathlib import Path
from urllib.parse import unquote, urlsplit

ROOT = Path(__file__).resolve().parents[1]
ERRORS: list[str] = []
COUNTS = {"files": 0, "local_links": 0, "paper_page_links": 0, "external_links": 0}
REQUIRED = [
    "README.md", "AGENTS.md", "LLMS.txt", "ATTRIBUTION.md", "LICENSE",
    "CONTRIBUTING.md", "CITATION.cff", "references/paper.bib",
    "metadata/paper.json", "metadata/claims.json", "metadata/sources.json",
    "docs/01-concepts-and-context.md", "docs/02-method-and-protocols.md",
    "docs/03-results.md", "docs/04-analysis-and-limitations.md",
    "docs/05-paper-map.md", "docs/06-discussion-and-replication.md",
]

def require(condition: bool, message: str) -> None:
    if not condition:
        ERRORS.append(message)

def without_fences(text: str) -> str:
    lines, in_fence = [], False
    for line in text.splitlines():
        if re.match(r"^\s*(\x60{3}|~~~)", line):
            in_fence = not in_fence
        elif not in_fence:
            lines.append(line)
    return "\n".join(lines)

def anchors(text: str) -> set[str]:
    found: set[str] = set()
    duplicates: dict[str, int] = {}
    for line in without_fences(text).splitlines():
        match = re.match(r"^#{1,6}\s+(.+?)\s*#*\s*$", line)
        if match:
            title = re.sub(r"\[([^\]]+)\]\([^)]+\)", r"\1", match.group(1))
            title = re.sub(r"<[^>]+>", "", title).lower()
            title = "".join(ch for ch in title if ch.isalnum() or ch in "_- ")
            base = title.replace(" ", "-")
            occurrence = duplicates.get(base, 0)
            duplicates[base] = occurrence + 1
            found.add(base if occurrence == 0 else f"{base}-{occurrence}")
    found.update(re.findall(r'<a\s+(?:name|id)=["\']([^"\']+)', text))
    return found

def inspect_url(value: str, context: str, current: Path | None = None) -> None:
    parsed = urlsplit(value)
    if parsed.scheme:
        require(parsed.scheme in {"https", "http", "mailto"}, f"{context}: unexpected URL scheme {value}")
        COUNTS["external_links"] += 1
        if parsed.netloc == "arxiv.org" and parsed.path == "/pdf/2609.35738v1":
            if parsed.fragment:
                match = re.fullmatch(r"page=(\d+)", parsed.fragment)
                require(bool(match), f"{context}: invalid PDF fragment {value}")
                if match:
                    require(1 <= int(match.group(1)) <= 36, f"{context}: out-of-range paper page {value}")
                    COUNTS["paper_page_links"] += 1
        return
    if current is None:
        return
    target = (current.parent / unquote(parsed.path)).resolve() if parsed.path else current
    try:
        target.relative_to(ROOT)
    except ValueError:
        ERRORS.append(f"{context}: local link escapes repository: {value}")
        return
    COUNTS["local_links"] += 1
    require(target.is_file(), f"{context}: missing local link {value}")
    if parsed.fragment and target.is_file():
        require(unquote(parsed.fragment) in anchors(target.read_text(encoding="utf-8")),
                f"{context}: missing local anchor {value}")

def inspect_json_urls(value: object, context: str) -> None:
    if isinstance(value, dict):
        for key, item in value.items():
            inspect_json_urls(item, f"{context}.{key}")
    elif isinstance(value, list):
        for index, item in enumerate(value):
            inspect_json_urls(item, f"{context}[{index}]")
    elif isinstance(value, str) and value.startswith(("http://", "https://")):
        inspect_url(value, context)

for name in REQUIRED:
    require((ROOT / name).is_file(), f"Missing required file: {name}")

files = [p for p in ROOT.rglob("*") if p.is_file() and ".git" not in p.parts
         and "__pycache__" not in p.parts]
for file in files:
    COUNTS["files"] += 1
    try:
        text = file.read_text(encoding="utf-8")
    except UnicodeError:
        ERRORS.append(f"{file.relative_to(ROOT)}: not UTF-8 text")
        continue
    require("\ufffd" not in text, f"{file.relative_to(ROOT)}: replacement character")
    require("\x00" not in text, f"{file.relative_to(ROOT)}: unexpected NUL")
    require(not any(ord(char) < 32 and char not in "\n\r\t" for char in text),
            f"{file.relative_to(ROOT)}: unexpected control character")
    if file.suffix == ".md" or file.name == "LLMS.txt":
        fences = sum(bool(re.match(r"^\s*(\x60{3}|~~~)", line)) for line in text.splitlines())
        require(fences % 2 == 0, f"{file.relative_to(ROOT)}: unclosed code fence")
        for target in re.findall(r"(?<!!)\[[^\]]+\]\(([^)\s]+)\)", without_fences(text)):
            inspect_url(target, str(file.relative_to(ROOT)), file)

try:
    paper = json.loads((ROOT / "metadata/paper.json").read_text(encoding="utf-8"))
    claims = json.loads((ROOT / "metadata/claims.json").read_text(encoding="utf-8"))
    sources = json.loads((ROOT / "metadata/sources.json").read_text(encoding="utf-8"))
    for name, data in [("paper", paper), ("claims", claims), ("sources", sources)]:
        require(data.get("schema_version") == "1.0.0", f"{name}: unsupported schema version")
        inspect_json_urls(data, name)
    expected_authors = ["Alvin Zhang", "Xuecheng Liu", "Zixuan Wang", "Fahim Tajwar",
                        "Daman Arora", "Ruslan Salakhutdinov", "Daniel Khashabi",
                        "Yuda Song", "Andrea Zanette"]
    require([a["name"] for a in paper["authors"]] == expected_authors, "Paper author order/content mismatch")
    require(paper["arxiv"]["id"] == "2609.35738" and paper["arxiv"]["version"] == "v1",
            "Wrong paper version")
    require(paper["page_count"] == 36, "Wrong paper page count")
    require(bool(re.fullmatch(r"[0-9a-f]{64}", paper["provenance"]["sha256"])), "Malformed source SHA-256")
    require(paper["license"]["spdx"] == "CC-BY-4.0", "Unexpected paper license")
    require(paper["companion"]["experiments_run"] is False, "Companion research-scope mismatch")
    require(paper["companion"]["implementation_reproduced"] is False, "Replication-scope mismatch")
    require(paper["provenance"]["attachment_binary_equality_verified"] is False,
            "Attachment binary equality was not established")
    require(claims["paper_version"] == "2609.35738v1", "Claims version mismatch")
    claim_ids = [c["id"] for c in claims["claims"]]
    require(len(claim_ids) == len(set(claim_ids)), "Duplicate claim IDs")
    for claim in claims["claims"]:
        require(bool(claim.get("sources")), f"{claim['id']}: no primary source")
        require(claim["kind"] in {"reported_method", "reported_result", "reported_protocol", "authors_analysis"},
                f"{claim['id']}: unknown claim kind")
        for source in claim["sources"]:
            require(1 <= source["page"] <= 36, f"{claim['id']}: page out of range")
            require(source["url"].endswith(f"#page={source['page']}"), f"{claim['id']}: page/URL mismatch")
    source_ids = [s["id"] for s in sources["sources"]]
    require(len(source_ids) == len(set(source_ids)), "Duplicate source IDs")
    bib = (ROOT / "references/paper.bib").read_text(encoding="utf-8")
    cff = (ROOT / "CITATION.cff").read_text(encoding="utf-8")
    require("cff-version: 1.2.0" in cff, "Missing CFF version")
    require("preferred-citation:" in cff, "Missing paper preferred citation")
    for author in paper["authors"]:
        require(f"{author['family']}, {author['given']}" in bib, f"BibTeX omits {author['name']}")
        require(f'given-names: "{author["given"]}"' in cff
                and f'family-names: "{author["family"]}"' in cff,
                f"CFF omits {author['name']}")
    require("2609.35738v1" in bib and "2609.35738v1" in cff, "Citation version mismatch")
except (KeyError, ValueError, OSError) as error:
    ERRORS.append(f"Metadata/citation integrity: {error}")

if ERRORS:
    print("\n".join(f"ERROR: {error}" for error in ERRORS))
    sys.exit(1)
print("PASS: " + ", ".join(f"{name}={value}" for name, value in COUNTS.items()))
print("Scope: document integrity, JSON fields, citation consistency, local anchors and PDF page ranges.")
print("External reachability, full CFF schema, and research validity require separate checks.")
