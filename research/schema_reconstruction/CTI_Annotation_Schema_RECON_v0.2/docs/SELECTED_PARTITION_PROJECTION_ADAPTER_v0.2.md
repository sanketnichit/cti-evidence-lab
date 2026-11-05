# Selected-partition projection adapter — RECON v0.2

**Status:** draft integration layer; synthetic fixtures only. Not approved for real-report use.

## Purpose

The v0.1 adapter accepts an exact report/annotator/pass triple from its caller. The v0.2 wrapper resolves that triple from `analysis_partition_selection.csv`, so an unselected development or repeat pass cannot be supplied directly by a caller.

## Inputs

- the v0.2 package root;
- report ID and exact frozen source text;
- `analysis_lock_confirmed=True`;
- the exact selected-analysis `sha256:` reference.

The caller does not supply annotator or pass IDs; they are read from the one valid `SELECTED_FINAL` row.

## Lock coverage

`compute_analysis_lock_reference()` layers a second digest over:

1. the original v0.1 annotation lock, covering the source text and all v0.1 register rows for the selected partition;
2. all v0.2 temporal-relation evidence rows for that partition; and
3. the final-selection decision fields, excluding the row's own `lock_reference` to avoid a circular digest.

A change to the source, any v0.1 partition register, v0.2 evidence row, or final selection metadata invalidates the selected-analysis lock. This digest detects changes; it is not a digital signature or proof of authorship.

## Fail-closed sequence

1. Require explicit lock confirmation.
2. Validate the selection register and require exactly one selected-final row for the requested report.
3. Validate the temporal-evidence extension against the parent temporal relations, activity units, evidence spans and time evidence.
4. Recompute the selected-analysis digest and compare it with both the register value and caller-supplied value.
5. Recompute the v0.1 partition lock and delegate to the unchanged v0.1 adapter.

The parent adapter continues to enforce source hashes, structural validity, eligibility, local-use permission, review completion, mapping restrictions and A_120 membership.

## Synthetic tests

Run the full v0.2 package test suite:

```bash
python -m unittest discover -s research/schema_reconstruction/CTI_Annotation_Schema_RECON_v0.2/tests -v
```

Tests cover the missing-selection gate, explicit confirmation, valid selection, stale temporal evidence, stale selection metadata, invalid final roles, invalid endpoint support and changed base annotations.

## Current limitation

The selection register is still header-only. No report or annotation pass has been selected. The wrapper is implemented and synthetic-tested, but there is no real-report projection result and the schema remains draft-only.
