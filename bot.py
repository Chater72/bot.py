import telebot
import requests


TELEGRAM_TOKEN = '7678229968:AAFFACUrPcFurq7L312etRYO8NgECXvJw8g'
bot = telebot.TeleBot(TELEGRAM_TOKEN)


OPENROUTER_API_URL = 'https://openrouter.ai/api/v1/chat/completions'
OPENROUTER_API_KEY = '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'


MODEL = 'openai/gpt-3.5-turbo'


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
        'Content-Type': 'application/json'
    }
    data = {
        "model": MODEL,
        "messages": [
            {"role": "user", "content": prompt}
        ]
    }
    try:
        response = requests.post(OPENROUTER_API_URL, headers=headers, json=data)
        response.raise_for_status()
        return response.json()['choices'][0]['message']['content']
    except Exception as e:
        return f"Ошибка при запросе: {e}"


bot.polling()
