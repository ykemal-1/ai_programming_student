"""
Oefening: TicTacToe met Minimax & Alpha-Beta
==============================================
"""
import copy


class TicTacToe:
    def __init__(self):
        self.board = [[' ' for _ in range(3)] for _ in range(3)]
        self.random_turn = False  # Eerste computerzet is optimaal.

    def possible_moves(self):
        """Geef alle lege velden terug."""
        return [
            (r, c)
            for r in range(3)
            for c in range(3)
            if self.board[r][c] == ' '
        ]

    def is_valid_move(self, x, y):
        return (
            0 <= x < 3
            and 0 <= y < 3
            and self.board[x][y] == ' '
        )

    def make_move(self, x, y, player):
        if player not in ('X', 'O'):
            raise ValueError("De speler moet X of O zijn.")

        if not self.is_valid_move(x, y):
            return False

        self.board[x][y] = player
        return True

    def undo_move(self, x, y):
        self.board[x][y] = ' '

    def check_winner(self):
        """Geef X, O of None terug."""
        lines = []

        # Rijen.
        lines.extend(self.board)

        # Kolommen.
        for c in range(3):
            lines.append([self.board[r][c] for r in range(3)])

        # Diagonalen.
        lines.append([self.board[i][i] for i in range(3)])
        lines.append([self.board[i][2 - i] for i in range(3)])

        for line in lines:
            if line[0] != ' ' and line[0] == line[1] == line[2]:
                return line[0]

        return None

    def is_draw(self):
        return len(self.possible_moves()) == 0 and not self.check_winner()

    def evaluate(self):
        """Score vanuit het standpunt van de computer."""
        winner = self.check_winner()

        if winner == 'O':
            return 1
        if winner == 'X':
            return -1

        return 0

    def minimax(
        self,
        depth,
        is_maximizing,
        alpha=None,
        beta=None,
        max_depth=None,
        random_turn=False
    ):
        if alpha is None:
            alpha = float('-inf')
        if beta is None:
            beta = float('inf')

        # Controleer eerst of het spel afgelopen is.
        if self.check_winner() or self.is_draw():
            return self.evaluate()

        # Zoeklimiet: een niet-terminale toestand krijgt score 0.
        if max_depth is not None and depth >= max_depth:
            return 0

        moves = self.possible_moves()

        # Willekeurige computerbeurt: bereken de verwachte waarde.
        if is_maximizing and random_turn:
            total = 0

            for x, y in moves:
                self.make_move(x, y, 'O')

                # Elke uitkomst moet exact geëvalueerd worden.
                # Daarom krijgt elke kansuitkomst een volledig zoekvenster.
                total += self.minimax(
                    depth=depth + 1,
                    is_maximizing=False,
                    alpha=float('-inf'),
                    beta=float('inf'),
                    max_depth=max_depth,
                    random_turn=False
                )

                self.undo_move(x, y)

            return total / len(moves)

        # Optimale computerbeurt: maximaliseren.
        if is_maximizing:
            best_score = float('-inf')

            for x, y in moves:
                self.make_move(x, y, 'O')

                score = self.minimax(
                    depth=depth + 1,
                    is_maximizing=False,
                    alpha=alpha,
                    beta=beta,
                    max_depth=max_depth,
                    random_turn=True
                )

                self.undo_move(x, y)

                best_score = max(best_score, score)
                alpha = max(alpha, best_score)

                if alpha >= beta:
                    break

            return best_score

        # Menselijke beurt: minimaliseren.
        best_score = float('inf')

        for x, y in moves:
            self.make_move(x, y, 'X')

            score = self.minimax(
                depth=depth + 1,
                is_maximizing=True,
                alpha=alpha,
                beta=beta,
                max_depth=max_depth,
                random_turn=random_turn
            )

            self.undo_move(x, y)

            best_score = min(best_score, score)
            beta = min(beta, best_score)

            if alpha >= beta:
                break

        return best_score

    def find_best_move(self, max_depth=None):
        """
        Zoek de beste computerzet.

        De huidige computerzet telt als diepte 1.
        None betekent zoeken tot het einde van het spel.
        """
        if max_depth is not None and max_depth < 1:
            raise ValueError("max_depth moet minstens 1 zijn, of None.")

        if self.check_winner() or self.is_draw():
            return None

        best_move = None
        best_score = float('-inf')
        alpha = float('-inf')

        moves = self.possible_moves()
        random.shuffle(moves)  # Wissel af bij gelijkwaardige zetten.

        for x, y in moves:
            self.make_move(x, y, 'O')

            score = self.minimax(
                depth=1,
                is_maximizing=False,
                alpha=alpha,
                beta=float('inf'),
                max_depth=max_depth,
                random_turn=True
            )

            self.undo_move(x, y)

            if score > best_score:
                best_score = score
                best_move = (x, y)

            alpha = max(alpha, best_score)

        return best_move

    def print_board(self):
        horizontal_line = "+---+---+---+"
        print(horizontal_line)

        for row in self.board:
            print("| {} | {} | {} |".format(*row))
            print(horizontal_line)

    def play(self, max_depth=None):
        if max_depth is not None and max_depth < 1:
            raise ValueError("max_depth moet minstens 1 zijn, of None.")

        print("Jij bent X. De computer is O.")
        print("Gebruik rij en kolom van 1 tot en met 3.")

        if max_depth is not None:
            print(
                f"Zoeklimiet: {max_depth} zetten. "
                "Bij de limiet stopt het zoeken en krijgt "
                "een onbesliste toestand score 0."
            )

        self.print_board()

        while True:
            # Menselijke beurt.
            while True:
                try:
                    x, y = map(
                        int,
                        input("Jouw zet (rij kolom, bijvoorbeeld 1 3): ").split()
                    )

                    if self.make_move(x - 1, y - 1, 'X'):
                        break

                    print("Ongeldige zet. Kies een leeg veld.")
                except ValueError:
                    print("Geef twee gehele getallen, bijvoorbeeld: 1 3")

            self.print_board()

            if self.check_winner() or self.is_draw():
                break

            # Computerbeurt.
            if self.random_turn:
                print("De computer speelt willekeurig.")
                move = random.choice(self.possible_moves())
            else:
                print("De computer kiest de beste zet binnen de zoekdiepte.")
                move = self.find_best_move(max_depth)

            self.make_move(*move, 'O')
            self.random_turn = not self.random_turn

            self.print_board()

            if self.check_winner() or self.is_draw():
                break

        winner = self.check_winner()

        if winner == 'X':
            print("Je hebt gewonnen!")
        elif winner == 'O':
            print("De computer heeft gewonnen!")
        else:
            print("Gelijkspel!")


if __name__ == "__main__":
    game = TicTacToe()
    game.play(max_depth=5)