from fastapi import FastAPI, HTTPException, Depends, Request
from fastapi.responses import JSONResponse, PlainTextResponse
from sqlalchemy.orm import Session
from app.database import get_db, Message
from app.whatsapp_handler import WhatsAppHandler
from app.config import ALVOCHAT_TOKEN
from datetime import datetime
import logging
import json

app = FastAPI()
whatsapp_handler = WhatsAppHandler()

logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)

@app.get("/webhook")
async def verify_webhook(request: Request):
    mode = request.query_params.get("hub.mode")
    token = request.query_params.get("hub.verify_token")
    challenge = request.query_params.get("hub.challenge")

    if mode and token:
        if mode == "subscribe" and token == ALVOCHAT_TOKEN:
            logger.info("Webhook verified successfully")
            return PlainTextResponse(content=challenge)
        else:
            logger.warning("Webhook verification failed")
            raise HTTPException(status_code=403, detail="Verification failed")
    else:
        return JSONResponse(content={"message": "Webhook GET request received"})

@app.post("/webhook")
async def webhook(request: Request, db: Session = Depends(get_db)):
    logger.debug("Webhook POST request received")
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
            text = message.get("text", {}).get("body", "")
            timestamp = datetime.fromtimestamp(int(message.get("timestamp")))

            # Store the message in the database
            new_message = Message(sender=sender, content=text, timestamp=timestamp)
            db.add(new_message)
            db.commit()
            logger.debug(f"Message stored in database: {new_message}")

            # Process the message and generate a response
            response = whatsapp_handler.process_message(text)
            logger.debug(f"Generated response: {response}")

            # Send the response back via WhatsApp
            whatsapp_response = whatsapp_handler.send_message(sender, response)
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
    return {"message": "WhatsApp Chatbot is running"}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000, log_level="debug")

