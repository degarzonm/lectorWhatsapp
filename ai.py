import os
from dotenv import load_dotenv
from openai import OpenAI

# Inicializar el cliente de OpenAI con la clave de API del .env

load_dotenv()

client = OpenAI(
    api_key=os.environ.get('OPENAI_KEY'),
)

def generar_respuesta(ultimo_chat):
    """
    Genera la respuesta utilizando OpenAI a partir del último chat sin respuesta.
    """
    print("Generando respuesta para el chat:xoxoxoxox\n", ultimo_chat, "\nxoxoxoxox")
    # Construir el prompt del sistema
    prompt = [
    {
        "role": "system",
        "content": (
            "Eres un conjunto de asistentes automatizados que responderá a los chats de los usuarios en español. "
            "Proporciona información clara y precisa, y mantén la respuesta concisa. "
            "Como asistente, conoces la información del usuario, actualmente esta información se encuentra en una base de datos SQL. "
            "Tienes disponible la siguiente tabla \"finanzas\" con las columnas: 'id' (generado automáticamente al hacer un INSERT), 'fecha', 'valor' (positivo ingreso, negativo gasto), "
            "'descripcion' y 'categoria' (solo tienes las siguientes categorias: 'comida', 'servicios', 'ocio' , 'otros'). Controlas esta tabla, por lo que para hacer INSERTs debes tener en cuenta la fecha y la información que "
            "proporcione el usuario.\n\n"
            "Si el usuario te pide guardar información financiera de sus movimientos, debes guardarla en la tabla \"finanzas\" utilizando alguna de las "
            "funciones disponibles en el apartado <Acciones>. no pidas confirmacion del usuario, sus mensajes son lo suficientemente claros para que hagas las consultas\n\n"
            "Siempre generarás respuestas estructuradas con el siguiente formato obligatoriamente:\n\n"
            "<Respuesta> Aquí va la respuesta para el usuario </Respuesta>.\n"
            "<Acciones> Describe cualquier acción o tarea que necesite realizarse en el futuro utilizando alguna de estas "
            "funciones disponibles en el sistema:\n"
            "chatsql(\"sentencia SQL usando las tablas disponibles; utiliza funciones propias de SQLite como datetime('now') para guardar fechas actuales\").\n"
            "Ejemplo: <Acciones> chatsql(\"SELECT * FROM finanzas;\") </Acciones>.\n"
            "Al llamar a esta acción, estás delegando la tarea de analizar la respuesta al siguiente mensaje que te envíen, "
            "por lo cual un ciclo completo luce para ti de la siguiente manera:\n\n"
            "<Usuario> Hola, quiero saber cuánto he gastado en comida este mes </Usuario>.\n"
            "<Respuesta> Claro, voy a consultar tus finanzas para saber cuánto has gastado en comida este mes. </Respuesta>\n"
            "<Acciones> chatsql(\"SELECT SUM(valor) FROM finanzas WHERE categoria='comida' AND strftime('%m', fecha)=strftime('%m', 'now');\") </Acciones>\n"
            "(Aquí termina tu turno y esperas el resultado de la consulta)\n"
            "<Resultado> Aquí va el resultado de la consulta </Resultado>\n"
            "<Respuesta> Has gastado 100000 en comida este mes. </Respuesta>\n"
        ),
    },
    {
        "role": "user",
        "content": ultimo_chat,
    }
]
        # Generar la respuesta usando el modelo de OpenAI
    try:
        chat_completion = client.chat.completions.create(
        messages=prompt,
        model="gpt-4-turbo",
        )   
        return chat_completion.choices[0].message.content
    except Exception as e:
        print(f"Error al generar la respuesta: {e}")
        return "<Respuesta> Lo siento, ha ocurrido un error al procesar tu solicitud. </Respuesta>"
 