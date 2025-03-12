# Imports
import argparse
from pathlib import Path

from game import Game
from energy_resource import ResourceType

# Variables
ROOT = Path(__file__).parent

# Code

def parse_input(file: str):
    input_file = ROOT / "inputs" / file
    output_file = ROOT / "outputs" / file

    with open(input_file, "r") as f:
        game_setup = f.readline().strip()
        # Read game setup line
        initial_money, rss_count, turn_count = [int(stat) for stat in game_setup.split()]

        # Read resources available
        rss = []
        for _ in range(rss_count):
            raw_rs = f.readline().strip().split()
            base_rs_info = [int(stat) for stat in raw_rs[:7]]
            if len(raw_rs) == 7:
                rs = ResourceType(*base_rs_info)
            else:
                special_rs_info = raw_rs[7:]
                rs = ResourceType(*base_rs_info, *special_rs_info)
            rss.append(rs)

        # Read turn requirements
        turns = []
        for _ in range(turn_count):
            turn = [int(stat) for stat in f.readline().strip().split()]
            turns.append(turn)

    game = Game(initial_money, rss, turns, output_file)
    return game


def main():
    argparser = argparse.ArgumentParser()
    argparser.add_argument("--file", "-f", help="Input file to read")
    args = argparser.parse_args()
    game = parse_input(args.file)
    game.run()


if __name__ == "__main__":
    main()
