# Verification record

Checked on **12 October 2026**, against **arXiv:2609.35738v1**.

## Source and factual review

- The full 36-page official PDF, including references and Appendices A–F, was read across the preparation team.
- Relevant figure pixels, table cells, captions, and equations were inspected alongside text extraction. Figures 1–12 and the quantitative tables used in the notes were included.
- Title, all nine authors in order, contribution footnotes, submission date, categories, paper license, and official project/code links were checked against primary sources.
- The main numerical claims were checked with their populations, metrics, failure accounting, and selection rules. An independent audit reviewed the overview, citation/metadata files, source map, and licensing boundaries.
- Source PDF SHA-256 and byte count are recorded in [paper metadata](metadata/paper.json). Attachment binary equality was not established after the supported Library helper encountered a Windows extended-attribute limitation.

## Documentation checks

- The repository validator passed: required files, UTF-8 integrity, JSON fields, author order, citation consistency, local file links, local section anchors, and PDF page ranges.
- [CITATION.cff](CITATION.cff) passed the official CFF 1.2.0 JSON schema using YAML parsing and JSON Schema validation.
- The 13 distinct external paper, attribution, license, maintainer, and official-project/code URLs reached HTTP 200, including the DOI redirect. The arXiv record still marked DOI registration pending; those two observations are preserved separately.
- Git whitespace checks passed before publication.

The portable check is:

```bash
python scripts/validate_repository.py
```

This script performs offline documentation checks. It does not recheck network reachability or perform full CFF schema validation, which were separate preparation checks.

## Scope of verification

No research experiments were run, no model was trained, no learned harness was executed, and no benchmark score was reproduced. This is an unofficial source-grounded reading companion. The official code repository was marked “Code coming soon!” when checked. Source status and external reachability can change after this date.
