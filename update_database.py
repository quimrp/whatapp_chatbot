import sys
import os
import logging
from sqlalchemy import create_engine, text, MetaData, Table, Column, Integer, String, DateTime, ForeignKey, JSON
from sqlalchemy.exc import OperationalError, ProgrammingError

# Añadir el directorio raíz del proyecto al path de Python
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from app.config import DATABASE_URL

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def update_database():
    logger.info("Iniciando actualización de la base de datos...")

    # Crear el motor de la base de datos
    engine = create_engine(DATABASE_URL)
    metadata = MetaData()

    # Definir todas las tablas
    messages = Table('messages', metadata,
        Column('id', Integer, primary_key=True),
        Column('sender', String(255)),
        Column('content', String(1000)),
        Column('message_type', String(50)),
        Column('timestamp', DateTime)
    )

    media_messages = Table('media_messages', metadata,
        Column('id', Integer, primary_key=True),
        Column('message_id', Integer, ForeignKey('messages.id')),
        Column('media_type', String(50)),
        Column('media_url', String(500)),
        Column('timestamp', DateTime)
    )

    interactive_messages = Table('interactive_messages', metadata,
        Column('id', Integer, primary_key=True),
        Column('message_id', Integer, ForeignKey('messages.id')),
        Column('interactive_type', String(50)),
        Column('content', JSON),
        Column('timestamp', DateTime)
    )

    flow_states = Table('flow_states', metadata,
        Column('id', Integer, primary_key=True),
        Column('user_id', String(255)),
        Column('current_flow', String(255)),
        Column('current_node', String(255)),
        Column('timestamp', DateTime)
    )

    try:
        with engine.connect() as connection:
            # Actualizar tabla messages
            if not engine.dialect.has_table(connection, 'messages'):
                messages.create(engine)
                logger.info("Tabla 'messages' creada")
            else:
                try:
                    connection.execute(text("ALTER TABLE messages ADD COLUMN message_type VARCHAR(50)"))
                    logger.info("Columna 'message_type' añadida a la tabla 'messages'")
                except ProgrammingError:
                    logger.info("La columna 'message_type' ya existe en la tabla 'messages'")

            # Crear tabla media_messages si no existe
            if not engine.dialect.has_table(connection, 'media_messages'):
                media_messages.create(engine)
                logger.info("Tabla 'media_messages' creada")
            else:
                logger.info("La tabla 'media_messages' ya existe")

            # Crear tabla interactive_messages si no existe
            if not engine.dialect.has_table(connection, 'interactive_messages'):
                interactive_messages.create(engine)
                logger.info("Tabla 'interactive_messages' creada")
            else:
                logger.info("La tabla 'interactive_messages' ya existe")

            # Crear tabla flow_states si no existe
            if not engine.dialect.has_table(connection, 'flow_states'):
                flow_states.create(engine)
                logger.info("Tabla 'flow_states' creada")
            else:
                logger.info("La tabla 'flow_states' ya existe")

            connection.commit()
        logger.info("Base de datos actualizada con éxito")

    except OperationalError as e:
        logger.error(f"Error operacional al actualizar la base de datos: {e}")
        raise
    except Exception as e:
        logger.error(f"Error inesperado al actualizar la base de datos: {e}")
        raise

if __name__ == "__main__":
    update_database()

