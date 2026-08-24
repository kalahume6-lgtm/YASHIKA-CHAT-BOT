import sys
import asyncio
import importlib
import os
import threading
from flask import Flask
from pyrogram import idle, filters
from pyrogram.types import BotCommand, Message
from pyrogram.errors import FloodWait

from config import OWNER_ID
from YASHIKA import LOGGER, YASHIKA
from YASHIKA.database import init_db
from YASHIKA.modules import ALL_MODULES


async def boot():
    # Initialize SQLite database
    try:
        await init_db()
    except Exception as e:
        LOGGER.error(f"Database init failed: {e}")
        sys.exit(1)

    # Start bot
    try:
        await YASHIKA.start()
    except FloodWait as e:
        wait_time = int(e.value)
        LOGGER.error(f"FloodWait: sleeping {wait_time}s...")
        await asyncio.sleep(wait_time + 5)
        await YASHIKA.start()
    except Exception as ex:
        LOGGER.error(f"Start failed: {ex}")
        sys.exit(1)

    LOGGER.info(f"Bot Started as {YASHIKA.name}")
    LOGGER.info(f"Username: @{YASHIKA.username}")

    # Load modules
    for module in ALL_MODULES:
        try:
            importlib.import_module("YASHIKA.modules." + module)
            LOGGER.info(f"Successfully imported : {module}")
        except Exception as e:
            LOGGER.error(f"Failed to import {module}: {e}")

    # Extra test handler
    @YASHIKA.on_message(filters.command("test"))
    async def test_cmd(client, message: Message):
        await message.reply_text("✅ Test OK - Bot is receiving messages & SQLite is working!")

    # Set bot commands
    try:
        await YASHIKA.set_bot_commands(
            commands=[
                BotCommand("start", "Start the bot"),
                BotCommand("help", "Help menu"),
                BotCommand("ping", "Check ping"),
                BotCommand("stats", "Bot stats"),
                BotCommand("id", "Get IDs"),
                BotCommand("chatbot", "Enable / Disable chatbot"),
                BotCommand("lang", "Set language"),
                BotCommand("status", "Chatbot status"),
                BotCommand("shayri", "Random Shayri"),
                BotCommand("repo", "Source code"),
                BotCommand("test", "Test bot"),
            ]
        )
        LOGGER.info("Bot commands set successfully.")
    except Exception as ex:
        LOGGER.error(f"Failed to set bot commands: {ex}")

    LOGGER.info(f"@{YASHIKA.username} is online. Waiting for messages...")

    if OWNER_ID:
        try:
            await YASHIKA.send_message(
                int(OWNER_ID),
                f"{YASHIKA.mention} started successfully!\nDatabase: **SQLite** ✅\nSend /test or /start",
            )
        except Exception as e:
            LOGGER.info(f"Owner notify failed: {e}")

    await idle()


app = Flask(__name__)


@app.route("/")
def home():
    return "YASHIKA CHAT BOT is running | Database: SQLite"


@app.route("/health")
def health():
    return "OK", 200


def run_flask():
    port = int(os.environ.get("PORT", 10000))
    app.run(host="0.0.0.0", port=port)


if __name__ == "__main__":
    flask_thread = threading.Thread(target=run_flask, daemon=True)
    flask_thread.start()
    LOGGER.info(f"Health check on port {os.environ.get('PORT', 10000)}")
    asyncio.run(boot())
