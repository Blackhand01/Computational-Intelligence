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
    return np.exp(np.add(np.power(np.sqrt(np.maximum(x[0], x[1])), np.exp(np.add(np.power(np.sqrt(np.maximum(x[0], x[1])), np.add(np.subtract(0.373, 0.239), np.add(x[1], x[0]))), np.tan(np.subtract(np.power(0.192, 0.943), np.power(x[1], -0.759)))))), np.maximum(x[0], x[1])))


def f3(x: np.ndarray) -> np.ndarray:
    return np.subtract(np.log10(np.subtract(np.negative(x[2]), np.divide(np.add(np.log10(np.maximum(x[1], x[2])), np.log2(np.subtract(x[1], 0.759))), np.abs(-0.72)))), np.minimum(np.log10(np.maximum(x[1], x[2])), np.add(np.log10(np.maximum(x[1], x[2])), np.log2(np.subtract(x[1], 0.759)))))


def f4(x: np.ndarray) -> np.ndarray:
    return np.subtract(np.negative(np.negative(np.exp(np.exp(np.cos(x[1]))))), np.exp(np.divide(0.021, 0.792)))


def f5(x: np.ndarray) -> np.ndarray:
    return 0.012


def f6(x: np.ndarray) -> np.ndarray:
    return np.add(x[1], np.add(x[1], np.tan(np.cos(np.multiply(-0.829, x[0])))))


def f7(x: np.ndarray) -> np.ndarray:
    return np.power(np.maximum(np.maximum(np.sin(np.abs(-0.721)), np.log10(np.log2(x[0]))), np.negative(np.log10(np.abs(x[0])))), np.log10(np.multiply(np.log10(np.log2(x[0])), np.add(np.subtract(x[1], x[0]), np.maximum(x[0], 0.681)))))


def f8(x: np.ndarray) -> np.ndarray:
    return np.minimum(np.sqrt(np.multiply(np.exp(np.abs(x[3])), np.negative(np.power(0.995, 0.352)))), np.add(np.log(np.tan(np.maximum(x[5], -0.694))), np.minimum(np.sqrt(np.multiply(np.exp(np.abs(x[3])), np.log2(np.log2(-0.201)))), np.add(np.log2(np.log10(np.multiply(x[5], 0.731))), np.log(np.log10(np.multiply(x[5], 0.682)))))))
