from fastapi import FastAPI, Request, HTTPException, Depends
from sqlalchemy.orm import Session
from app.database.models import Message, InteractiveMessage, MultimediaMessage, Order, OrderItem, UserState
from app.database.connection import get_db
from app.services.alvochat_api import AlvoChatAPI
from app.config import settings
from app.flows import get_flow
import logging
from datetime import datetime
import json

# Definir palabras clave para los flujos
FLOW_KEYWORDS = {
    "simple": ["hola", "inicio", "empezar"],
    "support": ["ayuda", "soporte", "problema"],
    "product": ["producto", "comprar", "catálogo"],
    "product_catalog": ["catálogo", "productos", "ver productos"]
}

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

            # Save the base message to the database
            new_message = Message(
                wamid=message_data.get("id"),
                waba_id=message_data.get("waba_id"),
                phone_number_id=message_data.get("phone_number_id"),
                from_number=sender,
                to=message_data.get("to"),
                pushname=message_data.get("pushname"),
                type=message_type,
                body=message_body,
                time=str(timestamp),
                raw_data=json.dumps(message_data)
            )
            db.add(new_message)
            db.flush()

            # Handle different message types
            if message_type in ["button", "list", "template"]:
                interactive_message = InteractiveMessage(
                    message_id=new_message.id,
                    interactive_type=message_type,
                    content=json.dumps(message_data.get("interactive", {}))
                )
                db.add(interactive_message)
            elif message_type in ["image", "video", "audio", "document"]:
                multimedia_message = MultimediaMessage(
                    message_id=new_message.id,
                    media_type=message_type,
                    media_id=message_data.get("media", {}).get("id"),
                    media_url=message_data.get("media", {}).get("url")
                )
                db.add(multimedia_message)
            elif message_type == "order":
                order_data = message_data.get("order", {})
                total_price = sum(item.get("item_price", 0) * item.get("quantity", 0) for item in order_data.get("product_items", []))
                new_order = Order(
                    message_id=new_message.id,
                    catalog_id=order_data.get("catalog_id"),
                    status="recibido",
                    total_price=total_price,
                    order_time=timestamp
                )
                db.add(new_order)
                db.flush()

                for index, item in enumerate(order_data.get("product_items", []), start=1):
                    order_item = OrderItem(
                        order_id=new_order.id,
                        product_retailer_id=item.get("product_retailer_id"),
                        catalog_id=order_data.get("catalog_id"),
                        item_id=item.get("product_id"),
                        quantity=item.get("quantity"),
                        item_price=item.get("item_price"),
                        currency=item.get("currency"),
                        item_order=index
                    )
                    db.add(order_item)

            db.commit()

            # Process the message through the conversation flow
            user_state = db.query(UserState).filter(UserState.user_id == sender).first()
            if not user_state:
                user_state = UserState(user_id=sender, current_flow=None, current_node=None)
                db.add(user_state)
                db.commit()

            # Check if the message contains a keyword to trigger a flow
            triggered_flow = None
            for flow, keywords in FLOW_KEYWORDS.items():
                if any(keyword in message_body.lower() for keyword in keywords):
                    triggered_flow = flow
                    break

            if triggered_flow:
                user_state.current_flow = triggered_flow
                user_state.current_node = "start"
                db.commit()

                current_flow = get_flow(user_state.current_flow)
                if not current_flow:
                    logger.error(f"Invalid flow: {user_state.current_flow}")
                    raise HTTPException(status_code=400, detail="Invalid flow")

                current_node = current_flow.get_node(user_state.current_node)
                response_content = current_node.to_alvochat_format()
            else:
                # If no keyword is found, just echo the message
                response_content = {
                    "type": "text",
                    "text": f"Has dicho: {message_body}"
                }

            # Send the response using the AlvoChatAPI
            send_result = alvochat_api.send_message(sender, response_content)
            
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

if __name__ == "__main__":
    import uvicorn
    logger.info("Starting FastAPI application")
    uvicorn.run(app, host="0.0.0.0", port=8000, log_level="debug")

