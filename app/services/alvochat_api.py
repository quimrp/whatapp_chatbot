import requests
import urllib3
import urllib.parse
from app.config import settings
import logging
import json

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

logger = logging.getLogger(__name__)

class AlvoChatAPI:
    def __init__(self):
        self.base_url = settings.ALVOCHAT_API_URL
        self.token = settings.ALVOCHAT_TOKEN
        self.instance_id = settings.ALVOCHAT_INSTANCE_ID
        logger.info(f"AlvoChatAPI initialized with URL: {self.base_url}, Instance ID: {self.instance_id}")

    def _build_url(self, endpoint):
        return f"{self.base_url.rstrip('/')}/{endpoint}"

    def send_message(self, to: str, message: str, priority: str = "", preview_url: str = "", message_id: str = ""):
        url = self._build_url("messages/chat")
        logger.debug(f"Sending message to URL: {url}")
        payload = f"token={self.token}&to={to}&body={message}&priority={priority}&preview_url={preview_url}&message_id={message_id}"
        payload = payload.encode('utf8').decode('iso-8859-1')
        headers = {'content-type': 'application/x-www-form-urlencoded'}
        try:
            response = requests.post(url, data=payload, headers=headers, verify=False)
            response.raise_for_status()
            logger.info(f"Message sent successfully to {to}")
            return response.json()
        except requests.RequestException as e:
            logger.error(f"Error sending message to {to}: {str(e)}")
            raise

    def send_image_message(self, to: str, image_url: str, caption: str = "", priority: str = "", message_id: str = ""):
        url = self._build_url("messages/image")
        logger.debug(f"Sending image message to URL: {url}")
        payload = f"token={self.token}&to={to}&image={image_url}&caption={caption}&priority={priority}&message_id={message_id}"
        payload = payload.encode('utf8').decode('iso-8859-1')
        headers = {'content-type': 'application/x-www-form-urlencoded'}
        try:
            response = requests.post(url, data=payload, headers=headers, verify=False)
            response.raise_for_status()
            logger.info(f"Image message sent successfully to {to}")
            return response.json()
        except requests.RequestException as e:
            logger.error(f"Error sending image message to {to}: {str(e)}")
            raise

    def send_button_message(self, to: str, body: str, buttons: list, header: str = "", footer: str = "", priority: str = "", message_id: str = ""):
        url = self._build_url("messages/button")
        payload = f"token={self.token}&to={to}&header={header}&body={body}&footer={footer}&priority={priority}&message_id={message_id}"
        for i, button in enumerate(buttons):
            payload += f"&buttons[{i}]={button}"
        payload = payload.encode('utf8').decode('iso-8859-1')
        headers = {'content-type': 'application/x-www-form-urlencoded'}
        try:
            response = requests.post(url, data=payload, headers=headers, verify=False)
            response.raise_for_status()
            logger.info(f"Button message sent successfully to {to}")
            return response.json()
        except requests.RequestException as e:
            logger.error(f"Error sending button message to {to}: {str(e)}")
            raise

    def send_list_message(self, to: str, body: str, button: str, sections: list, header: str = "", footer: str = "", priority: str = "", message_id: str = ""):
        url = self._build_url("messages/list")
        logger.debug(f"Sending list message to URL: {url}")

        payload = {
            "token": self.token,
            "to": to,
            "body": body,
            "button": button,
            "sections": json.dumps(sections)
        }

        if header:
            payload["header"] = header
        if footer:
            payload["footer"] = footer
        if priority:
            payload["priority"] = priority
        if message_id:
            payload["message_id"] = message_id

        encoded_payload = urllib.parse.urlencode(payload)
        encoded_payload = encoded_payload.encode('utf8').decode('iso-8859-1')
        headers = {'content-type': 'application/x-www-form-urlencoded'}

        logger.debug(f"Sending list message with payload: {encoded_payload}")

        try:
            response = requests.post(url, data=encoded_payload, headers=headers, verify=False)
            response.raise_for_status()
            logger.info(f"List message sent successfully to {to}")
            logger.debug(f"Response from AlvoChat API: {response.text}")
            return response.json()
        except requests.RequestException as e:
            logger.error(f"Error sending list message to {to}: {str(e)}")
            logger.error(f"Response content: {e.response.content if e.response else 'No response'}")
            raise

    def send_multiple_messages(self, to: str, messages: list):
        results = []
        for message in messages:
            if isinstance(message, dict):
                if message['type'] == 'image':
                    result = self.send_image_message(
                        to, 
                        message['content']['url'], 
                        caption=message['content'].get('caption', '')
                    )
                elif message['type'] == 'text':
                    result = self.send_message(to, message['content']['text'])
                elif message['type'] == 'button':
                    result = self.send_button_message(
                        to,
                        message['content']['body'],
                        message['content']['buttons'],
                        header=message['content'].get('header', ''),
                        footer=message['content'].get('footer', '')
                    )
                elif message['type'] == 'list':
                    result = self.send_list_message(
                        to,
                        message['content']['body'],
                        message['content']['button'],
                        message['content']['sections'],
                        header=message['content'].get('header', ''),
                        footer=message['content'].get('footer', '')
                    )
                else:
                    logger.warning(f"Unsupported message type: {message['type']}")
                    continue
            else:
                result = self.send_message(to, message)
            results.append(result)
            logger.info(f"Message of type {message['type'] if isinstance(message, dict) else 'text'} sent successfully")
        return results




