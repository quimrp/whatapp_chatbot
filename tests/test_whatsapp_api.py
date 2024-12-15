import requests
import os
from dotenv import load_dotenv
import logging

# Set up logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

# Load environment variables
load_dotenv()

# WhatsApp Business API credentials
PHONE_NUMBER_ID = os.getenv('PHONE_NUMBER_ID')
ACCESS_TOKEN = os.getenv('WHATSAPP_ACCESS_TOKEN')

# API endpoint
API_URL = f"https://graph.facebook.com/v17.0/{PHONE_NUMBER_ID}/messages"

def send_whatsapp_message(to_phone_number, message_text):
    headers = {
        'Authorization': f'Bearer {ACCESS_TOKEN}',
        'Content-Type': 'application/json'
    }

    payload = {
        "messaging_product": "whatsapp",
        "recipient_type": "individual",
        "to": to_phone_number,
        "type": "text",
        "text": {
            "body": message_text
        }
    }

    try:
        response = requests.post(API_URL, headers=headers, json=payload)
        response.raise_for_status()
        logger.info(f"Message sent successfully: {response.json()}")
        return response.json()
    except requests.RequestException as e:
        logger.error(f"Error sending message: {e}")
        if hasattr(e, 'response') and e.response is not None:
            logger.error(f"Response content: {e.response.text}")
        return None

if __name__ == "__main__":
    # Replace with the recipient's phone number (including country code)
    to_phone_number = "34661878157"
    message_text = "Hello! This is a test message from the WhatsApp Business API."

    result = send_whatsapp_message(to_phone_number, message_text)
    
    if result:
        logger.info("Test completed successfully.")
    else:
        logger.error("Test failed.")

