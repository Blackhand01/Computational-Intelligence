import random
from abc import ABC, abstractmethod
from tree import Node, random_variable, random_constant
from safe_math import ALL_OPERATORS
from gp.utils import get_random_node

class BaseMutationStrategy(ABC):
    """
    Abstract base class for mutation strategies.
    """

    @abstractmethod
    def mutate(self, individual: Node, n_features: int) -> Node:
        pass

class SimpleMutation(BaseMutationStrategy):
    """
    Simple mutation strategy that preserves the arity of the operator.
    """

    def mutate(self, individual: Node, n_features: int) -> Node:
        mutant = individual.copy_tree()
        node, _ = get_random_node(mutant)

        if node.op is None:  # Leaf node
            if node.is_variable():
                node.value = random_constant()
            else:
                node.value = random_variable(n_features)
        else:  # Internal node
            current_arity = ALL_OPERATORS[node.op].arity
            valid_ops = [op for op in ALL_OPERATORS.values() if op.arity == current_arity]
            node.op = random.choice(valid_ops).name

        return mutant

class SubtreeMutation(BaseMutationStrategy):
    """
    Replaces a randomly chosen subtree with a new randomly generated tree.
    """

    def mutate(self, individual: Node, n_features: int) -> Node:
        mutant = individual.copy_tree()
        node, _ = get_random_node(mutant)

        # Replace subtree
        new_subtree = Node.generate_random_tree(depth=3, n_features=n_features, grow=True)
        node.replace_with(new_subtree)

        return mutant

class HoistMutation(BaseMutationStrategy):
    """
    Replaces the root of a subtree with one of its children.
    """

    def mutate(self, individual: Node, n_features: int) -> Node:
        mutant = individual.copy_tree()
        node, _ = get_random_node(mutant)

        if not node.is_leaf():
            # Randomly select one of the children to hoist
            hoisted_child = random.choice(node.children)
            node.replace_with(hoisted_child.copy_tree())

        return mutant

class CreepMutation(BaseMutationStrategy):
    """
    Slightly adjusts constants within the tree by adding a small random value.
    """

    def mutate(self, individual: Node, n_features: int) -> Node:
        mutant = individual.copy_tree()
        node, _ = get_random_node(mutant)

        if node.op is None and not node.is_variable():  # Only adjust constants
            creep_value = random.uniform(-0.1, 0.1)  # Small adjustment
            node.value += creep_value

        return mutant

class ShrinkMutation(BaseMutationStrategy):
    """
    Replaces a subtree with a leaf node.
    """

    def mutate(self, individual: Node, n_features: int) -> Node:
        mutant = individual.copy_tree()
        node, _ = get_random_node(mutant)

        if node.op is not None:  # Only apply to non-leaf nodes
            node.op = None
            node.value = random.choice([random_constant(), random_variable(n_features)])
            node.children = []

        return mutant

class NoopMutation(BaseMutationStrategy):
    """
    Does nothing (useful for testing).
    """

    def mutate(self, individual: Node, n_features: int) -> Node:
        return individual.copy_tree()

################################
# Manager adattivo
################################
class AdaptiveMutationManager:
    def __init__(self, statistics):
        self.strategies = {
            "simple": SimpleMutation(),
            "subtree": SubtreeMutation(),
            "hoist": HoistMutation(),
            "shrink": ShrinkMutation(),
            "noop": NoopMutation()
        }
        self.statistics = statistics
        self.active_strategy = "simple"  # Default strategy

    def choose_strategy(self) -> BaseMutationStrategy:
        if self.statistics.get("complexity", 0) > 10:
            self.active_strategy = "shrink"
        elif self.statistics.get("diversity", 0) < 5:
            self.active_strategy = "subtree"
        elif self.statistics.get("stagnation", False):
            self.active_strategy = "hoist"
        else:
            self.active_strategy = "simple"

        return self.strategies[self.active_strategy]

    def mutate(self, individual: Node, n_features: int) -> Node:
        chosen_strategy = self.choose_strategy()
        return chosen_strategy.mutate(individual, n_features)

    def get_active_strategy(self) -> str:
        """Restituisce la strategia attiva."""
        return self.active_strategy
