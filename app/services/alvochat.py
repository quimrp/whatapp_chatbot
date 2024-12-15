import requests
import logging
from ..config import settings

logger = logging.getLogger(__name__)

class AlvoChatService:
    def __init__(self):
        self.base_url = settings.ALVOCHAT_API_URL
        self.token = settings.ALVOCHAT_TOKEN

    def send_message(self, to: str, message: str) -> dict:
        url = f"{self.base_url}/send"
        payload = {
            "token": self.token,
            "to": to,
            "body": message
        }
        headers = {
            "Content-Type": "application/json",
            "User-Agent": "WhatsAppBot/1.0",
            "bypass-tunnel-reminder": "true"
        }

        try:
            response = requests.post(url, json=payload, headers=headers, verify=False)
            response.raise_for_status()
            return response.json()
        except requests.RequestException as e:
            logger.error(f"Error sending message: {str(e)}")
            return None

