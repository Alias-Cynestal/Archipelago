from dataclasses import dataclass
from typing import List, Union


@dataclass(frozen=True)
class ClearanceCondition:
    clearanceLevel: int

@dataclass(frozen=True)
class SectorCondition:
    """Resolves to state.has(sectorName, player)"""
    sectorName: str

@dataclass(frozen=True)
class MissionCondition:
    """Resolves to state.has(Events.mission_events_by_mission_id[missionGID].event_item_name, player)."""
    missionGID: int

Condition = Union[ClearanceCondition, SectorCondition, MissionCondition, None]

@dataclass(frozen=True)
class RegionData:
    name: str
    parent: str
    conditions: List[Condition]

REGIONS = [
    RegionData(
        "Executive Sector, Clearance 0",
        "Menu",
        [
            None
        ]
    ),
    RegionData(
        "Executive Sector, Clearance 1",
        "Executive Sector, Clearance 0",
        [
            ClearanceCondition(1),
        ]
    ),
    RegionData(
        "Executive Sector, Clearance 2",
        "Executive Sector, Clearance 1",
        [
            ClearanceCondition(2)
        ]
    ),
    RegionData(
        "Executive Sector, Clearance 3",
        "Executive Sector, Clearance 2",
        [
            ClearanceCondition(3),
        ]
    ),
    RegionData(
        "Executive Sector, Clearance 4",
        "Executive Sector, Clearance 3",
        [
            ClearanceCondition(4),
        ]
    ),
    RegionData(
        "Executive Sector, Clearance 5",
        "Executive Sector, Clearance 4",
        [
            ClearanceCondition(5),
        ]
    ),
    RegionData(
        "Executive Sector, Clearance 6",
        "Executive Sector, Clearance 5",
        [
            ClearanceCondition(6),
        ]
    ),
    RegionData(
        "Maintenance Sector, Clearance 1",
        "Executive Sector, Clearance 1",
        [
            ClearanceCondition(1),
            SectorCondition("Maintenance Sector"),
            MissionCondition(4262696584514748496),
        ]
    ),
    RegionData(
        "Maintenance Sector, Clearance 2",
        "Maintenance Sector, Clearance 1",
        [
            ClearanceCondition(2),
        ]
    ),
    RegionData(
        "Maintenance Sector, Clearance 3",
        "Maintenance Sector, Clearance 2",
        [
            ClearanceCondition(3),
        ]
    ),
    RegionData(
        "Maintenance Sector, Clearance 4",
        "Maintenance Sector, Clearance 3",
        [
            ClearanceCondition(4),
        ]
    ),
    RegionData(
        "Maintenance Sector, Clearance 5",
        "Maintenance Sector, Clearance 4",
        [
            ClearanceCondition(5),
        ]
    ),
    RegionData(
        "Maintenance Sector, Clearance 6",
        "Maintenance Sector, Clearance 5",
        [
            ClearanceCondition(6),
        ]
    ),
    RegionData(
        "Research Sector, Clearance 1",
        "Maintenance Sector, Clearance 1",
        [
            ClearanceCondition(1),
            SectorCondition("Research Sector"),
        ]
    ),
    RegionData(
        "Research Sector, Clearance 2",
        "Research Sector, Clearance 1",
        [
            ClearanceCondition(2),
        ]
    ),
    RegionData(
        "Research Sector, Clearance 3",
        "Research Sector, Clearance 2",
        [
            ClearanceCondition(3),
        ]
    ),
    RegionData(
        "Research Sector, Clearance 4",
        "Research Sector, Clearance 3",
        [
            ClearanceCondition(4),
        ]
    ),
    RegionData(
        "Research Sector, Clearance 5",
        "Research Sector, Clearance 4",
        [
            ClearanceCondition(5),
        ]
    ),
    RegionData(
        "Research Sector, Clearance 6",
        "Research Sector, Clearance 5",
        [
            ClearanceCondition(6),
        ]
    ),
    RegionData(
        "Containment Sector, Clearance 1",
        "Maintenance Sector, Clearance 1",
        [
            ClearanceCondition(1),
            SectorCondition("Containment Sector"),
        ]
    ),
    RegionData(
        "Containment Sector, Clearance 2",
        "Containment Sector, Clearance 1",
        [
            ClearanceCondition(2),
        ]
    ),
    RegionData(
        "Containment Sector, Clearance 3",
        "Containment Sector, Clearance 2",
        [
            ClearanceCondition(3),
        ]
    ),
    RegionData(
        "Containment Sector, Clearance 4",
        "Containment Sector, Clearance 3",
        [
            ClearanceCondition(4),
        ]
    ),
    RegionData(
        "Containment Sector, Clearance 5",
        "Containment Sector, Clearance 4",
        [
            ClearanceCondition(5),
        ]
    ),
    RegionData(
        "Containment Sector, Clearance 6",
        "Containment Sector, Clearance 5",
        [
            ClearanceCondition(6),
        ]
    )
]