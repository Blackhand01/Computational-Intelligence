import os

def print_repository_structure(directory, max_depth, output_file):
    """
    Stampa la struttura del repository con profondità massima e salva in un file.
    Per la directory 'src', esplora fino alla profondità massima specifica.
    """
    with open(output_file, 'w', encoding='utf-8') as out_file:
        out_file.write("Repository Structure:\n")
        print("Repository Structure:")
        
        for root, dirs, files in os.walk(directory):
            depth = root[len(directory):].count(os.sep)
            
            # Per 'src', ignora il limite di profondità
            if "src" in os.path.relpath(root, directory).split(os.sep):
                current_max_depth = float('inf')
            else:
                current_max_depth = max_depth
            
            if depth >= current_max_depth:
                dirs[:] = []
                continue
            
            indent = "  " * depth
            folder_name = os.path.basename(root) or root
            out_file.write(f"{indent}{folder_name}/\n")
            print(f"{indent}{folder_name}/")
            
            for file in files:
                file_indent = "  " * (depth + 1)
                out_file.write(f"{file_indent}{file}\n")
                print(f"{file_indent}{file}")


def collect_code_to_file(directory, output_file):
    """
    Raccoglie codice rilevante dai file nel repository e lo salva in un file di output.
    """
    # Escludi file e directory irrilevanti
    exclude_files = {'.DS_Store', '.gitignore','data',}
    exclude_dirs = {'.pytest_cache', '__pycache__', '.venv', 'node_modules', 'dist', 'build', 'docs/_build', '.git', 'history.csv',
                    'symbolic_regression/scripts/trace_code.py'}

    # Assicurati che la directory del file di output esista
    os.makedirs(os.path.dirname(output_file), exist_ok=True)

    with open(output_file, 'a', encoding='utf-8') as out_file:  # Usa modalità 'a' per appendere
        out_file.write('"""\n\nRepository Code Collection\n\n')
        
        for root, dirs, files in os.walk(directory):
            # Escludi directory specificate
            dirs[:] = [d for d in dirs if d not in exclude_dirs]

            for file in files:
                if file in exclude_files:
                    continue

                file_path = os.path.join(root, file)
                relative_path = os.path.relpath(file_path, directory)
                
                # Filtra file binari o con permessi non accessibili
                try:
                    with open(file_path, 'r', encoding='utf-8') as f:
                        lines = f.readlines()
                except (UnicodeDecodeError, PermissionError):
                    print(f"Skipping file {relative_path} due to encoding/permission issues.")
                    continue
                
                # Stampa il nome del file e il contenuto
                out_file.write(f'# File: {relative_path}\n')
                out_file.write(f'# Number of Lines: {len(lines)}\n')
                out_file.write(''.join(lines))
                out_file.write('\n\n')  # Spazio tra i file
        out_file.write('"""\n\n')

    print(f"Code collected and saved to {output_file}.")


if __name__ == "__main__":
    # Configura la directory del repository e il file di output
    repository_path_structure = "/Users/stefanoroybisignano/Desktop/P_CI/symbolic_regression"
    repository_path = "/Users/stefanoroybisignano/Desktop/P_CI/symbolic_regression/src"
    output_file_path = "/Users/stefanoroybisignano/Desktop/P_CI/symbolic_regression/scripts/collected_code.txt"

    # Stampa la struttura del repository e salva nel file di output
    print_repository_structure(repository_path_structure, max_depth=4, output_file=output_file_path)

    # Raccogli il codice e salva nel file di output
    collect_code_to_file(repository_path, output_file_path)
