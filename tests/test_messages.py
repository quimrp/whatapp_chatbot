import sys
import os
import logging
from app.whatsapp_handler import WhatsAppHandler
from app.config import settings

# Add the project root directory to Python path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

# Configure logger
logging.basicConfig(level=logging.DEBUG, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

def test_messages():
    # Create an instance of WhatsAppHandler
    handler = WhatsAppHandler()

    # Test phone number (replace with a real number)
    test_number = "34661878157"  # Replace this with your test phone number

    # Send text message
    logger.info("Sending text message...")
    text_response = handler.send_text_message(test_number, "This is a test text message")
    logger.info(f"Text message response: {text_response}")

    # Send image message
    logger.info("Sending image message...")
    image_response = handler.send_image_message(test_number, "https://alvochat-example.s3-accelerate.amazonaws.com/image/1.jpeg", "This is a test image")
    logger.info(f"Image message response: {image_response}")

    # Send audio message
    logger.info("Sending audio message...")
    audio_response = handler.send_audio_message(test_number, "https://alvochat-example.s3-accelerate.amazonaws.com/audio/1.mp3")
    logger.info(f"Audio message response: {audio_response}")

    # Send video message
    logger.info("Sending video message...")
    video_response = handler.send_video_message(test_number, "https://www.sample-videos.com/video321/mp4/720/big_buck_bunny_720p_5mb.mp4", "This is a test video")
    logger.info(f"Video message response: {video_response}")

    # Send document message
    logger.info("Sending document message...")
    document_response = handler.send_document_message(test_number, "https://www.w3.org/WAI/ER/tests/xhtml/testfiles/resources/pdf/dummy.pdf", "test_document.pdf", "This is a test document")
    logger.info(f"Document message response: {document_response}")

    # Send sticker message
    logger.info("Sending sticker message...")
    sticker_response = handler.send_sticker_message(test_number, "https://alvochat-example.s3-accelerate.amazonaws.com/sticker/1.webp")
    logger.info(f"Sticker message response: {sticker_response}")

    # Send button message
    logger.info("Sending button message...")
    body = "Please select one of the following options"
    buttons = ["Option 1", "Option 2", "Option 3"]
    header = "Test Header"
    footer = "Test Footer"
    try:
        button_response = handler.send_button_message(test_number, body, buttons, header, footer)
        if button_response:
            logger.info(f"Button message sent successfully. Response: {button_response}")
        else:
            logger.error("Failed to send button message")
    except Exception as e:
        logger.error(f"Error sending button message: {str(e)}")

    # Send list message
    logger.info("Sending list message...")
    list_body = "Please select an item from the list"
    list_button = "View List"
    list_sections = [
        {
            "title": "List of 10 Items",
            "rows": [
                {"id": "1", "title": "Item 1", "description": "Description of Item 1"},
                {"id": "2", "title": "Item 2", "description": "Description of Item 2"},
                {"id": "3", "title": "Item 3", "description": "Description of Item 3"},
                {"id": "4", "title": "Item 4", "description": "Description of Item 4"},
                {"id": "5", "title": "Item 5", "description": "Description of Item 5"},
                {"id": "6", "title": "Item 6", "description": "Description of Item 6"},
                {"id": "7", "title": "Item 7", "description": "Description of Item 7"},
                {"id": "8", "title": "Item 8", "description": "Description of Item 8"},
                {"id": "9", "title": "Item 9", "description": "Description of Item 9"},
                {"id": "10", "title": "Item 10", "description": "Description of Item 10"}
            ]
        }
    ]
    list_header = "Test List Header"
    list_footer = "Test List Footer"
    try:
        list_response = handler.send_list_message(test_number, list_body, list_button, list_sections, list_header, list_footer)
        if list_response:
            logger.info(f"List message sent successfully. Response: {list_response}")
        else:
            logger.error("Failed to send list message")
    except Exception as e:
        logger.error(f"Error sending list message: {str(e)}")

    # Log the API URL and token being used (without revealing the full token)
    logger.info(f"Using API URL: {ALVOCHAT_API_URL}")
    logger.info(f"Using token: {ALVOCHAT_TOKEN[:5]}...{ALVOCHAT_TOKEN[-5:]}")

if __name__ == "__main__":
    test_messages()

