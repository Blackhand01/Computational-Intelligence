from gxgp.gp_dag import DagGP

def calculate_mse(model, x, y):
    """Calcola il Mean Squared Error"""
    y_pred = DagGP.evaluate(model, x.T)
    return sum((y - y_pred) ** 2) / len(y)
