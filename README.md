# registry

Builds the data behind the Aloft radar registry: one GeoJSON file with a point
per deployment (a radar at a place for a period), read by the
[radar registry widget](https://github.com/aloftdata/deploy-map).

## How it works

- `registry/adapters/`: one module per source. Each has `fetch()`, which
  downloads the source, and `parse()`, which turns it into deployments.
- `sources.toml`: the adapters that run.
- `curated/overrides.csv`: corrections by hand (`deployment_id`, `field`,
  `value`). They always win over a harvested value. The value is JSON, so
  `51`, `null` and `["a"]` keep their type; anything else is text.
- `registry/merge.py`: combines the adapters, applies the corrections, sorts,
  and checks the result against `schema/registry.schema.json`.
- `registry/build.py`: runs it all and writes `dist/v1/registry.json`.

The output is deterministic: the same sources give the same file.

## Sources

| Adapter | Source | Gives |
|---|---|---|
| `opera` | [OPERA radar database](https://www.eumetnet.eu/activities/observations-programme/current-activities/opera/) (EUMETNET) | European weather radars |

Rows of the OPERA database without an ODIM code or without a position are
left out.

## Usage

With [uv](https://docs.astral.sh/uv/):

```
uv run python -m registry.build
uv run pytest
```

The tests run on a saved sample of each source (`tests/data/`), never on the
network.

## Adding a source

Add a module to `registry/adapters/` with `fetch()` and `parse()`, a sample and
tests in `tests/`, and its name to `sources.toml`.
