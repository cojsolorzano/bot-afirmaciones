import telebot
import schedule
import time
import threading
import random
import os
from flask import Flask

# --- CONFIGURACIÓN ---
TOKEN = os.environ.get('TELEGRAM_TOKEN') 
CHAT_ID = os.environ.get('TELEGRAM_CHAT_ID') 

bot = telebot.TeleBot(TOKEN)
app = Flask(__name__)

# --- LISTA DE AFIRMACIONES ---
afirmaciones = [
    "Hoy es un día lleno de oportunidades.",
    "Tengo la capacidad de crear la vida que deseo.",
    "Soy suficiente tal y como soy.",
    "Atraigo energía positiva a mi vida.",
    "Mis desafíos me ayudan a crecer.",
]

# --- NUEVO: RESPONDER A COMANDOS ---
# Esto hace que si le escribes /start o /hola, te responda
@bot.message_handler(commands=['start', 'hola'])
def send_welcome(message):
    bot.reply_to(message, "¡Hola! Soy tu bot de afirmaciones. Estoy funcionando correctamente. 🤖")

# --- LÓGICA DEL BOT ---
def enviar_afirmacion():
    frase = random.choice(afirmaciones)
    try:
        bot.send_message(CHAT_ID, f"✨ Afirmación del día:\n\n{frase}")
        print("Mensaje enviado con éxito")
    except Exception as e:
        print(f"Error al enviar: {e}")

# Programar la hora (Ajusta esto si quieres probar. Ej: si son las 10:00, pon 10:05)
schedule.every().day.at("13:00").do(enviar_afirmacion)

# --- SERVIDOR WEB ---
@app.route('/')
def home():
    return "¡El Bot de Afirmaciones está vivo! 🤖"

def run_schedule():
    while True:
        schedule.run_pending()
        time.sleep(1)

# --- INICIO ---
if __name__ == "__main__":
    # Hilo para el cronograma
    t = threading.Thread(target=run_schedule)
    t.start()
    
    # Hilo para escuchar mensajes (Polling)
    # Esto permite que el bot responda cuando le escribes
    t_bot = threading.Thread(target=bot.infinity_polling)
    t_bot.start()

    # ENVIO DE PRUEBA AL INICIAR
    # Esto enviará un mensaje apenas Render termine de cargar
    try:
        bot.send_message(CHAT_ID, "🟢 El sistema se ha reiniciado. ¡Estoy listo!")
    except:
        pass

    # Iniciar servidor web
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)
