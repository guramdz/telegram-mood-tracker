from pathlib import Path

# Create a README.md file with the full content for GitHub
readme_content = """
# 🧠 Mood Tracker Telegram Bot

A lightweight personal Telegram bot to track your daily mood using emoji buttons and short notes. Built with Python and [pyTelegramBotAPI](https://github.com/eternnoir/pyTelegramBotAPI).

> 📌 This bot was originally developed as a demonstration for an Upwork project proposal. If hired, the final working version will be delivered privately to the client, and this repository may be made private or removed.

---

## ✨ Features

- `/start` – Welcome message and help overview  
- `/mood` – Choose your mood with emoji buttons (😊 😐 😞)  
- `/note` – Add a short daily note after logging mood  
- `/stats` – View a 7-day summary of your mood entries  
- Data saved per-user in a local `mood_data.json` file

---

## 🚀 How to Run

### 1. Clone the Repository
```bash
git clone https://github.com/yourusername/telegram-mood-tracker.git
cd telegram-mood-tracker
