import sys
import os
from pathlib import Path

# Add the project root directory to the Python path
project_root = Path(__file__).parent.parent
sys.path.append(str(project_root))

print(f"Project root: {project_root}")
print(f"Current working directory: {os.getcwd()}")
print(f"Python path: {sys.path}")

try:
    from app.database import Base
    from app.config import settings
except ImportError as e:
    print(f"Error importing modules: {e}")
    sys.exit(1)

from sqlalchemy import create_engine
import logging

logging.basicConfig(level=logging.DEBUG, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

def init_db():
    logger.info("Iniciando la creación de la base de datos...")
    logger.debug(f"Usando DATABASE_URL: {settings.DATABASE_URL}")
    
    try:
        logger.debug("Creando el motor de la base de datos...")
        engine = create_engine(settings.DATABASE_URL, echo=True)
        
        logger.debug("Creando las tablas...")
        Base.metadata.create_all(bind=engine)
        
        logger.info("Base de datos creada con éxito")
    except Exception as e:
        logger.error(f"Error al crear la base de datos: {e}", exc_info=True)
        raise

if __name__ == "__main__":
    logger.info("Comenzando el script de inicialización de la base de datos")
    init_db()
    logger.info("Script de inicialización de la base de datos completado")

