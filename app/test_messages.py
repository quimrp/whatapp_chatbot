import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from app.whatsapp_handler import WhatsAppHandler
from app.config import settings

def test_whatsapp_handler_initialization():
    handler = WhatsAppHandler()
    assert handler.token == settings.ALVOCHAT_TOKEN
    assert handler.api_url == settings.ALVOCHAT_API_URL

if __name__ == "__main__":
    test_whatsapp_handler_initialization()
    print("Test completed successfully!")

