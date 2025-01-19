import random
from tree import Node

class AdaptiveCrossoverManager:
    def __init__(self, statistics, logger=None):
        """
        Adaptive crossover manager for genetic programming.

        Args:
            statistics (dict): Dictionary containing statistics for decision-making.
            logger (Logger, optional): Logger for recording strategy changes.
        """
        self.statistics = statistics
        self.logger = logger
        self.active_strategy = "one_point"  # Default strategy
        self.previous_strategy = None  # To track changes in strategy

    def subtree_crossover(self, parent1: Node, parent2: Node) -> tuple[Node, Node]:
        """
        Subtree crossover strategy:
        - Selects a random node in parent1 and parent2, swaps the subtrees.
        """
        child1 = parent1.copy_tree()
        child2 = parent2.copy_tree()

        node1, _ = Node.get_random_node(child1)
        node2, _ = Node.get_random_node(child2)

        # Swap operations and children
        node1.op, node2.op = node2.op, node1.op
        node1.value, node2.value = node2.value, node1.value
        node1.children, node2.children = node2.children, node1.children

        return child1, child2

    def one_point_crossover(self, parent1: Node, parent2: Node) -> tuple[Node, Node]:
        """
        One-point crossover strategy:
        - Swaps a single child node between parent1 and parent2.
        """
        child1 = parent1.copy_tree()
        child2 = parent2.copy_tree()

        node1, _ = Node.get_random_node(child1)
        node2, _ = Node.get_random_node(child2)

        # Swap only the first child if both nodes have children
        if len(node1.children) >= 1 and len(node2.children) >= 1:
            node1.children[0], node2.children[0] = node2.children[0], node1.children[0]

        return child1, child2

    def uniform_crossover(self, parent1: Node, parent2: Node) -> tuple[Node, Node]:
        """
        Uniform crossover strategy:
        - Randomly selects genes from both parents for the offspring.
        """
        child1 = parent1.copy_tree()
        child2 = parent2.copy_tree()

        for node1, node2 in zip(child1.iterate_nodes(), child2.iterate_nodes()):
            if random.random() < 0.5:
                node1.op, node2.op = node2.op, node1.op
                node1.value, node2.value = node2.value, node1.value

        return child1, child2

    def blended_crossover(self, parent1: Node, parent2: Node) -> tuple[Node, Node]:
        """
        Blended crossover strategy:
        - Combines numerical values from parents to create offspring.
        """
        child1 = parent1.copy_tree()
        child2 = parent2.copy_tree()

        for node1, node2 in zip(child1.iterate_nodes(), child2.iterate_nodes()):
            if isinstance(node1.value, (int, float)) and isinstance(node2.value, (int, float)):
                blend = 0.5 * (node1.value + node2.value)
                node1.value, node2.value = blend, blend

        return child1, child2

    def noop_crossover(self, parent1: Node, parent2: Node) -> tuple[Node, Node]:
        """
        No-operation crossover strategy (useful for testing).
        """
        return parent1.copy_tree(), parent2.copy_tree()

    def choose_strategy(self):
        """
        Choose the active crossover strategy based on statistics and log the reason for changes.
        """
        new_strategy = self.active_strategy  # Default to current strategy
        reason = "Default strategy (one_point)"

        if self.statistics.get("complexity", 0) > 10:
            new_strategy = "blended"
            reason = "High complexity (>10)"
        elif self.statistics.get("diversity", 0) < 5:
            new_strategy = "uniform"
            reason = "Low diversity (<5)"
        elif self.statistics.get("stagnation", False):
            new_strategy = "subtree"
            reason = "Stagnation detected"

        # Log if the strategy changes
        if new_strategy != self.active_strategy:
            self.previous_strategy = self.active_strategy
            self.active_strategy = new_strategy
            if self.logger:
                self.logger.info(
                    [f"Crossover strategy changed from {self.previous_strategy} to {self.active_strategy}", f"Reason: {reason}"]
                )
                
    def crossover(self, parent1: Node, parent2: Node) -> tuple[Node, Node]:
        """
        Apply the selected crossover strategy to the parents.
        """
        self.choose_strategy()
        strategies = {
            "subtree": self.subtree_crossover,
            "one_point": self.one_point_crossover,
            "uniform": self.uniform_crossover,
            "blended": self.blended_crossover,
            "noop": self.noop_crossover
        }
        return strategies[self.active_strategy](parent1, parent2)

    def get_active_strategy(self) -> str:
        """
        Return the currently active strategy.
        """
        return self.active_strategy
