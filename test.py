import openai

mensaje_sistema = {
    "role": "system",
    "content": "Eres un sommelier experto. Responde de forma clara y profesional preguntas sobre vinos."
}

preguntas = [
    "¿Cuál es la temperatura ideal para servir un vino tinto?",
    "¿Qué tipo de vino va mejor con carne roja?",
    "¿Qué son los taninos en el vino?",
    "¿Cuánto tiempo puede envejecer un vino blanco?",
    "¿Qué diferencia hay entre un vino joven y un vino de crianza?"
]

print("=== Validación del SommelierBot ===")
for i, pregunta in enumerate(preguntas, 1):
    print(f"\nPregunta {i}: {pregunta}")
    try:
        respuesta = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=[mensaje_sistema, {"role": "user", "content": pregunta}]
        )
        print("Respuesta:", respuesta['choices'][0]['message']['content'].strip())
    except Exception as e:
        print("Error:", str(e))
