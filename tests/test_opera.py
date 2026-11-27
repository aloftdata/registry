import json
from pathlib import Path

from registry.adapters import opera

SAMPLE = (Path(__file__).parent / "data" / "opera_sample.json").read_bytes()


def by_id(features):
    return {feature["properties"]["deployment_id"]: feature for feature in features}


def test_row_becomes_a_deployment_with_numbers_and_units():
    """The database stores every value as text and uses its own field names.
    The registry panel needs numbers and the registry's names, with longitude
    first as GeoJSON requires: a swapped pair would put the radar in the sea.
    """
    feature = by_id(opera.parse(SAMPLE))["nldhl-1"]
    assert feature["geometry"] == {"type": "Point", "coordinates": [4.7906, 52.9528]}
    properties = feature["properties"]
    assert properties["radar_id"] == "nldhl"
    assert properties["alt_codes"] == ["6234"]
    assert properties["type"] == "weather"
    assert properties["location"] == "Den Helder"
    assert properties["polarization"] == "dual"
    assert isinstance(properties["frequency"], float)
    assert isinstance(properties["max_range"], int)


def test_rows_without_code_or_position_are_left_out():
    """Some rows have no ODIM code (no identity to link datasets to) and the
    mobile radars have no longitude. Neither can be a point in the registry,
    and a crash on them would stop the whole nightly build.
    """
    rows = json.loads(SAMPLE)
    assert any(not row["odimcode"] for row in rows)
    assert any(not row["longitude"] for row in rows)
    features = opera.parse(SAMPLE)
    assert sorted(by_id(features)) == ["bezav-1", "dkrom-1", "nldhl-1"]


def test_empty_value_becomes_null():
    """An empty value in the database must stay "not known" (null), not become
    zero: a site at 0 m or an antenna of 0 m would be shown as a fact.
    """
    blank = json.loads(SAMPLE)[0] | {"heightofstation": "", "diameterantenna": " "}
    properties = opera.parse(json.dumps([blank]).encode())[0]["properties"]
    assert properties["elevation"] is None
    assert properties["antenna_diameter"] is None
