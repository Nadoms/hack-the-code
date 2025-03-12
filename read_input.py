# Imports
import argparse
from pathlib import Path

from game import Game
from energy_resource import Resource

# Variables
ROOT = Path(__file__).parent

# Code

def parse_input(file: str):
    input_file = ROOT / "input" / file
    output_file = ROOT / "output" / file

    with open(input_file, "r") as f:
        game_setup = f.readline().strip()
        # Read game setup line
        initial_money, rss_count, turns = [int(stat) for stat in game_setup.split()]

        # Read resources available
        rss = []
        for i in range(rss_count):
            raw_rs = f.readline().strip().split()
            base_rs_info = [int(stat) for stat in raw_rs[:7]]
            if len(raw_rs) == 7:
                rs = Resource(*base_rs_info)
            else:
                special_rs_info = raw_rs[7:]
                rs = Resource(*base_rs_info, *special_rs_info)
            rss.append(rs)

        # Read turns
        turns = []
        for i in range(turns):
            turn = f.readline().strip().split()
            turns.append(turn)  # Make turn object

    game = Game(initial_money, rss, turns, output_file)
    return game


def main():
    argparser = argparse.ArgumentParser()
    argparser.add_argument("-f", "file", help="Input file to read")
    args = argparser.parse_args()
    game = parse_input(args.input)
    # game.start()


if __name__ == "__main__":
    main()
