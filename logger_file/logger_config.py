import os
import logging

LOGS_DIR = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "logs")
os.makedirs(LOGS_DIR, exist_ok=True)

def setup_logger(name: str, log_file: str, level=logging.INFO) -> logging.Logger:
    """Configures and returns a dedicated logger writing to logs/ directory."""
    file_path = os.path.join(LOGS_DIR, log_file)
    
    formatter = logging.Formatter(
        "%(asctime)s [%(levelname)s] [%(name)s]: %(message)s",
        datefmt="%Y-%m-%d %H:%M:%S"
    )

    file_handler = logging.FileHandler(file_path)
    file_handler.setFormatter(formatter)

    console_handler = logging.StreamHandler()
    console_handler.setFormatter(formatter)

    logger = logging.getLogger(name)
    logger.setLevel(level)

    if not logger.handlers:
        logger.addHandler(file_handler)
        logger.addHandler(console_handler)

    return logger

# Loggers mapping directly to your logs folder
ingestion_logger = setup_logger("ingestion", "ingestion.log")
etl_logger = setup_logger("etl_processing", "etl_processing.log")
db_logger = setup_logger("db_writes", "db_writes.log")