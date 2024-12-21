import logging

from config import settings
import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from services.alvochat_api import AlvoChatAPI


# Configurar logging
logging.basicConfig(level=logging.DEBUG, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

def test_send_message():
    api = AlvoChatAPI()
    test_number = settings.TEST_PHONE_NUMBER  # Asegúrate de tener este valor en tu archivo de configuración
    test_message = "Este es un mensaje de prueba enviado desde el bot de WhatsApp."

    logger.info(f"Intentando enviar mensaje de prueba a {test_number}")
    try:
        result = api.send_message(test_number, test_message)
        logger.info(f"Mensaje enviado exitosamente. Respuesta: {result}")
    except Exception as e:
        logger.error(f"Error al enviar el mensaje: {str(e)}")

    # Imprimir información de depuración
    logger.debug(f"URL de la API: {settings.ALVOCHAT_API_URL}")
    logger.debug(f"ID de la instancia: {settings.ALVOCHAT_INSTANCE_ID}")
    # No imprimas el token completo por razones de seguridad
    logger.debug(f"Token (primeros 5 caracteres): {settings.ALVOCHAT_TOKEN[:5]}...")

if __name__ == "__main__":
    test_send_message()

