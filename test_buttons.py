import sys
import os
import logging
from app.whatsapp_handler import WhatsAppHandler
from app.config import ALVOCHAT_TOKEN, ALVOCHAT_API_URL

# Add the project root directory to Python path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

# Configure logger
logging.basicConfig(level=logging.DEBUG, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

def test_button_message():
    # Create an instance of WhatsAppHandler
    handler = WhatsAppHandler()

    # Test phone number (replace with a real number)
    test_number = "34661878157"  # Replace this with your test phone number

    # Button message test
    logger.info("Sending button message...")
    body = "elige la opcion que quieres"
    buttons = ["Pvc", "aluminio", "aluminio-madera"]
    header = "perfil"
    footer = "selecciona tu preferencia"

    try:
        response = handler.send_button_message(test_number, body, buttons, header, footer)
        if response:
            logger.info(f"Button message sent successfully. Response: {response}")
        else:
            logger.error("Failed to send button message")
    except Exception as e:
        logger.error(f"Error sending button message: {str(e)}")

    # Log the API URL and token being used (without revealing the full token)
    logger.info(f"Using API URL: {ALVOCHAT_API_URL}")
    logger.info(f"Using token: {ALVOCHAT_TOKEN[:5]}...{ALVOCHAT_TOKEN[-5:]}")

if __name__ == "__main__":
    test_button_message()

