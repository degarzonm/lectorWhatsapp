import pyautogui
import pytesseract
from PIL import ImageChops, Image, ImageEnhance

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

def mejorar_imagen(imagen):
    """
    Mejora la imagen ajustando el contraste y brillo para mejorar el OCR.
    """
    enhancer = ImageEnhance.Contrast(imagen)
    imagen = enhancer.enhance(2)
    enhancer = ImageEnhance.Brightness(imagen)
    imagen = enhancer.enhance(1.5)
    return imagen

def extraer_texto(imagen):
    """
    Realiza OCR en la imagen para extraer el texto.
    """
    imagen = mejorar_imagen(imagen)
    return pytesseract.image_to_string(imagen, lang='spa')

def comparar_imagenes(imagen1, imagen2):
    """
    Compara dos imágenes y determina si son diferentes.
    """
    diff = ImageChops.difference(imagen1, imagen2)
    return diff.getbbox() is not None