import random
from pyrogram import filters
from pyrogram.errors import MessageEmpty
from pyrogram.enums import ChatAction, ChatType
from pyrogram.types import (
    InlineKeyboardButton,
    InlineKeyboardMarkup,
    Message,
    CallbackQuery,
)
from deep_translator import GoogleTranslator

from YASHIKA.database import (
    add_served_chat,
    add_served_user,
    get_chatbot_status,
    set_chatbot_status,
    get_chat_language,
    set_chat_language,
    get_reply,
    save_reply,
)
from YASHIKA import YASHIKA, LOGGER
from YASHIKA.modules.helpers import (
    CHATBOT_ON,
    ABOUT_BTN,
    BACK,
    CHATBOT_BACK,
    DEV_OP,
    HELP_BTN,
    HELP_READ,
    START,
    get_about_read,
    get_chatbot_read,
    get_tools_data_read,
)

IGNORE_COMMANDS = {
    "start", "aistart", "help", "repo", "ping", "stats", "id",
    "broadcast", "gcast", "chatbot", "status", "lang", "language",
    "setlang", "resetlang", "nolang", "shayri", "gf", "bf",
    "sari", "shari", "love", "test",
}


def not_bot_command(_, __, message: Message):
    if not message or not message.text:
        return True
    text = message.text.strip()
    if text.startswith("/"):
        cmd = text[1:].split("@")[0].split()[0].lower()
        if cmd in IGNORE_COMMANDS:
            return False
    return True


command_filter = filters.create(not_bot_command)


@YASHIKA.on_message(filters.command("status"))
async def status_command(client, message: Message):
    chat_id = message.chat.id
    current = await get_chatbot_status(chat_id)
    if current:
        await message.reply(f"Chatbot status: **{current}**")
    else:
        await message.reply("Status: **not set** (groups me default disabled)")


languages = {
    "english": "en", "hindi": "hi", "russian": "ru", "spanish": "es",
    "arabic": "ar", "turkish": "tr", "german": "de", "french": "fr",
    "italian": "it", "persian": "fa", "indonesian": "id", "portuguese": "pt",
    "korean": "ko", "japanese": "ja", "urdu": "ur", "bengali": "bn",
    "telugu": "te", "marathi": "mr", "gujarati": "gu", "kannada": "kn",
    "malayalam": "ml", "punjabi": "pa", "tamil": "ta",
}


def generate_language_buttons(languages_dict):
    buttons = []
    current_row = []
    for lang, code in languages_dict.items():
        current_row.append(
            InlineKeyboardButton(lang.capitalize(), callback_data=f"setlang_{code}")
        )
        if len(current_row) == 4:
            buttons.append(current_row)
            current_row = []
    if current_row:
        buttons.append(current_row)
    return InlineKeyboardMarkup(buttons)


@YASHIKA.on_message(filters.command(["lang", "language", "setlang"]))
async def set_language(client, message: Message):
    await message.reply_text(
        "Please select your chat language:",
        reply_markup=generate_language_buttons(languages),
    )


@YASHIKA.on_callback_query(filters.regex(r"^setlang_"))
async def language_selection_callback(client, callback_query: CallbackQuery):
    lang_code = callback_query.data.split("_")[1]
    chat_id = callback_query.message.chat.id
    if lang_code in languages.values():
        await set_chat_language(chat_id, lang_code)
        await callback_query.answer(f"Language set to {lang_code.title()}.", show_alert=True)
        await callback_query.message.edit_text(
            f"Chat language set to **{lang_code.title()}**."
        )
    else:
        await callback_query.answer("Invalid language.", show_alert=True)


@YASHIKA.on_message(filters.command(["resetlang", "nolang"]))
async def reset_language(client, message: Message):
    await set_chat_language(message.chat.id, "nolang")
    await message.reply_text("**Language reset to mixed.**")


@YASHIKA.on_message(filters.command("chatbot"))
async def chatbot_command(client, message: Message):
    chat_id = message.chat.id
    existing = await get_chatbot_status(chat_id)
    if not existing:
        await set_chatbot_status(chat_id, "disabled")
    await message.reply_text(
        f"Chat: {message.chat.title or 'Private'}\n**Enable / Disable chatbot:**",
        reply_markup=InlineKeyboardMarkup(CHATBOT_ON),
    )


@YASHIKA.on_callback_query()
async def cb_handler(client, query: CallbackQuery):
    data = query.data
    if not data:
        return

    if data == "HELP":
        await query.message.edit_text(
            text=HELP_READ,
            reply_markup=InlineKeyboardMarkup(HELP_BTN),
            disable_web_page_preview=True,
        )
    elif data == "CLOSE":
        await query.message.delete()
        await query.answer("Closed!", show_alert=True)
    elif data == "BACK":
        await query.message.edit(
            text=START.format(YASHIKA.mention or "Bot", 0, 0, "0s"),
            reply_markup=InlineKeyboardMarkup(DEV_OP),
        )
    elif data == "ABOUT":
        await query.message.edit(
            text=get_about_read(),
            reply_markup=InlineKeyboardMarkup(ABOUT_BTN),
            disable_web_page_preview=True,
        )
    elif data == "TOOLS_DATA":
        await query.message.edit(
            text=get_tools_data_read(),
            reply_markup=InlineKeyboardMarkup(CHATBOT_BACK),
        )
    elif data == "CHATBOT_CMD":
        await query.message.edit(
            text=get_chatbot_read(),
            reply_markup=InlineKeyboardMarkup(CHATBOT_BACK),
        )
    elif data == "CHATBOT_BACK":
        await query.message.edit(
            text=HELP_READ,
            reply_markup=InlineKeyboardMarkup(HELP_BTN),
        )
    elif data == "enable_chatbot":
        await set_chatbot_status(query.message.chat.id, "enabled")
        await query.answer("Chatbot Enabled ✅", show_alert=True)
        await query.edit_message_text(
            f"Chat: {query.message.chat.title or 'Private'}\n**Chatbot Enabled.**"
        )
    elif data == "disable_chatbot":
        await set_chatbot_status(query.message.chat.id, "disabled")
        await query.answer("Chatbot Disabled", show_alert=True)
        await query.edit_message_text(
            f"Chat: {query.message.chat.title or 'Private'}\n**Chatbot Disabled.**"
        )


# ==================== MAIN REPLY HANDLER ====================

@YASHIKA.on_message(filters.incoming & command_filter & \~filters.bot)
async def chatbot_response(client, message: Message):
    try:
        chat_id = message.chat.id
        is_private = message.chat.type == ChatType.PRIVATE
        is_group = message.chat.type in (ChatType.GROUP, ChatType.SUPERGROUP)

        # Status check
        status = await get_chatbot_status(chat_id)

        if is_group:
            if status != "enabled":
                return  # Group me sirf enabled hone pe reply
        # Private me hamesha allow

        if not message.text and not message.sticker:
            return

        # Learn from reply
        if message.reply_to_message and message.text:
            await _save_from_message(message.reply_to_message, message)

        # Decide whether to reply
        should_reply = False
        if is_private:
            should_reply = True
        elif message.reply_to_message and message.reply_to_message.from_user:
            if message.reply_to_message.from_user.id == YASHIKA.id:
                should_reply = True
        elif not message.reply_to_message:
            should_reply = True

        if not should_reply:
            return

        await client.send_chat_action(chat_id, ChatAction.TYPING)

        text = (message.text or "").strip()
        reply_data = await get_reply(text) if text else None

        if reply_data:
            response_text = reply_data["text"]
            chat_lang = await get_chat_language(chat_id)

            if chat_lang and chat_lang != "nolang":
                try:
                    response_text = GoogleTranslator(
                        source="auto", target=chat_lang
                    ).translate(response_text)
                except Exception:
                    pass

            check = reply_data.get("check", "none")
            if check == "sticker":
                await message.reply_sticker(reply_data["text"])
            elif check == "photo":
                await message.reply_photo(reply_data["text"])
            elif check == "video":
                await message.reply_video(reply_data["text"])
            elif check == "audio":
                await message.reply_audio(reply_data["text"])
            elif check == "gif":
                await message.reply_animation(reply_data["text"])
            else:
                await message.reply_text(response_text)
        else:
            # Empty DB hone pe bhi reply do (testing ke liye)
            defaults = [
                "Haan bolo?",
                "Kya hua?",
                "Samajh nahi aaya 😅",
                "Phir se bolo?",
                "Hmm...",
                "Ji?",
            ]
            await message.reply_text(random.choice(defaults))

        # Track user/chat
        if is_group:
            await add_served_chat(chat_id)
        elif message.from_user:
            await add_served_user(message.from_user.id)

    except MessageEmpty:
        try:
            await message.reply_text("...")
        except Exception:
            pass
    except Exception as e:
        LOGGER.error(f"chatbot_response error: {e}")


async def _save_from_message(original_message: Message, reply_message: Message):
    try:
        if not original_message or not original_message.text:
            return
        word = original_message.text.strip()
        if not word:
            return

        if reply_message.sticker:
            await save_reply(word, reply_message.sticker.file_id, "sticker")
        elif reply_message.photo:
            await save_reply(word, reply_message.photo.file_id, "photo")
        elif reply_message.video:
            await save_reply(word, reply_message.video.file_id, "video")
        elif reply_message.audio:
            await save_reply(word, reply_message.audio.file_id, "audio")
        elif reply_message.animation:
            await save_reply(word, reply_message.animation.file_id, "gif")
        elif reply_message.text:
            await save_reply(word, reply_message.text.strip(), "none")
    except Exception as e:
        LOGGER.error(f"save_reply error: {e}")
# ==================== TEMPORARY TEST HANDLER ====================

@YASHIKA.on_message(filters.private & filters.text & \~filters.command(["start", "help", "ping", "test", "stats", "id", "chatbot", "lang", "status", "repo", "shayri"]))
async def simple_private_reply(client, message: Message):
    try:
        await message.reply_text(f"Main alive hoon! ✅\nTumne likha: `{message.text}`")
    except Exception as e:
        LOGGER.error(f"simple_private_reply error: {e}")
