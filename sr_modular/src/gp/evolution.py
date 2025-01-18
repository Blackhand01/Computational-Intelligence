import random
from tree import generate_random_tree, copy_tree
from gp.mutation import mutate
from gp.crossover import crossover
from gp.selection import tournament_selection
from gp_config import MAX_DEPTH, ELITISM, POP_SIZE, PARTIAL_REINIT_EVERY, PARTIAL_REINIT_RATIO, CROSSOVER_RATE, MUTATION_RATE
from evaluator import Evaluator


def generate_population(max_depth, n_features):
    """
    Crea la popolazione iniziale.
    """
    population = [
        generate_random_tree(max_depth, n_features, grow=random.random() > 0.5)
        for _ in range(POP_SIZE)
    ]
    return population

def evolve_population(population, x, y, n_features, generation, bloat_penalty):
    """
    Evoluzione della popolazione.
    """
    ranked_pop = sorted(population, key=lambda ind: Evaluator.fitness_function(ind, x, y, bloat_penalty))
    new_population = ranked_pop[:ELITISM]

    while len(new_population) < POP_SIZE:
        parent1 = tournament_selection(ranked_pop, x, y, bloat_penalty)
        parent2 = tournament_selection(ranked_pop, x, y, bloat_penalty)

        if random.random() < CROSSOVER_RATE:
            off1, off2 = crossover(parent1, parent2)
        else:
            off1, off2 = copy_tree(parent1), copy_tree(parent2)

        if random.random() < MUTATION_RATE:
            off1 = mutate(off1, n_features)
        if random.random() < MUTATION_RATE:
            off2 = mutate(off2, n_features)

        new_population.append(off1)
        if len(new_population) < POP_SIZE:
            new_population.append(off2)

    if generation % PARTIAL_REINIT_EVERY == 0 and generation != 0:
        for i in range(int(PARTIAL_REINIT_RATIO * POP_SIZE)):
            new_population[-(i + 1)] = generate_random_tree(MAX_DEPTH, n_features, grow=True)

    return new_population


class GeneticProgramming:
    """
    Coordina la programmazione genetica.
    """
    @staticmethod
    def run_gp(x, y, n_features, generations, bloat_penalty):
        # Genera la popolazione iniziale
        population = generate_population(MAX_DEPTH, n_features)
        evaluator = Evaluator()

        for gen in range(generations):
            population = evolve_population(population, x, y, n_features, gen, bloat_penalty)

        # Restituisci il miglior individuo dalla popolazione finale
        best_individual, _ = evaluator.get_best_individual(population, x, y, bloat_penalty)
        return best_individual

