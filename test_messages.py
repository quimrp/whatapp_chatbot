import sys
import os
import logging
from sqlalchemy.orm import Session
from app.database import SessionLocal, engine, Base
from app.whatsapp_handler import WhatsAppHandler

# Add the project root directory to Python path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

# Configure logger
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

def test_messages():
    # Create an instance of WhatsAppHandler
    handler = WhatsAppHandler()

    # Create a database session
    db = SessionLocal()

    try:
        # Test phone number (replace with a real number)
        test_number = "34661878157"

        # Send text message
        logger.info("Sending text message...")
        handler.send_text_message(test_number, "This is a test text message")

        # Send image message
        logger.info("Sending image message...")
        handler.send_image_message(test_number, "https://alvochat-example.s3-accelerate.amazonaws.com/image/1.jpeg", "This is a test image")

        # Send audio message
        logger.info("Sending audio message...")
        handler.send_audio_message(test_number, "https://codeskulptor-demos.commondatastorage.googleapis.com/pang/paza-moduless.mp3")

        # Send video message
        logger.info("Sending video message...")
        handler.send_video_message(test_number, "https://www.sample-videos.com/video321/mp4/720/big_buck_bunny_720p_5mb.mp4", "This is a test video")

        # Send document message
        logger.info("Sending document message...")
        handler.send_document_message(test_number, "https://www.w3.org/WAI/ER/tests/xhtml/testfiles/resources/pdf/dummy.pdf", "test_document.pdf", "This is a test document")

        # Send sticker message
        logger.info("Sending sticker message...")
        handler.send_sticker_message(test_number, "https://alvochat-example.s3-accelerate.amazonaws.com/sticker/1.webp")

        # Send contact message
        logger.info("Sending contact message...")
        contact_data = {
            "addresses": [{"city": "Madrid", "country": "Spain"}],
            "name": {"first_name": "John", "last_name": "Doe"},
            "phones": [{"phone": "+34123456789", "type": "CELL"}]
        }
        handler.send_contact_message(test_number, json.dumps(contact_data))

        # Send location message
        logger.info("Sending location message...")
        handler.send_location_message(test_number, 40.4168, -3.7038, "Madrid", "Puerta del Sol, Madrid, Spain")

        # Send button message
        logger.info("Sending button message...")
        buttons = ["Option 1", "Option 2", "Option 3"]
        handler.send_button_message(test_number, "Please select an option:", buttons, "Test Header", "Test Footer")

        # Send list message
        logger.info("Sending list message...")
        sections = [
            {
                "title": "Section 1",
                "rows": [
                    {"id": "1", "title": "Option 1", "description": "Description of option 1"},
                    {"id": "2", "title": "Option 2", "description": "Description of option 2"}
                ]
            }
        ]
        handler.send_list_message(test_number, "Choose an option from the list:", "View options", sections, "List Header", "List Footer")

        # Send template message
        logger.info("Sending template message...")
        template_name = "hello_world"
        language = "en"
        handler.send_template_message(test_number, template_name, language)

        # Send product message
        logger.info("Sending product message...")
        catalog_id = "your_catalog_id"  # Replace with actual catalog ID
        product_id = "your_product_id"  # Replace with actual product ID
        handler.send_product_message(test_number, "Check out this product!", catalog_id, product_id, "Product Header", "Product Footer")

        # Mark message as read
        logger.info("Marking message as read...")
        message_id = "test_message_id"  # Replace with an actual message ID
        handler.mark_message_as_read(message_id)

        # Resend messages by status
        logger.info("Resending messages by status...")
        status = "failed"
        handler.resend_messages_by_status(status)

        logger.info("All test messages have been sent.")

    except Exception as e:
        logger.error(f"Error during tests: {e}")
    finally:
        db.close()

if __name__ == "__main__":
    test_messages()


