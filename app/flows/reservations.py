from .base import ConversationFlow, ConversationNode

reservation_flow = ConversationFlow(
    "reservations",
    {
        "start": ConversationNode(
            "Bienvenido al Asistente de Reservas. ¿En qué puedo ayudarte?",
            ["Reservar mesa", "Ver menú", "Contactar soporte"]
        ),
        "reservar_mesa": ConversationNode(
            "¿Para qué fecha te gustaría hacer la reserva?",
            ["Hoy", "Mañana", "Otro día"]
        ),
        "elegir_hora": ConversationNode(
            "¿A qué hora te gustaría reservar?",
            ["19:00", "20:00", "21:00", "Otra hora"]
        ),
        "confirmar_reserva": ConversationNode(
            "¿Quieres confirmar tu reserva?",
            ["Sí", "No"]
        ),
        "ver_menu": ConversationNode(
            "¿Qué sección del menú te gustaría ver?",
            ["Entradas", "Platos principales", "Postres"]
        ),
        "contactar_soporte": ConversationNode(
            "Por favor, proporciona tu número de teléfono y un representante te contactará pronto."
        ),
        "finalizar": ConversationNode(
            "Gracias por usar nuestro servicio. ¿Hay algo más en lo que pueda ayudarte?",
            ["Volver al inicio", "Finalizar"]
        )
    }
)

