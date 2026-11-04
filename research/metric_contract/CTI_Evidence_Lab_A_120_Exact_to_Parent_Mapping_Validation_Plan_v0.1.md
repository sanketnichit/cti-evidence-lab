# CTI Evidence Lab — A_120 Exact-to-Parent Mapping Validation Plan v0.1

**Prepared:** 4 November 2026  
**Status:** Technical audit and proposed implementation plan. Not researcher-approved; no ATT&CK release or crosswalk is frozen by this document.  
**Scope:** Validate the relationship between an exact ATT&CK technique/sub-technique ID and the parent-level ID supplied for the ChronoCTI `A_120` projection.

## 1. Why this check is required

The RECON v0.1 validator currently verifies that:

- the derived `A_120` identifier list has 120 unique IDs and the expected ChronoCTI source commit/path;
- `baseline_parent_technique_id` is a member of that list when `baseline_mapping_status=IN_VOCAB`;
- the stored `baseline_vocabulary_id` and `baseline_vocabulary_sha256` match the derived `A_120` artifact;
- accepted mapping rows have an exact technique ID and a non-empty `attack_version`.

It does **not** independently verify that `baseline_parent_technique_id` is the actual parent of `exact_technique_id` in the declared ATT&CK release. It also does not currently verify that the exact ID exists in that release or that the value of `attack_version` matches a pinned release.

Consequently, a row could provide a valid but unrelated `A_120` ID as its parent and pass the present membership check. The validator is therefore checking vocabulary membership, not exact-to-parent semantic correctness.

This is a pre-freeze validation gap. Do not treat current A_120 validator success as proof that parent mappings are correct.

## 2. What is already pinned

The `A_120` list is an ordered identifier-only extraction from ChronoCTI's `temporal-learner-code/selected_techniquesWName.json` at commit:

`4906a0a5e399b6e2aa10435fd6e3894e041e4549`

The source Git blob is `ca14535ad0b67af4c8297707b4c134c9de2d577f`. The derived JSON in RECON v0.1 has SHA-256:

`97b599ffdcfcc5864a9352cf1467de0f6cac92f9141053a76098e4f2d33fb1bc`

That is the **selected parent-level vocabulary artifact**. It is not an ATT&CK release crosswalk and does not establish how any exact/sub-technique ID maps to one of its 120 members.

The pinned ChronoCTI temporal-learner commit metadata dates to 29 December 2023. More importantly, the ChronoCTI version-of-record paper explicitly states in Section 4.1 that the study used MITRE ATT&CK **v12.1**, containing 193 techniques. This paper statement is the primary provenance for the baseline release; do not infer the release from source commit chronology. The exact source file containing the selected 120 techniques remains pinned separately.

## 3. ATT&CK release selection — proposed, not frozen

**Source-aligned primary crosswalk candidate: Enterprise ATT&CK v12.1.**

Rationale: ChronoCTI's published paper explicitly names v12.1 in Section 4.1. Using the same named release is the most defensible starting point for a historically faithful reconstruction of the `A_120` parent vocabulary. This does not mean the derived `A_120` list alone is a v12.1 crosswalk, and the exact-to-parent relationships still require verification from the official versioned STIX collection.

Enterprise v14.1 has been inspected separately as a non-primary compatibility preflight (Section 3.1). It may be used later as a taxonomy-version sensitivity comparison, but it must not silently replace v12.1 in the primary comparison.

**No ATT&CK release is approved or frozen by this plan.** Before implementation, the researcher must approve the source-aligned v12.1 choice. Then obtain the exact official versioned Enterprise STIX collection, record its immutable source identity and SHA-256, and use that exact file as the reproducibility input. Do not use a moving `master` reference as the source for a frozen crosswalk.

Official references:

- MITRE ATT&CK version history: https://attack.mitre.org/resources/previous-versions/
- MITRE ATT&CK STIX data repository and version index: https://github.com/mitre-attack/attack-stix-data
- MITRE technique data model, including the `subtechnique-of` relationship: https://mitre-attack.github.io/attack-data-model/schemas/3.3.0/sdo/technique.schema/
- Pinned ChronoCTI source commit: https://github.com/rayhanur-rahman/ChronoCTI/commit/4906a0a5e399b6e2aa10435fd6e3894e041e4549

### 3.1 Non-primary compatibility preflight — Enterprise ATT&CK v14.1 (4 November 2026)

An exploratory check was run against the official, versioned Enterprise ATT&CK v14.1 STIX collection. This was a compatibility preflight only. It does **not** approve v14.1 for the primary crosswalk, freeze the release, or override ChronoCTI's paper-stated v12.1 version.

Source identity recorded for this inspection:

- Versioned file: `enterprise-attack/enterprise-attack-14.1.json` in `mitre-attack/attack-stix-data`.
- GitHub file URL: https://github.com/mitre-attack/attack-stix-data/blob/master/enterprise-attack/enterprise-attack-14.1.json
- Git blob SHA-1: `57df0ea1181a3902b39f33fc3134ae5117c96502`.
- Retrieved-file SHA-256: `13af7514ad1bcb59deba6b6b46571168544bbe674eb52f41361916bb1cd9c3d6`.
- STIX bundle ID: `bundle--feb75802-6feb-4205-87dd-3d739c429ed4`.
- Collection metadata: `Enterprise ATT&CK`, version `14.1`, modified `2023-11-14T14:00:00.188Z`.

Preflight results:

| Check | Result |
|---|---:|
| Enterprise attack-pattern objects | 768 |
| Top-level techniques | 341 |
| Sub-techniques | 427 |
| Explicit `subtechnique-of` relationships | 427 |
| Sub-techniques with exactly one valid top-level parent | 427 |
| Sub-techniques with missing, multiple, or invalid parents | 0 |
| Orphaned `subtechnique-of` relationships | 0 |
| ChronoCTI `A_120` IDs found in v14.1 | 120/120 |
| `A_120` IDs represented as top-level techniques | 120/120 |
| `A_120` IDs missing or unexpectedly sub-techniques | 0 |
| Revoked/deprecated flags among the 120 `A_120` objects | 0 |
| Sub-techniques whose parent is in `A_120` | 341 |
| Sub-techniques whose parent is outside `A_120` | 86 |

Interpretation: v14.1 contains every selected ChronoCTI parent-level ID and explicit parent relationships for all sub-techniques in that release. This establishes compatibility with the selected 120 parent IDs only. It does not reproduce ChronoCTI's primary release, which the paper identifies as v12.1.

No v14.1 crosswalk has been generated or added to RECON. Keep these results as a non-primary compatibility record.

### 3.2 Primary crosswalk preflight still required — Enterprise ATT&CK v12.1

The paper's Section 4.1 statement is the source-grounded reason to use v12.1 as the primary crosswalk candidate. The official versioned Enterprise v12.1 STIX file must still be retrieved, hashed and parsed. For that exact release, verify that all 120 `A_120` IDs exist as top-level techniques and resolve every sub-technique to exactly one parent via the explicit `subtechnique-of` relationship. Also record any missing, revoked, deprecated, or otherwise unresolved identifiers. No v12.1 STIX artifact or crosswalk has yet been added to the repository, and this plan does not claim the compatibility checks have passed.

Official ChronoCTI paper: https://doi.org/10.1007/s10115-025-02491-6 (Section 4.1, ATT&CK v12.1). The primary versioned ATT&CK input must come from MITRE's official versioned collection: https://github.com/mitre-attack/attack-stix-data.

## 4. Required crosswalk semantics

The crosswalk must be generated from the selected, versioned Enterprise ATT&CK STIX collection.

For each exact ID:

1. Resolve the ID to exactly one Enterprise `attack-pattern` object using its MITRE external reference.
2. Preserve the object's canonical name, STIX object ID, sub-technique flag, and lifecycle flags (including revoked/deprecated status).
3. If it is a top-level technique, its parent-level ID is itself.
4. If it is a sub-technique, derive the parent only from the explicit STIX `subtechnique-of` relationship whose source is that sub-technique object and whose target is its parent technique object.
5. Require exactly one valid parent for a sub-technique. Missing, malformed, or conflicting relationships must fail closed.
6. Verify that the resolved parent is a top-level Enterprise technique object in the same pinned release.
7. Determine `IN_VOCAB` only when the resolved parent ID belongs to the pinned `A_120` list. A valid parent outside `A_120` is `OUT_OF_VOCAB`. An exact ID or parent relationship that cannot be resolved in the chosen release is `UNRESOLVED`; do not silently convert it to out-of-vocabulary.
8. Never infer the parent by truncating the sub-technique ID string. The ID format can be used as a sanity check, but the release's explicit relationship is authoritative.
9. Never auto-remap a revoked, deprecated, renamed, or absent technique to a similarly named current technique. Preserve the original exact ID and its lifecycle status; any replacement/equivalence is a separate reviewed decision.

The `attack_version` field must be defined as the fixed Enterprise ATT&CK release used for this crosswalk (for example, `Enterprise ATT&CK v14.1`). If a report itself explicitly identifies a different ATT&CK version, preserve that source statement separately; do not overload the analysis crosswalk version with it.

## 5. Crosswalk artifact and provenance

Generate a small, deterministic project artifact, for example:

`research/schema_reconstruction/CTI_Annotation_Schema_RECON_v0.1/vocabulary/A_120_Exact_to_Parent_Crosswalk_v0.1.csv`

Minimum fields:

- `attack_release`
- `exact_technique_id`
- `exact_technique_name`
- `stix_object_id`
- `is_subtechnique`
- `parent_technique_id`
- `parent_technique_name`
- `revoked`
- `deprecated`
- `relationship_type`
- `relationship_source_object_id`
- `relationship_target_object_id`

Also record the versioned STIX source URL, retrieval date, source-file SHA-256, crosswalk-generation script version, output SHA-256, record count, and release identifier in a project manifest. Preserve the derived `A_120` artifact and its hash as a separate input. Do not commit the entire upstream STIX collection or raw CTI reports merely to support this crosswalk.

A row should exist for every exact technique/sub-technique ID in the pinned Enterprise release, not just for the 120 parent techniques. This allows a future source-supported sub-technique mapping to be checked without hand-entering a parent.

## 6. Validator and adapter acceptance rules

After the crosswalk is generated and the researcher approves the release, the validator should:

- reject an `attack_version` that differs from the one pinned in the manifest;
- reject an exact ID that does not resolve uniquely in the pinned crosswalk;
- reject an `IN_VOCAB` row with no resolved parent;
- reject a supplied `baseline_parent_technique_id` that differs from the crosswalk-derived parent;
- reject `IN_VOCAB` when the crosswalk-derived parent is not in `A_120`;
- reject `OUT_OF_VOCAB` when the crosswalk-derived parent is in `A_120`;
- reject a parent technique object incorrectly represented as a sub-technique, or vice versa;
- fail closed on missing or multiple `subtechnique-of` relationships;
- verify crosswalk and A_120 hashes before accepting any baseline mapping;
- retain revoked/deprecated status as provenance and apply only a pre-approved rule for whether such an ID may contribute to primary mapping sets.

The adapter must not use a user-supplied parent value until the validator has checked it against the pinned crosswalk. The projection function may continue to consume only accepted, source-supported, in-vocabulary parent IDs after this validation.

## 7. Required synthetic regression tests

At minimum, add tests for:

1. A top-level technique correctly maps to itself.
2. A sub-technique maps to its parent using the explicit STIX relationship.
3. A valid but unrelated `A_120` parent is rejected even though it passes simple vocabulary membership.
4. An exact ID absent from the pinned release is rejected or explicitly unresolved, never guessed.
5. A parent outside `A_120` is correctly labelled out-of-vocabulary.
6. A sub-technique with no `subtechnique-of` relationship fails closed.
7. A sub-technique with conflicting parent relationships fails closed.
8. A technique with a version mismatch is rejected.
9. A crosswalk hash mismatch is rejected.
10. A top-level technique supplied with a different parent ID is rejected.
11. Revoked/deprecated records retain lifecycle status and are handled by the declared policy.
12. Alternative, rejected, unresolved, and workbook-only mappings remain excluded from primary A_120 mapping sets.

Tests must include a deliberately incorrect parent that is nevertheless a member of A_120. That is the regression case the current membership-only validator cannot catch.

## 8. Current conclusion and next implementation order

- The A_120 membership/hash check is implemented.
- Exact-ID existence, pinned-release consistency, and exact-to-parent verification are **not implemented**.
- No official ATT&CK Enterprise crosswalk is currently bundled in RECON v0.1.
- No real report annotations exist, so this gap has not yet produced a known empirical misclassification; it remains a readiness defect.
- No ATT&CK release is approved by this plan.

Next order:

1. Researcher approves or changes the source-aligned Enterprise ATT&CK v12.1 candidate.
2. Obtain and hash the official versioned v12.1 STIX collection.
3. Generate and independently inspect the 768/total-release appropriate exact-to-parent crosswalk from explicit STIX relationships; record its true object counts rather than assuming v14.1 counts apply.
4. Implement validator checks against that pinned crosswalk and `A_120`.
5. Add the full crosswalk regression suite, then run local tests and GitHub Actions.
6. Update the project state and package checksums only after the approved release and crosswalk are frozen.

**Do not freeze RECON or begin formal annotation until this validation gate is complete.**

---
