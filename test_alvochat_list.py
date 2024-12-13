import requests
import json

url = "https://api.alvochat.com/instance4109/messages/list"

payload = {
    "token": "etsxm8w7vpxw2dc3",
    "to": 34661878157,
    "header": {
        "type": "text",
        "text": "Catálogo de Productos"
    },
    "body": "Selecciona un producto:",
    "footer": "Selecciona un producto para ver más detalles",
    "button": "Ver productos",
    "sections": [
        {
            "title": "Catálogo de productos",
            "rows": [
                {
                    "id": "1",
                    "title": "Producto 1",
                    "description": "Descripción del Producto 1",
                    "image": {
                        "url": "https://alvochat-example.s3-accelerate.amazonaws.com/image/1.jpeg"
                    }
                },
                {
                    "id": "2",
                    "title": "Producto 2",
                    "description": "Descripción del Producto 2",
                    "image": {
                        "url": "https://alvochat-example.s3-accelerate.amazonaws.com/image/2.jpeg"
                    }
                },
                {
                    "id": "3",
                    "title": "Producto 3",
                    "description": "Descripción del Producto 3",
                    "image": {
                        "url": "https://alvochat-example.s3-accelerate.amazonaws.com/image/3.jpeg"
                    }
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

response = requests.request("POST", url, headers=headers, data=json.dumps(payload))

print(response.text)