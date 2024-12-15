import logging
from app.whatsapp_handler import WhatsAppHandler
from app.config import ALVOCHAT_TOKEN, ALVOCHAT_API_URL

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

def test_send_product_message():
    handler = WhatsAppHandler()

    # Test data
    to = "34661878157"  # Replace with the actual recipient's phone number
    body = "Check out our new product!"
    catalog_id = "5848405878587482"  # Replace with your actual catalog ID
    product_id = "5,6"  # Replace with your actual product ID(s)
    header = "New Product Announcement"
    footer = "Limited time offer"

    logger.info("Sending product message...")
    response = handler.send_product_message(to, body, catalog_id, product_id, header, footer)

    if response:
        logger.info(f"Product message sent successfully. Response: {response}")
    else:
        logger.error("Failed to send product message")

    # Log the API URL and token being used (without revealing the full token)
    logger.info(f"Using API URL: {ALVOCHAT_API_URL}")
    logger.info(f"Using token: {ALVOCHAT_TOKEN[:5]}...{ALVOCHAT_TOKEN[-5:]}")

if __name__ == "__main__":
    test_send_product_message()

