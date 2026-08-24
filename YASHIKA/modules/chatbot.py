import random
from pyrogram import filters
from pyrogram.enums import ChatAction, ChatType
from pyrogram.types import InlineKeyboardButton, InlineKeyboardMarkup, Message, CallbackQuery
from deep_translator import GoogleTranslator

from YASHIKA.database import (
    add_served_chat, add_served_user,
    get_chatbot_status, set_chatbot_status,
    get_chat_language, set_chat_language,
    get_reply, save_reply
)
from YASHIKA import YASHIKA, LOGGER
from YASHIKA.modules.helpers import CHATBOT_ON, HELP_BTN, HELP_READ, CHATBOT_BACK, get_chatbot_read, get_tools_data_read, get_about_read, ABOUT_BTN, START, DEV_OP


IGNORE = {"start", "help", "ping", "stats", "id", "chatbot", "lang", "status", "repo", "shayri", "test", "broadcast"}


def is_not_command(_, __, m):
    if not m or not m.text:
        return True
    if m.text.startswith("/"):
        cmd = m.text[1:].split("@")[0].split()[0].lower()
        if cmd in IGNORE:
            return False
    return True


no_cmd = filters.create(is_not_command)


@YASHIKA.on_message(filters.command("chatbot"))
async def chatbot_cmd(_, m: Message):
    await set_chatbot_status(m.chat.id, "disabled")
    await m.reply_text(
        "Enable / Disable Chatbot:",
        reply_markup=InlineKeyboardMarkup(CHATBOT_ON)
    )


@YASHIKA.on_callback_query()
async def callbacks(_, q: CallbackQuery):
    data = q.data
    if data == "enable_chatbot":
        await set_chatbot_status(q.message.chat.id, "enabled")
        await q.answer("Enabled ✅", show_alert=True)
        await q.edit_message_text("Chatbot **Enabled**")
    elif data == "disable_chatbot":
        await set_chatbot_status(q.message.chat.id, "disabled")
        await q.answer("Disabled", show_alert=True)
        await q.edit_message_text("Chatbot **Disabled**")
    elif data == "HELP":
        await q.message.edit_text(HELP_READ, reply_markup=InlineKeyboardMarkup(HELP_BTN))
    elif data == "CLOSE":
        await q.message.delete()


@YASHIKA.on_message(filters.incoming & no_cmd & \~filters.bot)
async def reply_handler(client, message: Message):
    try:
        chat_id = message.chat.id
        is_private = message.chat.type == ChatType.PRIVATE
        is_group = message.chat.type in (ChatType.GROUP, ChatType.SUPERGROUP)

        status = await get_chatbot_status(chat_id)

        if is_group and status != "enabled":
            return

        if not message.text:
            return

        # Learn
        if message.reply_to_message and message.reply_to_message.text and message.text:
            await save_reply(message.reply_to_message.text.strip(), message.text.strip())

        # Should reply?
        if is_private or (message.reply_to_message and message.reply_to_message.from_user and message.reply_to_message.from_user.id == YASHIKA.id) or (not message.reply_to_message):
            await client.send_chat_action(chat_id, ChatAction.TYPING)

            data = await get_reply(message.text.strip())
            if data:
                text = data["text"]
                lang = await get_chat_language(chat_id)
                if lang and lang != "nolang":
                    try:
                        text = GoogleTranslator(source="auto", target=lang).translate(text)
                    except:
                        pass
                await message.reply_text(text)
            else:
                await message.reply_text(random.choice(["Haan bolo?", "Kya hua?", "Ji?", "Hmm..."]))

            if is_group:
                await add_served_chat(chat_id)
            elif message.from_user:
                await add_served_user(message.from_user.id)

    except Exception as e:
        LOGGER.error(f"reply error: {e}")
