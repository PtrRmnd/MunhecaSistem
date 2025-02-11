from Amigo import Amigo
from BaseDatos import BaseDatos
from typing import Optional
import os

def evaluar_interaccion(mensaje_usuario: str) -> tuple[int, Optional[str]]:
    """
    Evalúa si el usuario está cumpliendo con los objetivos del Nivel 1:
    - Saludos adecuados (2 puntos).
    - Preguntas abiertas bien formuladas (3 puntos, sin importar si llevan tilde o signos de interrogación).

    Args:
        mensaje_usuario (str): Mensaje del usuario.

    Returns:
        tuple[int, Optional[str]]: Puntos obtenidos y mensaje de feedback (si aplica).
    """
    saludos = ["hola", "buenos dias", "buenas tardes", "buenas noches", "que tal", "como estas"]
    preguntas_abiertas = ["que", "como", "por que", "donde", "cuando", "quien", "cual"]

    mensaje = mensaje_usuario.lower().strip()

    # Detectar saludos
    if any(saludo in mensaje for saludo in saludos):
        return 2, "¡Buen saludo! 😊"

    # Detectar preguntas abiertas sin depender de acentos o signos de interrogación
    if any(palabra in mensaje for palabra in preguntas_abiertas) and len(mensaje.split()) > 2:
        return 3, "¡Buena pregunta! Eso ayuda a continuar la conversación. 🎯"

    return 0, None  # No mensaje de corrección inmediata

def iniciar_conversacion():
    """
    Nivel 1: Saludar, iniciar y mantener una conversación.
    """
    db = BaseDatos()
    api_key = os.getenv("APIKEY")
    buddy = Amigo(api_key)

    while True:  # Permite reiniciar el nivel si el usuario falla
        print("\nBienvenido al Nivel 1: Aprender a saludar e iniciar una conversación.")
        print("Escribe 'salir' en cualquier momento para terminar la conversación.")
        print("\n¡Comencemos!\n")

        interacciones = 0
        puntaje = 0
        conversacion = []

        # Saludo inicial de Buddy
        respuesta_buddy = buddy.saludar()
        print(f"Buddy: {respuesta_buddy}")
        conversacion.append(('Hola', respuesta_buddy))
        db.guardar_interaccion('Hola', respuesta_buddy)

        # Iniciar el bucle de conversación
        while interacciones < 8:
            mensaje_usuario = input("Tú: ").strip()

            if mensaje_usuario.lower() == "salir":
                print("Buddy: ¡Hasta luego! Cuídate mucho.")
                db.cerrar_conexion()
                return

            # Evaluar la calidad de la interacción
            puntos_obtenidos, feedback = evaluar_interaccion(mensaje_usuario)
            puntaje += puntos_obtenidos

            # Solo mostrar corrección si no obtuvo puntos
            if puntos_obtenidos == 0:
                print("Buddy: Intenta hacer una pregunta abierta para que la conversación fluya mejor. 🤔")
            elif feedback:  # Solo mostrar feedback positivo si es relevante
                print(f"Buddy: {feedback}")

            # Obtener la respuesta de Buddy desde OpenAI
            respuesta_buddy = buddy.generar_respuesta_con_openai(mensaje_usuario)
            print(f"Buddy: {respuesta_buddy}")

            # Guardar la interacción
            db.guardar_interaccion(mensaje_usuario, respuesta_buddy)
            conversacion.append((mensaje_usuario, respuesta_buddy))

            interacciones += 1

        # Evaluación final
        print("\n--- Evaluación del Nivel 1 ---")

        if puntaje < 10:
            print("😥 Parece que aún necesitas mejorar en saludos y preguntas abiertas.")
            print("🔄 ¡No te preocupes! Puedes intentarlo nuevamente.")
            print("💡 Consejo: Usa más saludos y preguntas abiertas para que la conversación fluya.")
            print("\nReiniciando Nivel 1...\n")
            continue  # Reinicia el nivel

        print("🎉 ¡Felicidades! Has completado el Nivel 1 con éxito.")
        print(f"Tu puntaje final fue: {puntaje}/16")
        db.cerrar_conexion()
        break  # Sale del bucle si el usuario pasa el nivel

if __name__ == "__main__":
    iniciar_conversacion()
