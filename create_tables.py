from app.database import init_db
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

if __name__ == "__main__":
    logger.info("Iniciando la creación de tablas...")
    init_db()
    logger.info("Proceso de creación de tablas completado.")

