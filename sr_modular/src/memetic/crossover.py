import random
from core.tree import Node

class AdaptiveCrossoverManager:
    """
    Gestore adattivo dei crossover per la programmazione genetica.
    
    Questa classe permette di selezionare e applicare dinamicamente diverse strategie
    di crossover, in base alle statistiche dell'evoluzione.
    """

    def __init__(self, statistics):
        """
        Inizializza il gestore adattivo dei crossover.

        Args:
            statistics (GPStatistics): Oggetto che traccia statistiche e dati sull'evoluzione.
            logger (Logger, opzionale): Oggetto per registrare eventi e cambi di strategia.
        """
        self.statistics = statistics
        self.active_strategy = "one_point"  # Strategia predefinita

    def subtree_crossover(self, parent1: Node, parent2: Node) -> tuple[Node, Node]:
        """
        Strategia di crossover per sottoalberi:
        - Seleziona casualmente un nodo da entrambi i genitori.
        - Scambia i sottoalberi radicati nei nodi selezionati.

        Questa strategia favorisce grandi cambiamenti nella struttura degli alberi,
        utile per aumentare la diversità nella popolazione.
        """
        child1 = parent1.copy_tree()
        child2 = parent2.copy_tree()

        node1, _ = Node.get_random_node(child1)
        node2, _ = Node.get_random_node(child2)

        # Scambia le informazioni tra i nodi selezionati
        node1.op, node2.op = node2.op, node1.op
        node1.value, node2.value = node2.value, node1.value
        node1.children, node2.children = node2.children, node1.children

        return child1, child2

    def one_point_crossover(self, parent1: Node, parent2: Node) -> tuple[Node, Node]:
        """
        Strategia di crossover a singolo punto:
        - Scambia il primo figlio di due nodi casualmente selezionati nei genitori.
        
        Utile per generare variazioni locali mantenendo gran parte della struttura originale.
        """
        child1 = parent1.copy_tree()
        child2 = parent2.copy_tree()

        node1, _ = Node.get_random_node(child1)
        node2, _ = Node.get_random_node(child2)

        if len(node1.children) >= 1 and len(node2.children) >= 1:
            node1.children[0], node2.children[0] = node2.children[0], node1.children[0]

        return child1, child2

    def uniform_crossover(self, parent1: Node, parent2: Node) -> tuple[Node, Node]:
        """
        Strategia di crossover uniforme:
        - Per ogni nodo corrispondente nei due genitori, scambia casualmente le informazioni.
        
        Utile per una combinazione più equilibrata delle caratteristiche dei genitori.
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
        Strategia di crossover misto:
        - Combina i valori numerici dei nodi corrispondenti tra i due genitori.
        
        Ideale per problemi con parametri continui, promuovendo una mediazione tra i genitori.
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
        Strategia di non-crossover:
        - Restituisce copie esatte dei genitori, senza modifiche.
        
        Utile per testare altri aspetti del sistema o per mantenere invariati alcuni individui.
        """
        return parent1.copy_tree(), parent2.copy_tree()

    def choose_strategy(self):
        """
        Cambia la strategia attiva in base alle statistiche attuali.
        """
        old_strategy = self.active_strategy
        new_strategy = old_strategy  # Mantiene la strategia corrente come predefinita
        reason = "Strategia predefinita (one_point)"

        
        if self.statistics.generations_no_improvement > 3:
            new_strategy = "subtree"
            reason = "Stagnazione rilevata"
        elif self.statistics.diversity < 0.5:
            new_strategy = "uniform"
            reason = "Bassa diversità (<0.5)"
        elif self.statistics.complexity >20:
            new_strategy = "blended"
            reason = "Alta complessità (>20)"
        

        self.statistics.update_single_strategy(
            strategy_type="crossover",
            old_strategy=old_strategy,
            new_strategy=new_strategy,
            reason=reason
        )

        self.active_strategy = new_strategy

    def crossover(self, parent1: Node, parent2: Node) -> tuple[Node, Node]:
        """
        Applica la strategia di crossover selezionata ai genitori forniti.
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
        Restituisce la strategia di crossover attualmente attiva.
        """
        return self.active_strategy
