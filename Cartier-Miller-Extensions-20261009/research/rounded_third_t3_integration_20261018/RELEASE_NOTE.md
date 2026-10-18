# Release note for this folder (added 18 October 2026)

## Received files

| File | SHA-256 | Use here |
|---|---|---|
| `Cartier_Miller_Rounded_Third_GitHub_Handover_20261018.md` | b62fd9cb43c5aa7123b114ff9fb34ec7e0c13f37025d527f3efc25f12ef59aed | Kept verbatim |
| `Cartier_Miller_T3_Integration_20261018.zip` (5,872,832 bytes uncompressed, 216 files) | 0af630b767ab93a9eebeaa6d09d5eaf2d74ba69475764676b6844d108bfa986a | Unpacked to `package/cm_r3_integration_20261018/` |
| `Cartier_Miller_T3_Integration_REPORT_20261018.md` | 00a73b60ed6a1f673330876d7b882760b9ef3390084dbd9cdb2f14dd52fce2d1 (matches the handover) | Byte-identical to `package/cm_r3_integration_20261018/REPORT.md`, so not duplicated |
| `Atkin_Endpoint_Round3_20261018.zip` (581,320 bytes) | 433b88da7c49d4ac7b65c4a1c31ca40bd42de22737634cd2e0b4f3ca999192d6 | Source of one restored file; not otherwise redistributed |

## Changes from the received package

Apart from these two changes, the package is byte-for-byte as received.

1. **Restored: `vendor/atkin_r3/MANIFEST.json`.**
   - The received integration zip omitted this file, although both `evidence/FREEZE.json` and `provenance/VENDOR_HASHES.json` list it with SHA-256 e3a610f78376c06f3661ed55c0d48108110bee8441b00bc607ece26fffe01129. Without it, the package's own `audit.py` failed.
   - It was taken from `Atkin_Endpoint_Round3_20261018.zip`, where `atkin_round3_20261018/MANIFEST.json` has exactly that hash. That archive's other 106 files are byte-identical to the package's `vendor/atkin_r3/`.
   - With the file restored, `audit.py` passed: 196 freeze, 187 vendor and 215 manifest entries.
   - The zip supplied for this purpose does not have the archive-level hash and size that `provenance/INPUT_ARCHIVES.json` records for `Atkin_Endpoint_Round3_20261018.zip` (00ea2e688c144f0df77f0f2a50b88d899581237ead77fc2046e86653a948417f, 583,371 bytes). Its contents nevertheless match every recorded file hash. The difference is in the zip container only, most likely a re-pack. The recorded value is left unchanged.
2. **Not redistributed: `vendor/atkin_r3/r3/sources/PARI_2.17.2_installed_doc.json`.**
   - The file is 6,752 bytes, with SHA-256 9e1ffb9d88273dc61d0001ecfa48094f24a982e4a92e82fbd39dd60c67c2ad84.
   - It is a verbatim copy of the PARI/GP 2.17.2 documentation for `qfbclassno` and `quadclassunit`. PARI/GP is GPL-licensed, and this repository does not redistribute GPL material.
   - No code in the package reads the file. The integrated T3 route does not use PARI; the file documented an earlier class-number-dependent route.
   - The now-empty `sources/` directory is absent.

## How to verify

The package's unmodified `audit.py` now stops at the excluded PARI file. That is expected, and the frozen script is deliberately left unedited. Use instead:

```console
python verify_import.py
```

It runs the same three hash lists, allows only that one named file (by hash) to be absent, and exits 1 on anything else: a mismatch, another missing file, or an uncovered extra file. Running it against altered copies (an edited file, an added file, a removed manifest) made it fail in each case.

## Other notes

- **`.log` files:** the package's ten `.log` evidence files are listed in its manifests. They are committed even though the repository's `.gitignore` ignores `*.log`.
- **Absolute paths:** `vendor/atkin_r3/r3/evidence/CONFIRMATION_R3.log` and `CONFIRMATION_R3_run1_FAILED.log` record paths from the producing environment. They are left unchanged as hashed evidence.
- **Windows scripts:** the three `.bat` files under `vendor/boundary/` are retained Windows helper scripts from the workbench release, kept as received. The integration itself is tested only on Linux.
- **Licence screen:** the screen found no other GPL- or LGPL-licensed text and no binaries. The FLINT and GMP libraries are installed through pip (`requirements.txt`), not shipped.
- **Repository licence:** the repository's MIT licence covers this folder (see the Extensions folder's `LICENSE`).

## Reruns

The reruns are recorded in `repository_rerun_20261018/` and summarized in `README.md`. The benchmark, survey and confirmation scripts were not rerun, because they overwrite frozen evidence.
