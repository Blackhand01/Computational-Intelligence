# File: src/core/dynamic_strategies.py

import numpy as np
from typing import List
from src.core.tree import Tree

def population_diversity(population: List[Tree]) -> float:
    """
    Calcola una misura di diversità basata sulla variazione delle dimensioni degli alberi.
    Puoi sostituire questa metrica con altre più sofisticate, come la distanza strutturale.
    
    Args:
        population (List[Tree]): Lista di alberi nella popolazione.
    
    Returns:
        float: Misura di diversità normalizzata tra 0 e 1.
    """
    sizes = [ind.size() for ind in population]
    if not sizes:
        return 0.0
    max_size = max(sizes)
    min_size = min(sizes)
    diversity = (max_size - min_size) / (max_size + 1e-9)  # Evita divisioni per zero
    return diversity

def choose_mutation(population: List[Tree], fitness_scores: List[float], generation: int, max_generations: int) -> str:
    """
    Seleziona dinamicamente la strategia di mutazione basata su diversità, complessità e generazione corrente.
    
    Args:
        population (List[Tree]): Lista di alberi nella popolazione.
        fitness_scores (List[float]): Lista dei punteggi di fitness corrispondenti.
        generation (int): Numero della generazione corrente.
        max_generations (int): Numero massimo di generazioni.
    
    Returns:
        str: Nome della strategia di mutazione selezionata.
    """
    diversity = population_diversity(population)
    avg_fitness = np.mean(fitness_scores) if fitness_scores else float("inf")
    complexity = np.mean([tree.size() for tree in population]) if population else 0

    if diversity < 0.3:
        return "subtree"  # Aumenta la diversità sostituendo sottoalberi
    elif complexity > 50:
        return "shrink"   # Controlla la complessità riducendo la dimensione
    elif generation > 0.8 * max_generations:
        return "point"    # Raffina le soluzioni nelle fasi finali
    else:
        return "hoist"    # Esplora nuovi spazi

def choose_crossover(population: List[Tree], generation: int, max_generations: int) -> str:
    """
    Seleziona dinamicamente la strategia di crossover basata su diversità e generazione corrente.
    
    Args:
        population (List[Tree]): Lista di alberi nella popolazione.
        generation (int): Numero della generazione corrente.
        max_generations (int): Numero massimo di generazioni.
    
    Returns:
        str: Nome della strategia di crossover selezionata.
    """
    diversity = population_diversity(population)

    if diversity > 0.5 and generation < 0.5 * max_generations:
        return "subtree"   # Fase di esplorazione: subtree crossover
    elif generation > 0.5 * max_generations:
        return "uniform"   # Fase di sfruttamento: uniform crossover
    else:
        return "size_limit"  # Controllo della complessità: size limit crossover
