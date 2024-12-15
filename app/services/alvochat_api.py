import requests
from app.config import settings
import logging

logger = logging.getLogger(__name__)

class AlvoChatAPI:
    def __init__(self):
        self.base_url = f"https://api.alvochat.com/{settings.ALVOCHAT_INSTANCE_ID}"
        self.token = settings.ALVOCHAT_TOKEN

    def send_message(self, to: str, message: str) -> dict:
        url = f"{self.base_url}/messages/chat"
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

    def resend_webhooks_by_status(self, status: str) -> dict:
        url = f"{self.base_url}/webhooks/resendByStatus"
        payload = f"token={self.token}&status={status}"
        headers = {'content-type': 'application/x-www-form-urlencoded'}

        try:
            response = requests.post(url, data=payload, headers=headers)
            response.raise_for_status()
            return response.json()
        except requests.RequestException as e:
            logger.error(f"Error resending webhooks: {str(e)}")
            return None

