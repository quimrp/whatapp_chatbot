from typing import Dict, Any, Optional, Callable, List, Union

class ConversationNode:
    def __init__(self, node_type: str, content: Union[Dict[str, Any], List[Dict[str, Any]]]):
        self.node_type = node_type
        self.content = content
        self.jumps = []

    def to_alvochat_format(self) -> Union[Dict[str, Any], List[Dict[str, Any]]]:
        return self.content

    def get_next_node(self, user_response: str) -> Optional[str]:
        for jump in self.jumps:
            if jump["condition"](user_response):
                return jump["target"]
        return None

class FlowBuilder:
    def __init__(self, name: str, keywords: List[str]):
        self.name = name
        self.keywords = keywords
        self.nodes = {}
        self.current_node = None

    def add_node(self, node_name: str, node_type: str, content: Union[Dict[str, Any], List[Dict[str, Any]]]) -> 'FlowBuilder':
        self.nodes[node_name] = ConversationNode(node_type, content)
        self.current_node = node_name
        return self

    def add_text_node(self, node_name: str, text: str) -> 'FlowBuilder':
        return self.add_node(node_name, "text", {"text": text})

    def add_image_node(self, node_name: str, prompt: str) -> 'FlowBuilder':
        return self.add_node(node_name, "image", {"prompt": prompt})

    def add_interactive_button_node(self, node_name: str, text: str, buttons: List[Dict[str, str]]) -> 'FlowBuilder':
        return self.add_node(node_name, "interactive", {
            "type": "button",
            "body": {"text": text},
            "action": {"buttons": buttons}
        })

    def add_interactive_list_node(self, node_name: str, text: str, button_text: str, sections: List[Dict[str, Any]]) -> 'FlowBuilder':
        return self.add_node(node_name, "interactive", {
            "type": "list",
            "body": {"text": text},
            "action": {
                "button": button_text,
                "sections": sections
            }
        })

    def add_multi_message_node(self, node_name: str, messages: List[Dict[str, Any]]) -> 'FlowBuilder':
        return self.add_node(node_name, "multi_message", messages)

    def add_jump(self, source: str, target: str, condition: Callable[[str], bool] = lambda _: True) -> 'FlowBuilder':
        if source not in self.nodes:
            raise ValueError(f"Source node '{source}' does not exist")
        if target not in self.nodes:
            raise ValueError(f"Target node '{target}' does not exist")
        
        self.nodes[source].jumps.append({"target": target, "condition": condition})
        return self

    def build(self) -> 'ConversationFlow':
        if "start" not in self.nodes:
            raise ValueError("Flow must have a 'start' node.")
        return ConversationFlow(self.name, self.keywords, self.nodes)

class ConversationFlow:
    def __init__(self, name: str, keywords: List[str], nodes: Dict[str, ConversationNode]):
        self.name = name
        self.keywords = keywords
        self.nodes = nodes

    def get_node(self, node_id: str) -> Optional[ConversationNode]:
        return self.nodes.get(node_id)

    def process_message(self, current_node: str, message_data: Dict[str, Any], context: Dict[str, Any]) -> tuple[Optional[str], Union[str, List[Dict[str, Any]]]]:
        node = self.get_node(current_node)
        if not node:
            return None, "Lo siento, no puedo procesar tu mensaje en este momento."
        
        next_node = node.get_next_node(message_data.get("body", ""))
        
        if node.node_type == "multi_message":
            return next_node, node.content
        elif node.node_type == "interactive":
            return next_node, node.content
        else:
            response = node.content.get("text", "")
            if node.node_type == "interactive":
                response = node.content.get("body", {}).get("text", "")
        
        return next_node, response

