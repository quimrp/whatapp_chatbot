import requests
import json
import logging
from app.config import ALVOCHAT_TOKEN, ALVOCHAT_API_URL

logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)

class WhatsAppHandler:
    def __init__(self):
        self.token = ALVOCHAT_TOKEN
        self.api_url = ALVOCHAT_API_URL
        logger.info(f"WhatsAppHandler initialized with API URL: {self.api_url}")

    def send_message(self, to: str, message: str):
        url = f"{self.api_url}/messages/chat"
        
        payload = json.dumps({
            "token": self.token,
            "to": int(to),
            "body": message,
            "priority": "",
            "preview_url": "",
            "message_id": ""
        })
        
        headers = {
            'Content-Type': 'application/json'
        }

        logger.info(f"Attempting to send message to {to}")
        try:
            response = requests.post(url, headers=headers, data=payload, timeout=10)
            response.raise_for_status()
            logger.info(f"Full response from AlvoChat: {response.text}")
            return response.json()
        except requests.RequestException as e:
            logger.error(f"Error sending message via AlvoChat: {e}")
            logger.error(f"Response content: {e.response.content if e.response else 'No response'}")
            return None
        except json.JSONDecodeError as e:
            logger.error(f"Error decoding JSON response: {e}")
            return None
        except Exception as e:
            logger.error(f"Unexpected error sending message: {e}")
            return None

    def process_message(self, message: str) -> str:
        # Here you can implement your chatbot logic
        # For now, we'll just echo the message
        return f"has escrito: {message}"

