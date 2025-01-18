import random


def get_random_node(node):
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