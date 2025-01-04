from typing import Callable, Dict, NamedTuple, Optional
import numpy as np

# Global Constants
MAX_EXP = 10
MAX_POWER = 5
MAX_FLOAT = 1e10
MIN_FLOAT = 1e-10
FLOAT_PRECISION = np.float64


def safe_divide(x: np.ndarray, y: np.ndarray) -> np.ndarray:
    """Performs element-wise safe division, avoiding division by zero."""
    return np.divide(x, y, out=np.zeros_like(x), where=y != 0)


def safe_log(x: np.ndarray) -> np.ndarray:
    """Applies logarithm safely, avoiding log(0) and negative values."""
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
        self._define_unary_operators()
        self._define_binary_operators()

    def _define_unary_operators(self):
        """Defines unary operators."""
        self.operators["neg"] = OperatorSpec(
            name="neg", function=lambda x: -x, precedence=4, arity=1, symbol="-", latex_symbol="-", cost=0.1
        )
        self.operators["abs"] = OperatorSpec(
            name="abs", function=np.abs, precedence=4, arity=1, symbol="abs", latex_symbol="|x|", cost=0.2
        )
        self.operators["log"] = OperatorSpec(
            name="log", function=safe_log, precedence=5, arity=1, symbol="log", latex_symbol=r"\log(x)", cost=1.0
        )
        self.operators["log2"] = OperatorSpec(
            name="log2", function=safe_log2, precedence=5, arity=1, symbol="log2", latex_symbol=r"\log_2(x)", cost=1.0
        )
        self.operators["log10"] = OperatorSpec(
            name="log10", function=safe_log10, precedence=5, arity=1, symbol="log10", latex_symbol=r"\log_{10}(x)", cost=1.0
        )
        self.operators["sqrt"] = OperatorSpec(
            name="sqrt", function=safe_sqrt, precedence=5, arity=1, symbol="sqrt", latex_symbol=r"\sqrt{x}", cost=1.2
        )
        self.operators["exp"] = OperatorSpec(
            name="exp", function=safe_exp, precedence=5, arity=1, symbol="exp", latex_symbol=r"e^{x}", cost=1.5
        )
        self.operators["sin"] = OperatorSpec(
            name="sin", function=np.sin, precedence=5, arity=1, symbol="sin", latex_symbol=r"\sin(x)", cost=0.5
        )
        self.operators["cos"] = OperatorSpec(
            name="cos", function=np.cos, precedence=5, arity=1, symbol="cos", latex_symbol=r"\cos(x)", cost=0.5
        )
        self.operators["tan"] = OperatorSpec(
            name="tan", function=np.tan, precedence=5, arity=1, symbol="tan", latex_symbol=r"\tan(x)", cost=0.5
        )
        self.operators["sinh"] = OperatorSpec(
            name="sinh", function=np.sinh, precedence=5, arity=1, symbol="sinh", latex_symbol=r"\sinh(x)", cost=0.6
        )
        self.operators["cosh"] = OperatorSpec(
            name="cosh", function=np.cosh, precedence=5, arity=1, symbol="cosh", latex_symbol=r"\cosh(x)", cost=0.6
        )
        self.operators["tanh"] = OperatorSpec(
            name="tanh", function=np.tanh, precedence=5, arity=1, symbol="tanh", latex_symbol=r"\tanh(x)", cost=0.6
        )

    def _define_binary_operators(self):
        """Defines binary operators."""
        self.operators["add"] = OperatorSpec(
            name="add", function=np.add, precedence=1, arity=2, symbol="+", latex_symbol="+", cost=0.1
        )
        self.operators["sub"] = OperatorSpec(
            name="sub", function=np.subtract, precedence=1, arity=2, symbol="-", latex_symbol="-", cost=0.1
        )
        self.operators["mul"] = OperatorSpec(
            name="mul", function=np.multiply, precedence=2, arity=2, symbol="*", latex_symbol=r"\times", cost=0.2
        )
        self.operators["div"] = OperatorSpec(
            name="div", function=safe_divide, precedence=2, arity=2, symbol="/", latex_symbol=r"\div", cost=0.5
        )
        self.operators["pow"] = OperatorSpec(
            name="pow", function=safe_power, precedence=3, arity=2, symbol="^", latex_symbol="^", cost=1.5
        )
        self.operators["min"] = OperatorSpec(
            name="min", function=lambda x, y: np.minimum(x, y), precedence=1, arity=2, symbol="min", latex_symbol=r"\min(x, y)", cost=0.3
        )
        self.operators["max"] = OperatorSpec(
            name="max", function=lambda x, y: np.maximum(x, y), precedence=1, arity=2, symbol="max", latex_symbol=r"\max(x, y)", cost=0.3
        )
        self.operators["atan2"] = OperatorSpec(
            name="atan2", function=np.arctan2, precedence=3, arity=2, symbol="atan2", latex_symbol=r"\arctan2(x, y)", cost=1.0
        )
        self.operators["hypot"] = OperatorSpec(
            name="hypot", function=np.hypot, precedence=2, arity=2, symbol="hypot", latex_symbol=r"\hypot(x, y)", cost=0.4
        )
        self.operators["mod"] = OperatorSpec(
            name="mod", function=lambda x, y: np.mod(x, y), precedence=2, arity=2, symbol="%", latex_symbol=r"x \mod y", cost=0.3
        )
        self.operators["floor_div"] = OperatorSpec(
            name="floor_div", function=lambda x, y: np.floor_divide(x, y), precedence=2, arity=2, symbol="//", latex_symbol=r"\lfloor \frac{x}{y} \rfloor", cost=0.4
        )
        self.operators["pow2"] = OperatorSpec(
            name="pow2", function=lambda x: np.power(x, 2), precedence=3, arity=1, symbol="pow2", latex_symbol=r"x^2", cost=1.0
        )
        self.operators["pow3"] = OperatorSpec(
            name="pow3", function=lambda x: np.power(x, 3), precedence=3, arity=1, symbol="pow3", latex_symbol=r"x^3", cost=1.0
        )
        self.operators["pow4"] = OperatorSpec(
            name="pow4", function=lambda x: np.power(x, 4), precedence=3, arity=1, symbol="pow4", latex_symbol=r"x^4", cost=1.0
        )
        self.operators["pow5"] = OperatorSpec(
            name="pow5", function=lambda x: np.power(x, 5), precedence=3, arity=1, symbol="pow5", latex_symbol=r"x^5", cost=1.0
        )

    def get_sorted_operators(self, by: str = "cost") -> Dict[str, OperatorSpec]:
        """
        Returns operators sorted by a specified attribute (default: cost).

        Args:
            by (str): Attribute to sort by ("cost" or "precedence").

        Returns:
            Dict[str, OperatorSpec]: Dictionary of sorted operators.
        """
        if by not in {"cost", "precedence"}:
            raise ValueError(f"Invalid sort key: {by}")
        return dict(
            sorted(
                self.operators.items(),
                key=lambda item: getattr(item[1], by)
            )
        )

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
