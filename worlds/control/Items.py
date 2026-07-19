"""Loads item data from data/items.csv."""

import csv
import enum
from dataclasses import dataclass
from typing import Dict, List

from BaseClasses import Item, ItemClassification

from . import data


class ControlItem(Item):
    game: str = "Control"


class ItemCategory(enum.Enum):
    clearance = "clearance"
    sector = "sector"
    weapon = "weapon"
    weapon_mod = "weapon_mod"
    player_mod = "player_mod"
    resource = "resource"


DEFAULT_CLASSIFICATION: Dict[ItemCategory, ItemClassification] = {
    ItemCategory.clearance: ItemClassification.progression,
    ItemCategory.sector: ItemClassification.progression,
    ItemCategory.weapon: ItemClassification.useful,
    ItemCategory.weapon_mod: ItemClassification.filler,
    ItemCategory.player_mod: ItemClassification.filler,
    ItemCategory.resource: ItemClassification.filler,
}


@dataclass(frozen=True)
class ItemData:
    id: int
    name: str
    category: ItemCategory
    classification: ItemClassification


def _load_items() -> List[ItemData]:
    try:
        from importlib.resources import files
    except ImportError:
        from importlib_resources import files  # noqa

    items = []
    with files(data).joinpath("items.csv").open(encoding="utf-8") as file:
        for row in csv.DictReader(file):
            category = ItemCategory(row["category"])
            override = row["classification"].strip()
            items.append(ItemData(
                id=int(row["id"]),
                name=row["name"],
                category=category,
                classification=(
                    ItemClassification[override] if override else DEFAULT_CLASSIFICATION[category]
                ),
            ))
    return items


all_items: List[ItemData] = _load_items()
item_table: Dict[str, ItemData] = {item.name: item for item in all_items}
items_by_category: Dict[ItemCategory, List[ItemData]] = {}
for item in all_items:
    items_by_category.setdefault(item.category, []).append(item)

item_name_to_id: Dict[str, int] = {item.name: item.id for item in all_items}

# One copy of this stands in for one clearance level: holding N of them is clearance level N.
PROGRESSIVE_CLEARANCE_NAME = "Progressive Clearance Level"

# The six named levels, i.e. the clearance category minus the progressive item.
clearance_levels: List[ItemData] = [
    item for item in items_by_category[ItemCategory.clearance]
    if item.name != PROGRESSIVE_CLEARANCE_NAME
]

# The base form of each weapon. Upgrade levels are catalogued but stay out of
# the pool, and Grip has no Level 1 entry because the player starts with it.
base_weapons: List[ItemData] = [
    item for item in items_by_category[ItemCategory.weapon] if item.name.endswith("- Level 1")
]

# Every mod, used as the filler remainder once resource percentages are rolled.
mod_names: List[str] = [
    item.name
    for category in (ItemCategory.weapon_mod, ItemCategory.player_mod)
    for item in items_by_category[category]
]
