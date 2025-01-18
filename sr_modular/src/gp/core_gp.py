import gp_config as config

class GeneticProgram:
    def __init__(self):
        self.population_size = config.POP_SIZE
        self.max_depth = config.MAX_DEPTH
        self.mutation_rate = config.MUTATION_RATE
        self.crossover_rate = config.CROSSOVER_RATE

    def evolve(self):
        for gen in range(config.N_GENERATIONS):
            # Logica di evoluzione
            pass
