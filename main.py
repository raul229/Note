# Importamos las librerías necesarias
from watchdog.observers import Observer       # Permite observar cambios en archivos y carpetas
from watchdog.events import FileSystemEventHandler  # Clase base para manejar eventos de archivos
import time, os, re, spacy

patron_celular=re.compile(r'\b9\d{8}\b')

patron_dni=re.compile(r'\b\d{8}\b')

nlp = spacy.load('es_core_news_md', disable=["parser", "ner", "lemmatizer"])

def reconoce_nombre(texto):
    # texto = texto.strip()
    doc = nlp(texto.strip())
    # si spaCy no generó tokens válidos, salimos
    if len(doc) == 0:
        return texto.rstrip()+'\n'
    
    # Regla 1: todas las palabras son letras (sin números)
    solo_letras = all(re.match(r'^[A-Za-zÁÉÍÓÚáéíóúÜüÑñ]+$', token.text) for token in doc)

    # Regla 2: todas las palabras están capitalizadas o en mayúsculas
    mayusculas = all(token.text.istitle() or token.text.isupper() for token in doc)

    # Regla 3: la mayoría son sustantivos propios o desconocidos
    proporción_propios = sum(token.pos_ == "PROPN" for token in doc) / len(doc)
    
    if solo_letras and mayusculas and proporción_propios >= 0.5:
        return f'NOMBRE: {texto}'.rstrip()+'\n'

    return texto

def reconoce_dni(texto):
    m=patron_dni.search(texto)
    
    return f'DNI: {m.group(0)}'.rstrip()+'\n' if m else texto

def reconoce_celular(texto):
    m = patron_celular.search(texto)
    return f'CELULAR: {m.group(0)}'.rstrip()+'\n' if m else texto

# Definimos una clase que manejará los eventos de modificación de archivos
class MiHandler(FileSystemEventHandler):
    # El constructor recibe el nombre del archivo que queremos observar
    def __init__(self, archivo_objetivo):
        # Guardamos la ruta absoluta del archivo a observar
        self.archivo_objetivo = os.path.abspath(archivo_objetivo)
        # Guardamos el momento del último evento de modificación, para evitar repeticiones
        self.ultima_modificacion = 0

    # Método que se ejecuta automáticamente cuando el archivo es modificado
    def on_modified(self, event):
        # Verifica si el archivo modificado es exactamente el que estamos observando
        if os.path.abspath(event.src_path) == self.archivo_objetivo:
            ahora = time.time()  # Obtenemos el tiempo actual

            # Evita que el evento se dispare múltiples veces en menos de 0.5 segundos
            # (muchos editores generan varios eventos por un solo guardado)
            if ahora - self.ultima_modificacion < 0.5:
                return  # sale sin hacer nada si ya se procesó un evento reciente

            # Actualizamos el momento del último evento procesado
            self.ultima_modificacion = ahora

            # Esperamos 0.3 segundos para asegurarnos de que el editor terminó de escribir el archivo
            time.sleep(0.3)

            try:
                # Abrimos el archivo en modo lectura/escritura (r+)
                # encoding='utf-8' asegura que no falle con caracteres especiales
                with open(self.archivo_objetivo, 'r+', encoding='utf-8') as f:
                    # Leemos todas las líneas en una lista
                    lineas = f.readlines()
                    
                    print(lineas)
                                        
                
                    # Procesamos las líneas. Aquí el ejemplo reemplaza "######" por "---FIN---"
                    nuevas = [re.sub(r'#+', '#' * 20, l).rstrip()+'\n' for l in lineas]
                    #procesamos los numenos de celular 
                    nuevas =[reconoce_celular(celular) for celular in nuevas]
                    
                    nuevas=[reconoce_dni(dni) for dni in nuevas]
                    
                    nuevas=[reconoce_nombre(nombre) for nombre in nuevas]
                    
                    # Regresamos el cursor al inicio del archivo
                    f.seek(0)
                    
                    print(nuevas)
                    # Escribimos las líneas modificadas
                    f.writelines(nuevas)
                    # Eliminamos el contenido sobrante si las nuevas líneas son más cortas
                    f.truncate()

                    print("Archivo actualizado automáticamente.")

            # Si el archivo está en uso (por ejemplo, el editor aún lo está guardando)
            # capturamos el error para no detener el script
            except PermissionError:
                print("Archivo en uso, reintentando más tarde.")

            # Cualquier otro error inesperado se muestra en pantalla
            except Exception as e:
                print(f"Error: {e}")

# Bloque principal del script
if __name__ == "__main__":
    # Nombre o ruta del archivo a observar
    archivo = "nota.txt"

    # Obtenemos solo la carpeta donde está el archivo
    ruta = os.path.dirname(os.path.abspath(archivo))

    # Creamos el manejador de eventos para ese archivo
    handler = MiHandler(archivo)

    # Creamos el observador (el componente que vigila el sistema de archivos)
    observer = Observer()

    # Le decimos al observador que use nuestro handler para esa ruta
    observer.schedule(handler, ruta, recursive=False)

    # Iniciamos el observador
    observer.start()

    print(f"Observando cambios en {archivo}...")

    try:
        # Bucle infinito que mantiene el programa corriendo
        while True:
            time.sleep(1)  # Evita que consuma CPU innecesariamente
    except KeyboardInterrupt:
        # Si el usuario presiona Ctrl+C, detenemos el observador ordenadamente
        observer.stop()

    # Esperamos a que el observador termine completamente
    observer.join()
