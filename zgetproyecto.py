import os

def main():
    # Obtener el directorio actual
    directorio_actual = os.getcwd()

    # Obtener una lista de todos los archivos en el directorio actual
    archivos = os.listdir(directorio_actual)

    # Abrir el archivo de salida en modo escritura
    with open('z.txt', 'w', encoding='utf-8') as archivo_salida:
        # Iterar sobre cada archivo en el directorio
        for nombre_archivo in archivos:
            # Verificar si el archivo termina con '.js'
            if nombre_archivo.endswith('.py') and nombre_archivo != 'zgetproyecto.py':
                # Leer el contenido del archivo .js
                with open(nombre_archivo, 'r', encoding='utf-8') as archivo_js:
                    contenido = archivo_js.read()
                    # Escribir el nombre del archivo y su contenido en el archivo de salida
                    archivo_salida.write(f'// Contenido del archivo: {nombre_archivo}\n')
                    archivo_salida.write(contenido)
                    archivo_salida.write('\n\n')  # Agregar una línea en blanco entre archivos

if __name__ == '__main__':
    main()
