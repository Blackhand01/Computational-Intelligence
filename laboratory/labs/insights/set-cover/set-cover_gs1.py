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
import numpy as np

from tqdm.auto import tqdm
from icecream import ic

# %% [markdown]
# ## Reproducible Initialization
# 
# If you want to get reproducible results, use `rng` (and restart the kernel); for non-reproducible ones, use `np.random`.

# %%
UNIVERSE_SIZE = 10_000
NUM_SETS = 1000
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
# # Squillero's greedy solution

# %% [markdown]
# ## Helper Functions

# %%
def valid(solution):
    """Checks wether solution is valid (ie. covers all universe)"""
    return np.all(np.logical_or.reduce(SETS[solution]))


def num_covered(solution):
    """Checks wether solution is valid (ie. covers all universe)"""
    return np.sum(np.logical_or.reduce(SETS[solution]))

# %% [markdown]
# ## Have Fun!

# %%
availabe_sets = np.append(SETS, np.full(UNIVERSE_SIZE, np.False_)).reshape((NUM_SETS + 1, -1))
availabe_sets = SETS.copy()
weight = np.array([cost(s) for s in np.diag([1] * NUM_SETS)])

solution = np.full(NUM_SETS, np.False_)
targets = np.full(UNIVERSE_SIZE, np.True_)
with tqdm(total=UNIVERSE_SIZE) as pbar:
    while np.any(targets):
        pression = 1 + np.exp(-10 * (availabe_sets.sum(axis=0) - 1))
        # pression = 1
        useful_sets = availabe_sets.copy()
        useful_sets[:, np.logical_not(targets)] = np.False_
        usefulness = useful_sets.sum(axis=1)
        candidates = (useful_sets * pression).sum(axis=1) / weight
        solution[candidates.argmax()] = np.True_
        old = targets.sum()
        targets = np.logical_not(np.logical_or.reduce(availabe_sets[solution]))
        new = targets.sum()
        pbar.update(old - new)
ic(cost(solution), cost.calls)
None

# %%



