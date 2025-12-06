import telebot
import schedule
import time
import threading
import random
import os
from datetime import datetime
from flask import Flask

# --- CONFIGURACIÓN ---
TOKEN = os.environ.get('TELEGRAM_TOKEN') 
CHAT_ID = os.environ.get('TELEGRAM_CHAT_ID') 

bot = telebot.TeleBot(TOKEN)
app = Flask(__name__)

# --- MEGA LISTA DE AFIRMACIONES ---
AFIRMACIONES = [
    "✨ Soy un imán para los milagros.",
    "💖 Mi corazón está abierto a recibir amor.",
    "🌿 Merezco descansar y recuperarme.",
    "⚖️ Tomo decisiones con claridad y confianza.",
    "🦋 Acepto mis emociones y las dejo fluir.",
    "🎶 Mi voz es importante y merezco ser escuchado/a.",
    "🌱 Estoy creciendo a mi propio ritmo, y eso está bien.",
    "🌟 Soy suficiente, hice suficiente, tengo suficiente.",
    "💫 El dinero fluye hacia mí de formas inesperadas.",
    "🙏 Perdono mi pasado y abrazo mi presente.",
    "🚀 No persigo, atraigo. Lo que es para mí, me encuentra.",
    "🌈 Soy el arquitecto de mi propio destino.",
    "💎 Mi potencial es ilimitado.",
    "🕊️ Suelto la necesidad de controlarlo todo.",
    "🌻 Hoy elijo la paz sobre la preocupación.",
    "🔥 Tengo la fuerza para superar esto.",
    "🍃 Mi mente está calmada y enfocada.",
    "🎨 Creo belleza donde quiera que voy.",
    "⚡ Soy valiente y enfrento mis miedos.",
    "🏆 Mi éxito es inevitable."
]

# --- FÁBRICA INFINITA (Generador) ---
SUJETOS = ["El universo", "Mi energía", "La vida", "Mi intuición", "Hoy", "Mi destino", "La luz divina"]
ACCIONES = ["conspira para darme", "está creando", "manifiesta", "atrae hacia mí", "construye", "multiplica", "me regala"]
RESULTADOS = ["abundancia ilimitada.", "una paz profunda.", "éxito rotundo.", "oportunidades de oro.", "milagros inesperados.", "amor puro.", "salud perfecta."]

# --- COMANDOS ---

@bot.message_handler(commands=['start', 'inicio'])
def inicio(message):
    nombre = message.from_user.first_name
    texto = f"¡Hola {nombre}! 🌟\n\nComandos:\n/afirmacion - Frase lista\n/magica - ¡Crear frase nueva!\n/diaria - Frase de hoy"
    bot.send_message(message.chat.id, texto)

@bot.message_handler(commands=['afirmacion'])
def afirmacion_aleatoria(message):
    bot.reply_to(message, f"✨ {random.choice(AFIRMACIONES)}")

@bot.message_handler(commands=['magica'])
def frase_magica(message):
    # Aquí ocurre la magia de mezclar palabras
    s = random.choice(SUJETOS)
    a = random.choice(ACCIONES)
    r = random.choice(RESULTADOS)
    frase = f"{s} {a} {r}"
    bot.reply_to(message, f"🔮 *Creación Mágica:*\n\n✨ {frase}", parse_mode='Markdown')

@bot.message_handler(commands=['diaria'])
def afirmacion_diaria(message):
    hoy = datetime.now().day
    indice = (hoy - 1) % len(AFIRMACIONES)
    bot.reply_to(message, f"📅 *Día {hoy}:* {AFIRMACIONES[indice]}", parse_mode='Markdown')

# --- AUTOMATIZACIÓN Y SERVIDOR ---

def tarea_diaria():
    hoy = datetime.now().day
    indice = (hoy - 1) % len(AFIRMACIONES)
    try:
        bot.send_message(CHAT_ID, f"☀️ *Buenos días:*\n\n{AFIRMACIONES[indice]}", parse_mode='Markdown')
    except:
        pass

schedule.every().day.at("13:00").do(tarea_diaria)

@app.route('/')
def home():
    return "Bot Activo 🤖"

def run_schedule():
    while True:
        schedule.run_pending()
        time.sleep(1)

if __name__ == "__main__":
    t = threading.Thread(target=run_schedule)
    t.start()
    t_bot = threading.Thread(target=bot.infinity_polling)
    t_bot.start()
    app.run(host='0.0.0.0', port=int(os.environ.get('PORT', 5000)))
