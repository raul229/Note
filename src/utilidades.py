import re

patron_celular=re.compile(r'\b9\d{8}\b')

patron_dni=re.compile(r'\b\d{8}\b')

patron_coordenadas=re.compile(r'[-+]?([1-8]?\d(\.\d+)?|90(\.0+)?)[ ,]+[-+]?(180(\.0+)?|((1[0-7]\d)|(\d{1,2}))(\.\d+)?)')


#extraemos palabras comunes del diccionario
with open("palabras.txt", "r", encoding="utf-8") as f:
    lista = [linea.strip() for linea in f if linea.strip()]
    f.close()
    
palabras_comunes = set(lista)

def reconoce_nombre(fila: str) -> str:
 
    palabras = fila.lower().split()
    # Casos base
    if not palabras or fila.strip().isdigit():
            
        return fila

    encabezados = {'nombre:', 'dni:', 'celular:', '####################', 'coordenadas:'}
    if palabras[0] in encabezados:
        return fila

    # Si todas las palabras no están en el conjunto común, se asume nombre
    es_nombre = all(p not in palabras_comunes for p in palabras)
    if es_nombre:
        return f'NOMBRE: {' '.join(palabras).upper()}'.rstrip()+'\n'
    
    return ' '.join(palabras).upper().rstrip()+'\n'



def reconoce_dni(texto):
    m=patron_dni.search(texto)
    
    return f'DNI: {m.group(0)}'.rstrip()+'\n' if m else texto

def reconoce_celular(texto):
    m = patron_celular.search(texto)
    return f'CELULAR: {m.group(0)}'.rstrip()+'\n' if m else texto

def reconoce_coordenadas(coordenadas):
    m=patron_coordenadas.search(coordenadas)
    
    return f'COORDENADAS: {m.group(0)}'.strip()+'\n' if m else coordenadas


def procesar_texto(lista_filas:list)->list:
    
    # Procesamos las líneas. Aquí el ejemplo reemplaza "######" por "---FIN---"
    nuevas = [re.sub(r'#+', '#' * 20, l).rstrip()+'\n' for l in lista_filas]
    
    #procesamos los numenos de celular 
    nuevas =[reconoce_celular(celular) for celular in nuevas]
    
    #procesamos numeros de dni                   
    nuevas=[reconoce_dni(dni) for dni in nuevas]
    
    #procesamos coordenadas
    nuevas=[reconoce_coordenadas(coordenadas) for coordenadas in nuevas]
    
    #procesamos nombres
    nuevas=[reconoce_nombre(nombre) for nombre in nuevas]
    
    return nuevas

