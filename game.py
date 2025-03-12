# Imports
from pathlib import Path
from energy_resource import Resource

# Variables


# Code
class Game:
    def __init__(
        self,
        initial_money: int,
        resources: list[Resource],
        turns: list,
        output_file: Path,
    ):
        self.money = initial_money
        self.current_turn = 0
        self.resources = resources
        self.turns = turns
        self.output_file = output_file

    def calculate_turn_profit(self, min_builds, max_builds, unit_profit) -> int: 
        num_buildings = len(self.resources)
        return min(num_buildings, max_builds) * unit_profit if min_builds <= num_buildings else 0

    def process_turns(self):
        for turn in self.turns:
            turn_profit = self.calculate_turn_profit(turn)

    def write_turn(self):
        self.output_file
        pass  # save what happened to the output file
