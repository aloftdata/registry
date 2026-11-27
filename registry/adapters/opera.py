"""European weather radars, from the OPERA radar database (EUMETNET)."""

import json
import urllib.request

URL = (
    "https://www.eumetnet.eu/wp-content/themes/aeron-child/observations-programme/"
    "current-activities/opera/database/OPERA_Database/OPERA_RADARS_DB.json"
)

POLARIZATION = {"S": "single", "D": "dual"}


def fetch() -> bytes:
    """Download the database: one JSON list, every value a string."""
    # The server refuses requests without a user agent.
    request = urllib.request.Request(URL, headers={"User-Agent": "aloft-registry"})
    with urllib.request.urlopen(request, timeout=60) as response:
        return response.read()


def _number(text: str) -> float | int | None:
    """A number from the database's text, None when empty or not a number."""
    try:
        value = float(text)
    except ValueError:
        return None
    return int(value) if value.is_integer() else value


def parse(raw: bytes) -> list[dict]:
    """Turn the database into deployments (GeoJSON features).

    Rows without an ODIM code or without a position are left out: the code is
    the radar's identity, and a point needs a place on the map.

    ponytail: one deployment per radar, since the database has one row per
    code. Replaced or moved radars need the archive database or curated rows.
    """
    features = []
    for row in json.loads(raw):
        code = row["odimcode"].strip()
        lon, lat = _number(row["longitude"]), _number(row["latitude"])
        if not code or lon is None or lat is None:
            continue
        features.append(
            {
                "type": "Feature",
                "geometry": {"type": "Point", "coordinates": [lon, lat]},
                "properties": {
                    "deployment_id": f"{code}-1",
                    "radar_id": code,
                    "alt_codes": [row["wmocode"].strip()] if row["wmocode"].strip() else [],
                    "type": "weather",
                    "source": "opera",
                    "country": row["country"].strip(),
                    "location": row["location"].strip(),
                    "start": row["startyear"].strip() or None,
                    "end": None,
                    "band": row["band"].strip() or None,
                    "frequency": _number(row["frequency"]),
                    "polarization": POLARIZATION.get(row["polarization"].strip()),
                    "gain": _number(row["gain"]),
                    "beamwidth": _number(row["beam"]),
                    "antenna_diameter": _number(row["diameterantenna"]),
                    "max_range": _number(row["maxrange"]),
                    "elevation": _number(row["heightofstation"]),
                    "antenna_height": _number(row["heightantenna"]),
                    "datasets": [],
                },
            }
        )
    return features
