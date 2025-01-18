
# ==============================================
# Funzione per salvare la formula migliore in un file
# ==============================================
def update_formula_in_file(formula_str, file_path, function_name):
    """
    Sovrascrive completamente la funzione `function_name` in `file_path`
    con `return formula_str`, assicurandosi che sia nel formato NumPy corretto.
    """
    with open(file_path, 'r') as file:
        lines = file.readlines()

    new_lines = []
    inside_function = False
    for line in lines:
        if line.strip().startswith(f"def {function_name}"):
            inside_function = True
            new_lines.append(f"def {function_name}(x: np.ndarray) -> np.ndarray:\n")
            new_lines.append(f"    return {formula_str}\n")
            continue
        if inside_function:
            if line.strip() == "" or line.strip().startswith("def "):
                inside_function = False
        if not inside_function:
            new_lines.append(line)

    with open(file_path, 'w') as file:
        file.writelines(new_lines)

    print(f"Formula aggiornata in {file_path} nella funzione {function_name}.")
