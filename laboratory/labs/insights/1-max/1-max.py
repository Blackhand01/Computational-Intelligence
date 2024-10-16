# %% [markdown]
# Copyright **`(c)`** 2024 Giovanni Squillero `<squillero@polito.it>`  
# `https://github.com/squillero/computational-intelligence`  
# Free for personal or classroom use; see 'LICENCE.md' for details.

# %%
import random
from icecream import ic

# %%
PROBLEM_SIZE = 100

# %%
def quality(solution):
    return max(sum(solution), PROBLEM_SIZE-sum(solution))


def tweak(solution):
    new_solution = solution[:]
    pos = random.randrange(PROBLEM_SIZE)
    new_solution[pos] = 1 - new_solution[pos]
    return new_solution

# %%
initial_solution = [random.randint(0, 1) for _ in range(PROBLEM_SIZE)]
ic(quality(initial_solution))
None

# %%
current_solution = initial_solution
steps = 0
ic(steps, quality(current_solution))
while quality(current_solution) < PROBLEM_SIZE:
    steps += 1
    solution = tweak(current_solution)
    if quality(solution) > quality(current_solution):
        current_solution = solution
ic(steps, quality(current_solution))
None

# %%
ic(current_solution[0])

# %%
current_solution = initial_solution
steps = 0
ic(steps, quality(current_solution))
while quality(current_solution) < PROBLEM_SIZE:
    temp = current_solution[:]
    best_so_far = current_solution[:]
    for inner_step in range(10):
        steps += 1
        solution = tweak(current_solution)
        if quality(solution) > quality(best_so_far):
            best_so_far = solution
            # temp = solution
    if quality(best_so_far) > quality(current_solution):
        current_solution = best_so_far
ic(steps, quality(current_solution))
None

# %%
ic(current_solution[0])


