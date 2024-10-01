from screeninfo import get_monitors
import pyautogui
import pytesseract
from PIL import ImageChops, Image

def capturar_area_chat(rect):
    """
    Realiza una captura de pantalla y recorta el área del chat de WhatsApp.
    """
    captura_completa = pyautogui.screenshot(allScreens=True)
    return captura_completa.crop(rect)

def guardar_imagen(imagen, nombre_archivo):
    """
    Guarda una imagen con el nombre especificado.
    """
    imagen.save(nombre_archivo)

def extraer_texto(imagen):
    """
    Realiza OCR en la imagen para extraer el texto.
    """
    return pytesseract.image_to_string(imagen, lang='spa')

def comparar_imagenes(imagen1, imagen2):
    """
    Compara dos imágenes y determina si son diferentes.
    """
    return bool(ImageChops.difference(imagen1, imagen2).getbbox())
    
    
