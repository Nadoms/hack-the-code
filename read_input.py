# Imports
import argparse
from pathlib import Path

from game import GomeJim
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
        reg_len = 8
        rss = []
        for _ in range(rss_count):
            raw_rs = f.readline().strip().split()
            rs_info = [int(stat) for stat in raw_rs[:reg_len - 1]]
            rs_info.append(raw_rs[reg_len - 1])
            if len(raw_rs) > reg_len:
                rs_info.append(int(raw_rs[reg_len]))

            rss.append(ResourceType(*rs_info))

        # Read turn requirements
        turns = []
        for _ in range(turn_count):
            turn = [int(stat) for stat in f.readline().strip().split()]
            turns.append(turn)

    game = GomeJim(initial_money, rss, turns, output_file)
    return game


def main():
    argparser = argparse.ArgumentParser()
    argparser.add_argument("--file", "-f", help="Input file to read")
    args = argparser.parse_args()
    game = parse_input(args.file)
    game.run()


if __name__ == "__main__":
    main()
