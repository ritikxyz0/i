
import telebot
from telebot.types import InlineKeyboardMarkup, InlineKeyboardButton
import requests

BOT_TOKEN = "7594583741:AAFXqLuUiAdDfoeuXJi5j-3APbVzVEMXHeM"
SMM_API_URL = "https://your-smm-panel.com/api/v2"  # Change this
SMM_API_KEY = "your_api_key_here"                  # Change this
SERVICE_ID = 1234  # Replace with Instagram Likes service ID

bot = telebot.TeleBot(BOT_TOKEN)
user_links = {}  # Temporary store user links

@bot.message_handler(commands=['start'])
def start(message):
    bot.send_message(message.chat.id, "👋 Welcome! Send your Instagram post link.")

@bot.message_handler(func=lambda message: "instagram.com" in message.text)
def ask_likes(message):
    user_links[message.chat.id] = message.text
    markup = InlineKeyboardMarkup()
    markup.row_width = 3
    markup.add(
        InlineKeyboardButton("👍 10 Likes", callback_data="like_10"),
        InlineKeyboardButton("🔥 50 Likes", callback_data="like_50"),
        InlineKeyboardButton("💣 100 Likes", callback_data="like_100")
    )
    bot.send_message(message.chat.id, "How many likes do you want?", reply_markup=markup)

@bot.callback_query_handler(func=lambda call: call.data.startswith("like_"))
def send_likes(call):
    qty = int(call.data.split("_")[1])
    link = user_links.get(call.message.chat.id)

    if not link:
        bot.send_message(call.message.chat.id, "❌ Please send Instagram post link again.")
        return

    # Call SMM API
    response = requests.post(SMM_API_URL, data={
        "key": SMM_API_KEY,
        "action": "add",
        "service": SERVICE_ID,
        "link": link,
        "quantity": qty
    })

    if response.status_code == 200 and "order" in response.text:
        bot.send_message(call.message.chat.id, f"✅ Order placed for {qty} likes!\nLikes will appear soon.")
    else:
        bot.send_message(call.message.chat.id, "❌ Failed to place order. Try again later.")

bot.polling()
