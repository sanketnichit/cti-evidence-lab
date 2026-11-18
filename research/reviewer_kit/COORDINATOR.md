# Calibration packet workflow

The calibration instrument distributes the same five fixed reports and blank forms under pseudonymous reviewer IDs R1 and R2. It supports evaluation of the draft annotation rules; it is not a frozen gold-standard protocol or a completed review result.

## Independence and provenance

First passes are completed separately, without access to earlier project judgments or another reviewer's answers. Source files, prior exposure, report coverage and actual completion dates are recorded. Original returns are preserved before reconciliation. Packet archives contain source text and are excluded from the public repository.

## Reconciliation procedure

1. Verify the packet manifest and source hashes.
2. Establish the overlap of fully reviewed reports and identify missing decisions.
3. Resolve free-text evidence locators against the source, with confirmation of the originating interpretation.
4. Align activity units using evidence rather than local identifier equality; retain split/merge disagreements.
5. Compare occurrence status, incident scope, temporal labels and mappings separately, including coverage and raw aligned counts.
6. Record subsequent corrections and reasons without overwriting independent first passes.

Agreement statistics require a specified alignment/scoring rule and overlapping independent reviews. A reconciled table is not an additional independent annotation. Formal selected-final analysis remains subject to the applicable protocol, validation and lock requirements.

## Packet generation

```sh
python scripts/build_reviewer_packets.py --corpus-root /path/to/AnnoCTR/all --recover-crlf
```

Generated packets contain the [review instrument](REVIEW_GUIDE.md), source manifest, attribution and blank forms. AnnoCTR-derived materials retain CC BY-SA 4.0 terms. Public project software licensing does not replace source licensing.
