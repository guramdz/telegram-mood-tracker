import telebot
from telebot.types import InlineKeyboardMarkup, InlineKeyboardButton
import json
from datetime import datetime, timedelta
import os
from dotenv import load_dotenv
import webbrowser

# 🔐 Load .env token
load_dotenv()
TOKEN = os.getenv("TOKEN")

if not TOKEN:
    raise ValueError("❌ Bot token not found in .env file")

bot = telebot.TeleBot(TOKEN)
DATA_FILE = "mood_data.json"

# Create the data file if it doesn't exist
if not os.path.exists(DATA_FILE):
    with open(DATA_FILE, "w") as f:
        json.dump({}, f)

def load_data():
    with open(DATA_FILE, "r") as f:
        return json.load(f)

def save_data(data):
    with open(DATA_FILE, "w") as f:
        json.dump(data, f, indent=4)

# /start and /help command
@bot.message_handler(commands=['start', 'help'])
def send_welcome(message):
    bot.reply_to(message,
        "👋 Welcome to Mood Tracker Bot!\n\nCommands:\n"
        "/mood - Log your current mood\n"
        "/note - Add a note for today\n"
        "/stats - Show last 7-day mood summary\n"
        "/help - Show this help message"
    )

# /mood command
@bot.message_handler(commands=['mood'])
def ask_mood(message):
    ask_mood_stub(message.chat.id)

def ask_mood_stub(chat_id):
    markup = InlineKeyboardMarkup()
    markup.add(
        InlineKeyboardButton("😊 Good", callback_data="mood_Good"),
        InlineKeyboardButton("😐 Neutral", callback_data="mood_Neutral"),
        InlineKeyboardButton("😞 Bad", callback_data="mood_Bad")
    )
    bot.send_message(chat_id, "How are you feeling today?", reply_markup=markup)

@bot.callback_query_handler(func=lambda call: call.data.startswith("mood_"))
def handle_mood_selection(call):
    mood = call.data.split("_")[1]
    user_id = str(call.from_user.id)
    today = datetime.today().strftime('%Y-%m-%d')
    data = load_data()

    if user_id not in data:
        data[user_id] = {}
    if today not in data[user_id]:
        data[user_id][today] = {}

    # Preserve any existing note if it exists
    existing_note = data[user_id][today].get("note", "")
    data[user_id][today] = {"mood": mood}
    if existing_note:
        data[user_id][today]["note"] = existing_note

    save_data(data)
    bot.answer_callback_query(call.id, f"Mood saved: {mood}")
    bot.send_message(call.message.chat.id, f"✅ Your mood '{mood}' has been recorded for today.")

# /note command
@bot.message_handler(commands=['note'])
def add_note_prompt(message):
    msg = bot.send_message(message.chat.id, "📝 Please type a short note about today:")
    bot.register_next_step_handler(msg, save_note)

def save_note(message):
    user_id = str(message.from_user.id)
    today = datetime.today().strftime('%Y-%m-%d')
    data = load_data()

    if user_id in data and today in data[user_id]:
        data[user_id][today]["note"] = message.text
        save_data(data)
        bot.send_message(message.chat.id, "🗒️ Your note has been saved.")
    else:
        bot.send_message(message.chat.id, "⚠️ Please log your mood first using /mood.")

# /stats command
@bot.message_handler(commands=['stats'])
def show_stats(message):
    user_id = str(message.from_user.id)
    data = load_data()
    today = datetime.today()
    stats = {"Good": 0, "Neutral": 0, "Bad": 0}

    if user_id in data:
        for i in range(7):
            day = (today - timedelta(days=i)).strftime('%Y-%m-%d')
            if day in data[user_id] and "mood" in data[user_id][day]:
                mood = data[user_id][day]["mood"]
                if mood in stats:
                    stats[mood] += 1

    response = "📊 Your mood in the last 7 days:\n"
    for mood, count in stats.items():
        response += f"{mood} – {count} day(s)\n"

    bot.send_message(message.chat.id, response)

# 🔁 autotest on launch
def autotest(user_id):
    try:
        bot.send_message(user_id, "🛠 Auto-test started.\nWelcome to Mood Tracker Bot.")
        ask_mood_stub(user_id)
        bot.send_message(user_id, "ℹ️ Use /note to add a note.\nUse /stats to view your summary.")
    except Exception as e:
        print("Auto-test error:", e)

# 🧠 Entry point
if __name__ == "__main__":
    webbrowser.open("https://t.me/moodbot_2025_bot")
    bot.polling()
