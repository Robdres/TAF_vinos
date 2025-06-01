import os
import sys
import pandas as pd
from openai import OpenAI
import tkinter as tk
from tkinter import scrolledtext
from dotenv import load_dotenv
load_dotenv()

# Cargar clave de API desde variable de entorno
api_key = os.getenv("OPENAI_API_KEY")  # Guarda tu clave en el entorno o en .env
client = OpenAI(api_key=api_key)

# Leer CSV de vinos
df_vinos = pd.read_csv("vinos_ejemplo.csv")

# Crear contexto desde CSV
contexto = "Esta es una lista de vinos con sus características:\n\n"
for _, row in df_vinos.iterrows():
    contexto += (
        f"- {row['nombre']} ({row['año']}), uva: {row['uva']}, "
        f"maridaje: {row['maridaje']}, origen: {row['origen']}, "
        f"precio: ${row['precio_usd']:.2f} USD\n"
    )


contexto = """Eres un sommelier experto en vinos. Si preguntan sobre alguna recomendación,
intenta primero explicar de manera general en base a tu conocimiento de vinos,
y después has una recomendación, por favor dame el vino en una sola linea con
el precio, y el origen, junto a su año y el tipo de vua. Estos son los vinos
que tengo en mi stock, si preguntan sobre recomendaciones utiliza este
stock:""" + contexto


conversacion = [
    {"role": "system", "content": contexto}
]
# Función que consulta al modelo
def hacer_pregunta(pregunta):
    if not pregunta.strip():
        return

    conversacion.append({"role": "user", "content": pregunta})
    response = client.chat.completions.create(
        model="gpt-3.5-turbo",
        messages = conversacion,
        max_tokens=500
    )

    respuesta = response.choices[0].message.content.strip()
    return respuesta

def run_program():
# Función para consultar al modelo
    def print_response():
        pregunta = entrada.get()
        if not pregunta.strip():
            return
        chat.insert(tk.END, f"Tú: {pregunta}\n", "user")
        entrada.delete(0, tk.END)
        response = hacer_pregunta(pregunta)
        chat.insert(tk.END, f"SommelierBot: {response}\n\n", "bot")
        chat.see(tk.END)
    ventana = tk.Tk()
    ventana.title("SommelierBot 🍷")
    ventana.configure(bg="#f8f1e4")
    chat = scrolledtext.ScrolledText(ventana, wrap=tk.WORD, width=80, height=25, bg="#fffaf4", font=("Arial", 11))
    chat.tag_config("user", foreground="navy", font=("Arial", 11, "bold"))
    chat.tag_config("bot", foreground="darkgreen", font=("Arial", 11))
    chat.pack(padx=10, pady=10)
    entrada = tk.Entry(ventana, width=70, font=("Arial", 11))
    entrada.pack(side=tk.LEFT, padx=(10, 0), pady=(0, 10))
    boton = tk.Button(ventana, text="Enviar", command=print_response, bg="#800000", fg="white", font=("Arial", 10, "bold"))
    boton.pack(side=tk.LEFT, padx=(5, 10), pady=(0, 10))
    ventana.mainloop()

# Función de test automático
def run_tests():
    preguntas = [
        "¿Qué vino va bien con carne de cerdo?",
        "¿Cuál es el vino más barato de la lista?",
        "¿Tienes un vino argentino?",
        "Dime un vino con uva Malbec",
        "¿Cuál recomiendas con pescado?"
    ]
    for i, pregunta in enumerate(preguntas, 1):
        print(f"🧪 Test {i}: {pregunta}")
        respuesta = hacer_pregunta(pregunta)
        print("🤖", respuesta)
        print("-" * 50)

# Modo principal
if __name__ == "__main__":
    if "--test" in sys.argv:
        run_tests()
    else:
        run_program()
