from typing import Callable, Optional
import numpy as np

MAX_EXP = 10
MAX_POWER = 5
MAX_FLOAT = 1e10
MIN_FLOAT = 1e-10


# Funzioni di supporto
def clip_values(x: np.ndarray, min_value: float, max_value: float) -> np.ndarray:
    """Clip values to a specified range."""
    return np.clip(x, min_value, max_value)


def validate_array(array: np.ndarray) -> bool:
    """Check if array contains valid numbers (no NaN, inf, or extreme values)."""
    if not np.isfinite(array).all():
        return False
    if np.any(array > MAX_FLOAT) or np.any(array < -MAX_FLOAT):
        return False
    return True



# Operazioni sicure
def safe_divide(x: np.ndarray, y: np.ndarray) -> np.ndarray:
    """Perform element-wise safe division, avoiding division by zero."""
    y_safe = np.where(np.abs(y) < MIN_FLOAT, MIN_FLOAT, y)
    return np.divide(x, y_safe)


def safe_ln(x: np.ndarray) -> np.ndarray:
    """Apply natural logarithm safely, avoiding ln(0) and negative values."""
    return np.log(clip_values(x, MIN_FLOAT, MAX_FLOAT))


def safe_sqrt(x: np.ndarray) -> np.ndarray:
    """Apply square root safely, avoiding sqrt of negative numbers."""
    return np.sqrt(clip_values(x, 0, MAX_FLOAT))


def safe_power(x: np.ndarray, p: np.ndarray) -> np.ndarray:
    """Raise x to the power p safely, handling edge cases."""
    # Clip inputs to safe ranges
    x_safe = np.clip(x, MIN_FLOAT, MAX_FLOAT)  # Prevent overflow and invalid bases
    p_safe = np.clip(p, -MAX_POWER, MAX_POWER)

    # Handle negative bases with fractional powers
    is_fractional_power = (p_safe % 1 != 0)
    x_safe = np.where(
        (x_safe < 0) & is_fractional_power, 
        MIN_FLOAT,  # Replace invalid combinations with a small positive value
        x_safe
    )

    # Perform power operation
    result = np.power(x_safe, p_safe)

    # Handle invalid results (e.g., NaN, inf)
    result = np.nan_to_num(result, nan=MIN_FLOAT, posinf=MAX_FLOAT, neginf=-MAX_FLOAT)

    # Clip the final result
    return np.clip(result, -MAX_FLOAT, MAX_FLOAT)


def safe_exp(x: np.ndarray) -> np.ndarray:
    """Apply exponential safely, avoiding overflow."""
    return np.exp(clip_values(x, -MAX_EXP, MAX_EXP))


def safe_log2(x: np.ndarray) -> np.ndarray:
    """Apply log base 2 safely."""
    return np.log2(clip_values(x, MIN_FLOAT, MAX_FLOAT))


def safe_log10(x: np.ndarray) -> np.ndarray:
    """Apply log base 10 safely."""
    return np.log10(clip_values(x, MIN_FLOAT, MAX_FLOAT))


# Classe Operator
class Operator:
    """
    Rappresenta un operatore matematico con proprietà utili al progetto.

    Attributes:
        name (str): Nome identificativo dell'operatore.
        function (Callable): Funzione associata all'operatore.
        arity (int): Numero di operandi richiesti (1 per unario, 2 per binario).
        symbol (str): Simbolo in linguaggio naturale (es. "+", "-", "*", "/").
        numpy_symbol (str): Simbolo usato in NumPy per generare il codice.
        latex_symbol (str): Simbolo LaTeX.
        cost (float): Costo computazionale relativo dell'operatore.
        precedence (int): Precedenza dell'operatore (valore più alto = maggiore priorità).
    """

    def __init__(self, name: str, function: Callable, arity: int, symbol: str,
                 numpy_symbol: Optional[str] = None, latex_symbol: Optional[str] = None,
                 cost: float = 1.0, precedence: int = 1):
        self.name = name
        self.function = function
        self.arity = arity
        self.symbol = symbol
        self.numpy_symbol = numpy_symbol or symbol  # Simbolo NumPy o default al simbolo
        self.latex_symbol = latex_symbol or symbol  # Simbolo LaTeX o default al simbolo
        self.cost = cost
        self.precedence = precedence

    def __repr__(self):
        """
        Rappresentazione testuale dell'operatore.
        """
        return (f"Operator(name={self.name}, arity={self.arity}, "
                f"symbol='{self.symbol}', numpy_symbol='{self.numpy_symbol}', "
                f"precedence={self.precedence}, cost={self.cost})")

    def compute(self, *args: np.ndarray) -> np.ndarray:
        """
        Esegue l'operatore sugli input forniti.

        Args:
            *args (np.ndarray): Operandi per l'operatore.

        Returns:
            np.ndarray: Risultato dell'operazione.
        """
        if len(args) != self.arity:
            raise ValueError(f"L'operatore {self.name} richiede {self.arity} argomenti, "
                             f"ma ne sono stati forniti {len(args)}.")
        return self.function(*args)


# Definizione degli operatori unari
UNARY_OPERATORS = [
    Operator(name="neg", function=np.negative, arity=1, symbol="-",  numpy_symbol="np.negative", latex_symbol="-x", cost=0.0520, precedence=4),
    Operator(name="abs", function=np.abs, arity=1, symbol="abs",  numpy_symbol="np.abs", latex_symbol="|x|", cost=0.0458, precedence=4),
    Operator(name="ln", function=safe_ln, arity=1, symbol="ln",  numpy_symbol="np.log", latex_symbol=r"\ln(x)", cost=0.3761, precedence=5),
    Operator(name="log2", function=safe_log2, arity=1, symbol="log2",  numpy_symbol="np.log2", latex_symbol=r"\log_2(x)", cost=0.3967, precedence=5),
    Operator(name="log10", function=safe_log10, arity=1, symbol="log10",  numpy_symbol="np.log10", latex_symbol=r"\log_{10}(x)", cost=0.4175, precedence=5),
    Operator(name="sqrt", function=safe_sqrt, arity=1, symbol="sqrt",  numpy_symbol="np.sqrt", latex_symbol=r"\sqrt{x}", cost=0.1693, precedence=5),
    Operator(name="exp", function=safe_exp, arity=1, symbol="exp",  numpy_symbol="np.exp", latex_symbol=r"e^x", cost=0.3414, precedence=5),
    Operator(name="sin", function=np.sin, arity=1, symbol="sin",  numpy_symbol="np.sin", latex_symbol=r"\sin(x)", cost=0.7198, precedence=5),
    Operator(name="cos", function=np.cos, arity=1, symbol="cos",  numpy_symbol="np.cos", latex_symbol=r"\cos(x)", cost=0.7194, precedence=5),
    Operator(name="tan", function=np.tan, arity=1, symbol="tan",  numpy_symbol="np.tan", latex_symbol=r"\tan(x)", cost=0.4061, precedence=5),
   ]

# Definizione degli operatori binari
BINARY_OPERATORS = [
    Operator(name="add", function=np.add, arity=2, symbol="+",  numpy_symbol="np.add", latex_symbol="+", cost=0.0632, precedence=1),
    Operator(name="sub", function=np.subtract, arity=2, symbol="-",  numpy_symbol="np.subtract", latex_symbol="-", cost=0.0636, precedence=1),
    Operator(name="mul", function=np.multiply, arity=2, symbol="*",  numpy_symbol="np.multiply", latex_symbol=r"\times", cost=0.0631, precedence=2),
    Operator(name="div", function=safe_divide, arity=2, symbol="/",  numpy_symbol="np.divide", latex_symbol=r"\div", cost=0.1500, precedence=2),
    Operator(name="pow", function=safe_power, arity=2, symbol="^",  numpy_symbol="np.power", latex_symbol="^", cost=0.8958, precedence=3),
    Operator(name="min", function=lambda x, y: np.minimum(x, y), arity=2, symbol="min",  numpy_symbol="np.minimum", latex_symbol=r"\min(x, y)", cost=0.0608, precedence=1),
    Operator(name="max", function=lambda x, y: np.maximum(x, y), arity=2, symbol="max",  numpy_symbol="np.maximum", latex_symbol=r"\max(x, y)", cost=0.0618, precedence=1),
 ]

# Dizionario per accesso rapido
ALL_OPERATORS = {op.name: op for op in UNARY_OPERATORS + BINARY_OPERATORS}
