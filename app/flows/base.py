from typing import Dict, List, Optional

class ConversationNode:
    def __init__(self, message: str, options: Optional[List[str]] = None):
        self.message = message
        self.options = options or []

class ConversationFlow:
    def __init__(self, name: str, nodes: Dict[str, ConversationNode]):
        self.name = name
        self.nodes = nodes
        self.start_node = "start"

    def get_node(self, node_name: str) -> ConversationNode:
        return self.nodes.get(node_name, self.nodes[self.start_node])

