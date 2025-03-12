# Imports


# Variables


# Code

class ResourceType:

    resources = []

    def __init__(
        self,
        id: int,
        activation_cost: int,
        maintenance_cost: int,
        up_turns: int,
        down_turns: int,
        lifetime_turns: int,
        power: int,
        special_effect: str | None = None,
        special_quality: int | None = None,
    ):
        self.id = id
        self.activation_cost = activation_cost
        self.maintenance_cost = maintenance_cost
        self.up_turns = up_turns
        self.cycle_turns = up_turns + down_turns
        self.lifetime_turns = lifetime_turns
        self.power = power
        self.special_effect = special_effect
        self.special_quality = special_quality

        ResourceType.resources.append(self)


class Resource:

    powered_buildings = 0

    def __init__(
        self,
        id: int,
    ):
        self.id = id
        self.type : ResourceType = ResourceType.resources[id - 1]

        self.consumed = False
        self.is_on = False
        self.age = 0
        Resource.powered_buildings += self.type.power

    def activate(self) -> int:
        self.consumed = True
        self.is_on = True
        return self.type.activation_cost

    def update(self):
        if self.consumed:
            return None

        turn = self.age % self.type.cycle_turns
        if turn < self.type.up_turns:
            self.is_on = False
        else:
            Resource.powered_buildings += self.type.power
            self.is_on = True

        return self.type.maintenance_cost
