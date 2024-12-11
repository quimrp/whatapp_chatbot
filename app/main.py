from fastapi import FastAPI, HTTPException, Depends, Request
from fastapi.responses import JSONResponse
from sqlalchemy.orm import Session
from app.database import get_db, Message
from app.whatsapp_handler import WhatsAppHandler
from app.config import ALVOCHAT_TOKEN, ALVOCHAT_WEBHOOK_URL
from datetime import datetime
import logging
import json

app = FastAPI()
whatsapp_handler = WhatsAppHandler()

logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)

@app.get("/webhook")
async def verify_webhook(request: Request):
    logger.debug("Webhook GET request received for verification")
    mode = request.query_params.get("hub.mode")
    token = request.query_params.get("hub.verify_token")
    challenge = request.query_params.get("hub.challenge")

    if mode and token:
        if mode == "subscribe" and token == ALVOCHAT_TOKEN:
            logger.info(f"Webhook verified successfully. URL: {ALVOCHAT_WEBHOOK_URL}")
            return int(challenge)
        else:
            logger.warning("Webhook verification failed")
            raise HTTPException(status_code=403, detail="Verification failed")
    
    raise HTTPException(status_code=400, detail="Missing parameters")

@app.post("/webhook")
async def webhook(request: Request, db: Session = Depends(get_db)):
    logger.debug(f"Webhook POST request received at URL: {ALVOCHAT_WEBHOOK_URL}")
    try:
        body = await request.json()
        logger.info(f"Received webhook data: {json.dumps(body, indent=2)}")

        # Extract the message from the WhatsApp data structure
        entry = body.get("entry", [{}])[0]
        changes = entry.get("changes", [{}])[0]
        value = changes.get("value", {})
        messages = value.get("messages", [])

        if not messages:
            logger.info("No messages in the webhook payload")
            return JSONResponse(content={"status": "success", "message": "No messages to process"})

        for message in messages:
            sender = message.get("from")
            timestamp = datetime.fromtimestamp(int(message.get("timestamp")))

            # Process the message and generate a response
            response = whatsapp_handler.process_message(db, sender, message)
            logger.debug(f"Generated response: {response}")

            # Send the response back via WhatsApp
            whatsapp_response = whatsapp_handler.send_text_message(sender, response)
            if not whatsapp_response:
                logger.error("Error sending response message via WhatsApp")
            else:
                logger.debug("Response sent successfully")

        return JSONResponse(content={"status": "success", "message": "Messages processed successfully"})
    except Exception as e:
        logger.error(f"Error in webhook: {str(e)}", exc_info=True)
        return JSONResponse(status_code=500, content={"status": "error", "message": "Internal server error"})

@app.get("/")
async def root():
    logger.debug("Root endpoint accessed")
    return {"message": "WhatsApp Chatbot is running", "webhook_url": ALVOCHAT_WEBHOOK_URL}

if __name__ == "__main__":
    import uvicorn
    logger.info(f"Starting server with webhook URL: {ALVOCHAT_WEBHOOK_URL}")
    uvicorn.run(app, host="0.0.0.0", port=8000, log_level="debug")

