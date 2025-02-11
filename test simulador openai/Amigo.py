import openai
import random

class Amigo:
    """Clase para interactuar con la API de OpenAI para conversaciones."""

    def __init__(self, api_key: str):
        self.api_key = api_key
        self.client = openai.OpenAI(api_key=self.api_key)  # Configurar la clave de API
        self.contexto_inicial = (
            #Definir bien la personalidad de cada personaje en cada nivel.
            "Eres un amigo en un juego que tiene como finalidad ayudar al usuario a mejorar sus habilidades de comunicacion "
            "Iniciar con saludo amistoso"
            "Contar cada intercambio (usuario + asistente) como una interacción."
            "Evaluar tras 8 interacciones: uso de saludos, preguntas iniciales y fluidez."
            "Modelar conversación natural: usar saludos, preguntas y respuestas breves."
            "Fomentar preguntas abiertas para mantener el diálogo activo"
            "Usar emojis para tono amigable."
            "Fomentar preguntas abiertas para mantener el diálogo activo"
            "Mantener conversación en español para práctica del usuario."
            "Evaluar tras 8 interacciones: uso de saludos, preguntas iniciales y fluidez."
            "Dar feedback positivo o constructivo al final."
            "Asegurar respuestas cortas y relevantes para mantener el ritmo (no mas de 110 caracteres)"
            "No le digas al usuario que vamos a mejorar sus habilidades de comunicacion"
            "Piensa paso, a paso"
            "observa las preguntas y respuestas del usuario, no asumas las propias preguntas del asistente como parte de la evaluación. Mantener el enfoque en las respuestas del usuario"

        )

    def generar_respuesta_con_openai(self, mensaje_usuario: str) -> str:
        """
        Genera una respuesta usando la API de OpenAI.

        Args:
            mensaje_usuario (str): Mensaje del usuario para procesar.

        Returns:
            str: Respuesta generada o mensaje de error.
        """
        try:
            response = self.client.chat.completions.create(
                model="gpt-3.5-turbo",  # Usa el modelo más adecuado
                messages=[
                    {"role": "system", "content": self.contexto_inicial},
                    {"role": "user", "content": mensaje_usuario}
                ]
            )

            # Obtener la respuesta generada
            respuesta_texto = response.choices[0].message.content.strip()
            return respuesta_texto

        except openai.APIError as e:
            print(f"Error de conexión con OpenAI: {e}")
            return "¡Vaya! Parece que hay problemas de conexión con OpenAI. ¿Quieres intentarlo de nuevo?"

    def saludar(self) -> str:
        """Devuelve un saludo inicial personalizado."""
        saludos = ["¡Hola! 👋 ¿Cómo estás?","¡Buenos días! ☀️ ¿Qué tal tu día?","¡Hola! 😊 ¿En qué puedo ayudarte hoy?","¡Buenas tardes! 🌇 ¿Cómo te va?","¡Hola! ¿Qué cuentas?","¡Hola! 👋 ¿Todo bien por ahí?","¡Buenas! ¿Cómo has estado?","¡Hola! 😄 ¿Qué novedades hay?","¡Hola! ¿Cómo te trata el día?","¡Hola! 👋 ¿Qué tal todo?"]
        return random.choice(saludos)