import telebot
import openai

# Telegram Bot Token
TELEGRAM_TOKEN = "7771466336:AAHEqiJqjZsi_JykiFZ2PcNh9V4mul2WvG4"

# OpenRouter إعدادات
openai.api_base = "https://openrouter.ai/api/v1"
openai.api_key = "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"

bot = telebot.TeleBot(TELEGRAM_TOKEN)

@bot.message_handler(func=lambda message: True)
def chat_with_ai(message):
    try:
        response = openai.ChatCompletion.create(
            model="openai/gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": "أنت بوت تليجرام ظريف ومرح، بتتكلم كأنك صاحب المستخدم، وبتفهم هو ولد ولا بنت وبتتعامل على حسب الحالة النفسية أو الطلب."},
                {"role": "user", "content": message.text}
            ]
        )

        bot.reply_to(message, response["choices"][0]["message"]["content"])

    except Exception as e:
        bot.reply_to(message, f"حصل خطأ: {e}")

bot.infinity_polling()
