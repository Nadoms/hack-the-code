# Imports
from pathlib import Path
from energy_resource import Resource, ResourceType
import random

# Variables


# Code
class Game:
    def __init__(
        self,
        initial_money: int,
        available_resources: list[ResourceType],
        turns: list[list[int]],
        output_file: Path,
    ):
        self.money = initial_money
        self.current_turn = 0
        self.available_resources = available_resources
        self.turns = turns
        self.output_file = output_file

        self.bought_resources = []
        self.current_turn_resources = []
        self.min_builds = None
        self.max_builds = None
        self.unit_profit = None
        self.output_string = ""

    def _decide_resource_to_buy(self) -> int:
        """make an informed decision on the most green resource"""
        for resource_type in self.available_resources:
            if resource_type.activation_cost > self.money:
                continue
            return resource_type.id

    def start_turn(self, min_builds, max_builds, unit_profit):
        Resource.powered_buildings = 0

        self.min_builds = min_builds
        self.max_builds = max_builds
        self.unit_profit = unit_profit

        resource_id = self._decide_resource_to_buy()
        if resource_id is not None:
            new_resource = Resource(resource_id)
            
            buy_cost = new_resource.activate()
            self.money -= buy_cost

            self.bought_resources.append(new_resource)
            self.current_turn_resources.append(new_resource)

    def periodic_costs(self):
        remaining_resources = self.bought_resources
        for rs in self.bought_resources:
            maint_cost = rs.update()
            if maint_cost is None:
                remaining_resources.remove(rs)
                continue
            self.money -= maint_cost
            
        self.bought_resources = remaining_resources

    def turn_profit(self):
        power = Resource.powered_buildings
        if power > self.min_builds:
            return min(power, self.max_builds) * self.unit_profit 
        return 0

    def end_turn(self):
        print(f"MONEY REMAINING AT END OF TURN {self.current_turn}: {self.money}")
        line = f"{self.current_turn} {len(self.current_turn_resources)}"
        for rs in self.current_turn_resources:
            line += f" {rs.id}"
            
        if len(self.current_turn_resources) != 0:
            self.output_string += line + "\n"

        self.current_turn += 1
        self.current_turn_resources = []

    def end_game(self):
        self.output_file.write_text(self.output_string)

    def run(self):
        for turn in self.turns:
            self.start_turn(*turn)
            self.periodic_costs()
            self.turn_profit()
            self.end_turn()
        self.end_game()
