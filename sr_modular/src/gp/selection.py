import random
from evaluator import Evaluator

def tournament_selection(population, x, y, bloat_penalty, tournament_size=3):
    """
    Seleziona il miglior individuo da un sottoinsieme casuale della popolazione.

    Args:
        population (list[Node]): Lista degli alberi della popolazione.
        x (np.ndarray): Array di input.
        y (np.ndarray): Array di output atteso.
        bloat_penalty (float): Penalità applicata in base alla dimensione degli alberi.
        tournament_size (int): Dimensione del torneo.

    Returns:
        Node: L'individuo selezionato.
    """
    competitors = random.sample(population, tournament_size)
    evaluator = Evaluator()
    best = min(competitors, key=lambda ind: evaluator.fitness_function(ind, x, y, bloat_penalty))
    return best
