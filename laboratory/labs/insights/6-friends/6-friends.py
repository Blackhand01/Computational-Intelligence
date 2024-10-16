# %% [markdown]
# Copyright **`(c)`** 2024 Giovanni Squillero `<squillero@polito.it>`  
# `https://github.com/squillero/computational-intelligence`  
# Free for personal or classroom use; see 'LICENCE.md' for details.

# %%
NUM_FRIENDS = 6

# %%
from itertools import product, combinations
from multiset import Multiset
import matplotlib.pyplot as plt
import networkx as nx
from networkx.drawing.nx_pydot import graphviz_layout
from icecream import ic

# %%
def node2sets(node):
    home, pizzeria = node.split("-")
    return Multiset(home), Multiset(pizzeria)


def sets2node(home, pizzeria):
    return "".join(sorted(home)) + "-" + "".join(sorted(pizzeria))


sspace = nx.Graph()
for c, d, b in product(range(NUM_FRIENDS // 2 + 1), range(NUM_FRIENDS // 2 + 1), [True, False]):
    home = "C" * c + "D" * d + ("*" if b else "")
    pizzeria = "C" * (NUM_FRIENDS // 2 - c) + "D" * (NUM_FRIENDS // 2 - d) + ("*" if not b else "")
    sspace.add_node(home + "-" + pizzeria)

# %%
plt.figure(figsize=(8, 8))
nx.draw(sspace, with_labels=True)

# %%
def valid_node(node):
    home, pizzeria = node.split("-")
    if home == "*" or pizzeria == "*":
        return False
    home, pizzeria = node.split("-")
    return valid_location(home) and valid_location(pizzeria)


def valid_location(place):
    if place.count("D") == 0:
        return True
    elif place.count("D") >= place.count("C"):
        return True
    return False

# %%
plt.figure(figsize=(8, 8))
nx.draw(
    sspace,
    with_labels=True,
    node_color=["green" if valid_node(n) else "red" for n in sspace],
)

# %%
sspace = nx.Graph()

for c, d, b in product(range(NUM_FRIENDS // 2 + 1), range(NUM_FRIENDS // 2 + 1), [True, False]):
    home = "C" * c + "D" * d + ("*" if b else "")
    pizzeria = "C" * (NUM_FRIENDS // 2 - c) + "D" * (NUM_FRIENDS // 2 - d) + ("*" if not b else "")
    node = home + "-" + pizzeria
    if valid_node(node):
        sspace.add_node(node)

plt.figure(figsize=(8, 8))
nx.draw(sspace, with_labels=True)

# %%
def bike(from_, to):
    if '*' in from_[1]:
        return bike((from_[1], from_[0]), (to[1], to[0]))
    if '*' not in from_[0] or '*' not in to[1]:
        return None
    if not to[0] <= from_[0] or not from_[1] <= to[1]:
        return None
    moved = from_[0] - to[0]
    if not 2 <= len(moved) <= 3:
        return None
    if from_[1] + moved != to[1]:
        ic()
        return None
    return ''.join(sorted(moved))

# %%
for n1, n2 in combinations(sspace, 2):
    if bike(node2sets(n1), node2sets(n2)) is not None:
        sspace.add_edge(n1, n2, label=bike(node2sets(n1), node2sets(n2)))

pos = graphviz_layout(sspace, prog='neato')
colors = ['violet' if n[0] == '-' or n[-1] == '-' else 'lightskyblue' for n in sspace]

plt.figure(figsize=(16, 8))
nx.draw(sspace, pos=pos, node_color=colors, with_labels=True)

# %%
SOURCE = "C" * (NUM_FRIENDS // 2) + "D" * (NUM_FRIENDS // 2) + "*" + "-"
DESTINATION = "-" + "C" * (NUM_FRIENDS // 2) + "D" * (NUM_FRIENDS // 2) + "*"
nx.shortest_path(sspace, SOURCE, DESTINATION)

# %%



