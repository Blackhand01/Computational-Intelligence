from gxgp.node import Node
from gxgp.gp_dag import DagGP

def train_model(x_train, y_train):
    """Addestra un modello con GXGP"""
    operators = [lambda x, y: x + y, lambda x, y: x * y]
    variables = [f'x{i}' for i in range(x_train.shape[0])]
    gp = DagGP(operators, variables, constants=3)
    return gp.create_individual()

def evaluate_model(model, x, y):
    """Valuta il modello su un dataset"""
    return DagGP.mse(model, x.T, y)

def draw_model(model, output_file):
    """Disegna l'albero del modello"""
    model.draw(output_file)
