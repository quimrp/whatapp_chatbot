import logging
import sys

def setup_logger(name: str = None, level: int = logging.INFO) -> logging.Logger:
    logger = logging.getLogger(name or __name__)
    
    if not logger.handlers:
        handler = logging.StreamHandler(sys.stdout)
        handler.setFormatter(
            logging.Formatter(
                '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
            )
        )
        logger.addHandler(handler)
    
    logger.setLevel(level)
    return logger

