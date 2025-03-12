# Imports
from pathlib import Path
from energy_resource import Resource, ResourceType, Specials, clamp
import random

# Variables


# Code
class GomeJim:
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

# ==================================================================================================
    def _decide_resource_to_buy(self) -> int:
        """make an informed decision on the most green resource"""

        resourceInstances = self.bought_resources.copy()
        bestResource = None
        bestProfit = 0

        for resource_type in self.available_resources:            
            currentTestingBudget = self.money
            temp_profit = -resource_type.activation_cost

            temp_up_turns = resource_type.up_turns
            temp_down_turns = 0

            # this loop simulates the overall profit of all currently existing resources
            for existingResource in resourceInstances:
                timeLeft = existingResource.type.lifetime_turns - existingResource.age
                currentTestingBudget -= existingResource.type.maintenance_cost * timeLeft

            abort = False
            for i in range(self.current_turn, resource_type.lifetime_turns):
                # it actually was right, don't /j /s
                if temp_profit + currentTestingBudget < 0:
                    abort = True
                    break

                if temp_up_turns > 0:
                    temp_profit += self.turns[i][2]
                    temp_up_turns -= 1
                elif temp_up_turns == 0:
                    temp_down_turns = resource_type.down_turns
                
                if temp_down_turns > 0:
                    temp_down_turns -= 1
                elif temp_down_turns == 0:
                    temp_up_turns = resource_type.up_turns

                if i != 0:
                    temp_profit -= resource_type.maintenance_cost
                    
            if abort:
                continue

            currentTestingBudget += temp_profit

            if currentTestingBudget >= 0 and temp_profit > bestProfit:
                bestResource = resource_type.id
                bestProfit = temp_profit
                print("BUDGET " + str(currentTestingBudget))
                print("PROFIT " + str(temp_profit))
                
        return bestResource

# ==================================================================================================
    def start_turn(self, min_builds, max_builds, unit_profit):
        Resource.powered_buildings = 0
        Specials.reset()

        self.min_builds = min_builds
        self.max_builds = max_builds
        self.unit_profit = unit_profit

        resource_id = self._decide_resource_to_buy()
        while resource_id is not None:
            new_resource = Resource(resource_id)
            buy_cost = new_resource.activate()
            self.bought_resources.append(new_resource)
            self.current_turn_resources.append(new_resource)
            self.money -= buy_cost
            resource_id = self._decide_resource_to_buy()

        clamp(Resource.powered_buildings * Specials.powered_buildings_bonus, 0)


# ==================================================================================================
    def periodic_costs(self):
        remaining_resources = self.bought_resources
        for rs in self.bought_resources:
            maint_cost = rs.update()
            if maint_cost is None:
                remaining_resources.remove(rs)
                continue
            self.money -= maint_cost
            
        self.bought_resources = remaining_resources

# ==================================================================================================
    def turn_profit(self):
        power = Resource.powered_buildings
        print("POWERED BUILDING", power)
        if power > self.min_builds:
            return min(power, self.max_builds) * self.unit_profit 
        return 0

# ==================================================================================================
    def end_turn(self):
        print(f"MONEY REMAINING AT END OF TURN {self.current_turn}: {self.money}")
        self.money += self.turn_profit()
        
        line = f"{self.current_turn} {len(self.current_turn_resources)}"
        for rs in self.current_turn_resources:
            line += f" {rs.id}"
            
        if len(self.current_turn_resources) != 0:
            self.output_string += line + "\n"

        self.current_turn += 1
        self.current_turn_resources = []

# ==================================================================================================
    def end_game(self):
        self.output_file.write_text(self.output_string)

# ==================================================================================================
    def run(self):
        for turn in self.turns:
            self.start_turn(*turn)
            self.periodic_costs()
            self.end_turn()
        self.end_game()
