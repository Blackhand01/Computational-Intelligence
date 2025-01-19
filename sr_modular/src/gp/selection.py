import random
import numpy as np
from tree import Node
from evaluator import Evaluator


class AdaptiveSelectionManager:
    """
    Gestore adattivo della selezione per la programmazione genetica.

    Questa classe consente di scegliere e applicare dinamicamente strategie di selezione
    in base alle statistiche raccolte durante l'evoluzione.
    """

    def __init__(self, statistics):
        """
        Inizializza il gestore adattivo della selezione.

        Args:
            statistics (GPStatistics): Oggetto per tracciare le statistiche dell'evoluzione.
        """
        self.statistics = statistics
        self.active_strategy = "elitist"  # Strategia predefinita

    def tournament_selection(self, population: list[Node], x, y, bloat_penalty: float, tournament_size=3) -> Node:
        """
        Strategia di selezione a torneo:
        - Seleziona casualmente un gruppo di individui (competitors) dalla popolazione.
        - Valuta la fitness di ogni individuo nel torneo.
        - Restituisce l'individuo con la migliore fitness.

        Questa strategia bilancia esplorazione ed exploitazione, consentendo a individui
        meno adatti di partecipare al torneo, ma premiando quelli più performanti.
        """
        competitors = random.sample(population, tournament_size)
        fitness_values = [
            Evaluator.fitness_function(ind, x, y, bloat_penalty)
            for ind in competitors
        ]
        best_index = np.argmin(fitness_values)
        return competitors[best_index]

    def roulette_selection(self, population: list[Node], x, y, bloat_penalty: float) -> Node:
        """
        Strategia di selezione a ruota della fortuna:
        - Ogni individuo ottiene una probabilità di selezione proporzionale alla propria fitness.
        - Gli individui con fitness migliore hanno una maggiore probabilità di essere scelti.

        Questa strategia favorisce l'exploitazione dei migliori individui ma consente anche
        agli individui peggiori di essere selezionati, mantenendo la diversità.
        """
        fitness_values = [
            Evaluator.fitness_function(ind, x, y, bloat_penalty)
            for ind in population
        ]
        scores = [1 / (1 + f) for f in fitness_values]  # Conversione fitness in punteggi
        total = sum(scores)
        pick = random.random() * total
        current = 0
        for ind, s in zip(population, scores):
            current += s
            if current > pick:
                return ind
        return population[-1]  # Fallback nel caso non si selezioni nulla

    def rank_selection(self, population: list[Node], x, y, bloat_penalty: float) -> Node:
        """
        Strategia di selezione basata sul rango:
        - Ordina la popolazione in base alla fitness.
        - Assegna una probabilità di selezione a ogni individuo in base al rango.
        - Gli individui con rango migliore hanno maggiore probabilità di essere selezionati.

        Utile per prevenire il dominio assoluto dei migliori individui e mantenere la diversità.
        """
        fitness_values = [
            Evaluator.fitness_function(ind, x, y, bloat_penalty)
            for ind in population
        ]
        sorted_indices = np.argsort(fitness_values)
        ranks = np.arange(1, len(population) + 1)
        probabilities = ranks / ranks.sum()
        return population[np.random.choice(sorted_indices, p=probabilities)]

    def elitist_selection(self, population: list[Node], x, y, bloat_penalty: float) -> Node:
        """
        Strategia di selezione elitista:
        - Seleziona sempre l'individuo con la fitness migliore.

        Questa strategia massimizza l'exploitazione, ma rischia di ridurre la diversità
        della popolazione.
        """
        fitness_values = [
            Evaluator.fitness_function(ind, x, y, bloat_penalty)
            for ind in population
        ]
        best_index = np.argmin(fitness_values)
        return population[best_index]

    def choose_strategy(self):
        """
        Sceglie la strategia di selezione attiva in base alle statistiche e aggiorna GPStatistics.
        """
        old_strategy = self.active_strategy
        new_strategy = old_strategy  # Strategia predefinita
        reason = "Strategia predefinita (elitist)"

        if self.statistics.complexity > 10:
            new_strategy = "rank"
            reason = "Alta complessità (>10)"
        elif self.statistics.diversity < 5:
            new_strategy = "tournament"
            reason = "Bassa diversità (<5)"
        elif self.statistics.generations_no_improvement > 5:
            new_strategy = "roulette"
            reason = "Stagnazione rilevata"

        # Aggiorna la strategia tramite GPStatistics
        self.statistics.update_single_strategy(
            strategy_type="selection",
            old_strategy=old_strategy,
            new_strategy=new_strategy,
            reason=reason
        )

        self.active_strategy = new_strategy

    def select(self, population: list[Node], x, y, bloat_penalty: float) -> Node:
        """
        Applica la strategia di selezione attiva alla popolazione.
        """
        self.choose_strategy()
        strategies = {
            "tournament": self.tournament_selection,
            "roulette": self.roulette_selection,
            "rank": self.rank_selection,
            "elitist": self.elitist_selection
        }
        return strategies[self.active_strategy](population, x, y, bloat_penalty)

    def get_active_strategy(self) -> str:
        """
        Restituisce la strategia di selezione attualmente attiva.
        """
        return self.active_strategy
