import telebot
import schedule
import time
import threading
import random
import os
from datetime import datetime
from flask import Flask

# --- CONFIGURACIÓN DE RENDER ---
# Usamos las variables de entorno para seguridad
TOKEN = os.environ.get('TELEGRAM_TOKEN') 
CHAT_ID = os.environ.get('TELEGRAM_CHAT_ID') 

bot = telebot.TeleBot(TOKEN)
app = Flask(__name__)

# --- LISTA DE AFIRMACIONES (La versión completa) ---
AFIRMACIONES = [
    "✨ Pienso bien y atraigo bien.",
    "💖 Mis emociones son positivas y me guían.",
    "🌿 Mi cuerpo, mente y espíritu están en armonía.",
    "⚖️ Vivo en perfecto equilibrio interior.",
    "🦋 Confío plenamente en mi proceso de vida.",
    "🎶 Mi vida fluye con ritmo y dinamismo.",
    "🌱 Soy consciente y transformo mis pensamientos.",
    "🌟 Cada día evoluciono hacia mi mejor versión.",
    "💫 Merezco amor, éxito y abundancia infinita.",
    "🙏 Agradezco profundamente cada bendición.",
    "🚀 Tengo el poder de crear mi realidad.",
    "🌈 Mi luz interior brilla con intensidad.",
    "💎 Me acepto y me amo incondicionalmente.",
    "🕊️ Encuentro paz en cada respiración.",
    "🌻 Elijo la felicidad en este momento presente.",
    "🔥 Mi energía atrae oportunidades magníficas.",
    "🍃 Dejo ir lo que no sirve a mi crecimiento.",
    "🎨 Soy el artista de mi propia vida.",
    "⚡ Tengo claridad mental y enfoque poderoso.",
    "🏆 Supero cualquier desafío con sabiduría."
]

# --- FUNCIONES NUEVAS DEL BOT ---

# 1. Comando START (Bienvenida bonita)
@bot.message_handler(commands=['start', 'inicio', 'comenzar'])
def inicio(message):
    nombre = message.from_user.first_name
    respuesta = f"""🌟 *¡BIENVENIDO/A {nombre}!* 🌟

Soy tu *Bot de Afirmaciones Positivas* 💫
Mi misión es recordarte lo *INCREÍBLE* que eres cada día.

*📋 COMANDOS DISPONIBLES:*
/afirmacion - Recibe una afirmación aleatoria ✨
/diaria - La frase especial de hoy 📅
/todas - Ver la lista completa 📜
/fuerte - Afirmación de poder 💪
/saludo - Un saludo personalizado 👋
/ayuda - Muestra este menú ❓

*💌 Consejo:* Usa una afirmación al despertar y antes de dormir.
"""
    bot.send_message(message.chat.id, respuesta, parse_mode='Markdown')

# 2. Comando AFIRMACIÓN ALEATORIA
@bot.message_handler(commands=['afirmacion', 'frase', 'motivacion'])
def afirmacion_aleatoria(message):
    afirmacion = random.choice(AFIRMACIONES)
    respuesta = f"""💫 *AFIRMACIÓN DEL MOMENTO*

{afirmacion}

*✨ Repite esta afirmación 3 veces en voz alta ✨*
"""
    bot.reply_to(message, respuesta, parse_mode='Markdown')

# 3. Comando AFIRMACIÓN DIARIA (Manual)
@bot.message_handler(commands=['diaria', 'hoy'])
def afirmacion_del_dia_comando(message):
    hoy = datetime.now().day
    indice = (hoy - 1) % len(AFIRMACIONES)
    afirmacion = AFIRMACIONES[indice]
    
    respuesta = f"""📅 *AFIRMACIÓN DEL DÍA*
*Fecha:* {datetime.now().strftime('%d de %B')}

🎯 *{afirmacion}*

*☀️ Guárdala en tu corazón durante todo el día.*
"""
    bot.reply_to(message, respuesta, parse_mode='Markdown')

# 4. Comando TODAS LAS AFIRMACIONES
@bot.message_handler(commands=['todas', 'lista'])
def listar_todas(message):
    texto = "📜 *COLECCIÓN COMPLETA* 📜\n\n"
    for i, afirmacion in enumerate(AFIRMACIONES, 1):
        texto += f"*{i}.* {afirmacion}\n"
    
    # Enviar en fragmentos si es muy largo (seguridad de Telegram)
    if len(texto) > 4000:
        bot.send_message(message.chat.id, texto[:4000], parse_mode='Markdown')
        bot.send_message(message.chat.id, texto[4000:], parse_mode='Markdown')
    else:
        bot.send_message(message.chat.id, texto, parse_mode='Markdown')

# 5. Comando SALUDO
@bot.message_handler(commands=['saludo', 'hola'])
def saludo_personal(message):
    nombre = message.from_user.first_name
    saludos = [
        f"¡Hola {nombre}! Tu energía positiva inspira al mundo. 🌍",
        f"¡Qué alegría verte {nombre}! Hoy tienes dones especiales. 🎁",
        f"¡Hola {nombre}! Tu presencia hace del mundo un lugar mejor. 💖"
    ]
    bot.reply_to(message, random.choice(saludos))

# 6. Comando FUERTE (Empoderamiento)
@bot.message_handler(commands=['fuerte', 'poder'])
def afirmacion_fuerte(message):
    afirmaciones_fuertes = [
        "⚡ ¡SOY INVENCIBLE! Nada ni nadie puede detener mi luz.",
        "🔥 MI FUERZA INTERIOR ES MÁS GRANDE QUE CUALQUIER RETO.",
        "🏆 HOY RECLAMO MI PODER PERSONAL Y MI GRANDEZA.",
        "💥 LAS DIFICULTADES SE RINDEN ANTE MI DETERMINACIÓN."
    ]
    respuesta = f"""💪 *AFIRMACIÓN DE PODER*

{random.choice(afirmaciones_fuertes)}

*🏹 ¡Envíala al universo con convicción! 🏹*
"""
    bot.reply_to(message, respuesta, parse_mode='Markdown')

# 7. Respuestas Inteligentes (Sin comando)
@bot.message_handler(func=lambda m: m.text and 'gracias' in m.text.lower())
def responder_gracias(message):
    bot.reply_to(message, "¡A ti! 😘 Recuerda: mereces todo lo bueno del universo. 💫")

@bot.message_handler(func=lambda m: m.text and 'te quiero' in m.text.lower())
def responder_amor(message):
    bot.reply_to(message, "💖 ¡El amor que das regresa multiplicado! 🌹")

@bot.message_handler(commands=['ayuda', 'help'])
def ayuda(message):
    inicio(message)

# --- SISTEMA AUTOMÁTICO (Lo que mantiene vivo el bot) ---

def tarea_automatica_diaria():
    # Esta función se dispara sola a la hora programada
    hoy = datetime.now().day
    indice = (hoy - 1) % len(AFIRMACIONES)
    afirmacion = AFIRMACIONES[indice]
    try:
        bot.send_message(CHAT_ID, f"🔔 *RECORDATORIO AUTOMÁTICO*\n\n✨ {afirmacion}", parse_mode='Markdown')
        print("Mensaje automático enviado")
    except Exception as e:
        print(f"Error envío automático: {e}")

# Programar hora automática (Hora Servidor - UTC)
schedule.every().day.at("13:00").do(tarea_automatica_diaria)

# --- SERVIDOR FLASK (Para Render) ---
@app.route('/')
def home():
    return "¡El Bot de Afirmaciones está vivo y feliz! 🤖✨"

def run_schedule():
    while True:
        schedule.run_pending()
        time.sleep(1)

# --- INICIO PRINCIPAL ---
if __name__ == "__main__":
    # Hilo del cronograma
    t_sched = threading.Thread(target=run_schedule)
    t_sched.start()
    
    # Hilo del Bot (Polling)
    t_bot = threading.Thread(target=bot.infinity_polling)
    t_bot.start()

    # Servidor Web
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)
