from tree import copy_tree
from gp.utils import get_random_node

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
    node1, _ = get_random_node(child1)
    node2, _ = get_random_node(child2)

    # Saltiamo se uno dei nodi è una foglia
    if node1.op is None or node2.op is None:
        return child1, child2

    # Scambio nodi
    node1.op, node2.op = node2.op, node1.op
    node1.children, node2.children = node2.children, node1.children

    return child1, child2
