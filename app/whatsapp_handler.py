import requests
import json
import logging
from datetime import datetime
from sqlalchemy.orm import Session
from app.config import ALVOCHAT_TOKEN, ALVOCHAT_API_URL
from app.database import Message, MediaMessage, InteractiveMessage
from typing import List, Dict, Any, Optional
import urllib3

# Disable SSL warnings (not recommended for production)
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)

class WhatsAppHandler:
    def __init__(self):
        self.token = ALVOCHAT_TOKEN
        self.api_url = ALVOCHAT_API_URL
        logger.info(f"WhatsAppHandler initialized with API URL: {self.api_url}")

    def _send_request(self, endpoint: str, payload: Dict[str, Any]) -> Optional[Dict[str, Any]]:
        url = f"{self.api_url}/messages/{endpoint}"
        headers = {
            'Content-Type': 'application/json',
            'User-Agent': 'WhatsAppBot/1.0',  # Custom User-Agent for serveo
            'bypass-tunnel-reminder': 'true'  # Additional header for serveo
        }
        payload["token"] = self.token

        logger.info(f"Sending {endpoint} message to {payload.get('to', 'Unknown')}")
        logger.debug(f"Full URL: {url}")
        logger.debug(f"Payload: {json.dumps(payload, indent=2)}")

        try:
            response = requests.post(url, headers=headers, json=payload, timeout=10, verify=False)
            response.raise_for_status()
            logger.info(f"Full response from AlvoChat: {response.text}")
            return response.json()
        except requests.RequestException as e:
            logger.error(f"Error sending {endpoint} message via AlvoChat: {e}")
            logger.error(f"Response content: {e.response.content if e.response else 'No response'}")
        except json.JSONDecodeError as e:
            logger.error(f"Error decoding JSON response: {e}")
        except Exception as e:
            logger.error(f"Unexpected error sending {endpoint} message: {e}")
        return None

    def send_text_message(self, to: str, message: str) -> Optional[Dict[str, Any]]:
        payload = {
            "to": int(to),
            "body": message,
        }
        return self._send_request("chat", payload)

    def send_image_message(self, to: str, image_url: str, caption: str = "") -> Optional[Dict[str, Any]]:
        payload = {
            "to": int(to),
            "image": image_url,
            "caption": caption,
        }
        return self._send_request("image", payload)

    def send_audio_message(self, to: str, audio_url: str) -> Optional[Dict[str, Any]]:
        payload = {
            "to": int(to),
            "audio": audio_url,
            "messaging_product": "whatsapp"
        }
        return self._send_request("audio", payload)

    def send_video_message(self, to: str, video_url: str, caption: str = "") -> Optional[Dict[str, Any]]:
        payload = {
            "to": int(to),
            "video": video_url,
            "caption": caption,
        }
        return self._send_request("video", payload)

    def send_document_message(self, to: str, document_url: str, filename: str = "", caption: str = "") -> Optional[Dict[str, Any]]:
        payload = {
            "to": int(to),
            "document": document_url,
            "filename": filename,
            "caption": caption,
        }
        return self._send_request("document", payload)

    def send_sticker_message(self, to: str, sticker_url: str) -> Optional[Dict[str, Any]]:
        payload = {
            "to": int(to),
            "sticker": sticker_url,
        }
        return self._send_request("sticker", payload)

    def send_contact_message(self, to: str, contact_data: str) -> Optional[Dict[str, Any]]:
        payload = {
            "to": int(to),
            "contact": contact_data,
            "priority": "",
            "message_id": ""
        }
        return self._send_request("contact", payload)

    def send_location_message(self, to: str, lat: float, lng: float, name: str = "", address: str = "") -> Optional[Dict[str, Any]]:
        payload = {
            "to": int(to),
            "lat": lat,
            "lng": lng,
            "name": name,
            "address": address,
        }
        return self._send_request("location", payload)

    def send_template_message(self, to: str, template_name: str, language: str, header: Dict[str, Any] = None, 
                              body: List[str] = None, buttons: List[Dict[str, Any]] = None) -> Optional[Dict[str, Any]]:
        payload = {
            "to": int(to),
            "name": template_name,
            "language": language,
        }
        if header:
            payload["header"] = header
        if body:
            payload["body"] = body
        if buttons:
            payload["buttons"] = buttons
        return self._send_request("template", payload)

    def send_list_message(self, to: str, body: str, button: str, sections: List[Dict[str, Any]], 
                          header: Optional[Dict[str, Any]] = None, footer: str = "") -> Optional[Dict[str, Any]]:
        payload = {
            "to": int(to),
            "body": body,
            "button": button,
            "sections": sections,
            "footer": footer,
        }
        if header:
            payload["header"] = header

        return self._send_request("list", payload)

    def send_button_message(self, to: str, body: str, buttons: List[str], header: str = "", footer: str = "") -> Optional[Dict[str, Any]]:
        payload = {
            "to": int(to),
            "body": body,
            "buttons": ",".join(buttons),
            "header": header,
            "footer": footer,
            "priority": "",
            "message_id": ""
        }
        return self._send_request("button", payload)

    def send_product_message(self, to: str, body: str, catalog_id: str, product_id: str, 
                             header: str = "", footer: str = "") -> Optional[Dict[str, Any]]:
        payload = {
            "to": int(to),
            "body": body,
            "catalog_id": catalog_id,
            "product": product_id,
        }
        if header:
            payload["header"] = header
        if footer:
            payload["footer"] = footer
        return self._send_request("product", payload)

    def mark_message_as_read(self, message_id: str) -> Optional[Dict[str, Any]]:
        payload = {
            "message_id": message_id,
        }
        return self._send_request("read", payload)

    def resend_messages_by_status(self, status: str) -> Optional[Dict[str, Any]]:
        payload = {
            "status": status,
        }
        return self._send_request("resendByStatus", payload)

    def process_message(self, db: Session, sender: str, message: dict) -> str:
        message_type = self.get_message_type(message)
        content = self.extract_message_content(message)

        new_message = Message(sender=sender, content=content, message_type=message_type)
        db.add(new_message)
        db.flush()

        if message_type in ['image', 'video', 'audio', 'document', 'sticker']:
            media_url = message[message_type]['url']
            media_message = MediaMessage(message_id=new_message.id, media_type=message_type, media_url=media_url)
            db.add(media_message)
        elif message_type in ['button', 'list', 'product']:
            interactive_content = message['interactive']
            interactive_message = InteractiveMessage(
                message_id=new_message.id,
                interactive_type=message_type,
                content=interactive_content
            )
            db.add(interactive_message)
        elif message_type == 'location':
            location_content = {
                'latitude': message['location']['latitude'],
                'longitude': message['location']['longitude'],
                'name': message['location'].get('name', ''),
                'address': message['location'].get('address', '')
            }
            new_message.content = json.dumps(location_content)
        elif message_type == 'contact':
            contact_content = message['contacts'][0]  # Assuming we're processing the first contact
            new_message.content = json.dumps(contact_content)

        db.commit()

        return self.generate_response(message_type, content)

    def get_message_type(self, message: dict) -> str:
        if 'text' in message:
            return 'text'
        elif 'image' in message:
            return 'image'
        elif 'video' in message:
            return 'video'
        elif 'audio' in message:
            return 'audio'
        elif 'document' in message:
            return 'document'
        elif 'sticker' in message:
            return 'sticker'
        elif 'contacts' in message:
            return 'contact'
        elif 'location' in message:
            return 'location'
        elif 'interactive' in message:
            return message['interactive']['type']
        elif 'product' in message:
            return 'product'
        else:
            return 'unknown'

    def extract_message_content(self, message: dict) -> str:
        message_type = self.get_message_type(message)
        if message_type == 'text':
            return message['text']['body']
        elif message_type in ['image', 'video', 'audio', 'document', 'sticker']:
            return f"[{message_type.capitalize()}]"
        elif message_type in ['button', 'list', 'product']:
            return json.dumps(message['interactive'])
        elif message_type == 'contact':
            return json.dumps(message['contacts'][0])
        elif message_type == 'location':
            return json.dumps(message['location'])
        else:
            return "[Unknown message type]"

    def generate_response(self, message_type: str, content: str) -> str:
        return f"Recibí tu mensaje de tipo {message_type}. Contenido: {content}"

logger.info("WhatsAppHandler module loaded successfully")






