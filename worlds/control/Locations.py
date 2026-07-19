"""Loads location data from data/locations.csv"""

import csv
import enum
from dataclasses import dataclass
from typing import Dict, List, Tuple

from BaseClasses import Location

from . import data


class ControlLocation(Location):
    game: str = "Control"


class LocationCategory(enum.Enum):
    location = "location"
    control_point = "control_point"
    mission = "mission"
    sector = "sector"


@dataclass(frozen=True)
class LocationData:
    id: int
    name: str
    category: LocationCategory
    region: str = ""
    prerequisite_missions: Tuple[str, ...] = ()


def _parse_prerequisite_missions(value: str) -> Tuple[str, ...]:
    return tuple(name.strip() for name in value.split(";") if name.strip())


def _load_locations() -> List[LocationData]:
    try:
        from importlib.resources import files
    except ImportError:
        from importlib_resources import files  # noqa

    locations = []
    with files(data).joinpath("locations.csv").open(encoding="utf-8") as file:
        for row in csv.DictReader(file):
            locations.append(LocationData(
                id=int(row["id"]),
                name=row["name"],
                category=LocationCategory(row["category"]),
                region=row["region"],
                prerequisite_missions=_parse_prerequisite_missions(row["prerequisite_mission"]),
            ))
    return locations


all_locations: List[LocationData] = _load_locations()
location_table: Dict[str, LocationData] = {location.name: location for location in all_locations}
locations_by_category: Dict[LocationCategory, List[LocationData]] = {}
for location in all_locations:
    locations_by_category.setdefault(location.category, []).append(location)

location_name_to_id: Dict[str, int] = {location.name: location.id for location in all_locations}
