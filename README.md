# CU-14 seed

A lab repo instance for the cancel-mid-run unit.

## forge 1.0 verification (2026-11-16)

`.github/workflows/forge-lane.yml` is the forge 1.0 lane wrapper (pinned to forge commit
3ea9ed7f) and `.github/workflows/forge-verify.yml` provides the independent `unit`/`lint`
checks forge requires. The older `ci.yml` and `forge-harness.yml` are left unchanged.
Synthetic tasks only.
