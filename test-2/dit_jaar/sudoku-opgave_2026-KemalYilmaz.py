import numpy as np
import random
import math


class SudokuSASolver:
    def __init__(self, puzzle, initial_temp=10.0, alpha=0.99, max_iter=2000):
        self.initial_puzzle = np.array(puzzle)
        self.initial_temp = initial_temp
        self.alpha = alpha
        self.max_iter = max_iter

        self.grid = None
        self.fixed = None
        self.current_cost = None

    def _get_block_indices(self, block_idx):
        """Hardcoded lookup mapping: elke 2x2 blok krijgt exacte coördinaten terug."""
        blocks = {
            0: [(0, 0), (0, 1), (1, 0), (1, 1)],  # Boven-links blok
            1: [(0, 2), (0, 3), (1, 2), (1, 3)],  # Boven-rechts blok
            2: [(2, 0), (2, 1), (3, 0), (3, 1)],  # Onder-links blok
            3: [(2, 2), (2, 3), (3, 2), (3, 3)],  # Onder-rechts block
        }
        return blocks[block_idx]

    def _initialize_grid(self):
        """Vult lege plaatsen zpdat elke 2x2 blok begint met getallen 1-4."""
        self.grid = self.initial_puzzle.copy()
        self.fixed = self.initial_puzzle != 0

        for b in range(4):
            indices = self._get_block_indices(b)
            present = [self.grid[r, c] for r, c in indices if self.grid[r, c] != 0]
            missing = [val for val in [1, 2, 3, 4] if val not in present]
            random.shuffle(missing)

            for r, c in indices:
                if self.grid[r, c] == 0:
                    self.grid[r, c] = missing.pop()

    def _compute_cost(self, test_grid):
        """Telt hoeveel duplicates er zijn in rijen en kolommen (Perfect = 0). Hoe lager, hoe beter."""
        cost = 0
        for i in range(4):
            cost += 4 - len(np.unique(test_grid[i, :]))  # duplicaten per rij
            cost += 4 - len(np.unique(test_grid[:, i]))  # duplicaten per kolom
        return cost

    def _get_neighbor(self):
        """Swaps two non-clue numbers within a random 2x2 block."""
        new_grid = self.grid.copy()
        b = random.randint(0, 3)
        indices = self._get_block_indices(b)

        mutable = [(r, c) for r, c in indices if not self.fixed[r, c]]

        if len(mutable) >= 2:
            (r1, c1), (r2, c2) = random.sample(mutable, 2)
            new_grid[r1, c1], new_grid[r2, c2] = new_grid[r2, c2], new_grid[r1, c1]

        return new_grid

    def solve(self):
        """Dit algoritme zoekt een oplossing van de sudoku, of een goede benadering van een oplossing."""
        huidige_grid = self._initialize_grid()
        self.current_cost = self._compute_cost(self.grid)
        temperature = self.initial_temp

        # TODO Voorzie een check om vroegtijdig te stoppen als er een echte oplossing wordt gevonden
        best_grid = huidige_grid
        best_cost = 0

        self.GEVONDEN = False

        # TODO voorzie de rest van het algoritme

        for _ in range(self.max_iter):
            nieuwe_grid = (
                self._get_neighbor()
            )  # twee vakken in 1 blok kiezen om te verwisselen
            new_cost = self._compute_cost(nieuwe_grid)
            delta = new_cost - self.current_cost

            if delta < 0 or random.random() < math.exp(-delta / temperature):
                huidige_grid = nieuwe_grid
                current_cost = new_cost

                if current_cost < best_cost:
                    best_grid = huidige_grid
                    best_cost = self.current_cost

            temperature *= self.alpha

            if self._compute_cost(nieuwe_grid) == 0:
                self.GEVONDEN = True
                return nieuwe_grid

        # TODO print relevante outputs
        print("Reached max iterations without a perfect solution.")
        return self.grid


# --- Running the Code ---
if __name__ == "__main__":
    puzzle_data = [
        [1, 0, 0, 4],
        [0, 4, 1, 0],
        [2, 0, 4, 0],
        [0, 3, 0, 1],
    ]  # 0 = lege cel; deze puzzel heeft exact één oplossing

    solver = SudokuSASolver(puzzle_data, initial_temp=10.0, alpha=0.99, max_iter=2000)
    solved_board = solver.solve()
    # TODO print de oplossing
    if solver.GEVONDEN:
        print(f"Optimale oplossing gevonden: \n {solved_board}")
    else:
        print(solved_board)
