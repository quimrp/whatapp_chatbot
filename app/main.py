from fastapi import FastAPI, Request, HTTPException, Depends
from sqlalchemy.orm import Session
from .database.models import Message, MediaMessage, QuotedMessage
from .database.connection import get_db
from .config import settings
import logging
import json

# Configure logging
logging.basicConfig(level=logging.DEBUG, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

app = FastAPI()

@app.post("/webhook")
async def webhook(request: Request, db: Session = Depends(get_db)):
    logger.info(f"Received webhook request to path: {request.url.path}")
    logger.info(f"Query parameters: {request.query_params}")
    
    # Check if the token is provided as a query parameter
    token = request.query_params.get("token")
    if not token or token.strip() != settings.WEBHOOK_TOKEN:
        logger.warning(f"Invalid or missing token: {token}")
        raise HTTPException(status_code=403, detail="Invalid token")

    try:
        data = await request.json()
        logger.info(f"Processed webhook data: {data}")
        
        if data.get("event_type") == "message_received" and "data" in data:
            message_data = data["data"]
            
            # Create base message
            new_message = Message(
                id=message_data.get("id"),
                waba_id=message_data.get("waba_id"),
                phone_number_id=message_data.get("phone_number_id"),
                from_number=message_data.get("from"),
                to=message_data.get("to"),
                pushname=message_data.get("pushname"),
                type=message_data.get("type"),
                body=message_data.get("body"),
                time=message_data.get("time"),
                raw_data=json.dumps(message_data)
            )
            db.add(new_message)
            db.flush()

            # Handle media if present
            if message_data.get("media"):
                media_message = MediaMessage(
                    message_id=new_message.id,
                    media_id=message_data["media"].get("id"),
                    link=message_data["media"].get("link")
                )
                db.add(media_message)

            # Handle quoted message if present
            if message_data.get("quotedMsg"):
                quoted_message = QuotedMessage(
                    message_id=new_message.id,
                    quoted_data=json.dumps(message_data["quotedMsg"])
                )
                db.add(quoted_message)

            db.commit()

            logger.info(f"Received {new_message.type} message from {new_message.from_number}: {new_message.body}")

            # Generate and send response
            response_message = f"Has dicho: {new_message.body}"
            # Here you would typically use your WhatsApp API to send the response
            # For now, we'll just log it
            logger.info(f"Response to be sent to {new_message.from_number}: {response_message}")

            return {"status": "success", "message": "Message processed and response prepared"}

        return {"status": "success", "message": "Webhook received and processed"}
    except Exception as e:
        logger.error(f"Error processing webhook: {str(e)}", exc_info=True)
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/")
async def root():
    logger.info("Root endpoint accessed")
    return {"message": "WhatsApp Chatbot is running"}

if __name__ == "__main__":
    import uvicorn
    logger.info("Starting FastAPI application")
    uvicorn.run(app, host="0.0.0.0", port=8001, log_level="debug")

