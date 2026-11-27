"""Combine what the adapters return into one validated collection."""

import csv
import json
from pathlib import Path

import jsonschema

ROOT = Path(__file__).parent.parent
SCHEMA = ROOT / "schema" / "registry.schema.json"
OVERRIDES = ROOT / "curated" / "overrides.csv"


def read_overrides(path: Path = OVERRIDES) -> list[dict]:
    """Rows of the curated corrections: deployment_id, field, value (JSON)."""
    with open(path, newline="", encoding="utf-8") as file:
        return list(csv.DictReader(file))


def merge(features: list[dict], overrides: list[dict]) -> dict:
    """Apply the curated corrections, sort, and check against the schema.

    A correction always wins over a harvested value. Its value is JSON, so
    numbers, null and lists can be written as such; plain text is kept as text.
    """
    by_id = {}
    for feature in features:
        deployment_id = feature["properties"]["deployment_id"]
        if deployment_id in by_id:
            raise ValueError(f"deployment {deployment_id} comes from two sources")
        by_id[deployment_id] = feature
    for row in overrides:
        if row["deployment_id"] not in by_id:
            # A correction for a radar that is gone is a sign something changed upstream.
            raise ValueError(f"override for unknown deployment {row['deployment_id']}")
        try:
            value = json.loads(row["value"])
        except ValueError:
            value = row["value"]
        by_id[row["deployment_id"]]["properties"][row["field"]] = value
    collection = {
        "type": "FeatureCollection",
        "features": [by_id[key] for key in sorted(by_id)],
    }
    jsonschema.validate(collection, json.loads(SCHEMA.read_text(encoding="utf-8")))
    return collection
