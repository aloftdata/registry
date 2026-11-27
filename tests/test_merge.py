import jsonschema
import pytest

from registry.adapters import opera
from registry.build import dump
from registry.merge import merge

from test_opera import SAMPLE


def test_override_wins_and_keeps_its_type():
    """Curated corrections are the answer to patchy sources, so they must
    replace the harvested value. Values are read as JSON, so a number stays a
    number and the schema still accepts the result.
    """
    overrides = [
        {"deployment_id": "nldhl-1", "field": "elevation", "value": "51"},
        {"deployment_id": "nldhl-1", "field": "location", "value": "Den Helder (new)"},
    ]
    collection = merge(opera.parse(SAMPLE), overrides)
    properties = collection["features"][-1]["properties"]
    assert properties["elevation"] == 51
    assert properties["location"] == "Den Helder (new)"


def test_override_for_unknown_deployment_fails():
    """A correction whose radar no longer exists means the source changed (a
    renamed code, a removed radar). Ignoring it silently would drop the
    correction without anyone noticing.
    """
    with pytest.raises(ValueError, match="unknown deployment"):
        merge(opera.parse(SAMPLE), [{"deployment_id": "xx-1", "field": "end", "value": "2020"}])


def test_invalid_value_is_rejected_by_the_schema():
    """The schema is the contract with the widget. A value outside it, here a
    radar type the widget has no label or colour for, must stop the build.
    """
    with pytest.raises(jsonschema.ValidationError):
        merge(opera.parse(SAMPLE), [{"deployment_id": "nldhl-1", "field": "type", "value": "wether"}])


def test_output_does_not_depend_on_input_order():
    """The nightly build must give the same file when nothing changed, whatever
    order the source lists its radars in: otherwise every night shows a diff.
    """
    features = opera.parse(SAMPLE)
    assert dump(merge(features, [])) == dump(merge(features[::-1], []))
