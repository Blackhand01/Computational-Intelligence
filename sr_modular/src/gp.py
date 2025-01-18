# import random
# from tree import Node, generate_random_tree, copy_tree, tree_depth, is_variable, random_constant, random_variable
# from evaluator import Evaluator
# from gp_config import (POP_SIZE, MAX_DEPTH, N_GENERATIONS, TOURNAMENT_SIZE, 
#                        MUTATION_RATE, CROSSOVER_RATE, ELITISM, BLOAT_PENALTY,
#                        PARTIAL_REINIT_EVERY, PARTIAL_REINIT_RATIO)
# from safe_math import ALL_OPERATORS

# class GeneticProgramming:
#     """
#     Modulo per la programmazione genetica che include evoluzione, crossover e mutazione.
#     """
#     @staticmethod
#     def tournament_selection(population, x, y, bloat_penalty):
#         """
#         Seleziona il miglior individuo da un sottoinsieme casuale della popolazione.

#         Args:
#             population (list[Node]): Lista degli alberi della popolazione.
#             x (np.ndarray): Array di input.
#             y (np.ndarray): Array di output atteso.
#             bloat_penalty (float): Penalità applicata in base alla dimensione degli alberi.

#         Returns:
#             Node: L'individuo selezionato.
#         """
#         competitors = random.sample(population, TOURNAMENT_SIZE)
#         evaluator = Evaluator()
#         best = min(competitors, key=lambda ind: evaluator.fitness_function(ind, x, y, bloat_penalty))
#         return best

#     @staticmethod
#     def crossover(parent1, parent2):
#         """
#         Applica il crossover tra due alberi genitori.

#         Args:
#             parent1 (Node): Primo genitore.
#             parent2 (Node): Secondo genitore.

#         Returns:
#             Tuple[Node, Node]: Due figli risultanti dal crossover.
#         """
#         child1 = copy_tree(parent1)
#         child2 = copy_tree(parent2)

#         # Cerca nodi validi per il crossover
#         node1, _ = GeneticProgramming._get_random_node(child1)
#         node2, _ = GeneticProgramming._get_random_node(child2)

#         # Saltiamo se uno dei nodi è una foglia
#         if node1.op is None or node2.op is None:
#             return child1, child2  # Nessun cambiamento

#         op1 = ALL_OPERATORS[node1.op]
#         op2 = ALL_OPERATORS[node2.op]

#         # Se arità diversa, saltiamo lo scambio
#         if op1.arity != op2.arity:
#             return child1, child2  # Nessun cambiamento

#         # Altrimenti scambiamo
#         node1.op, node2.op = node2.op, node1.op
#         node1.value, node2.value = node2.value, node1.value
#         node1.children, node2.children = node2.children, node1.children

#         return child1, child2

#     @staticmethod
#     def mutate(individual, n_features):
#         """
#         Applica una mutazione casuale a un albero.

#         Args:
#             individual (Node): Albero da mutare.
#             n_features (int): Numero di feature disponibili.

#         Returns:
#             Node: Albero mutato.
#         """
#         mutant = copy_tree(individual)
#         node, _ = GeneticProgramming._get_random_node(mutant)

#         if node.op is None:
#             # Foglia: resta foglia o diventa un nodo unario o binario
#             if random.random() < 0.5:
#                 node.value = random_variable(n_features)
#             else:
#                 node.value = random_constant()
#         else:
#             current_arity = ALL_OPERATORS[node.op].arity
#             if current_arity == 1:
#                 # Cambiamo solo con operatori unari
#                 valid_unaries = [op for op in ALL_OPERATORS.values() if op.arity == 1]
#                 new_op = random.choice(valid_unaries)
#                 node.op = new_op.name
#                 node.children = node.children[:1]  # Manteniamo solo il primo figlio
#             elif current_arity == 2:
#                 # Cambiamo solo con operatori binari
#                 valid_binaries = [op for op in ALL_OPERATORS.values() if op.arity == 2]
#                 new_op = random.choice(valid_binaries)
#                 node.op = new_op.name
#                 # Se mancano figli, aggiungiamoli
#                 while len(node.children) < 2:
#                     node.children.append(generate_random_tree(1, n_features, grow=True))

#         return mutant

#     @staticmethod
#     def evolve_population(population, x, y, n_features, generation):
#         """
#         Evolve la popolazione per una generazione.

#         Args:
#             population (list[Node]): Lista degli alberi della popolazione.
#             x (np.ndarray): Array di input.
#             y (np.ndarray): Array di output atteso.
#             n_features (int): Numero di feature disponibili.
#             generation (int): Indice della generazione corrente.

#         Returns:
#             list[Node]: Nuova popolazione evoluta.
#         """
#         evaluator = Evaluator()
#         ranked_pop = sorted(population, key=lambda ind: evaluator.fitness_function(ind, x, y, BLOAT_PENALTY))
#         new_population = ranked_pop[:ELITISM]  # Elitismo

#         while len(new_population) < POP_SIZE:
#             parent1 = GeneticProgramming.tournament_selection(ranked_pop, x, y, BLOAT_PENALTY)
#             parent2 = GeneticProgramming.tournament_selection(ranked_pop, x, y, BLOAT_PENALTY)

#             if random.random() < CROSSOVER_RATE:
#                 off1, off2 = GeneticProgramming.crossover(parent1, parent2)
#             else:
#                 off1, off2 = copy_tree(parent1), copy_tree(parent2)

#             if random.random() < MUTATION_RATE:
#                 off1 = GeneticProgramming.mutate(off1, n_features)
#             if random.random() < MUTATION_RATE:
#                 off2 = GeneticProgramming.mutate(off2, n_features)

#             new_population.append(off1)
#             if len(new_population) < POP_SIZE:
#                 new_population.append(off2)

#         if generation % PARTIAL_REINIT_EVERY == 0 and generation != 0:
#             n_reinit = int(PARTIAL_REINIT_RATIO * POP_SIZE)
#             for i in range(n_reinit):
#                 new_population[-(i + 1)] = generate_random_tree(MAX_DEPTH, n_features, grow=True)

#         return new_population

#     @staticmethod
#     def _get_random_node(node):
#         """
#         Restituisce un nodo casuale e il suo genitore dall'albero.

#         Args:
#             node (Node): Nodo radice dell'albero.

#         Returns:
#             Tuple[Node, Node]: Nodo casuale e suo genitore.
#         """
#         all_nodes = []

#         def traverse(current, parent):
#             all_nodes.append((current, parent))
#             for child in current.children:
#                 traverse(child, current)

#         traverse(node, None)
#         return random.choice(all_nodes)
