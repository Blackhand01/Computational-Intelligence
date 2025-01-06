import logging
import os
from datetime import datetime

def setup_logging(log_dir: str = "logs", log_level: str = "DEBUG") -> logging.Logger:
    """
    Configura il sistema di logging per il progetto.

    Args:
        log_dir (str): Directory dove salvare i file di log.
        log_level (str): Livello di log (es. DEBUG, INFO).

    Returns:
        logging.Logger: Istanza del logger configurato.
    """
    os.makedirs(log_dir, exist_ok=True)
    log_file = os.path.join(log_dir, f"project_log_{datetime.now().strftime('%Y%m%d_%H%M%S')}.log")

    # Configura il logger
    logger = logging.getLogger("SymbolicRegression")
    logger.setLevel(log_level)

    # Formatter
    formatter = logging.Formatter(
        fmt="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
        datefmt="%Y-%m-%d %H:%M:%S"
    )

    # Handler per file
    file_handler = logging.FileHandler(log_file)
    file_handler.setLevel(log_level)
    file_handler.setFormatter(formatter)

    # Handler per console
    console_handler = logging.StreamHandler()
    console_handler.setLevel(log_level)
    console_handler.setFormatter(formatter)

    # Aggiunge i handler al logger
    logger.addHandler(file_handler)
    logger.addHandler(console_handler)

    logger.info("Logging system initialized.")
    logger.info(f"Log file: {log_file}")

    return logger
