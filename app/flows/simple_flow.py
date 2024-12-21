from .flow_builder import FlowBuilder

def create_simple_flow():
    return (FlowBuilder("simple")
        .add_node("start", "text", {
            "type": "text",
            "text": "Hola, bienvenido a nuestro servicio. ¿Cómo te llamas?"
        })
        .add_node("ask_preference", "interactive", {
            "type": "interactive",
            "interactive": {
                "type": "button",
                "body": {
                    "text": "Encantado de conocerte, {name}. ¿Prefieres hablar de música o de películas?"
                },
                "action": {
                    "buttons": [
                        {
                            "type": "reply",
                            "reply": {
                                "id": "music",
                                "title": "Música"
                            }
                        },
                        {
                            "type": "reply",
                            "reply": {
                                "id": "movies",
                                "title": "Películas"
                            }
                        }
                    ]
                }
            }
        })
        .add_node("music", "text", {
            "type": "text",
            "text": "¡Genial! La música es una forma maravillosa de expresión. ¿Cuál es tu género musical favorito?"
        })
        .add_node("movies", "text", {
            "type": "text",
            "text": "¡Excelente elección! El cine es un arte fascinante. ¿Cuál es tu película favorita?"
        })
        .add_node("end", "text", {
            "type": "text",
            "text": "Gracias por compartir eso conmigo. Ha sido un placer charlar contigo. ¿Hay algo más en lo que pueda ayudarte?"
        })
        .add_jump("start", "ask_preference")
        .add_jump("ask_preference", "music", condition=lambda response: response == "music")
        .add_jump("ask_preference", "movies", condition=lambda response: response == "movies")
        .add_jump("music", "end")
        .add_jump("movies", "end")
        .build()
    )

simple_flow = create_simple_flow()



simple_flow = create_simple_flow()

