import random
from core.tree import Node, random_variable, random_constant
from core.safe_math import ALL_OPERATORS


class AdaptiveMutationManager:
    """
    Gestore adattivo delle mutazioni per la programmazione genetica.

    La classe consente di selezionare e applicare dinamicamente diverse strategie di mutazione
    basate su statistiche e criteri di adattamento.
    """

    def __init__(self, statistics):
        """
        Inizializza il gestore adattivo delle mutazioni.

        Args:
            statistics (GPStatistics): Oggetto per tracciare statistiche e logging durante l'evoluzione.
        """
        self.statistics = statistics
        self.active_strategy = "simple"  # Strategia predefinita

    def simple_mutation(self, individual: Node, n_features: int) -> Node:
        """
        Strategia di mutazione semplice:
        - Preserva l'arietà dell'operatore nel nodo selezionato casualmente.
        - Per i nodi foglia, cambia la costante o la variabile.
        
        Questa strategia favorisce cambiamenti locali e semplici.
        """
        mutant = individual.copy_tree()
        node, _ = Node.get_random_node(mutant)

        if node.op is None:  # Nodo foglia
            if node.is_variable():
                node.value = random_constant()
            else:
                node.value = random_variable(n_features)
        else:  # Nodo interno
            current_arity = ALL_OPERATORS[node.op].arity
            valid_ops = [op for op in ALL_OPERATORS.values() if op.arity == current_arity]
            node.op = random.choice(valid_ops).name

        return mutant

    def subtree_mutation(self, individual: Node, n_features: int) -> Node:
        """
        Strategia di mutazione del sottoalbero:
        - Sostituisce un sottoalbero casualmente selezionato con un nuovo albero generato.
        
        Favorisce l'esplorazione introducendo strutture completamente nuove.
        """
        mutant = individual.copy_tree()
        node, _ = Node.get_random_node(mutant)

        new_subtree = Node.generate_random_tree(max_depth=3, n_features=n_features, grow=True)
        node.replace_with(new_subtree)

        return mutant

    def hoist_mutation(self, individual: Node, n_features: int) -> Node:
        """
        Strategia di mutazione con promozione:
        - Sostituisce un sottoalbero con uno dei suoi figli, rimuovendo un livello di profondità.

        Utile per ridurre la complessità degli alberi.
        """
        mutant = individual.copy_tree()
        node, _ = Node.get_random_node(mutant)

        if not node.is_leaf():
            hoisted_child = random.choice(node.children)
            node.replace_with(hoisted_child.copy_tree())

        return mutant

    def creep_mutation(self, individual: Node, n_features: int) -> Node:
        """
        Strategia di mutazione incrementale:
        - Modifica leggermente le costanti aggiungendo un piccolo valore casuale.

        Favorisce l'esplorazione fine in spazi numerici continui.
        """
        mutant = individual.copy_tree()
        node, _ = Node.get_random_node(mutant)

        if node.op is None and not node.is_variable():  # Solo per costanti
            creep_value = random.uniform(-0.1, 0.1)
            node.value = ('const', node.value[1] + creep_value)

        return mutant

    def shrink_mutation(self, individual: Node, n_features: int) -> Node:
        """
        Strategia di riduzione:
        - Sostituisce un sottoalbero con un nodo foglia, semplificando la struttura.

        Utile per ridurre l'eccessiva complessità (problema del bloat).
        """
        mutant = individual.copy_tree()
        node, _ = Node.get_random_node(mutant)

        if node.op is not None:  # Solo nodi interni
            node.op = None
            node.value = random.choice([random_constant(), random_variable(n_features)])
            node.children = []

        return mutant

    def noop_mutation(self, individual: Node, n_features: int) -> Node:
        """
        Strategia di non-mutazione:
        - Restituisce l'individuo invariato.

        Utile per testare altri aspetti del sistema.
        """
        return individual.copy_tree()

    def choose_strategy(self):
        """
        Seleziona la strategia di mutazione attiva in base alle statistiche e registra i motivi del cambiamento.
        """
        old_strategy = self.active_strategy
        new_strategy = old_strategy  # Strategia predefinita
        reason = "Strategia predefinita (simple)"

        if self.statistics.complexity > 10:
            new_strategy = "shrink"
            reason = "Alta complessità (>10)"
        elif self.statistics.diversity < 5:
            new_strategy = "subtree"
            reason = "Bassa diversità (<5)"
        elif self.statistics.generations_no_improvement > 5:
            new_strategy = "hoist"
            reason = "Stagnazione rilevata"

        self.statistics.update_single_strategy(
            strategy_type="mutation",
            old_strategy=old_strategy,
            new_strategy=new_strategy,
            reason=reason
        )

        self.active_strategy = new_strategy

    def mutate(self, individual: Node, n_features: int) -> Node:
        """
        Applica la strategia di mutazione selezionata all'individuo.
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
        Restituisce la strategia di mutazione attualmente attiva.
        """
        return self.active_strategy
