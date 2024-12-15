import sys
import os
from pathlib import Path
import logging

# Add the project root directory to the Python path
project_root = Path(__file__).parent.parent
sys.path.append(str(project_root))

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

try:
    from app.database.models import Base
    from app.database.connection import engine
except ImportError as e:
    logger.error(f"Error importing required modules: {e}")
    logger.error(f"Current Python path: {sys.path}")
    logger.error(f"Current working directory: {os.getcwd()}")
    sys.exit(1)

def create_tables():
    logger.info("Iniciando la creación de tablas...")
    try:
        Base.metadata.create_all(bind=engine)
        logger.info("Tablas creadas con éxito")
    except Exception as e:
        logger.error(f"Error al crear las tablas: {e}")
        raise

if __name__ == "__main__":
    create_tables()

