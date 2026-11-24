from collections import deque

class RiverCrossing:
    def __init__(self):
        self.initial_state = (3, 3, 0)  # (boeren_links, wolven_links, boot_kant)

        # Mogelijke overtochten (boeren, wolven)
        # een 'move' is een tuple (aantal_boeren, aantal_wolven) dat aangeeft hoeveel van elk type de boot overzet
        self.moves = [
            (1, 0), (2, 0),  # 1 of 2 boeren
            (0, 1), (0, 2),  # 1 of 2 wolven
            (1, 1),           # 1 boer en 1 wolf
        ]

        # je kan hier items als volgt uithalen:
        # for b, w in self.moves:
        #     print(f"Boeren: {b}, Wolven: {w}")

    def is_valid_state(self, boeren_links, wolven_links):
        boeren_rechts = 3 - boeren_links
        wolven_rechts = 3 - wolven_links

        if (0 <= boeren_rechts <= 3) and (0 <= wolven_rechts <= 3):
            if (0 <= boeren_links <= 3) and (0 <= wolven_links <= 3):
                result = True
            else:
                result = False
        else:
            result = False

        if result == False:
            return False

        if (boeren_links == 0 or boeren_links >= wolven_links) and (boeren_rechts == 0 or boeren_rechts >= wolven_rechts):
            result = True
        else:
            result = False

        return result

    def get_new_states(self, state):
        new_states = []
        boat = state[2]

        if boat == 0:
            new_boat = 1
        else:
            new_boat = 0

        for boer, wolf in self.moves:
            if boat == 0:
                new_state = (state[0] - boer, state[1] - wolf, new_boat)
            else:
                new_state = (state[0] + boer, state[1] + wolf, new_boat)

            if self.is_valid_state(new_state[0], new_state[1]):
                new_states.append(new_state)
        return new_states


    def solve(self):
        initial_state = tuple(self.initial_state)
        visited = {self.initial_state}
        frontier = deque([(initial_state, [initial_state])])

        while frontier:
            current, pad = frontier.popleft()

            if current == (0,0,1):
                print("Oplossing gevonden.")
                return pad

            for new_state in self.get_new_states(current):
                new_state = tuple(new_state)

                if new_state not in visited:
                    visited.add(new_state)
                    frontier.append((new_state, pad + [new_state]))

        return None    

# Testcode
rc = RiverCrossing()
start = rc.initial_state
print("Startstaat:", start)
print("Mogelijke eerste zetten:")
for s in rc.get_new_states(start):
    print(s)

print("Oplossing?")
solution = rc.solve()
#TODO: print de oplossing als die er is, anders geef aan dat er geen oplossing is

if solution is not None:
    print(f"Oplossing gevonden in {len(solution) - 1} overtochten:")

    for stap, state in enumerate(solution):
        boeren_links, wolven_links, boot = state
        boot_kant = "links" if boot == 0 else "rechts"

        print(
            f"Stap {stap}: "
            f"Links: {boeren_links} boeren, {wolven_links} wolven | "
            f"Rechts: {3 - boeren_links} boeren, {3 - wolven_links} wolven | "
            f"Boot: {boot_kant}"
        )
else:
    print("Geen oplossing gevonden.")