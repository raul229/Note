import debounce from 'just-debounce-it'
import { useState, useCallback } from 'react'

function App() {
  const [contenido, setContenido] = useState('')

  const enviarNota = async (nuevoContenido: string) => {
    try {
      const respuesta = await fetch('http://localhost:8000/notas/', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ contenido: nuevoContenido }),
      })

      const data = await respuesta.json()

      // evita loops
      if (data.contenido !== undefined && data.contenido !== "") {
        setContenido(data.contenido)
      }
    } catch (error) {
      console.error('Error al enviar la nota:', error)
    }
  }

  // debounce se crea una sola vez
  const consultaConDemora = useCallback(
    debounce((texto: string) => {
      enviarNota(texto)
    }, 1000),
    []
  )

  return (
    <div className="container">
      <h3 className="mb-3">Probar API Bloc de Notas</h3>
      <textarea
        className="form-control mb-3"
        rows={20}
        placeholder="Escribe algo aquí..."
        value={contenido}
        onChange={(e) => {
          const texto = e.target.value
          setContenido(texto)          // actualiza textarea
          consultaConDemora(texto)     // envía con debounce
        }}
      />
    </div>
  )
}

export default App
