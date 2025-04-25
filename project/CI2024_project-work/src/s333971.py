# Copyright © 2024 Giovanni Squillero <giovanni.squillero@polito.it>
# https://github.com/squillero/computational-intelligence
# Free under certain conditions — see the license for details.

import numpy as np

# All numpy's mathematical functions can be used in formulas
# see: https://numpy.org/doc/stable/reference/routines.math.html


# Notez bien: No need to include f0 -- it's just an example!
def f0(x: np.ndarray) -> np.ndarray:
    return np.subtract(np.add(np.negative(np.multiply(np.sin(np.abs(-0.039)), np.log2(np.exp(np.multiply(-0.096, x[1]))))), x[0]), np.negative(np.maximum(np.add(np.divide(np.maximum(np.sin(x[1]), np.log10(-0.646)), np.subtract(np.abs(0.26922984740844647), np.divide(0.931, -0.19060704824490138))), np.power(np.multiply(np.sqrt(-0.16), np.minimum(-0.165, -0.5671584170868271)), np.divide(np.log(-0.177), np.tan(-0.199)))), np.log2(-0.119))))


def f1(x: np.ndarray) -> np.ndarray:
    return np.sin(x[0])


def f2(x: np.ndarray) -> np.ndarray:
    return np.subtract(np.negative(np.add(np.add(np.sqrt(np.power(-0.106, x[0])), np.multiply(np.log2(-0.253), np.divide(x[1], 0.225))), np.sqrt(np.abs(np.power(-0.194, x[0]))))), np.abs(np.power(np.add(np.abs(np.negative(x[2])), np.abs(np.log10(-0.915))), np.multiply(np.minimum(np.tan(0.975), np.cos(0.651)), np.power(np.minimum(x[2], x[1]), np.add(-0.9, x[0]))))))


def f3(x: np.ndarray) -> np.ndarray:
    return np.negative(np.add(np.log10(np.multiply(np.exp(x[2]), np.add(np.negative(np.multiply(-0.835, np.negative(np.tan(np.add(-0.425, np.sin(x[1])))))), np.subtract(np.multiply(np.abs(x[0]), np.maximum(np.minimum(x[2], -0.946), np.maximum(np.multiply(np.cos(x[1]), np.subtract(np.maximum(-0.143, x[1]), np.subtract(0.757, -0.353))), -0.711))), np.sqrt(np.sin(np.minimum(x[1], 0.587))))))), np.add(np.multiply(np.abs(x[1]), np.add(np.add(-0.728, x[1]), np.add(x[1], x[1]))), np.subtract(np.multiply(np.abs(x[1]), np.add(np.add(x[2], -0.253), np.add(np.add(np.abs(x[1]), np.add(np.negative(np.add(-0.835, np.abs(np.negative(np.add(0.96, np.negative(x[0])))))), np.subtract(np.subtract(np.sin(-0.64), np.divide(np.add(x[1], x[1]), np.subtract(np.add(np.log2(-0.64), np.maximum(np.subtract(0.983, x[1]), np.multiply(x[2], x[2]))), x[1]))), np.abs(np.negative(np.add(0.977, x[0])))))), x[1]))), np.abs(np.negative(np.multiply(x[0], x[0])))))))


def f4(x: np.ndarray) -> np.ndarray:
    return np.add(np.minimum(np.maximum(np.negative(np.log2(np.divide(np.subtract(x[1], -0.909), np.log2(0.039)))), np.log10(np.abs(np.divide(np.minimum(-0.8152608049505645, 0.5591951904468146), np.maximum(0.035, 0.167))))), np.abs(np.multiply(np.log(np.add(np.add(-0.937, -0.78), np.abs(x[1]))), np.sin(np.maximum(np.sqrt(0.122), np.minimum(x[0], 0.082)))))), np.multiply(np.add(np.cos(np.divide(np.cos(np.minimum(0.38, x[1])), np.minimum(np.minimum(0.086, -0.211), np.maximum(-0.406, x[1])))), np.maximum(np.add(np.negative(np.power(-0.725, 0.174)), np.cos(np.negative(x[1]))), np.minimum(np.sin(np.negative(0.858)), np.add(np.multiply(x[1], -0.674), 0.884)))), np.exp(np.cos(np.tan(np.minimum(np.sin(x[1]), np.tan(-0.079)))))))


def f5(x: np.ndarray) -> np.ndarray:
    return np.divide(np.power(np.multiply(np.negative(np.cos(np.negative(np.exp(x[1])))), np.abs(np.sqrt(np.minimum(np.exp(0.524), np.minimum(0.929, -0.2538457058036703))))), np.cos(np.abs(np.tan(np.log10(np.log(-0.167)))))), np.subtract(np.log2(np.add(np.multiply(np.abs(x[1]), np.tan(np.maximum(-0.901, 0.516))), np.add(np.abs(0.175), np.divide(np.log10(-0.226), np.abs(x[0]))))), np.cos(np.log(np.add(np.tan(np.divide(-0.833, -0.822)), np.exp(np.sqrt(0.315)))))))


def f6(x: np.ndarray) -> np.ndarray:
    return np.minimum(np.add(np.abs(np.divide(np.sin(np.sin(np.tan(0.364))), np.cos(np.sqrt(np.maximum(0.441, 0.693))))), np.add(x[1], np.add(-0.445, np.multiply(np.divide(np.sqrt(0.342), np.sin(0.936)), np.minimum(np.subtract(x[1], x[0]), np.subtract(x[1], x[0])))))), np.exp(np.maximum(np.power(np.minimum(np.divide(np.cos(0.922), np.negative(-0.58)), np.subtract(np.log10(x[1]), np.subtract(-0.005, x[1]))), np.maximum(np.maximum(np.sqrt(x[1]), np.minimum(x[1], 0.391)), np.multiply(np.exp(x[1]), np.cos(0.466)))), np.negative(np.add(np.multiply(np.maximum(1.0, x[1]), np.log2(0.389)), np.multiply(np.subtract(x[1], -0.083), np.minimum(x[1], 0.365)))))))


def f7(x: np.ndarray) -> np.ndarray:
    return np.abs(np.add(np.divide(np.multiply(np.exp(np.add(np.minimum(x[1], x[0]), np.abs(x[0]))), np.log(np.sqrt(np.divide(x[1], 0.135)))), np.exp(np.negative(np.log(np.multiply(x[1], x[0]))))), np.log10(np.negative(np.subtract(np.maximum(np.power(-0.371, 0.549), np.log10(x[0])), np.cos(np.add(-0.344, -0.975)))))))


def f8(x: np.ndarray) -> np.ndarray:
    return np.negative(np.multiply(np.subtract(np.negative(np.multiply(np.maximum(np.power(0.265, -0.028), np.negative(x[5])), np.subtract(np.power(np.power(-0.478, -0.028), np.abs(x[5])), np.log(0.0)))), np.abs(np.add(np.abs(np.log10(-0.266)), np.multiply(np.log10(-0.272), np.negative(x[5]))))), np.subtract(np.abs(np.minimum(np.log(np.multiply(0.064, 0.874)), np.multiply(np.add(-0.965, x[5]), np.log2(-0.521)))), np.subtract(np.subtract(np.abs(np.log2(-0.875)), np.subtract(np.tan(-0.68), np.add(0.533, 0.8204544064093195))), np.maximum(np.multiply(np.maximum(x[1], 0.64), np.log2(-0.296)), np.minimum(np.tan(-0.818), np.subtract(x[5], 0.135)))))))
