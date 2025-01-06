# File: src/core/genetic_programming.py

import numpy as np
from typing import List, Tuple
from src.core.tree import Tree, validate_tree
from src.operators.crossover import CrossoverOperator
from src.operators.mutation import MutationOperator
from src.core.fitness import FitnessEvaluator, validate_fitness_scores
from src.core.dynamic_strategies import choose_crossover, choose_mutation
from src.operators.definitions import operator_set  # Importa operator_set

class GeneticProgram:
    """
    Gestisce il ciclo evolutivo di un sistema di programmazione genetica.
    """
    def __init__(
        self,
        population_size: int,
        max_generations: int,
        max_tree_depth: int,
        mutation_rate: float,
        crossover_rate: float,
        fitness_evaluator: FitnessEvaluator,
        max_nodes: int = 100,
        n_variables: int = 1,  # Aggiunto parametro
    ):
        """
        Inizializza il sistema di programmazione genetica.

        Args:
            population_size (int): Dimensione della popolazione.
            max_generations (int): Numero massimo di generazioni.
            max_tree_depth (int): Profondità massima degli alberi.
            mutation_rate (float): Probabilità di mutazione.
            crossover_rate (float): Probabilità di crossover.
            fitness_evaluator (FitnessEvaluator): Oggetto per la valutazione del fitness.
            max_nodes (int): Numero massimo di nodi consentiti per albero.
            n_variables (int): Numero di variabili nel dataset.
        """
        self.population_size = population_size
        self.max_generations = max_generations
        self.max_tree_depth = max_tree_depth
        self.initial_mutation_rate = mutation_rate  # Salva il valore iniziale
        self.initial_crossover_rate = crossover_rate  # Salva il valore iniziale
        self.fitness_evaluator = fitness_evaluator
        self.max_nodes = max_nodes
        self.n_variables = n_variables  # Inizializza l'attributo

        self.population: List[Tree] = []
        self.fitness_scores: List[float] = []

        # Operatori di crossover e mutazione
        self.crossover_operator = CrossoverOperator()
        self.mutation_operator = MutationOperator()

    def initialize_population(self) -> None:
        """
        Genera la popolazione iniziale di alberi casuali, validando ciascun albero.
        """
        self.population = []
        while len(self.population) < self.population_size:
            tree = Tree.generate_random_tree(
                max_depth=self.max_tree_depth, 
                operator_set=operator_set,  # Passa l'istanza di OperatorSet
                n_variables=self.n_variables  # Passa il numero di variabili
            )
            if validate_tree(tree, max_tree_depth=self.max_tree_depth, max_nodes=self.max_nodes, n_variables=self.n_variables):
                self.population.append(tree)

    def evaluate_population(self, x: np.ndarray) -> None:
        """
        Calcola la fitness per ogni individuo nella popolazione.

        Args:
            x (np.ndarray): Input del dataset per la valutazione del fitness.
        """
        self.fitness_scores = self.fitness_evaluator.evaluate_population(self.population)

    def select_parents(self, x: np.ndarray) -> Tuple[Tree, Tree]:
        """
        Seleziona due genitori dalla popolazione usando selezione a torneo.

        Args:
            x (np.ndarray): Input del dataset per la valutazione del fitness.

        Returns:
            Tuple[Tree, Tree]: Due alberi genitori selezionati.
        """
        # Implementazione della selezione a torneo
        tournament_size = 3
        selected = []
        for _ in range(2):
            participants = random.sample(list(zip(self.population, self.fitness_scores)), tournament_size)
            winner = min(participants, key=lambda ind: ind[1])[0]
            selected.append(winner)
        return selected[0], selected[1]

    def apply_crossover(self, parent1: Tree, parent2: Tree, crossover_strategy: str) -> Tuple[Tree, Tree]:
        """
        Applica crossover tra due genitori usando la strategia specificata.

        Args:
            parent1 (Tree): Primo genitore.
            parent2 (Tree): Secondo genitore.
            crossover_strategy (str): Strategia di crossover da applicare.

        Returns:
            Tuple[Tree, Tree]: Due nuovi alberi figli validati.
        """
        kwargs = {}
        if crossover_strategy == "size_limit":
            kwargs["max_size"] = self.max_nodes

        child1, child2 = self.crossover_operator.apply(parent1, parent2, strategy=crossover_strategy, **kwargs)
        if not validate_tree(child1, max_tree_depth=self.max_tree_depth, max_nodes=self.max_nodes, n_variables=self.n_variables):
            child1 = parent1.copy()
        if not validate_tree(child2, max_tree_depth=self.max_tree_depth, max_nodes=self.max_nodes, n_variables=self.n_variables):
            child2 = parent2.copy()
        return child1, child2

    def apply_mutation(self, tree: Tree, mutation_strategy: str) -> Tree:
        """
        Applica mutazione a un albero usando la strategia specificata.

        Args:
            tree (Tree): Albero su cui applicare la mutazione.
            mutation_strategy (str): Strategia di mutazione da applicare.

        Returns:
            Tree: Albero mutato validato.
        """
        kwargs = {}
        if mutation_strategy == "subtree":
            kwargs["max_depth"] = self.max_tree_depth
        kwargs["n_variables"] = self.n_variables  # Aggiungi n_variables

        mutated_tree = self.mutation_operator.apply(tree, strategy=mutation_strategy, **kwargs)
        if not validate_tree(mutated_tree, max_tree_depth=self.max_tree_depth, max_nodes=self.max_nodes, n_variables=self.n_variables):
            return tree.copy()
        return mutated_tree

    def evolve_population(self, x: np.ndarray, current_generation: int) -> None:
        """
        Evolve la popolazione corrente per una generazione utilizzando strategie dinamiche.

        Args:
            x (np.ndarray): Input del dataset per la valutazione del fitness.
            current_generation (int): Numero della generazione corrente.
        """
        new_population = []
        crossover_strategy = choose_crossover(self.population, current_generation, self.max_generations)
        mutation_strategy = choose_mutation(self.population, self.fitness_scores, current_generation, self.max_generations)

        while len(new_population) < self.population_size:
            parent1, parent2 = self.select_parents(x)
            child1, child2 = self.apply_crossover(parent1, parent2, crossover_strategy)
            child1 = self.apply_mutation(child1, mutation_strategy)
            child2 = self.apply_mutation(child2, mutation_strategy)

            if validate_tree(child1, max_tree_depth=self.max_tree_depth, max_nodes=self.max_nodes, n_variables=self.n_variables):
                new_population.append(child1)
            if len(new_population) < self.population_size and validate_tree(child2, max_tree_depth=self.max_tree_depth, max_nodes=self.max_nodes, n_variables=self.n_variables):
                new_population.append(child2)

        self.population = new_population[:self.population_size]
        self.evaluate_population(x)

    def run(self, x: np.ndarray, max_no_improvement: int = 10) -> Tree:
        """
        Esegue l'intero ciclo evolutivo con strategie dinamiche.

        Args:
            x (np.ndarray): Input del dataset per la valutazione del fitness.
            max_no_improvement (int): Numero massimo di generazioni senza miglioramenti.

        Returns:
            Tree: Miglior individuo trovato.
        """
        self.initialize_population()
        self.evaluate_population(x)

        if not validate_fitness_scores(self.fitness_scores):
            print("Invalid fitness scores detected after initialization. Re-evaluating...")
            self.evaluate_population(x)

        best_fitness = min(self.fitness_scores)
        best_individual = self.population[np.argmin(self.fitness_scores)]
        no_improvement = 0

        for generation in range(self.max_generations):
            print(f"Generazione {generation + 1}/{self.max_generations}")
            print(f"  Miglior fitness attuale: {best_fitness:.6f}")
            if no_improvement >= max_no_improvement:
                print("  Nessun miglioramento, fermo l'evoluzione.")
                break

            self.evolve_population(x, generation)

            if not validate_fitness_scores(self.fitness_scores):
                print("Invalid fitness scores detected during evolution. Re-evaluating...")
                self.evaluate_population(x)

            current_best_fitness = min(self.fitness_scores)
            if current_best_fitness < best_fitness:
                best_fitness = current_best_fitness
                best_individual = self.population[np.argmin(self.fitness_scores)]
                no_improvement = 0
            else:
                no_improvement += 1

        print(f"Fitness migliore trovato: {best_fitness:.6f}")
        return best_individual
