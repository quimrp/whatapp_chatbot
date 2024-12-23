from app.flows.flow_builder import FlowBuilder
from app.database.models import WindowQuote, Window
from sqlalchemy.orm import Session
from typing import Dict, Any, Optional, Union, List

def create_window_quote_flow():
    return (FlowBuilder("window_quote", ["presupuesto", "ventana", "ventanas", "cotización", "cotizar"])
        .add_multi_message_node("start", [
            {"type": "image", "content": {
                "url": "https://www.sevillanadepvc.es/wp-content/uploads/2023/08/ventanas-de-aluminio-a-medida.jpg",
                "caption": "Bienvenido al asistente de presupuestos de ventanas"
            }},
            {"type": "text", "content": {"text": "Bienvenido al asistente de presupuestos de ventanas. Vamos a comenzar con la primera ventana."}},
            {"type": "text", "content": {"text": "Por favor, proporciona una referencia para esta ventana (por ejemplo, 'Ventana Cocina')."}}
        ])
        .add_text_node("ask_width", "Indica el ancho de la ventana en centímetros.")
        .add_text_node("ask_height", "Ahora, indica el alto de la ventana en centímetros.")
        .add_text_node("ask_image", "Si tienes una imagen de la ventana o del espacio, por favor envíala ahora. Si no tienes una imagen, escribe 'no tengo'.")
        .add_interactive_list_node("ask_color", 
            {
                "header": {
                    "type": "text",
                    "text": "Selección de color"
                },
                "body": {
                    "text": "Por favor, selecciona el color de la ventana:"
                },
                "footer": {
                    "text": "Elige el color que mejor se adapte a tus necesidades"
                },
                "action": {
                    "button": "Ver colores",
                    "sections": [
                        {
                            "title": "Colores disponibles",
                            "rows": [
                                {"id": "1", "title": "Blanco", "description": "Color blanco clásico"},
                                {"id": "2", "title": "Negro", "description": "Color negro elegante"},
                                {"id": "3", "title": "Gris", "description": "Color gris moderno"},
                                {"id": "4", "title": "Madera", "description": "Efecto madera natural"}
                            ]
                        }
                    ]
                }
            }
        )
        .add_node("ask_blind", "button", {
            "header": "Opción de persiana",
            "body": "¿La ventana incluye persiana?",
            "footer": "Las persianas ofrecen privacidad y control de la luz",
            "action": {
                "buttons": [
                    {"id": "si", "title": "Sí"},
                    {"id": "no", "title": "No"}
                ]
            }
        })
        .add_node("ask_motor", "button", {
            "header": "Persiana motorizada",
            "body": "¿Deseas que la persiana sea motorizada?",
            "footer": "Las persianas motorizadas ofrecen comodidad y facilidad de uso",
            "action": {
                "buttons": [
                    {"id": "si", "title": "Sí"},
                    {"id": "no", "title": "No"}
                ]
            }
        })
        .add_interactive_list_node("ask_opening", 
            {
                "header": {
                    "type": "text",
                    "text": "Tipo de apertura"
                },
                "body": {
                    "text": "Selecciona el tipo de apertura para tu ventana:"
                },
                "footer": {
                    "text": "Cada tipo de apertura tiene sus ventajas"
                },
                "action": {
                    "button": "Ver opciones",
                    "sections": [
                        {
                            "title": "Tipos de apertura",
                            "rows": [
                                {"id": "batiente", "title": "Batiente", "description": "Se abre hacia adentro o afuera"},
                                {"id": "corredera", "title": "Corredera", "description": "Se desliza horizontalmente"},
                                {"id": "oscilobatiente", "title": "Oscilobatiente", "description": "Combina apertura batiente y abatible"},
                                {"id": "fija", "title": "Fija", "description": "No se abre, solo para iluminación"}
                            ]
                        }
                    ]
                }
            }
        )
        .add_node("ask_another", "button", {
            "header": "Añadir otra ventana",
            "body": "¿Deseas añadir otra ventana al presupuesto?",
            "footer": "Puedes añadir tantas ventanas como necesites",
            "action": {
                "buttons": [
                    {"id": "si", "title": "Sí, añadir otra"},
                    {"id": "no", "title": "No, finalizar presupuesto"}
                ]
            }
        })
        .add_text_node("end", "Gracias por utilizar nuestro asistente de presupuestos. En breve recibirás un resumen detallado por email y nos pondremos en contacto contigo.")

        # Definir los saltos entre nodos
        .add_jump("start", "ask_width")
        .add_jump("ask_width", "ask_height", lambda response: response.isdigit())
        .add_jump("ask_width", "ask_width", lambda response: not response.isdigit(), "Por favor, ingresa un número válido para el ancho de la ventana.")
        .add_jump("ask_height", "ask_image", lambda response: response.isdigit())
        .add_jump("ask_height", "ask_height", lambda response: not response.isdigit(), "Por favor, ingresa un número válido para el alto de la ventana.")
        .add_jump("ask_image", "ask_color")
        .add_jump("ask_color", "ask_blind")
        .add_jump("ask_blind", "ask_motor", lambda response: response == "Sí")
        .add_jump("ask_blind", "ask_opening", lambda response: response == "No")
        .add_jump("ask_motor", "ask_opening")
        .add_jump("ask_opening", "ask_another")
        .add_jump("ask_another", "ask_width", lambda response: response == "Sí, añadir otra")
        .add_jump("ask_another", "end", lambda response: response == "No, finalizar presupuesto")

        .build()
    )

window_quote_flow = create_window_quote_flow()

def save_window_quote(db: Session, user_id: str, window_data: dict):
    # Buscar una cotización existente o crear una nueva
    quote = db.query(WindowQuote).filter(WindowQuote.user_id == user_id, WindowQuote.status == "en_progreso").first()
    if not quote:
        quote = WindowQuote(user_id=user_id, status="en_progreso")
        db.add(quote)
        db.commit()
        db.refresh(quote)

    # Crear una nueva ventana y asociarla a la cotización
    window = Window(
        quote_id=quote.id,
        reference=window_data.get("reference"),
        width=float(window_data.get("width", 0)),
        height=float(window_data.get("height", 0)),
        color=window_data.get("color"),
        has_blind=window_data.get("has_blind"),
        motorized_blind=window_data.get("motorized_blind"),
        opening_type=window_data.get("opening_type"),
        image_url=window_data.get("image_url")
    )
    db.add(window)
    db.commit()
    db.refresh(window)

    return quote, window

def get_quote_summary(db: Session, user_id: str):
    quote = db.query(WindowQuote).filter(WindowQuote.user_id == user_id, WindowQuote.status == "en_progreso").first()
    if not quote:
        return "No se encontró ninguna cotización en progreso."

    windows = db.query(Window).filter(Window.quote_id == quote.id).all()
    summary = f"Resumen de tu cotización (ID: {quote.id}):\n\n"
    for i, window in enumerate(windows, 1):
        summary += f"Ventana {i}:\n"
        summary += f"- Referencia: {window.reference}\n"
        summary += f"- Dimensiones: {window.width}cm x {window.height}cm\n"
        summary += f"- Color: {window.color}\n"
        summary += f"- Persiana: {'Sí' if window.has_blind else 'No'}\n"
        if window.has_blind:
            summary += f"- Persiana motorizada: {'Sí' if window.motorized_blind else 'No'}\n"
        summary += f"- Tipo de apertura: {window.opening_type}\n"
        if window.image_url:
            summary += f"- Imagen: {window.image_url}\n"
        summary += "\n"

    return summary

