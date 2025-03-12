# Imports


# Variables


# Code

class Game:

    def __init__(
        self,
        initial_capital: int,
        rss_count: int,
        turns: int,
    ):
        self.capital = initial_capital
        self.rss_count = rss_count
        self.turns = turns
        self.current_turn = 0
