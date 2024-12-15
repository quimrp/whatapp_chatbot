from .reservations import reservation_flow

conversation_flows = {
    "reservations": reservation_flow
}

def get_flow(name: str):
    return conversation_flows.get(name)

