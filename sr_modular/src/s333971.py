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
    return np.subtract(np.exp(np.multiply(np.minimum(np.log2(0.715), np.log10(-0.855)), np.log10(np.multiply(x[0], -0.101)))), np.subtract(np.log10(np.tan(np.multiply(x[1], -0.149))), np.subtract(np.exp(np.multiply(np.divide(np.log2(0.715), np.log10(x[1])), np.log10(np.multiply(x[0], -0.101)))), np.subtract(np.sqrt(np.multiply(x[0], -0.101)), np.abs(np.sin(np.multiply(x[1], -0.149)))))))


def f3(x: np.ndarray) -> np.ndarray:
    return np.subtract(np.subtract(np.maximum(np.log2(x[1]), np.cos(np.sin(0.886))), np.multiply(np.add(0.212, np.maximum(np.tan(np.maximum(-0.557, -0.378)), np.cos(np.sin(-0.574)))), np.minimum(x[1], -0.135))), np.log2(np.negative(np.sin(np.negative(np.sin(np.add(np.negative(0.422), np.sqrt(np.log2(x[1])))))))))


def f4(x: np.ndarray) -> np.ndarray:
    return np.exp(np.cos(np.log(np.cos(np.add(-0.279, np.abs(np.minimum(np.log(np.power(np.add(x[1], 0.097), np.add(x[1], 0.097))), x[1])))))))


def f5(x: np.ndarray) -> np.ndarray:
    return 0.023


def f6(x: np.ndarray) -> np.ndarray:
    return x[1]


def f7(x: np.ndarray) -> np.ndarray:
    return np.exp(np.exp(np.sin(np.subtract(x[1], np.subtract(np.maximum(x[0], 0.432), x[0])))))


def f8(x: np.ndarray) -> np.ndarray:
    return np.divide(np.maximum(x[2], np.maximum(x[2], np.divide(np.divide(np.maximum(0.511, np.exp(x[5])), 0.189), 0.189))), 0.189)
