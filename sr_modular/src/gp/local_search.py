import random
import numpy as np
from tree import Node
from evaluator import Evaluator
from safe_math import ALL_OPERATORS


class LocalSearchManager:
    """
    Gestisce dinamicamente la scelta tra diverse strategie di local search
    (es. hill climbing, random improvement, best-subtree replacement, ecc.)
    allo scopo di migliorare localmente i singoli individui.
    """
    def __init__(self, statistics, logger):
        self.statistics = statistics
        self.evaluator = Evaluator()
        self.active_strategy = "hill_climb"  # Strategia di default
        self.logger = logger

    def hill_climb(self, individual: Node, x: np.ndarray, y: np.ndarray, bloat_penalty: float) -> Node:
        """
        Esempio semplice di hill climbing:
        1. Sceglie un nodo a caso
        2. Prova una piccola modifica (p.es. mutazione su op/valore)
        3. Se migliora la fitness, accetta la modifica
        """
        current_fitness = self.evaluator.fitness_function(individual, x, y, bloat_penalty)
        candidate = individual.copy_tree()

        # Esempio di piccola modifica: sostituisco un nodo a caso con uno generato casualmente
        node, _ = Node.get_random_node(candidate)

        # Se è un nodo interno, cambio operatore ma mantengo l'arity
        if node.op is not None:
            current_arity = ALL_OPERATORS[node.op].arity
            valid_ops = [op for op in ALL_OPERATORS.values() if op.arity == current_arity]
            node.op = random.choice(valid_ops).name
        else:
            # Se foglia, variabile o costante
            if node.is_variable():
                node.value = ('const', random.uniform(-1, 1))
            else:
                var_index = random.randint(0, x.shape[0] - 1)
                node.value = ('x', var_index)

        # Valuto la fitness della soluzione modificata
        new_fitness = self.evaluator.fitness_function(candidate, x, y, bloat_penalty)

        if new_fitness < current_fitness:
            self.logger.info(f"Hill climb improved fitness from {current_fitness:.4f} to {new_fitness:.4f}.")
            return candidate
        else:
            self.logger.info(f"Hill climb did not improve fitness: {current_fitness:.4f}.")
            return individual

    def random_improvement(self, individual: Node, x: np.ndarray, y: np.ndarray, bloat_penalty: float) -> Node:
        """
        Esempio di 'random improvement':
        - Si generano alcune copie mutate casualmente e si sceglie la migliore se migliora.
        """
        current_fitness = self.evaluator.fitness_function(individual, x, y, bloat_penalty)
        best_candidate = individual
        n_tries = 3  # Prova alcune piccole mutazioni casuali

        for _ in range(n_tries):
            candidate = individual.copy_tree()
            node, _ = Node.get_random_node(candidate)
            if node.op is not None:
                current_arity = ALL_OPERATORS[node.op].arity
                valid_ops = [op for op in ALL_OPERATORS.values() if op.arity == current_arity]
                node.op = random.choice(valid_ops).name
            else:
                if node.is_variable():
                    node.value = ('const', random.uniform(-1, 1))
                else:
                    var_index = random.randint(0, x.shape[0] - 1)
                    node.value = ('x', var_index)

            new_fitness = self.evaluator.fitness_function(candidate, x, y, bloat_penalty)
            if new_fitness < current_fitness:
                best_candidate = candidate
                current_fitness = new_fitness
                self.logger.info(f"Random improvement found better fitness: {new_fitness:.4f}.")

        return best_candidate

    def best_subtree_replacement(self, individual: Node, x: np.ndarray, y: np.ndarray, bloat_penalty: float) -> Node:
        """
        Esempio di sostituzione di un sotto-albero con uno nuovo, cercando miglioramento.
        """
        current_fitness = self.evaluator.fitness_function(individual, x, y, bloat_penalty)
        candidate = individual.copy_tree()
        node, _ = Node.get_random_node(candidate)

        new_subtree = Node.generate_random_tree(max_depth=2, n_features=x.shape[0], grow=True)
        node.replace_with(new_subtree)
        new_fitness = self.evaluator.fitness_function(candidate, x, y, bloat_penalty)

        if new_fitness < current_fitness:
            self.logger.info(f"Best subtree replacement improved fitness from {current_fitness:.4f} to {new_fitness:.4f}.")
            return candidate
        else:
            self.logger.info(f"Best subtree replacement did not improve fitness: {current_fitness:.4f}.")
            return individual

    def choose_strategy(self):
        """
        Sceglie dinamicamente la strategia di local search in base alle statistiche globali.
        """
        previous_strategy = self.active_strategy

        if self.statistics.get("complexity", 0) > 15:
            self.active_strategy = "hill_climb"
        elif self.statistics.get("diversity", 0) < 3:
            self.active_strategy = "best_subtree_replacement"
        else:
            self.active_strategy = "random_improvement"

        if self.active_strategy != previous_strategy:
            self.logger.info(
                [
                    f"Local search strategy changed from {previous_strategy} to {self.active_strategy}.",
                    f"Reason: complexity={self.statistics.get('complexity', 0):.2f}, diversity={self.statistics.get('diversity', 0):.2f}."
                ]
            )

    def local_search(self, individual: Node, x: np.ndarray, y: np.ndarray, bloat_penalty: float) -> Node:
        """
        Applica la strategia di local search scelta dinamicamente all'individuo.
        """
        self.choose_strategy()
        strategies = {
            "hill_climb": self.hill_climb,
            "random_improvement": self.random_improvement,
            "best_subtree_replacement": self.best_subtree_replacement
        }
        return strategies[self.active_strategy](individual, x, y, bloat_penalty)

    def get_active_strategy(self) -> str:
        """
        Ritorna la strategia di local search attualmente in uso.
        """
        return self.active_strategy
