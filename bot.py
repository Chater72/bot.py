import telebot
import requests

TELEGRAM_TOKEN = '7678229968:AAFFACUrPcFurq7L312etRYO8NgECXvJw8g'
bot = telebot.TeleBot(TELEGRAM_TOKEN)

# OpenRouter API
OPENROUTER_API_URL = 'https://openrouter.ai/api/v1/chat/completions'
OPENROUTER_API_KEY = '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'
MODEL = 'openai/gpt-3.5-turbo'  # Можно заменить на 'mistralai/mixtral-8x7b', 'meta-llama/llama-3-70b-instruct', и т.д.

@bot.message_handler(commands=['start'])
def send_start(message):
    bot.reply_to(message, "Здравствуйте, это ИИ-бот от @tolik_scripter. Чем я могу вам помочь?")

@bot.message_handler(commands=['help'])
def send_help(message):
    bot.reply_to(message, "Напишите любой вопрос или текст — и я постараюсь вам ответить с помощью искусственного интеллекта!")

@bot.message_handler(func=lambda message: True)
def handle_message(message):
    user_input = message.text
    response = get_openrouter_response(user_input)
    bot.reply_to(message, response)

def get_openrouter_response(prompt):
    headers = {
        'Authorization': f'Bearer {OPENROUTER_API_KEY}',
        'Content-Type': 'application/json',
        'HTTP-Referer': 'https://t.me/tolik_scripter',  # Свой Telegram username или сайт
        'User-Agent': 'TelegramBot/1.0'
    }

    data = {
        "model": MODEL,
        "messages": [
            {"role": "user", "content": prompt}
        ]
    }

    try:
        response = requests.post(OPENROUTER_API_URL, headers=headers, json=data, timeout=30)
        response.raise_for_status()
        return response.json()['choices'][0]['message']['content']
    except Exception as e:
        return f"❌ Ошибка при запросе к OpenRouter: {e}"

bot.polling()
