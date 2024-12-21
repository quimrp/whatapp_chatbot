import requests
import urllib3
from app.config import settings
import logging
from urllib.parse import urlencode

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

logger = logging.getLogger(__name__)

class AlvoChatAPI:
    def __init__(self):
        self.base_url = settings.ALVOCHAT_API_URL
        self.token = settings.ALVOCHAT_TOKEN
        self.instance_id = settings.ALVOCHAT_INSTANCE_ID
        logger.info(f"AlvoChatAPI initialized with URL: {self.base_url}")

    def _build_url(self, endpoint):
        return f"{self.base_url}/{endpoint}"

    def send_message(self, to: str, message: str, priority: str = "", preview_url: str = "", message_id: str = ""):
        url = self._build_url("messages/chat")
        logger.info(f"Sending message using URL: {url}")
        
        payload = {
            "token": self.token,
            "to": to,
            "body": message,
            "priority": priority,
            "preview_url": preview_url,
            "message_id": message_id
        }
        
        encoded_payload = urlencode(payload).encode('utf8').decode('iso-8859-1')
        
        headers = {
            "Content-Type": "application/x-www-form-urlencoded"
        }

        logger.debug(f"Sending message to {to}: {message}")
        try:
            response = requests.post(url, data=encoded_payload, headers=headers, verify=False)
            response.raise_for_status()
            logger.info(f"Message sent successfully to {to}")
            return response.json()
        except requests.RequestException as e:
            logger.error(f"Error sending message to {to}: {str(e)}")
            raise

    def send_interactive_message(self, to: str, interactive_content: dict):
        # Note: This method may need to be updated based on AlvoChat's specific requirements for interactive messages
        logger.warning("send_interactive_message method may need to be updated to match AlvoChat's API requirements")
        url = self._build_url("messages/chat")
        logger.info(f"Sending interactive message using URL: {url}")
        payload = {
            "token": self.token,
            "to": to,
            "body": str(interactive_content)
        }
        headers = {
            "Content-Type": "application/json"
        }
        try:
            response = requests.post(url, json=payload, headers=headers, verify=False)
            response.raise_for_status()
            logger.info(f"Interactive message sent successfully to {to}")
            return response.json()
        except requests.RequestException as e:
            logger.error(f"Error sending interactive message to {to}: {str(e)}")
            raise

