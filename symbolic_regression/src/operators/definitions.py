from typing import Callable, Dict, NamedTuple, Optional
import numpy as np

# Global Constants
MAX_EXP = 10
MAX_POWER = 5
MAX_FLOAT = 1e10
MIN_FLOAT = 1e-10


def safe_divide(x: np.ndarray, y: np.ndarray) -> np.ndarray:
    """Performs element-wise safe division, avoiding division by zero."""
    return np.divide(x, y, out=np.zeros_like(x), where=y != 0)


def safe_ln(x: np.ndarray) -> np.ndarray:
    """Applies natural logarithm safely, avoiding ln(0) and negative values."""
    return np.log(np.clip(x, MIN_FLOAT, MAX_FLOAT))


def safe_sqrt(x: np.ndarray) -> np.ndarray:
    """Applies square root safely, avoiding sqrt of negative numbers."""
    return np.sqrt(np.clip(x, 0, MAX_FLOAT))


def safe_power(x: np.ndarray, p: np.ndarray) -> np.ndarray:
    """Raises x to the power p safely, avoiding overflow."""
    return np.power(np.clip(x, MIN_FLOAT, MAX_FLOAT), np.clip(p, -MAX_POWER, MAX_POWER))


def safe_exp(x: np.ndarray) -> np.ndarray:
    """Applies exponential safely, avoiding overflow."""
    return np.exp(np.clip(x, -np.log(MAX_FLOAT), np.log(MAX_FLOAT)))


def safe_log2(x: np.ndarray) -> np.ndarray:
    """Applies log base 2 safely."""
    return np.log2(np.clip(x, MIN_FLOAT, MAX_FLOAT))


def safe_log10(x: np.ndarray) -> np.ndarray:
    """Applies log base 10 safely."""
    return np.log10(np.clip(x, MIN_FLOAT, MAX_FLOAT))


class OperatorSpec(NamedTuple):
    """
    Specification of a mathematical operator.

    Attributes:
        name (str): Identifier name of the operator.
        function (Callable): Mathematical function associated with the operator.
        precedence (int): Precedence level of the operator.
        arity (int): Arity of the operator (1 for unary, 2 for binary).
        symbol (str): Textual symbol of the operator.
        latex_symbol (Optional[str]): LaTeX symbol for visualization.
        cost (float): Relative computational cost of the operator.
    """
    name: str
    function: Callable[..., np.ndarray]
    precedence: int
    arity: int
    symbol: str
    latex_symbol: Optional[str] = None
    cost: float = 1.0  # Default cost


class OperatorSet:
    """
    Manages and encapsulates all available operators for symbolic regression.
    """
    def __init__(self):
        self.operators: Dict[str, OperatorSpec] = {}
        self.k = 1.0  # Default factor for binary costs
        self._define_unary_operators()
        self._define_binary_operators()

    def set_dynamic_k(self, dataset_size: int, max_tree_nodes: int, current_generation: int, max_generations: int):
        """
        Dynamically adjusts the cost factor for binary operators (k) based on conditions.

        Args:
            dataset_size (int): Number of samples in the dataset.
            max_tree_nodes (int): Maximum allowed nodes in the tree.
            current_generation (int): Current generation in the evolutionary process.
            max_generations (int): Total number of generations.
        """
        # Example logic: k grows with dataset size, tree complexity, and evolutionary progress
        size_factor = min(dataset_size / 10000, 2.0)  # Caps at 2.0 for large datasets
        complexity_factor = min(max_tree_nodes / 100, 2.0)  # Caps at 2.0 for complex trees
        evolution_factor = (current_generation / max_generations)  # Progressively increases with generations

        self.k = 1.0 + 0.5 * (size_factor + complexity_factor + evolution_factor)  # Weighted sum
        print(f"Dynamic k set to: {self.k:.2f}")
        self._update_binary_costs()

    def _update_binary_costs(self):
        """
        Updates the costs of binary operators based on the current value of k.
        """
        for name, operator in self.operators.items():
            if operator.arity == 2:  # Binary operators
                updated_cost = operator.cost * self.k
                self.operators[name] = operator._replace(cost=updated_cost)

    def _define_unary_operators(self):
        """Defines unary operators."""
        self.operators["neg"] = OperatorSpec(
            name="neg", function=lambda x: -x, precedence=4, arity=1, symbol="-", latex_symbol="-", cost=0.0520
        )
        self.operators["abs"] = OperatorSpec(
            name="abs", function=np.abs, precedence=4, arity=1, symbol="abs", latex_symbol="|x|", cost=0.0458
        )
        self.operators["ln"] = OperatorSpec(
            name="ln", function=safe_ln, precedence=5, arity=1, symbol="ln", latex_symbol=r"\ln(x)", cost=0.3761
        )
        self.operators["log2"] = OperatorSpec(
            name="log2", function=safe_log2, precedence=5, arity=1, symbol="log2", latex_symbol=r"\log_2(x)", cost=0.3967
        )
        self.operators["log10"] = OperatorSpec(
            name="log10", function=safe_log10, precedence=5, arity=1, symbol="log10", latex_symbol=r"\log_{10}(x)", cost=0.4175
        )
        self.operators["sqrt"] = OperatorSpec(
            name="sqrt", function=safe_sqrt, precedence=5, arity=1, symbol="sqrt", latex_symbol=r"\sqrt{x}", cost=0.1693
        )
        self.operators["exp"] = OperatorSpec(
            name="exp", function=safe_exp, precedence=5, arity=1, symbol="exp", latex_symbol=r"e^{x}", cost=0.3414
        )
        self.operators["sin"] = OperatorSpec(
            name="sin", function=np.sin, precedence=5, arity=1, symbol="sin", latex_symbol=r"\sin(x)", cost=0.7198
        )
        self.operators["cos"] = OperatorSpec(
            name="cos", function=np.cos, precedence=5, arity=1, symbol="cos", latex_symbol=r"\cos(x)", cost=0.7194
        )
        self.operators["tan"] = OperatorSpec(
            name="tan", function=np.tan, precedence=5, arity=1, symbol="tan", latex_symbol=r"\tan(x)", cost=0.4061
        )
        self.operators["tanh"] = OperatorSpec(
            name="tanh", function=np.tanh, precedence=5, arity=1, symbol="tanh", latex_symbol=r"\tanh(x)", cost=0.3009
        )

    def _define_binary_operators(self):
        """Defines binary operators."""
        self.operators["add"] = OperatorSpec(
            name="add", function=np.add, precedence=1, arity=2, symbol="+", latex_symbol="+", cost=0.0632
        )
        self.operators["sub"] = OperatorSpec(
            name="sub", function=np.subtract, precedence=1, arity=2, symbol="-", latex_symbol="-", cost=0.0636
        )
        self.operators["mul"] = OperatorSpec(
            name="mul", function=np.multiply, precedence=2, arity=2, symbol="*", latex_symbol=r"\times", cost=0.0631
        )
        self.operators["div"] = OperatorSpec(
            name="div", function=safe_divide, precedence=2, arity=2, symbol="/", latex_symbol=r"\div", cost=0.1500
        )
        self.operators["pow"] = OperatorSpec(
            name="pow", function=safe_power, precedence=3, arity=2, symbol="^", latex_symbol="^", cost=0.8958
        )
        self.operators["min"] = OperatorSpec(
            name="min", function=lambda x, y: np.minimum(x, y), precedence=1, arity=2, symbol="min", latex_symbol=r"\min(x, y)", cost=0.0608
        )
        self.operators["max"] = OperatorSpec(
            name="max", function=lambda x, y: np.maximum(x, y), precedence=1, arity=2, symbol="max", latex_symbol=r"\max(x, y)", cost=0.0618
        )
        self.operators["hypot"] = OperatorSpec(
            name="hypot", function=np.hypot, precedence=2, arity=2, symbol="hypot", latex_symbol=r"\hypot(x, y)", cost=0.2008
        )
        self.operators["mod"] = OperatorSpec(
            name="mod", function=lambda x, y: np.mod(x, y), precedence=2, arity=2, symbol="%", latex_symbol=r"x \mod y", cost=1.0000
        )
        self.operators["pow2"] = OperatorSpec(
            name="pow2", function=lambda x: x * x, precedence=3, arity=1, symbol="pow2", latex_symbol=r"x^2", cost=0.0441
        )
        self.operators["pow3"] = OperatorSpec(
            name="pow3", function=lambda x: x * x * x, precedence=3, arity=1, symbol="pow3", latex_symbol=r"x^3", cost=0.0679
        )

    def get_sorted_operators(self, by: str = "cost") -> Dict[str, OperatorSpec]:
        """
        Returns operators sorted by a specified attribute (default: cost).

        Args:
            by (str): Attribute to sort by ("cost", "precedence").

        Returns:
            Dict[str, OperatorSpec]: Dictionary of sorted operators.
        """
        valid_keys = {"cost", "precedence"}
        if by not in valid_keys:
            raise ValueError(f"Invalid sort key: {by}. Must be one of {valid_keys}")
        return dict(sorted(self.operators.items(), key=lambda item: getattr(item[1], by)))


    def get_unary_operators(self) -> Dict[str, OperatorSpec]:
        """Returns only unary operators."""
        return {name: op for name, op in self.operators.items() if op.arity == 1}

    def get_binary_operators(self) -> Dict[str, OperatorSpec]:
        """Returns only binary operators."""
        return {name: op for name, op in self.operators.items() if op.arity == 2}

# Initialize the operator set
operator_set = OperatorSet()

# Export sorted operators by cost and precedence for tree construction
SORTED_OPERATORS_BY_COST = operator_set.get_sorted_operators(by="cost")
SORTED_OPERATORS_BY_PRECEDENCE = operator_set.get_sorted_operators(by="precedence")

# Separate unary and binary operators for ease of use
UNARY_OPERATORS = operator_set.get_unary_operators()
BINARY_OPERATORS = operator_set.get_binary_operators()
