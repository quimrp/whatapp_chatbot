import requests
import json
import logging
from app.config import settings

logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)

def simulate_whatsapp_message(phone_number: str, message: str):
    payload = {
        "event_type": "message_received",
        "instanceId": "4120",
        "data": {
            "id": "wamid.HBgLMzQ2NjE4NzgxNTcVAgASGBQzQTg4NTVFMTU1RTYxMDBDQTI2NgA=",
            "waba_id": "162010303670319",
            "phone_number_id": "203800556139249",
            "from": phone_number,
            "to": "34611381517",
            "pushname": "INSTAL TANCAMENTS",
            "type": "text",
            "body": message,
            "media": {
                "id": "",
                "link": ""
            },
            "quotedMsg": {},
            "time": "1734176954"
        }
    }

    headers = {
        'Content-Type': 'application/json',
        'User-Agent': 'WhatsAppBot/1.0',
        'bypass-tunnel-reminder': 'true'
    }

    webhook_url = settings.ALVOCHAT_WEBHOOK_URL.rstrip('/')

    logger.info(f"Sending test message to webhook: {webhook_url}")
    logger.debug(f"Headers: {json.dumps(headers)}")
    logger.debug(f"Payload: {json.dumps(payload)}")

    try:
        response = requests.post(webhook_url, headers=headers, json=payload, verify=False)
        logger.debug(f"Response status code: {response.status_code}")
        logger.debug(f"Response content: {response.text}")
        response.raise_for_status()
        logger.info(f"Webhook response: {response.text}")
        return response.json()
    except requests.RequestException as e:
        logger.error(f"Error sending request to webhook: {str(e)}")
        if hasattr(e, 'response') and e.response is not None:
            logger.error(f"Status code: {e.response.status_code}")
            logger.error(f"Response content: {e.response.text}")
        return None

def main():
    message = "Test message for webhook"
    result = simulate_whatsapp_message(settings.TEST_PHONE_NUMBER, message)

    if result:
        logger.info(f"Webhook response: {json.dumps(result, indent=2)}")
    else:
        logger.error("Could not get a response from the webhook")

if __name__ == "__main__":
    main()

