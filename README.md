# 🚀 YASHIKA-CHAT-BOT

**Advanced Telegram Chat Bot** that **learns & replies** automatically.

### ✨ Features
- 🤖 **Learning Chatbot** – Learns from group messages and replies
- 🌐 **Multi Language** – 20+ languages support (`/lang`)
- ✅ **Enable / Disable** per group (`/chatbot`)
- 📊 Stats, Ping, ID, Broadcast, Shayri
- 💾 **SQLite Database** (No MongoDB required)
- 🐳 Ready for Heroku / Render / Koyeb / Railway / VPS

---

## 📦 Deployment

### Environment Variables (Required)
| Variable     | Description                  |
|--------------|------------------------------|
| `API_ID`     | From [my.telegram.org](https://my.telegram.org) |
| `API_HASH`   | From [my.telegram.org](https://my.telegram.org) |
| `BOT_TOKEN`  | From [@BotFather](https://t.me/BotFather) |
| `OWNER_ID`   | Your Telegram User ID        |

Optional: `SUPPORT_GRP`, `UPDATE_CHNL`, `OWNER_USERNAME`, `DB_PATH`

---

### ─「 Deploy on Heroku 」─
[![Deploy](https://www.herokucdn.com/deploy/button.svg)](https://dashboard.heroku.com/new?template=https://github.com/kalahume6-lgtm/YASHIKA-CHAT-BOT)

### ─「 Deploy on Render 」─
1. New → Web Service → Docker
2. Add env vars (API_ID, API_HASH, BOT_TOKEN, OWNER_ID)
3. Deploy

### ─「 Deploy on Koyeb / Railway 」─
Connect this repo → Add the same environment variables → Deploy

### Local Run
```bash
git clone https://github.com/kalahume6-lgtm/YASHIKA-CHAT-BOT
cd YASHIKA-CHAT-BOT
pip install -r requirements.txt
cp sample.env .env
# Edit .env with your values
python -m YASHIKA
```

---

## 📖 Commands

| Command       | Description                      |
|---------------|----------------------------------|
| `/start`      | Start the bot                    |
| `/help`       | Help menu                        |
| `/chatbot`    | Enable / Disable chatbot         |
| `/lang`       | Set language                     |
| `/status`     | Check chatbot status             |
| `/ping`       | Check bot speed                  |
| `/stats`      | Users & Chats count              |
| `/id`         | Get IDs                          |
| `/shayri`     | Random Shayri                    |
| `/broadcast`  | Owner only broadcast             |
| `/repo`       | Source code                      |

---

## 🗄 Database
This bot uses **SQLite** (file based).  
No MongoDB / No external database URL needed.  
Data is stored in `data/bot.db`.

---

## 📞 Contact
Made with ❤️  
[Support](https://t.me/ishika_support)
