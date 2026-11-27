# Decision log

## 2026-11-27 - Pipeline skeleton: Python adapters, GeoJSON output, OPERA first
**What:** One module per source under `registry/adapters/` (`fetch()` + `parse()`), a merge step with curated overrides and JSON Schema validation, output `dist/v1/registry.json` as GeoJSON with one point per deployment; OPERA is the only adapter. The 2025 Zenodo experiment files are removed.
**Why:** The widget reads GeoJSON directly, and one small file per source keeps adding a source cheap; standard library only for fetching and parsing, as each source is a single small file.
**Rejected:** Separate CSV tables plus a derived JSON (wait until datasets exist); a NEXRAD adapter (on hold, may never be needed for this project).
