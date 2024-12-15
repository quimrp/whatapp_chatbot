from fastapi import FastAPI, Request, HTTPException, Depends
from sqlalchemy.orm import Session
from app.database.models import Message
from app.database.connection import get_db
from app.services.alvochat_api import AlvoChatAPI
from app.config import settings
import logging
from datetime import datetime

app = FastAPI()
alvochat_api = AlvoChatAPI()

logging.basicConfig(level=logging.DEBUG, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

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
        logger.info(f"Received webhook data: {data}")
        
        if data.get("event_type") == "message_received" and "data" in data:
            message_data = data["data"]
            sender = message_data.get("from")
            message_body = message_data.get("body", "")
            message_type = message_data.get("type", "unknown")
            timestamp = datetime.fromtimestamp(int(message_data.get("time", 0)))

            logger.info(f"Processing {message_type} message from {sender}: {message_body}")

            # Save the message to the database
            new_message = Message(
                sender=sender,
                content=message_body,
                message_type=message_type,
                timestamp=timestamp
            )
            db.add(new_message)
            db.commit()

            # Generate and send response
            response_message = f"Has dicho: {message_body}"
            send_result = alvochat_api.send_message(sender, response_message)
            
            if send_result:
                logger.info(f"Response sent to {sender}. Result: {send_result}")
                return {"status": "success", "message": "Message processed and response sent"}
            else:
                logger.error(f"Failed to send response to {sender}")
                raise HTTPException(status_code=500, detail="Failed to send response")
        else:
            logger.info("No valid message data in the webhook payload")
            return {"status": "success", "message": "No valid message data to process"}
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



