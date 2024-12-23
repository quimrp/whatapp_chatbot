import os
import sys
import logging
from dotenv import load_dotenv

# Añadir el directorio raíz del proyecto al path de Python
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from app.services.alvochat_api import AlvoChatAPI

# Configurar logging
logging.basicConfig(level=logging.DEBUG, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

# Cargar variables de entorno
load_dotenv()

def create_simple_list():
    return {
        "header": "Selección de color",
        "body": "Por favor, selecciona el color de la ventana:",
        "footer": "Elige el color que mejor se adapte a tus necesidades",
        "button": "Ver colores",
        "sections": [
            {
                "id": "1",
                "title": "option_1",
                "description": "option 1 description"
            },
            {
                "id": "2",
                "title": "option_2",
                "description": "option 2 description"
            }
        ]
    }

def test_send_direct_list():
    # Crear una instancia de AlvoChatAPI
    alvochat_api = AlvoChatAPI()

    # Crear la lista simple
    list_message = create_simple_list()

    # Obtener el número de teléfono de prueba
    to = os.getenv("TEST_PHONE_NUMBER")

    if not to:
        logger.error("No se ha proporcionado un número de teléfono de prueba en las variables de entorno.")
        return

    logger.info(f"Intentando enviar mensaje de lista a: {to}")
    logger.debug(f"Contenido del mensaje: {list_message}")

    try:
        # Enviar el mensaje de lista
        response = alvochat_api.send_list_message(
            to=to,
            body=list_message["body"],
            button=list_message["button"],
            sections=list_message["sections"],
            header=list_message["header"],
            footer=list_message["footer"]
        )
        logger.info(f"Mensaje de lista enviado exitosamente. Respuesta: {response}")
    except Exception as e:
        logger.error(f"Error al enviar el mensaje de lista: {str(e)}")

if __name__ == "__main__":
    test_send_direct_list()

