import random
from tree import Node, random_variable, random_constant
from safe_math import ALL_OPERATORS

class AdaptiveMutationManager:
    def __init__(self, statistics):
        self.statistics = statistics
        self.active_strategy = "simple"  # Default strategy

    def simple_mutation(self, individual: Node, n_features: int) -> Node:
        """
        Simple mutation strategy that preserves the arity of the operator.
        """
        mutant = individual.copy_tree()
        node, _ = Node.get_random_node(mutant)

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

    def subtree_mutation(self, individual: Node, n_features: int) -> Node:
        """
        Replaces a randomly chosen subtree with a new randomly generated tree.
        """
        mutant = individual.copy_tree()
        node, _ = Node.get_random_node(mutant)

        # Replace subtree
        new_subtree = Node.generate_random_tree(max_depth=3, n_features=n_features, grow=True)
        node.replace_with(new_subtree)

        return mutant

    def hoist_mutation(self, individual: Node, n_features: int) -> Node:
        """
        Replaces the root of a subtree with one of its children.
        """
        mutant = individual.copy_tree()
        node, _ = Node.get_random_node(mutant)

        if not node.is_leaf():
            # Randomly select one of the children to hoist
            hoisted_child = random.choice(node.children)
            node.replace_with(hoisted_child.copy_tree())

        return mutant

    def creep_mutation(self, individual: Node, n_features: int) -> Node:
        """
        Slightly adjusts constants within the tree by adding a small random value.
        """
        mutant = individual.copy_tree()
        node, _ = Node.get_random_node(mutant)

        if node.op is None and not node.is_variable():  # Only adjust constants
            creep_value = random.uniform(-0.1, 0.1)  # Small adjustment
            node.value += creep_value

        return mutant

    def shrink_mutation(self, individual: Node, n_features: int) -> Node:
        """
        Replaces a subtree with a leaf node.
        """
        mutant = individual.copy_tree()
        node, _ = Node.get_random_node(mutant)

        if node.op is not None:  # Only apply to non-leaf nodes
            node.op = None
            node.value = random.choice([random_constant(), random_variable(n_features)])
            node.children = []

        return mutant

    def noop_mutation(self, individual: Node, n_features: int) -> Node:
        """
        Does nothing (useful for testing).
        """
        return individual.copy_tree()

    def choose_strategy(self):
        """
        Choose the active mutation strategy based on statistics.
        """
        if self.statistics.get("complexity", 0) > 10:
            self.active_strategy = "shrink"
        elif self.statistics.get("diversity", 0) < 5:
            self.active_strategy = "subtree"
        elif self.statistics.get("stagnation", False):
            self.active_strategy = "hoist"
        else:
            self.active_strategy = "simple"

    def mutate(self, individual: Node, n_features: int) -> Node:
        """
        Apply the selected mutation strategy to the individual.
        """
        self.choose_strategy()
        strategies = {
            "simple": self.simple_mutation,
            "subtree": self.subtree_mutation,
            "hoist": self.hoist_mutation,
            "creep": self.creep_mutation,
            "shrink": self.shrink_mutation,
            "noop": self.noop_mutation
        }
        return strategies[self.active_strategy](individual, n_features)

    def get_active_strategy(self) -> str:
        """
        Return the currently active strategy.
        """
        return self.active_strategy
