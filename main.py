import keyboard
import threading
from wa_driver import iniciar_whatsapp
from database import inicializar_base_datos

# Variable global para controlar el estado del programa
ejecutando = False

def manejar_inicio():
    """
    Función para manejar el inicio del asistente de WhatsApp.
    """
    global ejecutando
    if not ejecutando:
        print("Se presionó Ctrl+i. Iniciando asistente de WhatsApp.")
        threading.Thread(target=iniciar_whatsapp).start()
    else:
        print("El asistente ya está en ejecución.")

def manejar_fin():
    """
    Función para manejar la finalización del asistente de WhatsApp.
    """
    global ejecutando
    if ejecutando:
        print("Se presionó Ctrl+o. Finalizando asistente de WhatsApp.")
        ejecutando = False
    else:
        print("El asistente no está en ejecución.")

def configurar_teclas_rapidas():
    """
    Configura las combinaciones de teclas para iniciar y detener el asistente de WhatsApp.
    """
    keyboard.add_hotkey('ctrl+i', manejar_inicio)
    keyboard.add_hotkey('ctrl+o', manejar_fin)
    print("Presione Ctrl+i para iniciar el asistente, Ctrl+o para finalizar.")

def main():
    inicializar_base_datos()
    configurar_teclas_rapidas()
    keyboard.wait()

if __name__ == '__main__':
    main()