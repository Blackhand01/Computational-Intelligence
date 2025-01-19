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
            return f"x[{self.value[1]}]" if self.is_variable() else str(self.value[1])
        elif len(self.children) == 1:
            return f"{self.op}({self.children[0]})"
        elif len(self.children) == 2:
            return f"({self.children[0]} {self.op} {self.children[1]})"
        return "N/A"
    
    def iterate_nodes(self):
            """
            Itera su tutti i nodi dell'albero a partire dal nodo corrente.

            Yields:
                Node: Il nodo corrente durante l'iterazione.
            """
            yield self  # Ritorna il nodo corrente
            for child in self.children:  # Itera sui figli
                yield from child.iterate_nodes()  # Ricorsione sui figli
                
    def is_variable(self):
        return isinstance(self.value, tuple) and self.value[0] == 'x'

    def is_constant(self):
        return isinstance(self.value, tuple) and self.value[0] == 'const'

    def validate(self) -> bool:
        """
        Validates the structure of the current node and its children.
        """
        # Leaf node (variable or constant)
        if self.value is not None:
            return self.op is None and len(self.children) == 0

        # Unary operator
        if self.op in [op.name for op in ALL_OPERATORS.values() if op.arity == 1]:
            return len(self.children) == 1 and self.children[0].validate()

        # Binary operator
        if self.op in [op.name for op in ALL_OPERATORS.values() if op.arity == 2]:
            return len(self.children) == 2 and all(child.validate() for child in self.children)

        return False  # Invalid node structure

    def evaluate_tree(self, x: np.ndarray) -> np.ndarray:
        """
        Valuta il nodo corrente e i suoi figli (ricorsivamente).
        """
        if self.op is None:
            if self.is_variable():
                return x[self.value[1], :]
            return np.full(x.shape[1], self.value[1], dtype=float)

        operator = ALL_OPERATORS.get(self.op)
        if operator is None:
            raise ValueError(f"Operatore sconosciuto: {self.op}")

        if operator.arity == 1:
            return operator.function(self.children[0].evaluate_tree(x))
        elif operator.arity == 2:
            left = self.children[0].evaluate_tree(x)
            right = self.children[1].evaluate_tree(x)
            return operator.function(left, right)

    def tree_to_expression(self) -> str:
        """
        Converte il nodo e i suoi figli in una rappresentazione simbolica.
        """
        if self.op is None:
            return f"x[{self.value[1]}]" if self.is_variable() else str(self.value[1])

        operator = ALL_OPERATORS.get(self.op)
        if operator is None:
            raise ValueError(f"Operatore sconosciuto: {self.op}")

        if operator.arity == 1:
            return f"{operator.numpy_symbol}({self.children[0].tree_to_expression()})"
        elif operator.arity == 2:
            left = self.children[0].tree_to_expression()
            right = self.children[1].tree_to_expression()
            return f"{operator.numpy_symbol}({left}, {right})"

    def copy_tree(self):
        """
        Crea una copia profonda del nodo corrente.
        """
        return Node(op=self.op, value=self.value, children=[child.copy_tree() for child in self.children])

    def tree_size(self) -> int:
        """
        Restituisce il numero di nodi nell'albero (incluso il nodo corrente).
        """
        return 1 + sum(child.tree_size() for child in self.children)

    def tree_depth(self) -> int:
        """
        Restituisce la profondità massima dell'albero a partire dal nodo corrente.
        """
        if not self.children:
            return 1
        return 1 + max(child.tree_depth() for child in self.children)

    @staticmethod
    def generate_random_tree(max_depth: int, n_features: int, grow: bool = True):
        """
        Genera un albero casuale con una profondità massima.
        """
        if max_depth == 0:
            return Node(op=None, value=random_variable(n_features) if random.random() < 0.5 else random_constant())

        node_type = random.choice(['unary', 'binary', 'leaf']) if grow else random.choice(['unary', 'binary'])

        if node_type == 'leaf':
            return Node(op=None, value=random_variable(n_features) if random.random() < 0.5 else random_constant())
        elif node_type == 'unary':
            op = random.choice([op.name for op in ALL_OPERATORS.values() if op.arity == 1])
            child = Node.generate_random_tree(max_depth - 1, n_features, grow)
            return Node(op=op, children=[child])
        else:  # node_type == 'binary'
            op = random.choice([op.name for op in ALL_OPERATORS.values() if op.arity == 2])
            left_child = Node.generate_random_tree(max_depth - 1, n_features, grow)
            right_child = Node.generate_random_tree(max_depth - 1, n_features, grow)
            return Node(op=op, children=[left_child, right_child])

    @staticmethod
    def get_random_node(node):
        """
        Restituisce un nodo casuale e il suo genitore dall'albero.
        """
        all_nodes = []

        def traverse(current, parent):
            all_nodes.append((current, parent))
            for child in current.children:
                traverse(child, current)

        traverse(node, None)
        return random.choice(all_nodes)
    
    def replace_with(self, new_node):
        """
        Sostituisce il contenuto del nodo corrente con il contenuto di un altro nodo.
        Args:
            new_node (Node): Il nodo che sostituirà il nodo corrente.
        """
        self.op = new_node.op
        self.value = new_node.value
        self.children = [child.copy_tree() for child in new_node.children]

# Funzioni di supporto

def random_variable(n_features):
    i = random.randint(0, n_features - 1)
    return ('x', i)

def random_constant():
    c = np.round(random.uniform(-1, 1), 3)
    return ('const', c)
