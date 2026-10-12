# Release note for this folder (added 12 October 2026)

This folder is the ordinary Cartier-slope feasibility package, revision 2. It was received as `Ordinary_K_Feasibility_20261012_rev2.zip` (SHA-256 bfe5872d4a2aa8a573bcc5ab94d65c6137fddc79c618c784765f0043fcc5e1b4). It is reproduced here unchanged. Only this note was added; it is not covered by the package's own `SHA256SUMS.json`, which still verifies all 99 package files. The release-level `SHA256SUMS.json` covers this note too.

Start with `README.md`, then `Ordinary_K_Feasibility_Note_20261012_rev2.md` and `CHANGES.md`.

Three points for readers of the release:

1. **Scope of the result.** The study is a feasibility record, not a new algorithm. It derives Theorem A (Frobenius mod p is [[0, −β],[0, H]] in the low-pole basis) and Lemma B (κ ≡ σ_C/p for the canonical-subgroup kernel sum of any ordinary lift). Lemma B awaits specialist review. The study also shows that the constructions it examined give no cheaper complete algorithm for κ = β/H. It proves no lower bound and claims no speed-up or novelty. Much of it is probably classical; see Katz (2019) and Mazur–Stein–Tate (2006), as cited in the note.
2. **Reproduction.** Rerunning the pilot needs the received `Ordinary_K_Research_Handover_20261012` (for `ordinary_targets.csv`, `same_trace_different_slopes.json` and `retained_CM_tables.json`). That handover is not redistributed in this release. The pilot's other dependencies correspond to code already in this release: `research/depth_three_recognition_20261007/` and its sibling recognizers, and `research/cm_cartier_comparison_20261012/`. The recorded outputs in `ordinary_k_pilot/results/` and `independent_check/results_full/` are the evidence; the scripts exit nonzero on any failure.
3. **Recorded paths.** Several result JSONs record absolute paths from the environment in which they were produced (`/home/claude/...`). They are left unchanged, because they are hashed evidence. The `.log` files are part of the package manifest and are committed even though the repository's `.gitignore` ignores `*.log`.

The nested ZIPs under `evidence/` are earlier revisions of this package and the external review's evidence bundle. They were checked before release and contain no manuscript, GPL-licensed code or copyrighted scans.
