import sys
import os
import logging
from datetime import datetime
from sqlalchemy import inspect, text
from sqlalchemy.orm import Session

# Añadir el directorio raíz del proyecto al path de Python
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from app.database import engine, SessionLocal, Message, FlowState, MediaMessage, InteractiveMessage

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def verify_table_existence(inspector, table_name):
    if inspector.has_table(table_name):
        logger.info(f"La tabla '{table_name}' existe en la base de datos.")
        columns = inspector.get_columns(table_name)
        logger.info(f"Columnas de la tabla '{table_name}':")
        for column in columns:
            logger.info(f"  - {column['name']} ({column['type']})")
    else:
        logger.error(f"La tabla '{table_name}' no existe en la base de datos.")

def insert_test_data(session):
    # Insertar mensaje de texto de prueba
    test_message = Message(sender="123456789", content="Hola, este es un mensaje de prueba", message_type="text")
    session.add(test_message)
    session.flush()
    
    # Insertar mensaje de media de prueba
    test_media_message = MediaMessage(message_id=test_message.id, media_type="image", media_url="https://example.com/image.jpg")
    session.add(test_media_message)
    
    # Insertar mensaje interactivo de prueba
    test_interactive_message = InteractiveMessage(
        message_id=test_message.id,
        interactive_type="button",
        content={"type": "button", "body": {"text": "Elige una opción"}, "action": {"buttons": [{"type": "reply", "reply": {"id": "1", "title": "Opción 1"}}]}}
    )
    session.add(test_interactive_message)
    
    # Insertar estado de flujo de prueba
    test_flow_state = FlowState(user_id="123456789", current_flow="welcome", current_node="start")
    session.add(test_flow_state)
    
    session.commit()
    logger.info("Datos de prueba insertados correctamente.")

def query_test_data(session):
    # Consultar mensajes
    messages = session.query(Message).all()
    logger.info("Mensajes en la base de datos:")
    for message in messages:
        logger.info(f"  - Sender: {message.sender}, Content: {message.content}, Type: {message.message_type}, Timestamp: {message.timestamp}")
    
    # Consultar mensajes de media
    media_messages = session.query(MediaMessage).all()
    logger.info("Mensajes de media en la base de datos:")
    for media in media_messages:
        logger.info(f"  - Message ID: {media.message_id}, Type: {media.media_type}, URL: {media.media_url}")
    
    # Consultar mensajes interactivos
    interactive_messages = session.query(InteractiveMessage).all()
    logger.info("Mensajes interactivos en la base de datos:")
    for interactive in interactive_messages:
        logger.info(f"  - Message ID: {interactive.message_id}, Type: {interactive.interactive_type}, Content: {interactive.content}")
    
    # Consultar estados de flujo
    flow_states = session.query(FlowState).all()
    logger.info("Estados de flujo en la base de datos:")
    for state in flow_states:
        logger.info(f"  - User ID: {state.user_id}, Current Flow: {state.current_flow}, Current Node: {state.current_node}")

def main():
    logger.info("Iniciando verificación de la base de datos actualizada...")
    
    inspector = inspect(engine)
    
    # Verificar existencia de tablas
    verify_table_existence(inspector, "messages")
    verify_table_existence(inspector, "media_messages")
    verify_table_existence(inspector, "interactive_messages")
    verify_table_existence(inspector, "flow_states")
    
    # Crear una sesión
    session = SessionLocal()
    
    try:
        # Insertar datos de prueba
        insert_test_data(session)
        
        # Consultar datos de prueba
        query_test_data(session)
        
    except Exception as e:
        logger.error(f"Error durante la verificación de la base de datos: {e}")
    finally:
        session.close()
    
    logger.info("Verificación de la base de datos actualizada completada.")

if __name__ == "__main__":
    main()


