# ==============================================
#               CONFIGURAZIONE                  
# ==============================================
POP_SIZE = 100               # Dimensione della popolazione
MAX_DEPTH = 5                # Profondità massima degli alberi iniziali
N_GENERATIONS = 100          # Numero di generazioni
TOURNAMENT_SIZE = 3          # Dimensione del torneo (per la selezione)
MUTATION_RATE = 0.2          # Probabilità di mutazione
CROSSOVER_RATE = 0.8         # Probabilità di crossover
ELITISM = 1                  # Numero di individui elitari da tenere invariati

# Parametro per il controllo del bloat:
BLOAT_PENALTY = 0.01

# Parametri per la Partial Reinitialization
PARTIAL_REINIT_EVERY = 10
PARTIAL_REINIT_RATIO = 0.2
