import numpy as np
from typing import List, Optional, Union, Any
from src.operators.definitions import OperatorSpec, OperatorSet
import random
from sympy import Symbol

# Initialize the operator set
operator_set = OperatorSet()

# Separate unary and binary operators for ease of use
UNARY_OPERATORS = operator_set.get_unary_operators()
BINARY_OPERATORS = operator_set.get_binary_operators()

class Node:
    """
    Rappresenta un nodo in un albero sintattico.
    Può essere un operatore o una foglia (variabile/costante).
    """
    def __init__(
        self,
        operator: Optional[OperatorSpec] = None,
        left: Optional["Node"] = None,
        right: Optional["Node"] = None,
        variable_idx: Optional[int] = None,
        value: Optional[float] = None
    ):
        self.operator = operator
        self.left = left
        self.right = right
        self.variable_idx = variable_idx
        self.value = value

    def is_leaf(self) -> bool:
        """Determina se il nodo è una foglia."""
        return self.operator is None

    def evaluate(self, x: np.ndarray) -> np.ndarray:
        """
        Valuta ricorsivamente il nodo e i suoi figli.

        Args:
            x (np.ndarray): Array di input per la valutazione.

        Returns:
            np.ndarray: Risultato della valutazione del sottoalbero.
        """
        if self.is_leaf():
            if self.variable_idx is not None:
                return x[:, self.variable_idx]
            elif self.value is not None:
                return np.full(x.shape[0], self.value)
            else:
                raise ValueError("Nodo foglia senza variabile o valore definito.")
        else:
            if self.operator.arity == 1:
                left_val = self.left.evaluate(x)
                return self.operator.function(left_val)
            elif self.operator.arity == 2:
                left_val = self.left.evaluate(x)
                right_val = self.right.evaluate(x)
                return self.operator.function(left_val, right_val)
            else:
                raise ValueError(f"Arity dell'operatore non supportata: {self.operator.arity}")

    def mutate_value(self) -> None:
        """
        Cambia l'operatore del nodo, selezionando uno nuovo della stessa arità.
        """
        if self.is_leaf():
            # Mutazione di una foglia: cambiare variabile o valore
            if self.variable_idx is not None:
                self.variable_idx = random.randint(0, self.operator_set.n_variables - 1)
            elif self.value is not None:
                self.value = np.random.uniform(-10, 10)
        else:
            current_arity = self.operator.arity
            if current_arity == 1:
                self.operator = random.choice(list(UNARY_OPERATORS.values()))
            elif current_arity == 2:
                self.operator = random.choice(list(BINARY_OPERATORS.values()))


class Tree:
    """
    Represents a syntax tree for symbolic regression.
    """
    def __init__(self, root: Node):
        self.root = root

    def __str__(self):
        return self._to_string(self.root)

    def _to_string(self, node):
        if not node:
            return ""
        if node.is_leaf():
            return f"{node.operator.symbol}"
        left_str = self._to_string(node.left)
        right_str = self._to_string(node.right)
        return f"({left_str} {node.operator.symbol} {right_str})"

    def traverse(self) -> List[Node]:
        """
        Returns a list of all nodes in the tree in traversal order.

        Returns:
            List[Node]: Nodes in the tree.
        """
        nodes = []

        def _traverse(node):
            if node:
                nodes.append(node)
                _traverse(node.left)
                _traverse(node.right)

        _traverse(self.root)
        return nodes

    def random_node(self, allow_root: bool = True) -> Node:
        """
        Selects a random node in the tree.

        Args:
            allow_root (bool): Whether to include the root in the selection.

        Returns:
            Node: Randomly selected node.
        """
        nodes = self.traverse()
        if not allow_root:
            nodes = nodes[1:]  # Exclude the root
        return random.choice(nodes)

    def replace_subtree(self, target_node: Node, new_subtree: Node) -> None:
        """
        Replaces a subtree with a new node.

        Args:
            target_node (Node): Node to replace.
            new_subtree (Node): New node or subtree.
        """
        def _replace(node, parent, is_left):
            if node is target_node:
                if is_left:
                    parent.left = new_subtree
                else:
                    parent.right = new_subtree
                return True
            if node.left and _replace(node.left, node, True):
                return True
            if node.right and _replace(node.right, node, False):
                return True
            return False

        if self.root is target_node:
            self.root = new_subtree
        else:
            _replace(self.root, None, False)

    def size(self) -> int:
        """
        Returns the total number of nodes in the tree.

        Returns:
            int: Number of nodes.
        """
        return len(self.traverse())

    def depth(self) -> int:
        """
        Calculates the maximum depth of the tree.

        Returns:
            int: Depth of the tree.
        """
        def _depth(node):
            if not node:
                return 0
            return 1 + max(_depth(node.left), _depth(node.right))

        return _depth(self.root)

    def copy(self) -> "Tree":
        """
        Creates a copy of the tree.

        Returns:
            Tree: Copy of the tree.
        """
        def _copy(node):
            if not node:
                return None
            return Node(
                operator=node.operator,
                left=_copy(node.left),
                right=_copy(node.right),
            )

        return Tree(_copy(self.root))

    @staticmethod
    def generate_random_tree(max_depth: int, operator_set: OperatorSet, n_variables: int = 1) -> "Tree":
        """
        Genera un albero casuale con una profondità massima specificata.

        Args:
            max_depth (int): Profondità massima dell'albero.
            operator_set (OperatorSet): Set di operatori da utilizzare.
            n_variables (int): Numero di variabili disponibili.

        Returns:
            Tree: Albero generato casualmente.
        """
        def _generate_node(depth):
            if depth >= max_depth or (depth > 0 and np.random.rand() < 0.3):
                # Creazione di una foglia
                if np.random.rand() < 0.5:
                    # Variabile
                    var_idx = random.randint(0, n_variables - 1)
                    return Node(variable_idx=var_idx)
                else:
                    # Costante
                    return Node(value=np.random.uniform(-10, 10))
            else:
                # Creazione di un operatore
                operator = random.choice(list(operator_set.get_binary_operators().values()))
                return Node(
                    operator=operator,
                    left=_generate_node(depth + 1),
                    right=_generate_node(depth + 1),
                )

        root = _generate_node(0)
        return Tree(root)
    
    def to_sympy(self, variables: List[Symbol]) -> Any:
        """
        Converte l'albero in un'espressione SymPy.

        Args:
            variables (List[Symbol]): Lista di simboli variabili.

        Returns:
            Any: Espressione SymPy.
        """
        if self.is_leaf():
            if self.variable_idx is not None:
                return variables[self.variable_idx]
            elif self.value is not None:
                return self.value
        else:
            if self.operator.arity == 1:
                operand = self.left.to_sympy(variables)
                return self.operator.to_sympy(operand)
            elif self.operator.arity == 2:
                left = self.left.to_sympy(variables)
                right = self.right.to_sympy(variables)
                return self.operator.to_sympy(left, right)



def validate_tree(tree: Tree, max_tree_depth: int = 10, max_nodes: int = 100, n_variables: int = 1) -> bool:
    """
    Valida un albero per correttezza strutturale e computazionale.

    Args:
        tree (Tree): Albero da validare.
        max_tree_depth (int): Profondità massima consentita.
        max_nodes (int): Numero massimo di nodi consentiti.
        n_variables (int): Numero di variabili disponibili.

    Returns:
        bool: True se l'albero è valido, False altrimenti.
    """
    try:
        if tree.root is None:
            return False  # La radice deve essere valida

        if tree.depth() > max_tree_depth:
            return False  # Controllo della profondità massima

        if tree.size() > max_nodes:
            return False  # Controllo del numero massimo di nodi

        # Test di valutazione con input casuali
        test_input = np.random.rand(10, n_variables)  # Input casuale
        result = tree.root.evaluate(test_input)

        # Controlla se il risultato è numericamente valido
        if not np.all(np.isfinite(result)):
            return False

        return True
    except Exception as e:
        print(f"Validazione fallita: {e}")
        return False
