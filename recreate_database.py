import sys
import os
import logging
from sqlalchemy import create_engine, inspect, text
from sqlalchemy.exc import OperationalError, ProgrammingError

# Añadir el directorio raíz del proyecto al path de Python
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from app.config import DATABASE_URL
from app.database import Base, Message, MediaMessage, InteractiveMessage, FlowState

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def recreate_database():
    logger.info("Iniciando recreación de la base de datos...")

    # Crear el motor de la base de datos
    engine = create_engine(DATABASE_URL)

    try:
        # Eliminar todas las tablas existentes
        Base.metadata.drop_all(engine)
        logger.info("Todas las tablas existentes han sido eliminadas.")

        # Crear todas las tablas nuevamente
        Base.metadata.create_all(engine)
        logger.info("Todas las tablas han sido creadas nuevamente.")

        # Verificar que todas las tablas se hayan creado correctamente
        inspector = inspect(engine)
        tables = inspector.get_table_names()
        logger.info(f"Tablas creadas: {', '.join(tables)}")

        # Verificar las columnas de cada tabla
        for table_name in tables:
            columns = inspector.get_columns(table_name)
            logger.info(f"Columnas de la tabla '{table_name}':")
            for column in columns:
                logger.info(f"  - {column['name']} ({column['type']})")

        logger.info("Base de datos recreada con éxito.")

    except OperationalError as e:
        logger.error(f"Error operacional al recrear la base de datos: {e}")
        raise
    except ProgrammingError as e:
        logger.error(f"Error de programación al recrear la base de datos: {e}")
        raise
    except Exception as e:
        logger.error(f"Error inesperado al recrear la base de datos: {e}")
        raise

if __name__ == "__main__":
    recreate_database()

