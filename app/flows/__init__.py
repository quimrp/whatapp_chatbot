from .window_quote_flow import window_quote_flow
from app.database.models import WindowQuote, Window

conversation_flows = {
    "window_quote": window_quote_flow
}

def get_flow(name: str):
    return conversation_flows.get(name)

def get_all_flows():
    return list(conversation_flows.values())

__all__ = ['window_quote_flow', 'WindowQuote', 'Window', 'get_flow', 'get_all_flows']

