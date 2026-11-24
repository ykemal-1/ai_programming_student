from collections import deque


class RiverCrossing:
    def __init__(self):
        self.initial_state = (3, 3, 0)  # (boeren_links, wolven_links, boot_kant)

        # Mogelijke overtochten (boeren, wolven)
        # een 'move' is een tuple (aantal_boeren, aantal_wolven) dat aangeeft hoeveel van elk type de boot overzet
        self.moves = [
            (1, 0),
            (2, 0),  # 1 of 2 boeren
            (0, 1),
            (0, 2),  # 1 of 2 wolven
            (1, 1),  # 1 boer en 1 wolf
        ]

        # je kan hier items als volgt uithalen:
        # for b, w in self.moves:
        #     print(f"Boeren: {b}, Wolven: {w}")

    def is_valid_state(self, boeren_links, wolven_links):
        pass

    def get_new_states(self, state):
        pass

    def solve(self):
        pass


# Testcode
rc = RiverCrossing()
start = rc.initial_state
print("Startstaat:", start)
print("Mogelijke eerste zetten:")
for s in rc.get_new_states(start):
    print(s)

print("Oplossing?")
solution = rc.solve()
# TODO: print de oplossing als die er is, anders geef aan dat er geen oplossing is
