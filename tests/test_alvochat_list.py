import requests
import json
import logging

# Configurar logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

url = "https://api.alvochat.com/instance4109/messages/list"

payload = {
    "token": "etsxm8w7vpxw2dc3",
    "to": 34661878157,
    "header": {
        "type": "text",
        "text": "Catálogo de Productos"
    },
    "body": '<img src="https://alvochat-example.s3-accelerate.amazonaws.com/image/1.jpeg">',
    "footer": "Selecciona un producto para ver más detalles",
    "button": "Ver productos",
    "sections": [
        {
            "title": "Productos disponibles",
            "rows": [
                {
                    "id": "1",
                    "title": "Camiseta",
                    "description": "Camiseta de algodón 100%"
                },
                {
                    "id": "2",
                    "title": "Pantalón",
                    "description": "Pantalón vaquero clásico"
                },
                {
                    "id": "3",
                    "title": "Zapatos",
                    "description": "Zapatos deportivos cómodos"
                }
            ]
        }
    ],
    "priority": "",
    "message_id": ""
}

headers = {
    'Content-Type': 'application/json'
}

def send_list_message():
    try:
        response = requests.post(url, headers=headers, data=json.dumps(payload))
        response.raise_for_status()
        logger.info(f"Mensaje enviado exitosamente. Respuesta: {response.text}")
        return response.json()
    except requests.RequestException as e:
        logger.error(f"Error al enviar el mensaje: {str(e)}")
        if e.response is not None:
            logger.error(f"Contenido de la respuesta: {e.response.content}")
        return None

if __name__ == "__main__":
    logger.info("Iniciando envío de mensaje de lista con imagen en el cuerpo...")
    result = send_list_message()
    if result:
        logger.info("Mensaje de lista con imagen en el cuerpo enviado correctamente.")
    else:
        logger.error("No se pudo enviar el mensaje de lista con imagen en el cuerpo.")

