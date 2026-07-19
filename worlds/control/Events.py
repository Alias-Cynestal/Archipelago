"""Completion events for missions that gate something else."""

from dataclasses import dataclass
from typing import Dict, List, Optional

from BaseClasses import CollectionRule, Item, Region

from .Items import ControlItem
from .Locations import ControlLocation, LocationData, all_locations, location_table
from .Regions import REGIONS, MissionCondition


@dataclass(frozen=True)
class MissionEvent:
    mission_name: str
    mission_id: int
    event_item_name: str


def _prerequisite_mission_ids() -> List[int]:
    ids: List[int] = []

    def add(mission_id: int) -> None:
        if mission_id not in ids:
            ids.append(mission_id)

    for region in REGIONS:
        for condition in region.conditions:
            if isinstance(condition, MissionCondition):
                add(condition.missionGID)

    for location in all_locations:
        for prerequisite_name in location.prerequisite_missions:
            add(location_table[prerequisite_name].id)

    return ids


def _build_mission_events() -> List[MissionEvent]:
    locations_by_id = {location.id: location for location in all_locations}
    events = []
    for mission_id in _prerequisite_mission_ids():
        mission = locations_by_id[mission_id]
        events.append(MissionEvent(
            mission_name=mission.name,
            mission_id=mission.id,
            event_item_name=f"{mission.name} (Complete)",
        ))
    return events


mission_events: List[MissionEvent] = _build_mission_events()
mission_events_by_mission_id: Dict[int, MissionEvent] = {event.mission_id: event for event in mission_events}
mission_events_by_mission_name: Dict[str, MissionEvent] = {event.mission_name: event for event in mission_events}


def build_prerequisite_rule(location: LocationData, player: int) -> Optional[CollectionRule]:
    """Rule requiring every mission in `location.prerequisite_missions` to be done."""
    if not location.prerequisite_missions:
        return None

    item_names = [
        mission_events_by_mission_name[prerequisite_name].event_item_name
        for prerequisite_name in location.prerequisite_missions
    ]
    return lambda state: state.has_all(item_names, player)


def create_mission_event(region: Region, mission_name: str) -> Item:
    """Places the completion event for `mission_name` in `region`."""
    event = mission_events_by_mission_name[mission_name]

    return region.add_event(
        event.event_item_name,
        event.event_item_name,
        rule=build_prerequisite_rule(location_table[mission_name], region.player),
        location_type=ControlLocation,
        item_type=ControlItem,
    )
