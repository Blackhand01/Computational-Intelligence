import numpy as np
from typing import Callable, Optional
from src.core.tree import Tree, Node  # Presupponendo che Tree e Node siano definiti in tree.py

def point_mutation(tree: Tree, mutation_rate: float = 0.1) -> Tree:
    """
    Modifica casualmente i nodi di un albero con una certa probabilità.

    Args:
        tree (Tree): Albero su cui applicare la mutazione.
        mutation_rate (float): Probabilità di mutazione per ogni nodo.

    Returns:
        Tree: Albero mutato.
    """
    mutated_tree = tree.copy()
    for node in mutated_tree.traverse():
        if np.random.rand() < mutation_rate:
            node.mutate_value()
    return mutated_tree


def subtree_mutation(tree: Tree, max_depth: int) -> Tree:
    """
    Sostituisce un sottoalbero con un nuovo sottoalbero generato casualmente.

    Args:
        tree (Tree): Albero su cui applicare la mutazione.
        max_depth (int): Massima profondità del nuovo sottoalbero.

    Returns:
        Tree: Albero mutato.
    """
    mutated_tree = tree.copy()
    mutation_point = mutated_tree.random_node()
    new_subtree = Tree.generate_random_tree(max_depth=max_depth)
    mutated_tree.replace_subtree(mutation_point, new_subtree.root)
    return mutated_tree


def hoist_mutation(tree: Tree) -> Tree:
    """
    Sostituisce l'intero albero con uno dei suoi sottoalberi, riducendo la dimensione complessiva.

    Args:
        tree (Tree): Albero su cui applicare la mutazione.

    Returns:
        Tree: Albero mutato.
    """
    mutated_tree = tree.copy()
    mutation_point = mutated_tree.random_node()
    mutated_tree.root = mutation_point  # Usa il sottoalbero come nuovo albero
    return mutated_tree


def shrink_mutation(tree: Tree, max_size: int) -> Tree:
    """
    Riduce la dimensione dell'albero rimuovendo rami o nodi non necessari.

    Args:
        tree (Tree): Albero su cui applicare la mutazione.
        max_size (int): Dimensione massima desiderata.

    Returns:
        Tree: Albero mutato.
    """
    mutated_tree = tree.copy()
    while mutated_tree.size() > max_size:
        node_to_remove = mutated_tree.random_node(allow_root=False)
        mutated_tree.prune(node_to_remove)
    return mutated_tree


class MutationOperator:
    """
    Classe per gestire diverse strategie di mutazione.
    """
    def __init__(self):
        self.operators = {
            "point": point_mutation,
            "subtree": subtree_mutation,
            "hoist": hoist_mutation,
            "shrink": shrink_mutation,
        }

    def list_strategies(self) -> list:
        """
        Restituisce l'elenco delle strategie di mutazione disponibili.
        
        Returns:
            list: Nomi delle strategie disponibili.
        """
        return list(self.operators.keys())

    def apply(self, tree: Tree, strategy: str, **kwargs) -> Tree:
        """
        Applica la strategia di mutazione specificata.

        Args:
            tree (Tree): Albero su cui applicare la mutazione.
            strategy (str): Nome della strategia di mutazione.
            kwargs: Parametri aggiuntivi per la strategia.

        Returns:
            Tree: Albero mutato.
        """
        if strategy not in self.operators:
            raise ValueError(f"Strategia di mutazione non supportata: {strategy}")
        return self.operators[strategy](tree, **kwargs)
