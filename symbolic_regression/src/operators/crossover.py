import numpy as np
from typing import Tuple, Callable, Optional
from src.core.tree import Node, Tree  # Presupponendo che `Tree` e `Node` siano definiti in `tree.py`


def subtree_crossover(parent1: Tree, parent2: Tree) -> Tuple[Tree, Tree]:
    """
    Esegue il crossover per sottoalberi tra due alberi genitori.

    Args:
        parent1 (Tree): Primo albero genitore.
        parent2 (Tree): Secondo albero genitore.

    Returns:
        Tuple[Tree, Tree]: Due nuovi alberi figli dopo il crossover.
    """
    # Seleziona nodi casuali dai due alberi
    crossover_point1 = parent1.random_node()
    crossover_point2 = parent2.random_node()

    # Scambia i sottoalberi nei genitori
    child1 = parent1.copy()
    child2 = parent2.copy()

    child1.replace_subtree(crossover_point1, crossover_point2)
    child2.replace_subtree(crossover_point2, crossover_point1)

    return child1, child2


def uniform_crossover(parent1: Tree, parent2: Tree, prob: float = 0.5) -> Tuple[Tree, Tree]:
    """
    Applica un crossover uniforme, scambiando nodi casuali con una certa probabilità.

    Args:
        parent1 (Tree): Primo albero genitore.
        parent2 (Tree): Secondo albero genitore.
        prob (float): Probabilità di scambio per ogni nodo.

    Returns:
        Tuple[Tree, Tree]: Due nuovi alberi figli dopo il crossover uniforme.
    """
    child1 = parent1.copy()
    child2 = parent2.copy()

    for node1, node2 in zip(child1.traverse(), child2.traverse()):
        if np.random.rand() < prob:
            child1.replace_subtree(node1, node2)
            child2.replace_subtree(node2, node1)

    return child1, child2


def one_point_crossover(parent1: Tree, parent2: Tree) -> Tuple[Tree, Tree]:
    """
    Applica un crossover a un singolo punto tra due alberi genitori.

    Args:
        parent1 (Tree): Primo albero genitore.
        parent2 (Tree): Secondo albero genitore.

    Returns:
        Tuple[Tree, Tree]: Due nuovi alberi figli.
    """
    # Trova un punto di crossover casuale per ciascun genitore
    crossover_point1 = parent1.random_node()
    crossover_point2 = parent2.random_node()

    # Crea figli scambiando i sottoalberi
    child1 = parent1.copy()
    child2 = parent2.copy()

    child1.replace_subtree(crossover_point1, crossover_point2)
    child2.replace_subtree(crossover_point2, crossover_point1)

    return child1, child2


def size_limit_crossover(parent1: Tree, parent2: Tree, max_size: int) -> Tuple[Tree, Tree]:
    """
    Applica un crossover limitato nella dimensione degli alberi.

    Args:
        parent1 (Tree): Primo albero genitore.
        parent2 (Tree): Secondo albero genitore.
        max_size (int): Dimensione massima consentita per gli alberi figli.

    Returns:
        Tuple[Tree, Tree]: Due nuovi alberi figli.
    """
    for _ in range(10):  # Limita a 10 tentativi
        child1, child2 = subtree_crossover(parent1, parent2)
        if child1.size() <= max_size and child2.size() <= max_size:
            return child1, child2

    # Ritorna gli alberi genitori se non è possibile rispettare il limite di dimensione
    return parent1.copy(), parent2.copy()


class CrossoverOperator:
    """
    Classe per gestire diverse strategie di crossover.
    """
    def __init__(self):
        self.operators = {
            "subtree": subtree_crossover,
            "uniform": uniform_crossover,
            "one_point": one_point_crossover,
            "size_limit": size_limit_crossover,
        }
    
    def list_strategies(self) -> list:
        """
        Restituisce l'elenco delle strategie di crossover disponibili.
        
        Returns:
            list: Nomi delle strategie disponibili.
        """
        return list(self.operators.keys())

    def apply(self, parent1: Tree, parent2: Tree, strategy: str, **kwargs) -> Tuple[Tree, Tree]:
        """
        Applica la strategia di crossover specificata.

        Args:
            parent1 (Tree): Primo albero genitore.
            parent2 (Tree): Secondo albero genitore.
            strategy (str): Nome della strategia di crossover da applicare.
            kwargs: Parametri aggiuntivi per la strategia.

        Returns:
            Tuple[Tree, Tree]: Due nuovi alberi figli.
        """
        if strategy not in self.operators:
            raise ValueError(f"Strategia di crossover non supportata: {strategy}")
        return self.operators[strategy](parent1, parent2, **kwargs)
    