# ==============================================
#               CONFIGURAZIONE                  
# ==============================================
POP_SIZE = 50               # Incrementata la popolazione per maggiore diversità
MAX_DEPTH = 5               # Ridotta la profondità massima per mitigare il bloat
N_GENERATIONS = 500           # Aumentato il numero di generazioni
TOURNAMENT_SIZE = 5          # Maggiore pressione selettiva
MUTATION_RATE = 0.6          # Ridotto per bilanciare l'effetto del crossover
CROSSOVER_RATE = 0.9         # Incrementata per favorire l'esplorazione
ELITISM = 3                  # Aumentato il numero di individui elitari

# Parametro per il controllo del bloat:
BLOAT_PENALTY = 0.2          # Incrementata la penalità per favorire alberi più piccoli

# Parametri per la Partial Reinitialization
PARTIAL_REINIT_EVERY = 3     # Incrementata la frequenza
PARTIAL_REINIT_RATIO = 0.25  # Incrementata la proporzione di reinizializzazione
DIVERSITY_THRESHOLD = 3   # Soglia per attivare la reiniezione
REINIT_FRACTION = 0.9    # Percentuale della popolazione da reinizializzare

# Nuova opzione: abilitazione/disabilitazione della local search
ENABLE_LOCAL_SEARCH = False

# Nuova opzione: bilanciamento dinamico tra esplorazione e sfruttamento
ADAPTIVE_STRATEGY = False     # Attiva strategie adattive
SEED = 42

# Parametri per l'early stopping
MAX_GENERATIONS_NO_IMPROVEMENT = 50  # Numero massimo di generazioni senza miglioramenti
FITNESS_THRESHOLD = 100  # Soglia minima per la fitness migliore

