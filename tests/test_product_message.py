import logging
from app.whatsapp_handler import WhatsAppHandler
from app.config import settings

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

def test_send_product_message():
    handler = WhatsAppHandler()

    # Test data
    to = settings.TEST_PHONE_NUMBER  # Use the test phone number from settings
    body = "Check out our new product!"
    catalog_id = "5848405878587482"  # Replace with your actual catalog ID
    product_id = "5,6"  # Replace with your actual product ID(s)
    header = "New Product Announcement"
    footer = "Limited time offer"

    logger.info("Sending product message...")
    try:
        response = handler.send_product_message(to, body, catalog_id, product_id, header, footer)
        logger.info(f"Product message sent successfully. Response: {response}")
    except Exception as e:
        logger.error(f"Failed to send product message: {str(e)}")

    # Log the API URL and token being used (without revealing the full token)
    logger.info(f"Using API URL: {settings.ALVOCHAT_API_URL}")
    token = settings.ALVOCHAT_TOKEN
    logger.info(f"Using token: {token[:5]}...{token[-5:]}")

if __name__ == "__main__":
    test_send_product_message()



