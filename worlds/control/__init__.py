from typing import Callable, Dict, List, Optional

from BaseClasses import CollectionState, Item, Region, Tutorial
from worlds.AutoWorld import World, WebWorld
from worlds.control import Events, Items, Locations
from worlds.control.Items import ControlItem, ItemCategory
from worlds.control.Locations import ControlLocation, LocationData
from worlds.control.Options import ControlOptions, option_groups
from worlds.control.Regions import (
    REGIONS,
    ClearanceCondition,
    Condition,
    MissionCondition,
    SectorCondition,
)

# Maps each filler Range option to the resource it controls. Every resource in
# items.csv has an entry here; whatever the percentages leave under 100 is the
# chance of a mod instead (see get_filler_item_name).
FILLER_RESOURCE_OPTIONS: Dict[str, str] = {
    "astral_blip": "Resource: Astral Blip",
    "corrupted_sample": "Resource: Corrupted Sample",
    "entropic_echo": "Resource: Entropic Echo",
    "hidden_trend": "Resource: Hidden Trend",
    "house_memory": "Resource: House Memory",
    "intrusive_pattern": "Resource: Intrusive Pattern",
    "remote_thought": "Resource: Remote Thought",
    "ritual_impulse": "Resource: Ritual Impulse",
    "threshold_remnant": "Resource: Threshold Remnant",
    "undefined_reading": "Resource: Undefined Reading",
    "untapped_potential": "Resource: Untapped Potential",
}


class ControlWebWorld(WebWorld):
    theme = "stone"

    setup_en = Tutorial(
        tutorial_name="Start Guide",
        description="A guide to playing Control in Archipelago.",
        language="English",
        file_name="en_control.md",
        link="guide/en",
        authors=["Cynestal"]
    )

    setup_fr = Tutorial(
        tutorial_name="Tutoriel",
        description="Un guide pour jouer à Control dans Archipelago.",
        language="French",
        file_name="fr_control.md",
        link="guide/fr",
        authors=["Cynestal"]
    )

    tutorials = [setup_en, setup_fr]

    option_groups = option_groups

class ControlWorld(World):
    game = "Control"
    item_name_to_id = Items.item_name_to_id
    location_name_to_id = Locations.location_name_to_id
    web = ControlWebWorld()
    options: ControlOptions
    options_dataclass = ControlOptions

    def create_regions(self) -> None:
        regions: Dict[str, Region] = {"Menu": self.create_region("Menu")}
        for region_data in REGIONS:
            regions[region_data.name] = self.create_region(region_data.name)

        locations_by_region: Dict[str, List[LocationData]] = {}
        for location in Locations.all_locations:
            locations_by_region.setdefault(location.region, []).append(location)

        for region_name, region_locations in locations_by_region.items():
            regions[region_name].add_locations(
                {location.name: location.id for location in region_locations},
                ControlLocation,
            )

        for region_data in REGIONS:
            regions[region_data.parent].connect(
                regions[region_data.name],
                rule=self._build_rule(region_data.conditions),
            )

        for mission_name in Events.mission_events_by_mission_name:
            mission = Locations.location_table[mission_name]
            Events.create_mission_event(regions[mission.region], mission_name)

        for location_data in Locations.all_locations:
            rule = Events.build_prerequisite_rule(location_data, self.player)
            if rule is not None:
                self.set_rule(self.get_location(location_data.name), rule)

    def create_region(self, region_name: str) -> Region:
        region = Region(region_name, self.player, self.multiworld)
        self.multiworld.regions.append(region)
        return region

    def _build_rule(self, conditions: List[Condition]) -> Optional[Callable[[CollectionState], bool]]:
        """
        Compiles a region's Condition list into a single access rule.
        """
        required_counts: Dict[str, int] = {}
        for condition in conditions:
            if condition is None:
                continue
            elif isinstance(condition, ClearanceCondition):
                if not self.options.clearance_level_unlocks:
                    raise NotImplementedError(
                        "clearance_level_unlocks must be on: the story-progress path needs a "
                        "mapping of which mission grants each clearance level, which does not exist yet."
                    )
                if self.options.progressive_clearance_levels:
                    # N upgrades is clearance level N, so the deepest level asked
                    # for is the number of copies needed.
                    required_counts[Items.PROGRESSIVE_CLEARANCE_NAME] = max(
                        required_counts.get(Items.PROGRESSIVE_CLEARANCE_NAME, 0),
                        condition.clearanceLevel,
                    )
                else:
                    required_counts[f"Clearance Level {condition.clearanceLevel}"] = 1
            elif isinstance(condition, SectorCondition):
                if not self.options.sector_unlocks:
                    raise NotImplementedError(
                        "sector_unlocks must be on: the story-progress path needs a mapping of "
                        "which mission grants each sector, which does not exist yet."
                    )
                required_counts[condition.sectorName] = 1
            elif isinstance(condition, MissionCondition):
                required_counts[Events.mission_events_by_mission_id[condition.missionGID].event_item_name] = 1

        if not required_counts:
            return None
        return lambda state: state.has_all_counts(required_counts, self.player)

    def create_item(self, name: str) -> Item:
        item = Items.item_table[name]
        return ControlItem(name, item.classification, item.id, self.player)

    def get_filler_item_name(self) -> str:
        """
        Rolls one filler item: a resource per its percentage option, else a mod.
        """
        roll = self.random.random() * 100
        cumulative = 0.0
        for option_key, item_name in FILLER_RESOURCE_OPTIONS.items():
            cumulative += getattr(self.options, option_key).value
            if roll < cumulative:
                return item_name
        return self.random.choice(Items.mod_names)

    def create_items(self) -> None:
        pool: List[Item] = []

        if self.options.clearance_level_unlocks:
            if self.options.progressive_clearance_levels:
                pool += [
                    self.create_item(Items.PROGRESSIVE_CLEARANCE_NAME)
                    for _ in range(len(Items.clearance_levels))
                ]
            else:
                pool += [self.create_item(item.name) for item in Items.clearance_levels]
        if self.options.sector_unlocks:
            pool += [self.create_item(item.name) for item in Items.items_by_category[ItemCategory.sector]]

        pool += [self.create_item(item.name) for item in Items.base_weapons]

        remaining = len(self.multiworld.get_unfilled_locations(self.player)) - len(pool)
        pool += [self.create_item(self.get_filler_item_name()) for _ in range(remaining)]

        self.multiworld.itempool += pool
