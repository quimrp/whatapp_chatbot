import requests
import json
import logging
from typing import List, Union

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

# AlvoChat API configuration
ALVOCHAT_TOKEN = "k8y7e5olgzbqp8yd"
ALVOCHAT_INSTANCE_ID = "instance4120"
ALVOCHAT_API_URL = f"https://api.alvochat.com/{ALVOCHAT_INSTANCE_ID}/messages/product"

def send_product_message(
    to: int,
    body: str,
    catalog_id: int,
    products: Union[str, List[str]],
    header: str = "",
    footer: str = ""
) -> dict:
    """
    Send a product message using the AlvoChat API.

    :param to: The recipient's phone number
    :param body: The message body
    :param catalog_id: The catalog ID
    :param products: A string or list of product IDs
    :param header: Optional header text
    :param footer: Optional footer text
    :return: The API response as a dictionary
    """
    if isinstance(products, list):
        products = ",".join(map(str, products))

    payload = {
        "token": ALVOCHAT_TOKEN,
        "to": 34661878157,
        "body": body,
        "catalog_id":882214900405830 ,
        "product": 5,
        "header": header,
        "footer": footer,
        "priority": "",
        "message_id": ""
    }

    headers = {
        'Content-Type': 'application/json'
    }

    try:
        logger.info(f"Sending product message to {to}")
        response = requests.post(ALVOCHAT_API_URL, headers=headers, data=json.dumps(payload))
        response.raise_for_status()
        logger.info("Product message sent successfully")
        return response.json()
    except requests.RequestException as e:
        logger.error(f"Error sending product message: {str(e)}")
        if hasattr(e, 'response') and e.response is not None:
            logger.error(f"Response content: {e.response.text}")
        return None

def main():
    # Test sending a product message
    recipient = 34661878157
    message_body = "hola este es tu producto"
    catalog_id = 882214900405830
    product_ids = ["5", "6"]
    header = "New Products"
    footer = "Limited time offer"

    result = send_product_message(
        to=recipient,
        body=message_body,
        catalog_id=catalog_id,
        products=product_ids,
        header=header,
        footer=footer
    )

    if result:
        logger.info(f"API Response: {json.dumps(result, indent=2)}")
    else:
        logger.error("Failed to send product message")

if __name__ == "__main__":
    main()

