from collections import deque


class WaterJugState:
    def __init__(self, jug8, jug5, jug3):
        self.jug8 = jug8
        self.jug5 = jug5
        self.jug3 = jug3
        self.parent = None

    def __eq__(self, other):
        # deze krijg je cadeau, zodat python kan checken of twee states hetzelfde zijn
        return (
            self.jug8 == other.jug8
            and self.jug5 == other.jug5
            and self.jug3 == other.jug3
        )

    def __hash__(self):
        return hash((self.jug8, self.jug5, self.jug3))

    def is_valid_state(self, next_state):
        # kijken of de emmers niet te veel water hebben dan mogelijk of te weinig (negatief)
        if (
            (0 <= next_state[0] <= 3)
            and (0 <= next_state[1] <= 5)
            and (0 <= next_state[2] <= 8)
        ):
            result = True
        else:
            result = False

        return result

    def get_next_states(self):
        next_states = []
        self.state = (self.jug3, self.jug5, self.jug8)

        for i in range(1, 9):
            for j in self.state:
                # allemaal vullen

                current_jug3 = self.jug3
                current_jug5 = self.jug5
                current_jug8 = self.jug8

                # nu wordt j enkel 1 keer opgeteld bij hun allemaal, ik moet nog implementeren dat j ook 1 per element wordt opgeteld

                new_state = (current_jug3 + j, current_jug5 + j, current_jug8 + j)
                if self.is_valid_state():
                    next_states.append(new_state)

                # allemaal legen
                # nu wordt j enkel 1 keer afgetrokken bij hun allemaal, ik moet nog implementeren dat j ook 1 per element wordt afgetrokken

                new_state = (current_jug3 - j, current_jug5 - j, current_jug8 - j)
                if self.is_valid_state():
                    next_states.append(new_state)

                # overgieten
                jug3_optel = current_jug3 + j
                jug5_optel = current_jug5 + j
                jug8_optel = current_jug8 + j
                jug3_aftrek = current_jug3 - j
                jug5_aftrek = current_jug5 - j
                jug8_aftrek = current_jug8 - j

                # jug3 naar jug5
                new_state = (jug3_optel, (5 - self.jug5), self.jug8)
                if self.is_valid_state():
                    next_states.append(new_state)
                # jug5 naar jug8
                new_state = (self.jug3, self.jug5, (8 - self.jug8))
                if self.is_valid_state(new_state):
                    next_states.append(new_state)

                if self.is_valid_state(new_state):
                    next_states.append(new_state)
        return next_states

        # Mogelijke acties: vul jug8, vul jug5, vul jug3,  leeg jug8, leeg jug5, leeg jug3, elke mogelijk combinatie van giet van pot x naar pot y

        # HINT: als je overgiet van de bijvoorbeeld jug5 naar jug8, dan heb je in jug8 (8 - self.jug8) liter plaats,
        # en in jug5 heb je (self.jug5) liter water zitten. Het kleinste getal van die 2, kan je effectief overgieten zonder morsen.

    def find_solution(self):
        # we gaan hier BFS zoeken, aangezien we elke mogelijke optie geprobeerd willen hebben.
        frontier = deque([initial_state])
        explored = {initial_state}
        parent = {initial_state: None}

        while frontier:
            current = frontier.popleft()
            explored.add(current)
            for state in current.get_next_states():
                if state in explored or state in parent:
                    continue
                parent[state] = current
                if state[1] == 4 and state[2] == 4:
                    pad = [state.state]
                    stap = state

                    while state[stap] is not None:
                        stap = parent[stap]
                        pad.append(state.state)

                    pad.reverse()

                    return pad

                frontier.append(state)

        return None


if __name__ == "__main__":
    initial_state = WaterJugState(8, 5, 0)
    solution = initial_state.find_solution()
    if solution:
        print("Oplossing gevonden:")
        # print opeenvolgende stappen van de oplossing
        print(f"Pad: " + initial_state.find_solution())
    else:
        print("Geen oplossing gevonden.")
