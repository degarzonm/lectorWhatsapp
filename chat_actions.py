import re
from database import chatsql


def extraer_chat(texto_extraido):
    """
    Extrae el último bloque de chat que no tiene respuesta de nuestro sistema.
    """
    # Buscar todas las ocurrencias de "Chat:" y posibles respuestas "Respuesta:"
    bloques_chat = re.findall(r'Chat(.*?)(?=Chat|$)', texto_extraido, re.DOTALL)
    bloques_respuesta = re.findall(r'<Respuesta>', texto_extraido)
    print("Bloques de chat:\n", bloques_chat)
    print("Bloques de respuesta:\n", bloques_respuesta)
    
    
    # Si hay bloques de chat pero menos respuestas, se considera el último bloque sin respuesta
    if len(bloques_chat) > len(bloques_respuesta):
        print("Bloque de chat sin respuesta:\n", bloques_chat[-1])
        return "<Chat>" + bloques_chat[-1].strip() + "</Chat>"
    return None



def ejecutar_acciones(chat_string):
    """Extrae y ejecuta las acciones dentro de la etiqueta <Acciones>."""
    acciones = re.findall(r'<Acciones>(.*?)</Acciones>', chat_string, re.DOTALL)
    resultados = ""
    for accion in acciones:
        accion = accion.strip()
        # Verificar si es una llamada a chatsql
        match = re.match(r"chatsql\((['\"])(.*?)\1\)", accion, re.DOTALL)
        if match:
            sql_statement = match.group(2)
            resultado = chatsql(sql_statement)
            resultados += f"<Resultado>{resultado}</Resultado>\n"
    return resultados

