# %% [markdown]
# Copyright **`(c)`** 2024 Giovanni Squillero `<giovanni.squillero@polito.it>`  
# [`https://github.com/squillero/computational-intelligence`](https://github.com/squillero/computational-intelligence)  
# Free for personal or classroom use; see [`LICENSE.md`](https://github.com/squillero/computational-intelligence/blob/master/LICENSE.md) for details.  

# %% [markdown]
# # Set Cover problem
# 
# See: https://en.wikipedia.org/wiki/Set_cover_problem

# %%
import functools
from dataclasses import dataclass



import numpy as np



from tqdm.auto import tqdm



from icecream import ic

# %% [markdown]
# ## Reproducible Initialization
# 
# If you want to get reproducible results, use `rng` (and restart the kernel); for non-reproducible ones, use `np.random`.

# %%
UNIVERSE_SIZE = 10
NUM_SETS = 5
DENSITY = 0.3

# %%
# DON'T EDIT THESE LINES!

rng = np.random.Generator(np.random.PCG64([UNIVERSE_SIZE, NUM_SETS, int(10_000 * DENSITY)]))

SETS = np.random.random((NUM_SETS, UNIVERSE_SIZE)) < DENSITY
for s in range(UNIVERSE_SIZE):
    if not np.any(SETS[:, s]):
        SETS[np.random.randint(NUM_SETS), s] = True
COSTS = np.pow(SETS.sum(axis=1), 1.1)


def counter(fn):
    """Simple decorator for counting number of calls"""

    @functools.wraps(fn)
    def helper(*args, **kargs):
        helper.calls += 1
        return fn(*args, **kargs)

    helper.calls = 0
    return helper


@counter
def cost(solution):
    """Returns the cost of a solution (to be minimized) tracking number of calls"""
    return COSTS[solution].sum()

# %% [markdown]
# # Squillero's EA

# %% [markdown]
# ## Helper Functions

# %%
def valid(solution):
    """Checks wether solution is valid (ie. covers all universe)"""
    return np.all(np.logical_or.reduce(SETS[solution]))


def num_covered(solution):
    """Checks wether solution is valid (ie. covers all universe)"""
    return np.sum(np.logical_or.reduce(SETS[solution]))


@dataclass
class Individual:
    genome: np.ndarray
    fitness: float = None


def fitness(individual):
    return int(num_covered(individual.genome)), -float(cost(individual.genome))


def parent_selection(population):
    candidates = sorted(np.random.choice(population, 2), key=lambda e: e.fitness, reverse=True)
    return candidates[0]


def xover(p1: Individual, p2: Individual):
    m = np.random.rand(NUM_SETS) < 0.5
    genome = p1.genome.copy()
    genome[m] = p2.genome[m]
    return Individual(genome)

# %% [markdown]
# ## Have Fun!

# %%
POPULATION_SIZE = 10
population = [Individual(np.random.rand(NUM_SETS) < 0.5) for _ in range(POPULATION_SIZE)]
for i in population:
    i.fitness = fitness(i)

OFFSPRING_SIZE = 4

offspring = list()
for _ in range(OFFSPRING_SIZE):
    i1 = parent_selection(population)
    i2 = parent_selection(population)
    o = xover(i1, i2)
    offspring.append(o)

for i in offspring:
    i.fitness = fitness(i)

population.extend(offspring)
population.sort(key=lambda i: i.fitness, reverse=True)
population = population[:POPULATION_SIZE]

# %%
population

# %%
offspring

# %%
fitness(population[0])

# %%
population[0].genome

# %%
population[0].genome[np.array([False, True, False, False, False])] = False

# %%
population[0].genome

# %%



