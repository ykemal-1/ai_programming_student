"""
Oefening 3: Maze met DFS
=========================
Implementeer DFS om een weg door het maze te vinden.
"""

import numpy as np


class Maze:
    def __init__(self, size, start, end, walls):
        self.size = size
        self.start = start
        self.end = end
        self.maze = np.zeros(size, dtype=str)
        self.maze[:, :] = "."
        self.maze[start] = "S"
        self.maze[end] = "E"
        for wall in walls:
            self.maze[wall] = "#"

    def valid_moves(self, current):
        # TODO: geef lijst van (rij,kolom)-coördinaten die geldig zijn
        rij, kolom = current

        buren = [
            (rij - 1, kolom),  # boven
            (rij + 1, kolom),  # onder
            (rij, kolom - 1),  # links
            (rij, kolom + 1),  # rechts
        ]

        geldige_zetten = []

        for nieuwe_rij, nieuwe_kolom in buren:
            binnen_grid = (
                0 <= nieuwe_rij < self.size[0] and 0 <= nieuwe_kolom < self.size[1]
            )

            if binnen_grid:
                if self.maze[nieuwe_rij, nieuwe_kolom] != "#":
                    geldige_zetten.append((nieuwe_rij, nieuwe_kolom))

        return geldige_zetten

    def extract_path(self, stack):
        # TODO: haal het pad uit de stack van start tot end
        laatste_entry = stack[-1]
        positie, pad = laatste_entry
        return pad

    def print_maze(self):
        for row in self.maze:
            print(" ".join(row))


def find_path(maze):
    # TODO: implementeer DFS met een stack
    stack = [(maze.start, [maze.start])]
    visited = set()

    while stack:
        current, pad = stack[-1]

        if current == maze.end:
            pad = maze.extract_path(stack)
            return pad, len(pad) - 1

        # Verwijder de bovenste entry.
        current, pad = stack.pop()

        if current in visited:
            continue

        visited.add(current)

        for buur in maze.valid_moves(current):
            if buur not in visited:
                nieuwe_pad = pad + [buur]
                stack.append((buur, nieuwe_pad))

    # Alle mogelijkheden onderzocht, maar geen pad gevonden.
    return [], 0


if __name__ == "__main__":
    maze_size = (10, 10)
    start_point = (0, 0)
    end_point = (9, 9)
    walls = [
        (2, 1),
        (2, 2),
        (2, 3),
        (4, 6),
        (6, 6),
        (7, 6),
        (8, 6),
        (4, 7),
        (4, 8),
        (2, 2),
        (5, 2),
        (6, 2),
        (4, 2),
        (3, 2),
        (8, 0),
        (9, 6),
        (1, 8),
        (2, 8),
        (6, 9),
        (7, 9),
        (3, 6),
        (3, 7),
        (4, 1),
        (5, 1),
    ]

    my_maze = Maze(maze_size, start_point, end_point, walls)
    pad, stappen = find_path(my_maze)

    my_maze.print_maze()
    print("Pad:", pad)
    print("Stappen:", stappen)
