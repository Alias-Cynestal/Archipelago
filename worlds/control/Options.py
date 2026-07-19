from dataclasses import dataclass

from Options import Toggle, Range, OptionGroup, PerGameCommonOptions

control_option_groups = []


#---------------------------------------------------------#
#
#           Progression Options
#
#---------------------------------------------------------#
class EnableSectorUnlocksToggle(Toggle):
    """
    Sectors are no longer obtained by completing the story, they unlock as items in the randomizer
    """
    display_name = "Enable Sector Unlocks"
    default = 1  # off requires the story-progress mapping, which is not modelled yet

class EnableClearanceLevelUnlocksToggle(Toggle):
    """
    Clearance levels are no longer obtained by completing the story, they unlock as items in the randomizer
    """
    display_name = "Enable Clearance Level Unlocks"
    default = 1  # off requires the story-progress mapping, which is not modelled yet

class EnableProgressiveClearanceLevelToggle(Toggle):
    """
    Clearance levels are given based on the number of clearance level upgrades collected
    """
    display_name = "Enable Progressive Clearance Level"
    default = 1

#---------------------------------------------------------#
#
#           Filler Options
#
#---------------------------------------------------------#

class AstralBlipPercentageRange(Range):
    """
    Represents the chance of the player getting the House Memory Material as filler checks.
    """
    display_name = "Astral Blip Percentage"
    range_start = 0
    range_end = 100
    default = 10

class CorruptedSamplePercentageRange(Range):
    """
    Represents the chance of the player getting the Corrupted Sample Material as filler checks.
    """
    display_name = "Corrupted Sample Percentage"
    range_start = 0
    range_end = 100
    default = 10

class EntropicEchoPercentageRange(Range):
    """
    Represents the chance of the player getting the Entropic Echo Material as filler checks.
    """
    display_name = "Entropic Echo Percentage"
    range_start = 0
    range_end = 100
    default = 10

class HiddenTrendPercentageRange(Range):
    """
    Represents the chance of the player getting the Hidden Trend Material as filler checks.
    """
    display_name = "Hidden Trend Percentage"
    range_start = 0
    range_end = 100
    default = 5

class HouseMemoryPercentageRange(Range):
    """
    Represents the chance of the player getting the House Memory Material as filler checks.
    """
    display_name = "House Memory Percentage"
    range_start = 0
    range_end = 100
    default = 10

class IntrusivePatternPercentageRange(Range):
    """
    Represents the chance of the player getting the Intrusive Pattern Material as filler checks.
    """
    display_name = "Intrusive Pattern Percentage"
    range_start = 0
    range_end = 100
    default = 10

class RemoteThoughtPercentageRange(Range):
    """
    Represents the chance of the player getting the Remote Thought Material as filler checks.
    """
    display_name = "Remote Thought Percentage"
    range_start = 0
    range_end = 100
    default = 5

class RitualImpulsePercentageRange(Range):
    """
    Represents the chance of the player getting the Ritual Impulse Material as filler checks.
    """
    display_name = "Ritual Impulse Percentage"
    range_start = 0
    range_end = 100
    default = 10

class ThresholdRemnantPercentageRange(Range):
    """
    Represents the chance of the player getting the Threshold Remnant Material as filler checks.
    """
    display_name = "Threshold Remnant Percentage"
    range_start = 0
    range_end = 100
    default = 10

class UndefinedReadingPercentageRange(Range):
    """
    Represents the chance of the player getting the Undefined Reading Material as filler checks.
    """
    display_name = "Undefined Reading Percentage"
    range_start = 0
    range_end = 100
    default = 10

class UntappedPotentialPercentageRange(Range):
    """
    Represents the chance of the player getting the Untapped Potential Material as filler checks.
    """
    display_name = "Untapped Potential Percentage"
    range_start = 0
    range_end = 100
    default = 5


@dataclass
class ControlOptions(PerGameCommonOptions):
    # Game Options
    sector_unlocks: EnableSectorUnlocksToggle
    clearance_level_unlocks: EnableClearanceLevelUnlocksToggle
    progressive_clearance_levels: EnableProgressiveClearanceLevelToggle

    # Filler
    astral_blip: AstralBlipPercentageRange
    corrupted_sample: CorruptedSamplePercentageRange
    entropic_echo: EntropicEchoPercentageRange
    hidden_trend: HiddenTrendPercentageRange
    house_memory: HouseMemoryPercentageRange
    intrusive_pattern: IntrusivePatternPercentageRange
    remote_thought: RemoteThoughtPercentageRange
    ritual_impulse: RitualImpulsePercentageRange
    threshold_remnant: ThresholdRemnantPercentageRange
    undefined_reading: UndefinedReadingPercentageRange
    untapped_potential: UntappedPotentialPercentageRange

option_groups = [
    OptionGroup("Game", [
        EnableSectorUnlocksToggle,
        EnableClearanceLevelUnlocksToggle,
        EnableProgressiveClearanceLevelToggle
    ]),
    OptionGroup("Filler", [
        AstralBlipPercentageRange,
        CorruptedSamplePercentageRange,
        EntropicEchoPercentageRange,
        HiddenTrendPercentageRange,
        HouseMemoryPercentageRange,
        IntrusivePatternPercentageRange,
        RemoteThoughtPercentageRange,
        RitualImpulsePercentageRange,
        ThresholdRemnantPercentageRange,
        UndefinedReadingPercentageRange,
        UntappedPotentialPercentageRange,
    ])
]