from app.flows.flow_builder import FlowBuilder

def create_window_quote_flow():
    return (FlowBuilder("window_quote", ["presupuesto", "ventana", "ventanas", "cotización", "cotizar"])
        .add_node("start", "multi_message", {
            "messages": [
                "Bienvenido al asistente de presupuestos de ventanas. Vamos a comenzar con la primera ventana.",
                "Por favor, proporciona una referencia para esta ventana (por ejemplo, 'Ventana Cocina')."
            ]
        })
        .add_text_node("ask_width", "Indica el ancho de la ventana en centímetros.")
        .add_text_node("ask_height", "Ahora, indica el alto de la ventana en centímetros.")
        .add_image_node("ask_image", "Si tienes una imagen de la ventana o del espacio, por favor envíala ahora. Si no tienes una imagen, escribe 'no tengo'.")
        .add_interactive_list_node("ask_color", "Selecciona el color de la ventana:", "Ver colores", [
            {
                "title": "Colores disponibles",
                "rows": [
                    {"id": "blanco", "title": "Blanco"},
                    {"id": "negro", "title": "Negro"},
                    {"id": "gris", "title": "Gris"},
                    {"id": "madera", "title": "Efecto madera"}
                ]
            }
        ])
        .add_interactive_button_node("ask_blind", "¿La ventana incluye persiana?", [
            {"type": "reply", "reply": {"id": "si_persiana", "title": "Sí"}},
            {"type": "reply", "reply": {"id": "no_persiana", "title": "No"}}
        ])
        .add_interactive_button_node("ask_motor", "¿Deseas que la persiana sea motorizada?", [
            {"type": "reply", "reply": {"id": "si_motor", "title": "Sí"}},
            {"type": "reply", "reply": {"id": "no_motor", "title": "No"}}
        ])
        .add_interactive_list_node("ask_opening", "Selecciona el tipo de apertura:", "Ver opciones", [
            {
                "title": "Tipos de apertura",
                "rows": [
                    {"id": "batiente", "title": "Batiente"},
                    {"id": "corredera", "title": "Corredera"},
                    {"id": "oscilobatiente", "title": "Oscilobatiente"},
                    {"id": "fija", "title": "Fija"}
                ]
            }
        ])
        .add_interactive_button_node("ask_another", "¿Deseas añadir otra ventana al presupuesto?", [
            {"type": "reply", "reply": {"id": "si_otra", "title": "Sí, añadir otra"}},
            {"type": "reply", "reply": {"id": "no_otra", "title": "No, finalizar presupuesto"}}
        ])
        .add_text_node("end", "Gracias por utilizar nuestro asistente de presupuestos. En breve recibirás un resumen detallado por email y nos pondremos en contacto contigo.")

        # Definir los saltos entre nodos
        .add_jump("start", "ask_width")
        .add_jump("ask_width", "ask_height")
        .add_jump("ask_height", "ask_image")
        .add_jump("ask_image", "ask_color")
        .add_jump("ask_color", "ask_blind")
        .add_jump("ask_blind", "ask_motor", lambda response: response.get("interactive", {}).get("button_reply", {}).get("id") == "si_persiana")
        .add_jump("ask_blind", "ask_opening", lambda response: response.get("interactive", {}).get("button_reply", {}).get("id") == "no_persiana")
        .add_jump("ask_motor", "ask_opening")
        .add_jump("ask_opening", "ask_another")
        .add_jump("ask_another", "start", lambda response: response.get("interactive", {}).get("button_reply", {}).get("id") == "si_otra")
        .add_jump("ask_another", "end", lambda response: response.get("interactive", {}).get("button_reply", {}).get("id") == "no_otra")

        # Agregar saltos para manejar respuestas inesperadas
        .add_jump("ask_width", "ask_width", lambda response: not response.get("body", "").isdigit(), "Por favor, ingresa solo números para el ancho.")
        .add_jump("ask_height", "ask_height", lambda response: not response.get("body", "").isdigit(), "Por favor, ingresa solo números para el alto.")
        .add_jump("ask_image", "ask_image", lambda response: response.get("body", "").lower() not in ["no tengo"] and response.get("type") != "image", "Por favor, envía una imagen o escribe 'no tengo'.")

        .build()
    )

window_quote_flow = create_window_quote_flow()