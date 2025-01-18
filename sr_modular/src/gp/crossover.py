import random
from abc import ABC, abstractmethod
from tree import Node
from gp.utils import get_random_node

class BaseCrossoverStrategy(ABC):
    """
    Abstract base class for crossover strategies.
    """
    @abstractmethod
    def crossover(self, parent1: Node, parent2: Node) -> tuple[Node, Node]:
        pass

class SubtreeCrossoverStrategy(BaseCrossoverStrategy):
    """
    Subtree crossover strategy:
    - Selects a random node in parent1 and parent2, swaps the subtrees.
    """
    def crossover(self, parent1: Node, parent2: Node) -> tuple[Node, Node]:
        child1 = parent1.copy_tree()
        child2 = parent2.copy_tree()

        node1, _ = get_random_node(child1)
        node2, _ = get_random_node(child2)

        # Swap operations and children
        node1.op, node2.op = node2.op, node1.op
        node1.value, node2.value = node2.value, node1.value
        node1.children, node2.children = node2.children, node1.children

        return child1, child2

class OnePointCrossoverStrategy(BaseCrossoverStrategy):
    """
    One-point crossover strategy:
    - Swaps a single child node between parent1 and parent2.
    """
    def crossover(self, parent1: Node, parent2: Node) -> tuple[Node, Node]:
        child1 = parent1.copy_tree()
        child2 = parent2.copy_tree()

        node1, _ = get_random_node(child1)
        node2, _ = get_random_node(child2)

        # Swap only the first child if both nodes have children
        if len(node1.children) >= 1 and len(node2.children) >= 1:
            node1.children[0], node2.children[0] = node2.children[0], node1.children[0]

        return child1, child2

class UniformCrossoverStrategy(BaseCrossoverStrategy):
    """
    Uniform crossover strategy:
    - Randomly selects genes from both parents for the offspring.
    """
    def crossover(self, parent1: Node, parent2: Node) -> tuple[Node, Node]:
        child1 = parent1.copy_tree()
        child2 = parent2.copy_tree()

        for node1, node2 in zip(child1.iterate_nodes(), child2.iterate_nodes()):
            if random.random() < 0.5:
                node1.op, node2.op = node2.op, node1.op
                node1.value, node2.value = node2.value, node1.value

        return child1, child2

class BlendedCrossoverStrategy(BaseCrossoverStrategy):
    """
    Blended crossover strategy:
    - Combines numerical values from parents to create offspring.
    """
    def crossover(self, parent1: Node, parent2: Node) -> tuple[Node, Node]:
        child1 = parent1.copy_tree()
        child2 = parent2.copy_tree()

        for node1, node2 in zip(child1.iterate_nodes(), child2.iterate_nodes()):
            if isinstance(node1.value, (int, float)) and isinstance(node2.value, (int, float)):
                blend = 0.5 * (node1.value + node2.value)
                node1.value, node2.value = blend, blend

        return child1, child2

class NoopCrossoverStrategy(BaseCrossoverStrategy):
    """
    No-operation crossover strategy (useful for testing).
    """
    def crossover(self, parent1: Node, parent2: Node) -> tuple[Node, Node]:
        return parent1.copy_tree(), parent2.copy_tree()

class AdaptiveCrossoverManager:
    def __init__(self, statistics):
        self.strategies = {
            "subtree": SubtreeCrossoverStrategy(),
            "one_point": OnePointCrossoverStrategy(),
            "uniform": UniformCrossoverStrategy(),
            "blended": BlendedCrossoverStrategy(),
            "noop": NoopCrossoverStrategy()
        }
        self.statistics = statistics
        self.active_strategy = "one_point"  # Default strategy

    def choose_strategy(self) -> BaseCrossoverStrategy:
        if self.statistics.get("complexity", 0) > 10:
            self.active_strategy = "blended"
        elif self.statistics.get("diversity", 0) < 5:
            self.active_strategy = "uniform"
        elif self.statistics.get("stagnation", False):
            self.active_strategy = "subtree"
        else:
            self.active_strategy = "one_point"

        return self.strategies[self.active_strategy]

    def crossover(self, parent1: Node, parent2: Node) -> tuple[Node, Node]:
        chosen_strategy = self.choose_strategy()
        return chosen_strategy.crossover(parent1, parent2)

    def get_active_strategy(self) -> str:
        """Restituisce la strategia attiva."""
        return self.active_strategy
