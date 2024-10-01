import pyautogui
import time
import pyperclip
import re
from PIL import Image
from chat_actions import ejecutar_acciones, extraer_chat
from ai import generar_respuesta 
from screen import capturar_area_chat, guardar_imagen, extraer_texto, comparar_imagenes


WHATSAPP_BTN_POS = (455, 1055)
WHATSAPP_ICON_POS = (-1810, 450)
WHATSAPP_LOAD_DELAY = 4
# Definición de coordenadas para interactuar con el campo de texto en WhatsApp
CAMPO_TEXTO_POS = (-800, 1260)
WINDOWS_SEARCH_DELAY = 0.5
SCREENSHOT_INTERVAL = 3

CHAT_RECTANGLE = (1088, 682, 1700, 1231)

def chat_whatsapp(texto_extraido):
    """
    Función principal que coordina la extracción del chat, generación de respuesta
    y la interacción con WhatsApp.
    """
    # Extraer el último bloque de chat sin respuesta
    ultimo_chat = extraer_chat(texto_extraido)
    
    if ultimo_chat:
        # Generar la respuesta estructurada
        respuesta_completa = generar_respuesta(ultimo_chat)
        print("Respuesta generada:######\n", respuesta_completa , "\n######")
        
        # Extraer la sección de "Respuesta:"
        match_respuesta = re.search(r'<Respuesta>(.*?)</Respuesta>', respuesta_completa, re.DOTALL)
        mensaje_respuesta = match_respuesta.group(1).strip() if match_respuesta else ""
    
        if mensaje_respuesta:
            # Interactuar con WhatsApp usando pyautogui para enviar la respuesta inicial
            interactuar_con_whatsapp(mensaje_respuesta)
            print("Mensaje enviado al usuario:###\n", mensaje_respuesta, "\n###")
        else:
            print("No se pudo extraer la respuesta del asistente.")
        
        # Ejecutar las acciones necesarias
        resultado_acciones = ejecutar_acciones(respuesta_completa)
        if resultado_acciones:
            # Añadir el resultado al mensaje para generar una nueva respuesta
            respuesta_nueva = respuesta_completa + "\n" + resultado_acciones
            # Generar una nueva respuesta considerando el resultado de las acciones
            respuesta_final = generar_respuesta(respuesta_nueva)
            print("Respuesta después de ejecutar acciones:######\n", respuesta_final , "\n######")
            
            # Extraer la sección de "Respuesta:"
            match_respuesta = re.search(r'<Respuesta>(.*?)</Respuesta>', respuesta_final, re.DOTALL)
            mensaje_respuesta = match_respuesta.group(1).strip() if match_respuesta else ""
    
            if mensaje_respuesta:
                # Interactuar con WhatsApp usando pyautogui para enviar la respuesta final
                interactuar_con_whatsapp(mensaje_respuesta)
                print("Mensaje enviado al usuario:###\n", mensaje_respuesta, "\n###")
            else:
                print("No se pudo extraer la respuesta del asistente después de ejecutar acciones.")
    else:
        print("No hay nuevos mensajes para responder.")
        
def interactuar_con_whatsapp(mensaje_respuesta):
    """
    Realiza las acciones en WhatsApp utilizando pyautogui.
    """
    # Copiar el mensaje al portapapeles
    pyperclip.copy("<Respuesta> " + mensaje_respuesta + " </Respuesta>")
    
    # Hacer clic en el campo de texto de WhatsApp
    pyautogui.click(*CAMPO_TEXTO_POS)
    time.sleep(0.5)
    
    # Seleccionar todo el texto y eliminarlo
    pyautogui.hotkey("ctrl", "a")
    pyautogui.press("backspace")
    
    # Pegar el mensaje desde el portapapeles
    pyautogui.hotkey("ctrl", "v")
    time.sleep(0.5)
    
    # Enviar el mensaje
    pyautogui.press("enter")

def iniciar_whatsapp():
    """
    Inicia la aplicación de WhatsApp y toma la primera captura de pantalla del área de chat.
    """
    global ejecutando
    ejecutando = True

    abrir_whatsapp()
    chat_whatsapp = capturar_area_chat( CHAT_RECTANGLE )
    guardar_imagen(chat_whatsapp, 'captura_anterior.png')

    texto = extraer_texto(chat_whatsapp)
    print("Mensaje obtenido:###\n", texto, "\n###")

    # Iniciar el bucle principal
    bucle_principal()

def abrir_whatsapp():
    """
    Realiza las acciones necesarias para abrir WhatsApp a través del menú de inicio.
    """
    pyautogui.click(*WHATSAPP_BTN_POS)
    time.sleep(WINDOWS_SEARCH_DELAY)
    pyautogui.typewrite('whatsapp')
    pyautogui.press('enter')
    time.sleep(WHATSAPP_LOAD_DELAY)
    pyautogui.click(*WHATSAPP_ICON_POS)
    

def bucle_principal():
    """
    Bucle principal que monitoriza los cambios en el área del chat de WhatsApp.
    Responde automáticamente a los nuevos mensajes utilizando OpenAI.
    """
    global ejecutando
    captura_anterior = Image.open('captura_anterior.png')

    while ejecutando:
        # Espera el intervalo antes de verificar la siguiente captura
        time.sleep(SCREENSHOT_INTERVAL)

        # Captura la nueva imagen del área de chat de WhatsApp
        nueva_captura = capturar_area_chat(
CHAT_RECTANGLE )

        # Compara la nueva captura con la anterior
        if comparar_imagenes(captura_anterior, nueva_captura):
            # Actualiza la captura anterior con la nueva captura
            guardar_imagen(nueva_captura, 'captura_anterior.png')
            captura_anterior = nueva_captura

            # Extrae el texto de la nueva captura
            texto_extraido = extraer_texto(nueva_captura)
            print(f"Nuevo mensaje recibido a las {time.strftime('%H:%M:%S')}:")
            print(texto_extraido)

            # Procesar el nuevo texto y responder utilizando la función chat_whatsapp
            chat_whatsapp(texto_extraido)

        #else:
            # No hay cambios en la conversación
            # print("No hay nuevos mensajes a las", time.strftime("%H:%M:%S"))