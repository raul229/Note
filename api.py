from fastapi import FastAPI
from pydantic import BaseModel
from fastapi.middleware.cors import CORSMiddleware

from src import utilidades

app = FastAPI()

# Habilitar CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # o limita a ["http://127.0.0.1:5500"] por ejemplo
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class Nota(BaseModel):
    contenido:str

@app.post('/notas/')
def notas_view(nota: Nota):
    
    texto= nota.contenido
    
    texto=texto.split('\n')
    if not texto:
        return {'contenido': texto}
    
    lista_procesada = utilidades.procesar_texto(texto)
    
    procesado= ''.join(lista_procesada)
    
    print(procesado)
    return {'contenido': procesado}