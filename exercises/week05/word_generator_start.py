"""
Oefening 1: Word Generator (Genetisch Algoritme)
==================================================
Evolueer een populatie van willekeurige zinnen naar een doelzin.
"""

import random
import string


class WordPuzzle:
    def __init__(
        self,
        target_phrase,
        population_size=100,
        mutation_rate=0.01,
        num_generations=10000,
    ):
        self.target_phrase = target_phrase
        self.population_size = population_size
        self.mutation_rate = mutation_rate
        self.num_generations = num_generations

    def generate_phrase(self, length):
        # Kies voor elke positie een willekeurig karakter.
        return "".join(random.choice(string.printable) for _ in range(length))

    def calculate_fitness(self, phrase):
        if not self.target_phrase:
            return 1.0

        # Tel hoeveel karakters op de juiste positie staan.
        correct = sum(
            char == target_char for char, target_char in zip(phrase, self.target_phrase)
        )

        return correct / len(self.target_phrase)

    def generate_population(self, size, phrase_length):
        return [self.generate_phrase(phrase_length) for _ in range(size)]

    def crossover(self, phrase1, phrase2):
        # Voor een intern splitspunt zijn minstens 2 karakters nodig.
        if len(phrase1) < 2:
            return phrase1

        split_point = random.randint(1, len(phrase1) - 1)

        return phrase1[:split_point] + phrase2[split_point:]

    def mutate(self, phrase, rate):
        # Beslis voor elk karakter afzonderlijk of het muteert.
        return "".join(
            random.choice(string.printable) if random.random() < rate else char
            for char in phrase
        )

    def select_best(self, population):
        # Sorteer van hoogste naar laagste fitness.
        sorted_population = sorted(population, key=self.calculate_fitness, reverse=True)

        # Kies de beste 20%, met minstens 2 indien beschikbaar.
        number_to_select = max(2, len(population) // 5)

        return sorted_population[:number_to_select]

    def genetic_algorithm(self):
        # 1. Maak de startpopulatie.
        population = self.generate_population(
            self.population_size, len(self.target_phrase)
        )

        for generation in range(self.num_generations):
            # 2. Selecteer de beste kandidaten.
            best_phrases = self.select_best(population)
            best_phrase = best_phrases[0]
            best_fitness = self.calculate_fitness(best_phrase)

            # 3. Toon de vooruitgang om de 100 generaties.
            if generation % 100 == 0 or best_phrase == self.target_phrase:
                print(
                    f"Generatie {generation}: {best_phrase!r} "
                    f"| Fitness: {best_fitness:.2%}"
                )

            # 4. Stop zodra de doelzin gevonden is.
            if best_phrase == self.target_phrase:
                return best_phrase

            # 5. Behoud de beste zin ongewijzigd: elitisme.
            new_population = [best_phrase]

            # 6. Vul de overige plaatsen met kinderen.
            while len(new_population) < self.population_size:
                parent1 = random.choice(best_phrases)
                parent2 = random.choice(best_phrases)

                child = self.crossover(parent1, parent2)
                child = self.mutate(child, self.mutation_rate)

                new_population.append(child)

            population = new_population

        # Generatielimiet bereikt: geef de beste gevonden zin terug.
        return max(population, key=self.calculate_fitness)


def main():
    target_phrase = "De basiswetten van de robotica werden ontwikkeld door Asimov"
    puzzle = WordPuzzle(target_phrase)
    best_phrase = puzzle.genetic_algorithm()
    print(f"Beste zin: {best_phrase}")


if __name__ == "__main__":
    main()
