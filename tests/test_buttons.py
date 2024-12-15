import sys
import os
import logging
import json
from app.whatsapp_handler import WhatsAppHandler
from app.config import ALVOCHAT_TOKEN, ALVOCHAT_API_URL

# Add the project root directory to Python path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

# Configure logger
logging.basicConfig(level=logging.DEBUG, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

def test_contact_message():
    # Create an instance of WhatsAppHandler
    handler = WhatsAppHandler()

    # Test phone number (replace with a real number)
    test_number = "34661878157"  # Replace this with your test phone number

    # Contact message test
    logger.info("Sending contact message...")
    contact_data = json.dumps({
        "addresses": [
            {
                "street": "123 Main St",
                "city": "Anytown",
                "state": "CA",
                "zip": "12345",
                "country": "United States",
                "country_code": "US",
                "type": "HOME"
            }
        ],
        "birthday": "1990-01-01",
        "emails": [
            {
                "email": "john.doe@example.com",
                "type": "WORK"
            }
        ],
        "name": {
            "formatted_name": "John Doe",
            "first_name": "John",
            "last_name": "Doe",
            "middle_name": "",
            "suffix": "",
            "prefix": ""
        },
        "org": {
            "company": "Acme Inc.",
            "department": "Sales",
            "title": "Manager"
        },
        "phones": [
            {
                "phone": "+1234567890",
                "type": "CELL",
                "wa_id": "1234567890"
            }
        ],
        "urls": [
            {
                "url": "https://www.example.com",
                "type": "WORK"
            }
        ]
    })

    try:
        response = handler.send_contact_message(test_number, contact_data)
        if response:
            logger.info(f"Contact message sent successfully. Response: {response}")
        else:
            logger.error("Failed to send contact message")
    except Exception as e:
        logger.error(f"Error sending contact message: {str(e)}")

    # Log the API URL and token being used (without revealing the full token)
    logger.info(f"Using API URL: {ALVOCHAT_API_URL}")
    logger.info(f"Using token: {ALVOCHAT_TOKEN[:5]}...{ALVOCHAT_TOKEN[-5:]}")

if __name__ == "__main__":
    test_contact_message()

