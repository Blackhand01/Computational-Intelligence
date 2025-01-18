import random
import numpy as np
from safe_math import ALL_OPERATORS

class Node:
    """
    Classe che rappresenta un nodo dell’albero GP.
    - op: operatore (stringa) o None se foglia.
    - value: se foglia, ('x', i) oppure ('const', c).
    - children: lista di nodi (0, 1 o 2 a seconda dell'operatore).
    """
    def __init__(self, op=None, value=None, children=None):
        self.op = op
        self.value = value
        self.children = children or []

    def __str__(self):
        if self.op is None:
            return f"x[{self.value[1]}]" if is_variable(self.value) else str(self.value[1])
        elif len(self.children) == 1:
            return f"{self.op}({self.children[0]})"
        elif len(self.children) == 2:
            return f"({self.children[0]} {self.op} {self.children[1]})"
        return "N/A"

# Funzioni di supporto per foglie (variable/constant)
def random_variable(n_features):
    i = random.randint(0, n_features - 1)
    return ('x', i)

def random_constant():
    c = np.round(random.uniform(-1, 1), 3)
    return ('const', c)

def is_variable(value):
    return isinstance(value, tuple) and value[0] == 'x'

def is_constant(value):
    return isinstance(value, tuple) and value[0] == 'const'

# Funzioni per dimensione e profondità dell'albero
def tree_size(node):
    return 1 + sum(tree_size(child) for child in node.children)

def tree_depth(node):
    if len(node.children) == 0:
        return 1
    return 1 + max(tree_depth(child) for child in node.children)


# Generazione casuale dell'albero
def generate_random_tree(max_depth, n_features, grow=True):
    if max_depth == 0:
        return Node(op=None, value=random_variable(n_features) if random.random() < 0.5 else random_constant())

    node_type = random.choice(['unary', 'binary', 'leaf']) if grow else random.choice(['unary', 'binary'])

    if node_type == 'leaf':
        return Node(op=None, value=random_variable(n_features) if random.random() < 0.5 else random_constant())
    elif node_type == 'unary':
        op = random.choice([op.name for op in ALL_OPERATORS.values() if op.arity == 1])
        child = generate_random_tree(max_depth - 1, n_features, grow)
        return Node(op=op, children=[child])
    else:  # node_type == 'binary'
        op = random.choice([op.name for op in ALL_OPERATORS.values() if op.arity == 2])
        left_child = generate_random_tree(max_depth - 1, n_features, grow)
        right_child = generate_random_tree(max_depth - 1, n_features, grow)
        return Node(op=op, children=[left_child, right_child])


# Valutazione dell'albero
def evaluate_tree(node, x):
    if node.op is None:
        if is_variable(node.value):
            i = node.value[1]
            return x[i, :]
        else:
            c = node.value[1]
            return np.full(x.shape[1], c, dtype=float)

    operator = ALL_OPERATORS.get(node.op)
    if operator is None:
        raise ValueError(f"Operatore sconosciuto: {node.op}")

    if operator.arity == 1:
        return operator.function(evaluate_tree(node.children[0], x))
    elif operator.arity == 2:
        if len(node.children) < 2:
            raise ValueError(f"Nodo binario {node.op} ha meno di due figli: {node.children}")
        left = evaluate_tree(node.children[0], x)
        right = evaluate_tree(node.children[1], x)
        return operator.function(left, right)
    
def validate_tree(node):
    if node.op is None:
        return True
    operator = ALL_OPERATORS.get(node.op)
    if operator.arity != len(node.children):
        raise ValueError(f"Nodo {node.op} ha un numero errato di figli: {len(node.children)}")
    return all(validate_tree(child) for child in node.children)


# Copia di un albero
def copy_tree(node):
    return Node(op=node.op, value=node.value, children=[copy_tree(child) for child in node.children])

# Crossover
def crossover(parent1, parent2):
    child1 = copy_tree(parent1)
    child2 = copy_tree(parent2)
    node1, _ = get_random_node(child1)
    node2, _ = get_random_node(child2)

    node1.op, node2.op = node2.op, node1.op
    node1.value, node2.value = node2.value, node1.value
    node1.children, node2.children = node2.children, node1.children

    return child1, child2

# Mutazione
def mutate(individual, n_features):
    mutant = copy_tree(individual)
    node, _ = get_random_node(mutant)

    if node.op is None:
        node.value = random_constant() if is_variable(node.value) else random_variable(n_features)
    else:
        if len(node.children) == 1:
            node.op = random.choice([op.name for op in ALL_OPERATORS.values() if op.arity == 1])
        elif len(node.children) == 2:
            node.op = random.choice([op.name for op in ALL_OPERATORS.values() if op.arity == 2])

    return mutant

# Funzioni ausiliarie
def get_random_node(node):
    all_nodes = []

    def traverse(current, parent):
        all_nodes.append((current, parent))
        for child in current.children:
            traverse(child, current)

    traverse(node, None)
    return random.choice(all_nodes)

# Conversione dell'albero in espressione
def tree_to_expression(node):
    if node.op is None:
        return f"x[{node.value[1]}]" if is_variable(node.value) else str(node.value[1])

    operator = ALL_OPERATORS.get(node.op)
    if operator is None:
        raise ValueError(f"Operatore sconosciuto: {node.op}")

    if operator.arity == 1:
        return f"{operator.numpy_symbol}({tree_to_expression(node.children[0])})"
    elif operator.arity == 2:
        left = tree_to_expression(node.children[0])
        right = tree_to_expression(node.children[1])
        return f"{operator.numpy_symbol}({left}, {right})"

    return "0"
