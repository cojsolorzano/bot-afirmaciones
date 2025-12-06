import telebot
import schedule
import time
import threading
import random
import os
from flask import Flask

# --- CONFIGURACIÓN ---
# En Render, configurarás estas variables en la sección "Environment Variables"
TOKEN = os.environ.get('TELEGRAM_TOKEN') 
CHAT_ID = os.environ.get('TELEGRAM_CHAT_ID') # Tu ID o el del canal donde enviará el mensaje

bot = telebot.TeleBot(TOKEN)
app = Flask(__name__)

# --- LISTA DE AFIRMACIONES ---
afirmaciones = [
    "Hoy es un día lleno de oportunidades.",
    "Tengo la capacidad de crear la vida que deseo.",
    "Soy suficiente tal y como soy.",
    "Atraigo energía positiva a mi vida.",
    "Mis desafíos me ayudan a crecer.",
    "Merezco amor, felicidad y prosperidad.",
    "Confío en mi intuición y sabiduría.",
    # ¡Agrega todas las que quieras aquí!
]

# --- LÓGICA DEL BOT ---
def enviar_afirmacion():
    frase = random.choice(afirmaciones)
    try:
        bot.send_message(CHAT_ID, f"✨ Afirmación del día:\n\n{frase}")
        print("Mensaje enviado con éxito")
    except Exception as e:
        print(f"Error al enviar: {e}")

# Programar la hora (Formato 24h, hora del servidor - usualmente UTC)
# Ojo: Render usa hora UTC (Greenwich). Si estás en España son +1/+2 horas, Latam -3/-6 horas.
# Ajusta la hora según la diferencia. Ejemplo: "13:00" UTC podría ser tu mañana.
schedule.every().day.at("13:00").do(enviar_afirmacion)

# --- SERVIDOR WEB (Para mantener vivo a Render) ---
@app.route('/')
def home():
    return "¡El Bot de Afirmaciones está vivo! 🤖"

def run_schedule():
    while True:
        schedule.run_pending()
        time.sleep(1)

# --- INICIO ---
if __name__ == "__main__":
    # Hilo para el cronograma (se ejecuta en paralelo)
    t = threading.Thread(target=run_schedule)
    t.start()
    
    # Iniciar servidor web (requerido por Render)
    # Render asigna un puerto dinámico en la variable PORT
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)
