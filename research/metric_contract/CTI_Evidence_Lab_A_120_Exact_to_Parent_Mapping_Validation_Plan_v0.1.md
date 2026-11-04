# CTI Evidence Lab — A_120 Exact-to-Parent Mapping Validation Plan v0.1

**Prepared:** 4 November 2026  
**Status:** Technical audit and implementation plan. Enterprise ATT&CK v12.1 was selected as the working crosswalk release under delegated project direction on 4 November 2026. The exact STIX input and generated crosswalk are not yet frozen or integrated.  
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

## 3. ATT&CK release selection — working default selected, source input not frozen

**Selected working analysis release: Enterprise ATT&CK v12.1.**

Rationale: ChronoCTI's published paper explicitly names v12.1 in Section 4.1. Using the same named release is the most defensible choice for a historically aligned reconstruction of the `A_120` parent vocabulary. This does not mean the derived `A_120` list alone is a v12.1 crosswalk; exact-to-parent relationships still require verification from the official versioned STIX collection.

Enterprise v14.1 has been inspected separately as a non-primary compatibility preflight (Section 3.1). It may be used later as a taxonomy-version sensitivity comparison, but it must not silently replace v12.1 in the primary comparison.

**The v12.1 release choice is adopted as the working project default, not as a completed technical freeze.** Obtain the exact official versioned Enterprise STIX collection, verify it against the recorded Git blob and SHA-256, and record an immutable source identity and the retrieval date. The crosswalk must be generated from those exact bytes. Do not use a moving `master` reference as the source for the frozen crosswalk.

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

### 3.2 Non-freezing compatibility preflight — Enterprise ATT&CK v12.1 (4 November 2026)

The paper's Section 4.1 statement is the source-grounded reason for the adopted v12.1 working choice. A non-freezing structural preflight has been run against the official versioned Enterprise v12.1 STIX collection. This establishes compatibility of the selected `A_120` vocabulary with v12.1; it does not create a final crosswalk or freeze a schema input.

**Exact source identity used for this preflight**

- Versioned file: `enterprise-attack/enterprise-attack-12.1.json` in `mitre-attack/attack-stix-data`.
- Git blob SHA-1: `7a99efb3a8c89b06dd9db1a9a17e4201160ac4ee`.
- Retrieved-file SHA-256: `ad169215c75f94271124d3888791323e43aaedad2755f7d7eea8d4185af7f536`.
- STIX bundle ID: `bundle--19413d5e-67e5-4a48-a4c8-afb06b7954de`.
- Collection metadata: `Enterprise ATT&CK`, version `12.1`, modified `2022-11-08T14:00:00.188Z`.
- UTF-8 file size used for the SHA-256 calculation: 38,207,821 bytes.

**Compatibility preflight results**

| Check | Result |
|---|---:|
| Enterprise `attack-pattern` objects | 737 |
| Unique exact ATT&CK technique IDs | 737 |
| Top-level techniques | 333 |
| Sub-techniques | 404 |
| Explicit `subtechnique-of` relationships | 404 |
| Sub-techniques with exactly one valid top-level parent | 404 |
| Sub-techniques with missing, multiple or invalid parents | 0 |
| ChronoCTI `A_120` IDs found exactly once | 120/120 |
| `A_120` IDs represented as top-level techniques | 120/120 |
| `A_120` IDs missing, duplicated or unexpectedly sub-techniques | 0 |
| `A_120` objects with revoked/deprecated flags | 0 |

Interpretation: all 120 selected ChronoCTI IDs exist exactly once as top-level Enterprise ATT&CK v12.1 techniques. All 404 sub-techniques in the release have one explicit, valid top-level parent relationship. This supports v12.1 as a structurally suitable, source-aligned working release for the primary crosswalk. The exact-to-parent crosswalk has not yet been generated and independently inspected.

The full STIX bundle has not been committed to the repository. No v12.1 crosswalk has been added to RECON, and the `attack_version`/release manifest rule remains to be implemented and tested. The release selection is a working default; the technical freeze is still open.

Official ChronoCTI paper: https://doi.org/10.1007/s10115-025-02491-6 (Section 4.1, ATT&CK v12.1). Official ATT&CK source: https://github.com/mitre-attack/attack-stix-data (the immutable file identity above is recorded by Git blob SHA-1 and retrieved-file SHA-256).

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
- Enterprise ATT&CK v12.1 is selected as the working analysis release; the immutable file verification and crosswalk integration are still outstanding.

Next order:

1. Run `python scripts/build_attack_crosswalk.py --download`. The script downloads the official versioned Enterprise v12.1 file to the system temporary directory (unless `--stix` supplies a path), and refuses to proceed unless both the recorded Git blob SHA-1 and SHA-256 match.
2. Inspect the generated 737-row exact-to-parent crosswalk and manifest, confirming the 333/404 top-level/sub-technique split, all 404 explicit parent relationships, and 120/120 `A_120` top-level entries. The raw STIX bundle remains outside Git.
4. Implement validator checks against that pinned crosswalk and `A_120`.
5. Add the full crosswalk regression suite, then run local tests and GitHub Actions.
6. Update the project state and package checksums only after the approved release and crosswalk are frozen.

**Do not freeze RECON or begin formal annotation until this validation gate is complete.**

---
