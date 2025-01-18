import random
from tree import copy_tree, generate_random_tree, random_variable, random_constant
from safe_math import ALL_OPERATORS
from gp.utils import get_random_node

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
    node, _ = get_random_node(mutant)

    if node.op is None:
        # Nodo foglia
        node.value = random_variable(n_features) if random.random() < 0.5 else random_constant()
    else:
        current_arity = ALL_OPERATORS[node.op].arity
        if current_arity == 1:
            valid_unaries = [op for op in ALL_OPERATORS.values() if op.arity == 1]
            node.op = random.choice(valid_unaries).name
        elif current_arity == 2:
            valid_binaries = [op for op in ALL_OPERATORS.values() if op.arity == 2]
            node.op = random.choice(valid_binaries).name
            while len(node.children) < 2:
                node.children.append(generate_random_tree(1, n_features, grow=True))

    return mutant
