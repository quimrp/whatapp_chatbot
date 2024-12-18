import requests
import json
import logging

# Configurar logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

# URL del webhook (asegúrate de reemplazar esto con la URL correcta de tu aplicación)
WEBHOOK_URL = "https://chairman-spectrum-transportation-housing.trycloudflare.com/webhook?token=q5pejbvpm76yrmxo"  # Cambia esto si estás usando un túnel o una URL diferente

def simulate_whatsapp_message(phone_number: str, message: str):
    """
    Simula un mensaje de WhatsApp enviando una solicitud POST al webhook.
    """
    payload = {
        "entry": [{
            "changes": [{
                "value": {
                    "messages": [{
                        "from": phone_number,
                        "text": {
                            "body": message
                        },
                        "timestamp": "1234567890"
                    }]
                }
            }]
        }]
    }

    headers = {
        'Content-Type': 'application/json'
    }

    try:
        response = requests.post(WEBHOOK_URL, headers=headers, data=json.dumps(payload))
        response.raise_for_status()
        logger.info(f"Webhook response: {response.text}")
        return response.json()
    except requests.RequestException as e:
        logger.error(f"Error al enviar la solicitud al webhook: {str(e)}")
        if hasattr(e, 'response') and e.response is not None:
            logger.error(f"Contenido de la respuesta: {e.response.text}")
        return None

def main():
    # Simular un mensaje de WhatsApp
    phone_number = "34661878157"  # Reemplaza esto con un número de teléfono de prueba
    message = "Hola, esto es un mensaje de prueba para el webhook"

    result = simulate_whatsapp_message(phone_number, message)

    if result:
        logger.info(f"Respuesta del webhook: {json.dumps(result, indent=2)}")
    else:
        logger.error("No se pudo obtener una respuesta del webhook")

if __name__ == "__main__":
    main()

