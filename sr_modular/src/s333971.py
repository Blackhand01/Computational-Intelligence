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
    return x[0]


def f2(x: np.ndarray) -> np.ndarray:
    return np.abs(np.exp(np.divide(np.power(x[1], np.minimum(x[0], x[1])), np.add(np.subtract(x[0], -0.526), x[2]))))


def f3(x: np.ndarray) -> np.ndarray:
    return np.negative(np.log2(np.log(np.log10(np.divide(x[1], x[0])))))


def f4(x: np.ndarray) -> np.ndarray:
    return np.cos(x[1])


def f5(x: np.ndarray) -> np.ndarray:
    return -0.068


def f6(x: np.ndarray) -> np.ndarray:
    return x[1]


def f7(x: np.ndarray) -> np.ndarray:
    return np.subtract(np.log10(np.minimum(np.abs(np.subtract(x[0], x[0])), np.tan(np.sqrt(0.33)))), np.log(np.log2(np.minimum(np.log2(x[0]), np.power(x[1], x[0])))))


def f8(x: np.ndarray) -> np.ndarray:
    return np.abs(np.multiply(np.add(np.abs(0.962), np.abs(np.add(-0.706, x[0]))), np.divide(np.subtract(np.power(0.705, 0.396), np.multiply(-0.205, x[5])), 0.066)))
