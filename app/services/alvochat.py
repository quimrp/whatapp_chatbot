import requests
from app.config import settings
import logging

logger = logging.getLogger(__name__)

class AlvoChatAPI:
    def __init__(self):
        self.base_url = settings.ALVOCHAT_API_URL
        self.token = settings.ALVOCHAT_TOKEN
        self.instance_id = settings.ALVOCHAT_INSTANCE_ID
        logger.info(f"AlvoChatAPI initialized with URL: {self.base_url}")

    def send_message(self, to: str, message: str):
        url = f"{self.base_url}/messages"
        headers = {
            "Content-Type": "application/json",
            "Authorization": f"Bearer {self.token}"
        }
        payload = {
            "to": to,
            "type": "text",
            "text": {"body": message},
            "instanceId": self.instance_id
        }

        logger.debug(f"Sending message to {to}: {message}")
        try:
            response = requests.post(url, json=payload, headers=headers)
            response.raise_for_status()
            logger.info(f"Message sent successfully to {to}")
            return response.json()
        except requests.RequestException as e:
            logger.error(f"Error sending message to {to}: {str(e)}")
            raise

    def send_interactive_message(self, to: str, interactive_content: dict):
        url = f"{self.base_url}/messages"
        headers = {
            "Content-Type": "application/json",
            "Authorization": f"Bearer {self.token}"
        }
        payload = {
            "to": to,
            "type": "interactive",
            "interactive": interactive_content,
            "instanceId": self.instance_id
        }

        logger.debug(f"Sending interactive message to {to}: {interactive_content}")
        try:
            response = requests.post(url, json=payload, headers=headers)
            response.raise_for_status()
            logger.info(f"Interactive message sent successfully to {to}")
            return response.json()
        except requests.RequestException as e:
            logger.error(f"Error sending interactive message to {to}: {str(e)}")
            raise

