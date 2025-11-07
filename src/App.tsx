import { useState } from 'react'

function App() {
  const [contenido, setContenido] = useState('')

  const enviarNota = async () => {
    try {
      const respuesta = await fetch('http:localhost:8000/notas/', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ contenido }),
      })
      const data = await respuesta.json()
      setContenido(data.contenido || contenido)
    } catch (error) {
      console.error('Error al enviar la nota:', error)
    }
  }

  return (
    <div className="container">
      <h3 className="mb-3">Probar API Bloc de Notas</h3>
      <textarea
        className="form-control mb-3"
        rows={20}
        placeholder="Escribe algo aquí..."
        value={contenido}
        onChange={(e) => setContenido(e.target.value)}
      />
      <button onClick={enviarNota} className="btn btn-primary">
        Enviar
      </button>
    </div>
  )
}

export default App
