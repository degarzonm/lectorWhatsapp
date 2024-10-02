# Contenido del archivo: chat_actions.py
import re
import time
from database import (chatsql, guardar_mensaje, mensaje_ya_procesado,
                      generar_nuevo_message_id)

def extraer_ultimo_mensaje_usuario(texto_extraido):
    """
    Extracts the last unprocessed user message, including multi-line messages.
    It identifies new messages based on the first 20 characters and the time elapsed.
    Only the text after the 'Chat' prefix is considered.
    """
    lines = texto_extraido.strip().splitlines()
    mensaje_usuario = ''
    collected_lines = []

    # Start from the end and find the last 'Chat' line
    for idx in range(len(lines) - 1, -1, -1):
        line = lines[idx].strip()
        if not line:
            continue
        if line.startswith('Chat'):
            # Found the last 'Chat', start collecting
            # Remove 'Chat' prefix and collect the line
            collected_lines.append(line[len('Chat'):].strip())
            # Now collect any following lines until we hit 'Respuesta' or 'Chat'
            for j in range(idx + 1, len(lines)):
                next_line = lines[j].strip()
                if next_line.startswith('Respuesta') or next_line.startswith('Chat'):
                    break
                collected_lines.append(next_line)
            break  # We have collected the last message
    if collected_lines:
        mensaje_usuario = '\n'.join(collected_lines)
        mensaje_preview = mensaje_usuario[:20]
        timestamp_actual = time.time()
        if not mensaje_ya_procesado(mensaje_preview, timestamp_actual):
            # Generate a new message_id
            message_id = generar_nuevo_message_id()
            guardar_mensaje(message_id, timestamp_actual, mensaje_usuario, 'user')
            return message_id, mensaje_usuario
        else:
            print("El mensaje ya ha sido procesado recientemente.")
    else:
        print("No se encontró un nuevo mensaje del usuario.")
    return None, None

def ejecutar_acciones(respuesta):
    """Extrae y ejecuta las acciones dentro de la etiqueta <Acciones>."""
    acciones = re.findall(r'<Acciones>(.*?)</Acciones>', respuesta, re.DOTALL)
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
