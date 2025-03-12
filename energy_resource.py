# Imports
from enum import Enum
from math import floor


# Variables


# Code


class ResourceType:

    resources = {}

    def __init__(
        self,
        id: int,
        activation_cost: int,
        maintenance_cost: int,
        up_turns: int,
        down_turns: int,
        lifetime_turns: int,
        power: int,
        special_effect: str,
        special_quality: int | None = None,
    ):
        self.id = id
        self.activation_cost = activation_cost
        self.maintenance_cost = maintenance_cost
        self.up_turns = up_turns
        self.down_turns = down_turns
        self.cycle_turns = up_turns + down_turns
        self.lifetime_turns = lifetime_turns
        self.power = power
        self.special_effect = special_effect
        self.special_quality = special_quality

        ResourceType.resources[self.id] = self

    def __repr__(self):
        return f"ResourceType({self.id}, {self.activation_cost}, {self.maintenance_cost}, {self.up_turns}, {self.down_turns}, {self.lifetime_turns}, {self.power}, {self.special_effect}, {self.special_quality})"


class Resource:

    powered_buildings = 0

    def __init__(
        self,
        id: int,
    ):
        self.id = id
        self.type : ResourceType = ResourceType.resources[self.id]
        self.lifespan = clamp(self.type.lifetime_turns * Specials.rs_lifetime_bonus, 1)
        self.ability = Specials(self.type.special_effect, self.type.special_quality)

        self.consumed = False
        self.maintaining = False
        self.is_on = True
        self.age = 0

    def activate(self) -> int:
        return self.type.activation_cost

    def update(self):
        if self.age >= self.type.lifetime_turns:
            self.consumed = True
            return None

        turn = self.age % self.type.cycle_turns
        if turn >= self.type.up_turns:
            self.is_on = False
        else:
            self.ability()
            self.is_on = True
            Resource.powered_buildings += self.type.power

        self.age += 1

        if not self.maintaining:
            self.maintaining = True
            return None
        return self.type.maintenance_cost


def clamp(value: float, minimum: int):
    return floor(max(value, minimum))


class SpecialType(Enum):
    SMART_METER = "A"
    DISTRIBUTION_FACILITY = "B"
    MAINTENANCE_PLAN = "C"
    RENEWABLE_PLAN = "D"
    ACCUMULATOR = "E"


class Specials:

    powered_buildings_bonus = 1
    threshold_buildings_bonus = 1
    rs_lifetime_bonus = 1
    profit_bonus = 1
    accumulator = 1
    accumulation = 1

    def __init__(self, ability: SpecialType, quality: int | None):
        self.ability = ability
        self.quality = quality

    @classmethod
    def reset(self):
        # Kinda scuffed but oh well
        Specials.powered_buildings_bonus = 1
        Specials.threshold_buildings_bonus = 1
        Specials.rs_lifetime_bonus = 1
        Specials.profit_bonus = 1
        Specials.accumulator = 1

    def __call__(self):
        if self.ability == SpecialType.SMART_METER:
            Specials.powered_buildings_bonus += self.quality / 100

        elif self.ability == SpecialType.DISTRIBUTION_FACILITY:
            Specials.threshold_buildings_bonus += self.quality / 100

        elif self.ability == SpecialType.MAINTENANCE_PLAN:
            Specials.rs_lifetime_bonus += self.quality / 100

        elif self.ability == SpecialType.RENEWABLE_PLAN:
            Specials.profit_bonus += self.quality / 100

        elif self.ability == SpecialType.ACCUMULATOR:
            Specials.accumulator += 1
