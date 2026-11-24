"""
Oefening 2: Knapsack Probleem met pygad
=========================================
Los het knapsack probleem op met een genetisch algoritme.
"""

import pygad
import numpy as np

# Data
capaciteit = 10
gewichten = np.array([5, 4, 6, 3])
waarden = np.array([10, 40, 30, 50])
n_voorwerpen = len(gewichten)


def fitness_func(ga_instance, solution, solution_idx):
    # TODO: bereken totale waarde, straf als gewicht > capaciteit
    # Een 1 betekent dat het voorwerp wordt meegenomen.
    totaal_gewicht = np.sum(solution * gewichten)
    totale_waarde = np.sum(solution * waarden)

    # Strafscore wanneer de rugzak te zwaar is.
    if totaal_gewicht > capaciteit:
        return -1000

    return totale_waarde


# TODO: configureer pygad.GA (zie OneMax.py uit de cursus)
ga_instance = pygad.GA(
    num_generations=100,
    num_parents_mating=4,
    fitness_func=fitness_func,
    sol_per_pop=20,
    num_genes=n_voorwerpen,
    # Elk gen is een geheel getal: 0 of 1.
    gene_type=int,
    gene_space=[0, 1],
    # Selecteer de beste oplossingen als ouders.
    parent_selection_type="sss",
    # Behoud de twee beste oplossingen ongewijzigd.
    keep_elitism=2,
    crossover_type="single_point",
    mutation_type="random",
    mutation_percent_genes=10,
    # Maakt de uitvoering reproduceerbaar binnen dezelfde versie.
    random_seed=42,
)
ga_instance.run()

# Oplossing tonen
solution, solution_fitness, _ = ga_instance.best_solution()
print("Gekozen voorwerpen:", solution)
print("Totale waarde:", solution_fitness)
