"""Build dist/v1/registry.json: run the adapters, merge, write.

Usage: python -m registry.build
"""

import importlib
import json
import tomllib
from pathlib import Path

from registry.merge import ROOT, merge, read_overrides

OUTPUT = ROOT / "dist" / "v1" / "registry.json"


def dump(collection: dict) -> str:
    """The same text for the same data: a run without changes gives no diff."""
    return json.dumps(collection, indent=2, sort_keys=True, ensure_ascii=False) + "\n"


def main() -> None:
    config = tomllib.loads((ROOT / "sources.toml").read_text(encoding="utf-8"))
    features = []
    for name in config["adapters"]:
        adapter = importlib.import_module(f"registry.adapters.{name}")
        found = adapter.parse(adapter.fetch())
        print(f"{name}: {len(found)} deployments")
        features += found
    collection = merge(features, read_overrides())
    OUTPUT.parent.mkdir(parents=True, exist_ok=True)
    OUTPUT.write_text(dump(collection), encoding="utf-8")
    print(f"wrote {OUTPUT.relative_to(ROOT)}: {len(collection['features'])} deployments")


if __name__ == "__main__":
    main()
