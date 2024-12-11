import requests
import json

url = "http://localhost:8000/send-message"

payload = json.dumps({
    "to": "34661878157",  # Usa un número de ejemplo o reemplázalo con un número real para pruebas
    "message": "Este es un mensaje de prueba desde la API de quim"
})
headers = {
    'Content-Type': 'application/json'
}

response = requests.post(url, headers=headers, data=payload)

print(f"Código de estado: {response.status_code}")
print(f"Respuesta del servidor:")
print(json.dumps(response.json(), indent=2))