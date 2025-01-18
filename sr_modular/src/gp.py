import random
from tree import Node, generate_random_tree, copy_tree, tree_depth, is_variable, random_constant, random_variable
from evaluator import Evaluator
from gp_config import (POP_SIZE, MAX_DEPTH, N_GENERATIONS, TOURNAMENT_SIZE, 
                       MUTATION_RATE, CROSSOVER_RATE, ELITISM, BLOAT_PENALTY,
                       PARTIAL_REINIT_EVERY, PARTIAL_REINIT_RATIO)
from safe_math import ALL_OPERATORS

class GeneticProgramming:
    """
    Modulo per la programmazione genetica che include evoluzione, crossover e mutazione.
    """
    @staticmethod
    def tournament_selection(population, x, y, bloat_penalty):
        """
        Seleziona il miglior individuo da un sottoinsieme casuale della popolazione.

        Args:
            population (list[Node]): Lista degli alberi della popolazione.
            x (np.ndarray): Array di input.
            y (np.ndarray): Array di output atteso.
            bloat_penalty (float): Penalità applicata in base alla dimensione degli alberi.

        Returns:
            Node: L'individuo selezionato.
        """
        competitors = random.sample(population, TOURNAMENT_SIZE)
        evaluator = Evaluator()
        best = min(competitors, key=lambda ind: evaluator.fitness_function(ind, x, y, bloat_penalty))
        return best

    @staticmethod
    def crossover(parent1, parent2):
        """
        Applica il crossover tra due alberi genitori.

        Args:
            parent1 (Node): Primo genitore.
            parent2 (Node): Secondo genitore.

        Returns:
            Tuple[Node, Node]: Due figli risultanti dal crossover.
        """
        child1 = copy_tree(parent1)
        child2 = copy_tree(parent2)

        node1, _ = GeneticProgramming._get_random_node(child1)
        node2, _ = GeneticProgramming._get_random_node(child2)

        # Scambio "in-place"
        node1.op, node2.op = node2.op, node1.op
        node1.value, node2.value = node2.value, node1.value
        node1.children, node2.children = node2.children, node1.children

        return child1, child2

    @staticmethod
    def mutate(individual, n_features):
        """
        Applica una mutazione casuale a un albero.

        Args:
            individual (Node): Albero da mutare.
            n_features (int): Numero di feature disponibili.

        Returns:
            Node: Albero mutato.
        """
        mutant = copy_tree(individual)
        node, _ = GeneticProgramming._get_random_node(mutant)

        if node.op is None:
            # Switch costante/variabile
            node.value = (random_constant() if is_variable(node.value)
                          else random_variable(n_features))
        else:
            node.op = random.choice([op.name for op in ALL_OPERATORS.values()])

        return mutant

    @staticmethod
    def evolve_population(population, x, y, n_features, generation):
        """
        Evolve la popolazione per una generazione.

        Args:
            population (list[Node]): Lista degli alberi della popolazione.
            x (np.ndarray): Array di input.
            y (np.ndarray): Array di output atteso.
            n_features (int): Numero di feature disponibili.
            generation (int): Indice della generazione corrente.

        Returns:
            list[Node]: Nuova popolazione evoluta.
        """
        evaluator = Evaluator()
        ranked_pop = sorted(population, key=lambda ind: evaluator.fitness_function(ind, x, y, BLOAT_PENALTY))
        new_population = ranked_pop[:ELITISM]  # Elitismo

        while len(new_population) < POP_SIZE:
            parent1 = GeneticProgramming.tournament_selection(ranked_pop, x, y, BLOAT_PENALTY)
            parent2 = GeneticProgramming.tournament_selection(ranked_pop, x, y, BLOAT_PENALTY)

            if random.random() < CROSSOVER_RATE:
                off1, off2 = GeneticProgramming.crossover(parent1, parent2)
            else:
                off1, off2 = copy_tree(parent1), copy_tree(parent2)

            if random.random() < MUTATION_RATE:
                off1 = GeneticProgramming.mutate(off1, n_features)
            if random.random() < MUTATION_RATE:
                off2 = GeneticProgramming.mutate(off2, n_features)

            new_population.append(off1)
            if len(new_population) < POP_SIZE:
                new_population.append(off2)

        if generation % PARTIAL_REINIT_EVERY == 0 and generation != 0:
            n_reinit = int(PARTIAL_REINIT_RATIO * POP_SIZE)
            for i in range(n_reinit):
                new_population[-(i + 1)] = generate_random_tree(MAX_DEPTH, n_features, grow=True)

        return new_population

    @staticmethod
    def _get_random_node(node):
        """
        Restituisce un nodo casuale e il suo genitore dall'albero.

        Args:
            node (Node): Nodo radice dell'albero.

        Returns:
            Tuple[Node, Node]: Nodo casuale e suo genitore.
        """
        all_nodes = []

        def traverse(current, parent):
            all_nodes.append((current, parent))
            for child in current.children:
                traverse(child, current)

        traverse(node, None)
        return random.choice(all_nodes)

# Esempio di utilizzo
if __name__ == "__main__":
    import numpy as np
    from tree import generate_random_tree

    x = np.random.rand(3, 100)  # 3 feature, 100 campioni
    y = np.sin(x[0]) + np.cos(x[1])  # Output atteso

    population = [generate_random_tree(MAX_DEPTH, x.shape[0]) for _ in range(POP_SIZE)]

    gp = GeneticProgramming()
    for generation in range(N_GENERATIONS):
        population = gp.evolve_population(population, x, y, x.shape[0], generation)

    print("Evoluzione completata.")
