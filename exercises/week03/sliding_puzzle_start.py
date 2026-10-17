"""
Oefening 2: Sliding Puzzle (8-puzzle)
======================================
Implementeer de sliding puzzle en los hem op met BFS/DFS.
"""

import numpy as np
from collections import deque


class SlidingPuzzle:
    GRIDSIZE = 3
    EMPTY = 0
    GOAL = [[1, 2, 3], [4, 5, 6], [7, 8, 0]]

    def __init__(self, game):
        self.Game = np.array(game)

    def possible_new_configurations(self):
        # TODO: geef alle nieuwe configuraties door het lege vakje te verschuiven
        configuraties = []

        row, col = self.locate_empty()

        richtingen = [(-1, 0), (1, 0), (0, -1), (0, 1)]

        for row_change, col_change in richtingen:
            new_row = row + row_change
            new_col = col + col_change

            if 0 <= new_row < self.GRIDSIZE and 0 <= new_col < self.GRIDSIZE:
                new_puzzle = self.duplicate()

                new_puzzle.Game[row, col], new_puzzle.Game[new_row, new_col] = (
                    new_puzzle.Game[new_row, new_col],
                    new_puzzle.Game[row, col],
                )

                configuraties.append(new_puzzle)

        return configuraties

    def locate_empty(self):
        for row in range(self.GRIDSIZE):
            for col in range(self.GRIDSIZE):
                if self.Game[row][col] == self.EMPTY:
                    return (row, col)
        raise Exception("Geen leeg vakje!")

    def manhattan_distance(self):
        # TODO: bereken de Manhattan-afstand tot de goal-configuratie
        afstand = 0

        for row in range(self.GRIDSIZE):
            for col in range(self.GRIDSIZE):
                tegel = int(self.Game[row][col])

                if tegel != self.EMPTY:
                    doel_row = (
                        tegel - 1
                    ) // self.GRIDSIZE  # DEZE OPERATOR IS CRUCIAAL VOOR BORDSPELLEN
                    doel_col = (
                        tegel - 1
                    ) % self.GRIDSIZE  # DEZE OPERATOR IS CRUCIAAL VOOR BORDSPELLEN
                    afstand += abs(doel_row - row) + abs(doel_col - col)

        return afstand

    def is_goal(self):
        return np.array_equal(self.Game, self.GOAL)

    def duplicate(self):
        return SlidingPuzzle(
            [
                [self.Game[r][c] for c in range(self.GRIDSIZE)]
                for r in range(self.GRIDSIZE)
            ]
        )

    def log(self):
        print("---")
        for row in self.Game:
            print(", ".join(str(int(x)) for x in row))
        print("---")


def solve_puzzle(start_puzzle):
    # TODO: los de puzzel op met BFS

    # Elk element bevat een puzzel en het pad naar die puzzel.
    wachtrij = deque([(start_puzzle, [start_puzzle])])

    # Een tuple kan in een set worden opgeslagen.
    start_configuratie = tuple(start_puzzle.Game.flatten())
    bezocht = {start_configuratie}

    while wachtrij:
        # Neem de oudste puzzel uit de wachtrij: BFS.
        huidige_puzzel, pad = wachtrij.popleft()

        if huidige_puzzel.is_goal():
            return pad

        for nieuwe_puzzel in huidige_puzzel.possible_new_configurations():
            configuratie = tuple(nieuwe_puzzel.Game.flatten())

            # Verwerk elke configuratie maar één keer.
            if configuratie not in bezocht:
                bezocht.add(configuratie)

                nieuw_pad = pad + [nieuwe_puzzel]
                wachtrij.append((nieuwe_puzzel, nieuw_pad))

    # Alle bereikbare configuraties onderzocht, geen oplossing.
    return None

    pass


if __name__ == "__main__":
    game = [[1, 2, 3], [4, 5, 0], [7, 8, 6]]
    puzzle = SlidingPuzzle(game)
    print("Startconfiguratie:")
    puzzle.log()

    oplossing = solve_puzzle(puzzle)

    if oplossing is None:
        print("Geen oplossing gevonden.")
    else:
        print("Aantal zetten:", len(oplossing) - 1)

        for stap, configuratie in enumerate(oplossing):
            print(f"Stap {stap}:")
            configuratie.log()
