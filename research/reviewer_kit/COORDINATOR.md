# Sending and receiving the review packets

Give R1 to one friend and R2 to the other. Both packets contain the same five reports and blank forms, with different reviewer IDs. Send the ZIP files privately; they contain source text and are deliberately excluded from Git. Do not send the exploratory decisions or results with them.

Ask each person to read `START_HERE.md`, work independently and return the completed CSVs plus `manifest.json`. One person can help if two are unavailable, but only overlapping independent completed reviews can support an inter-reviewer comparison. There is no required positive finding.

The packets are a calibration exercise while the protocol is still a draft. They do not ask friends to sign off a frozen gold dataset. Preserve first-pass submissions unchanged under ignored `outputs/reviewer_returns/R1/` and `R2/`; work on copies for reconciliation. Record receipt dates and whether the reviewers had prior exposure. Do not publish names or contact information.

## On receipt

1. Verify the packet manifest and source hashes; reject changed source text.
2. Check which reports each person actually read completely and which decisions are missing.
3. Resolve free-text evidence locators to exact source spans, then ask the originating reviewer to confirm them. Do not silently replace their substantive decisions.
4. Align activity units using source evidence, keeping split/merge disagreements visible. Matching local IDs is not matching events.
5. Compare occurrence status, incident scope, temporal label and mapping separately. Report raw aligned counts and coverage before any summary score.
6. Discuss disagreements only after the independent first passes are preserved. Record each change and reason. A shared final table is reconciliation, not another independent annotation.
7. Use the returned work to revise and accept a versioned protocol. A formal study requires the applicable RECON validation, source and selection locks; these simple CSVs are not a bypass.

## Build the packets

From the repository root, with Python 3.11 or later:

```text
python scripts/build_reviewer_packets.py --corpus-root /path/to/AnnoCTR/all --recover-crlf
```

The optional CRLF recovery succeeds only if it reproduces the previously recorded source hash. Without it the source check is strict. The builder writes deterministic ZIP files under `outputs/reviewer_packets/`, contains no proposed answers, and never changes the corpus.

Source attribution and CC BY-SA 4.0 information are inside each packet. Keep them with any source-derived annotation material. The code and blank guide remain under the repository software/documentation licence.
