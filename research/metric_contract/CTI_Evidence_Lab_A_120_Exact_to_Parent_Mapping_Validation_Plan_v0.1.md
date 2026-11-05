# CTI Evidence Lab — A_120 Exact-to-Parent Mapping Validation Plan v0.1

**Prepared:** 4 November 2026  
**Status:** Enterprise ATT&CK v12.1 crosswalk generated, committed and integrated into the RECON v0.1 validator. The committed CSV was independently parsed and structurally checked on 5 November 2026; its SHA-256 was independently recomputed and matched the manifest. The complete 63-test RECON suite and root CI checks passed in GitHub Actions run [#41974194194](https://github.com/sanketnichit/cti-evidence-lab/actions/runs/41974194194) on commit `76f80e6341a57471588bc2b22d7d39eacf02c489`. This closes the crosswalk implementation gate, but it does not approve/freeze the reconstructed schema or establish semantic correctness of any report annotation.  
**Scope:** Validate the relationship between an exact ATT&CK technique/sub-technique ID and the parent-level ID supplied for the ChronoCTI `A_120` projection.

## 1. What the technical gate must protect

The selected A_120 vocabulary alone cannot verify a sub-technique's parent. A valid parent ID that happens to belong to A_120 may still be the wrong parent for a given exact technique. The crosswalk therefore has to resolve every exact technique ID against the pinned Enterprise ATT&CK release and use the explicit STIX relationship for sub-techniques.

That check is now implemented at two levels:

- The builder resolves exact technique objects, uses explicit subtechnique-of relationships, fails closed when a sub-technique has zero or multiple parents, and verifies the exact v12.1 source bytes against both recorded hashes before generation.
- The RECON validator verifies the crosswalk file and manifest, checks release and row structure, verifies exact-to-parent relationships, then checks each accepted mapping against the resolved exact ID, canonical name, parent, vocabulary membership and lifecycle flags.

The implementation prevents a mapping from passing merely because its supplied parent belongs to A_120. It does not decide whether a report actually supports a particular technique: that remains a source-grounded human annotation decision. The release remains a working project default, not an approved/frozen protocol decision.

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

**The v12.1 release choice is adopted as the working project default, not as a completed protocol/schema freeze.** The exact official versioned Enterprise STIX collection was obtained and checked against the recorded Git blob SHA-1 and SHA-256. The builder refuses to generate from bytes that do not match those pins. The full STIX collection remains outside Git; the crosswalk manifest records the source identity and the generated output hash.

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

### 3.2 Generated and independently inspected crosswalk — Enterprise ATT&CK v12.1 (5 November 2026)

The paper's Section 4.1 statement is the source-grounded reason for the adopted v12.1 working choice. The hash-verified v12.1 source was used to generate the committed exact-to-parent crosswalk. The committed file and manifest were then read back from main and independently checked.

**Exact source identity used for generation**

- Versioned file: enterprise-attack/enterprise-attack-12.1.json in mitre-attack/attack-stix-data.
- Git blob SHA-1: 7a99efb3a8c89b06dd9db1a9a17e4201160ac4ee.
- Retrieved-file SHA-256: e84679af4bc46bba2ba92f60182101f146d5b966898e47924de7321e6bffeaa1.
- STIX bundle ID: bundle--19413d5e-67e5-4a48-a4c8-afb06b7954de.
- Collection metadata: Enterprise ATT&CK, version 12.1, modified 2022-11-08T14:00:00.188Z.
- UTF-8 file size used for the SHA-256 calculation: 38,207,821 bytes.

**Crosswalk inspection results**

| Check | Result |
|---|---:|
| Exact technique/sub-technique rows | 737 |
| Unique exact ATT&CK IDs | 737 |
| Top-level techniques | 333 |
| Sub-techniques | 404 |
| Explicit subtechnique-of relationships | 404 |
| Sub-techniques resolving to an existing top-level parent row | 404/404 |
| Duplicate exact IDs | 0 |
| ChronoCTI A_120 IDs found exactly once | 120/120 |
| A_120 IDs represented as top-level self-parent mappings | 120/120 |
| parent_in_A_120 flags inconsistent with resolved parent membership | 0 |
| Revoked/deprecated flags among the 120 A_120 objects | 0 |

The inspection also confirmed that all 737 rows declare Enterprise ATT&CK v12.1; top-level rows use relationship_type=self and point to themselves; sub-technique rows use relationship_type=subtechnique-of and resolve through the target STIX object ID to a top-level parent row. The crosswalk CSV's independently recomputed SHA-256 is f449ff8bd1551b6d6656d2f25a82b7c55a0b134bbecd4215f0f10330ec85be29, matching the manifest.

The full STIX bundle has not been committed to Git. The crosswalk, manifest, builder, validator and regression tests are committed in RECON v0.1. The v12.1 release remains a working default; protocol/schema approval and freeze remain separate.

Official ChronoCTI paper: https://doi.org/10.1007/s10115-025-02491-6 (Section 4.1, ATT&CK v12.1). Official ATT&CK source: https://github.com/mitre-attack/attack-stix-data (the exact source identity is recorded by Git blob SHA-1 and retrieved-byte SHA-256).

## 4. Implemented crosswalk semantics

The builder and committed crosswalk implement the following semantics against the selected, versioned Enterprise ATT&CK STIX collection.

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

The `attack_version` field for accepted primary mapping rows must equal the fixed analysis crosswalk release, `Enterprise ATT&CK v12.1`. If a report itself explicitly identifies a different ATT&CK version, preserve that source statement separately; do not overload the analysis crosswalk version with it. If a report itself explicitly identifies a different ATT&CK version, preserve that source statement separately; do not overload the analysis crosswalk version with it.

## 5. Generated crosswalk artifact and provenance

The generated, committed project artifact is:

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

The adjacent `.manifest.json` records the versioned STIX source URL/path, source Git blob SHA-1, source-file SHA-256 and byte size, builder path, output SHA-256, record count, release identifier, generation counts, and the derived `A_120` path/hash as a separate input. The exact output SHA-256 is `f449ff8bd1551b6d6656d2f25a82b7c55a0b134bbecd4215f0f10330ec85be29`; an independent readback computation matched it. Do not commit the entire upstream STIX collection or raw CTI reports merely to support this crosswalk.

A row should exist for every exact technique/sub-technique ID in the pinned Enterprise release, not just for the 120 parent techniques. This allows a future source-supported sub-technique mapping to be checked without hand-entering a parent.

## 6. Validator and adapter checks now implemented

The RECON validator now performs the following checks before accepting primary mapping rows:

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

The validator also requires the accepted mapping's exact technique name to match the pinned v12.1 name, its parent ID to match the crosswalk-derived parent, and its IN_VOCAB/OUT_OF_VOCAB status to agree with the resolved parent. It excludes revoked/deprecated mappings from primary A_120 unless separately resolved. The adapter consumes only validated, eligible rows from the selected report/annotator/pass partition after explicit lock confirmation and a matching partition digest. These are structural checks; they do not replace source-based mapping judgment.

## 7. Synthetic regression coverage

The RECON package has 36 validator tests, 16 projection-metric tests and 11 annotation-to-projection adapter tests (63 total). The validator suite includes the following crosswalk-specific regression cases:

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

## 8. Current conclusion and remaining work

### Completed technical work

- The selected A_120 artifact is pinned to the ChronoCTI source commit/blob and its SHA-256.
- The official Enterprise ATT&CK v12.1 STIX input is pinned by both Git blob SHA-1 and retrieved-byte SHA-256. The builder verifies both before generating output.
- The 737-row exact-to-parent crosswalk and manifest are committed in RECON v0.1. Its output SHA-256 was independently recomputed and matched the manifest.
- Independent structural inspection confirms the 333/404 split, unique exact IDs, explicit parent resolution for all 404 sub-techniques, 120/120 top-level self-parent mappings for A_120, and zero parent_in_A_120 flag mismatches.
- The RECON validator checks the pinned crosswalk and each accepted mapping row against it. The synthetic tests include the adversarial case of a wrong but valid A_120 parent.
- RECON's 63 synthetic tests (36 validator, 16 projection, 11 adapter) and the root test suite passed in GitHub Actions run [#41974194194](https://github.com/sanketnichit/cti-evidence-lab/actions/runs/41974194194).

### Remaining limitations and decisions

- The full upstream STIX bundle is not stored in Git; source identity is preserved by the exact versioned path and hash pins, and the builder fails closed if the retrieved bytes change.
- The original Protocol v0.4.1 and Schema v0.4.2 files remain unrecovered. RECON v0.1 is a reconstruction and is not approved/frozen.
- No real report has been mapped or passed through the validator. The mapping checks validate consistency with the pinned taxonomy, not whether a report's evidence supports the mapping.
- The lifecycle rule remains conservative: revoked/deprecated IDs stay visible in the crosswalk and exact mapping record, but cannot enter primary A_120 without separate resolution.
- No human annotation, real-report projection result, IAA measurement or empirical finding exists.

Next work is therefore research governance, not more crosswalk engineering: resolve the source-scope and local-use decisions, approve or revise the remaining protocol choices, then freeze a clearly versioned new protocol/schema package before the first human annotation. Do not treat synthetic test success as evidence of annotation quality or empirical research progress.

---
