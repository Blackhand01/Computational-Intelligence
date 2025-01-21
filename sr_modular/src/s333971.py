# Copyright © 2024 Giovanni Squillero <giovanni.squillero@polito.it>
# https://github.com/squillero/computational-intelligence
# Free under certain conditions — see the license for details.

import numpy as np

# All numpy's mathematical functions can be used in formulas
# see: https://numpy.org/doc/stable/reference/routines.math.html


# Notez bien: No need to include f0 -- it's just an example!
def f0(x: np.ndarray) -> np.ndarray:
    return x[0]


def f1(x: np.ndarray) -> np.ndarray:
    return np.sin(x[0])


def f2(x: np.ndarray) -> np.ndarray:
    return np.multiply(x[0], np.maximum(np.maximum(np.subtract(x[2], np.sqrt(-0.146)), np.sqrt(np.power(x[0], x[0]))), np.add(0.92, x[0])))


def f3(x: np.ndarray) -> np.ndarray:
    return np.power(np.multiply(np.add(x[2], np.log(np.divide(-0.719, 0.613))), x[1]), 0.985)


def f4(x: np.ndarray) -> np.ndarray:
    return np.subtract(np.log2(np.exp(0.987)), np.subtract(-0.553, np.tan(np.cos(x[1]))))


def f5(x: np.ndarray) -> np.ndarray:
    return np.power(-0.705, np.power(0.094, np.divide(x[1], np.log10(-0.914))))


def f6(x: np.ndarray) -> np.ndarray:
    return np.minimum(np.add(x[1], x[1]), 0.024)


def f7(x: np.ndarray) -> np.ndarray:
    return np.divide(np.maximum(np.log2(x[0]), np.exp(np.multiply(np.maximum(x[0], x[0]), x[1]))), np.power(np.sqrt(np.abs(-0.088)), np.minimum(0.898, np.divide(0.43, 0.457))))


def f8(x: np.ndarray) -> np.ndarray:
    return np.exp(np.exp(np.sqrt(x[5])))
