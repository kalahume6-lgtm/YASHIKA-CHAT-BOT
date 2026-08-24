from pyrogram.types import InlineKeyboardButton
from config import SUPPORT_GRP, UPDATE_CHNL, OWNER_ID, OWNER_USERNAME
from YASHIKA import YASHIKA


def _owner_id():
    return OWNER_ID or 777000


def _support():
    return SUPPORT_GRP or "RU_DRA_098"


def _update():
    return UPDATE_CHNL or SUPPORT_GRP or "RU_DRA_098"


def _username():
    return YASHIKA.username or "YASHIKA_CHAT_BOT"


def _owner_uname():
    return OWNER_USERNAME or "KARTIK_NISHAD_3"


def get_start_bot():
    return [
        [
            InlineKeyboardButton(
                text="➕ Add me to group",
                url=f"https://t.me/{_username()}?startgroup=true",
            ),
        ],
        [
            InlineKeyboardButton(text="👑 Owner", user_id=_owner_id()),
            InlineKeyboardButton(text="💬 Support", url=f"https://t.me/{_support()}"),
        ],
        [
            InlineKeyboardButton(text="📖 Features", callback_data="HELP"),
        ],
    ]


DEV_OP = [
    [InlineKeyboardButton(text="Help", callback_data="HELP")],
    [InlineKeyboardButton(text="About", callback_data="ABOUT")],
]

BACK = [[InlineKeyboardButton(text="🔙 Back", callback_data="BACK")]]

HELP_BTN = [
    [
        InlineKeyboardButton(text="🤖 Chatbot", callback_data="CHATBOT_CMD"),
        InlineKeyboardButton(text="🛠 Tools", callback_data="TOOLS_DATA"),
    ],
    [InlineKeyboardButton(text="❌ Close", callback_data="CLOSE")],
]

CLOSE_BTN = [[InlineKeyboardButton(text="❌ Close", callback_data="CLOSE")]]

CHATBOT_ON = [
    [
        InlineKeyboardButton(text="✅ Enable", callback_data="enable_chatbot"),
        InlineKeyboardButton(text="❌ Disable", callback_data="disable_chatbot"),
    ],
]

CHATBOT_BACK = [
    [
        InlineKeyboardButton(text="🔙 Back", callback_data="CHATBOT_BACK"),
        InlineKeyboardButton(text="❌ Close", callback_data="CLOSE"),
    ],
]

ABOUT_BTN = [
    [
        InlineKeyboardButton(text="💬 Support", url=f"https://t.me/{_support()}"),
        InlineKeyboardButton(text="📖 Help", callback_data="HELP"),
    ],
    [
        InlineKeyboardButton(text="👑 Owner", user_id=_owner_id()),
    ],
    [
        InlineKeyboardButton(text="📢 Updates", url=f"https://t.me/{_update()}"),
        InlineKeyboardButton(text="🔙 Back", callback_data="BACK"),
    ],
]


# ==================== TEXTS ====================

START = (
    "**"
    "{} ᴛʜᴇ sᴜᴘᴇʀғᴀsᴛ ᴄʜᴀᴛʙᴏᴛ 💞\n\n"
    "➪ sᴜᴘᴘᴏʀᴛs ᴛᴇxᴛ, sᴛɪᴄᴋᴇʀ, ᴘʜᴏᴛᴏ, ᴠɪᴅᴇᴏ...\n"
    "➪ ᴍᴜʟᴛɪ-ʟᴀɴɢᴜᴀɢᴇ ғᴏʀ ᴇᴀᴄʜ ᴄʜᴀᴛ /lang\n"
    "➪ ᴄʜᴀᴛʙᴏᴛ ᴇɴᴀʙʟᴇᴅ/ᴅɪsᴀʙʟᴇᴅ ʙʏ /chatbot\n"
    "➪ ᴅᴀᴛᴀʙᴀsᴇ: **SQLite** (No MongoDB)\n\n"
    "๏ ᴛᴏᴛᴀʟ ᴜsᴇʀs : {}\n"
    "๏ ᴛᴏᴛᴀʟ ᴄʜᴀᴛs : {}\n"
    "๏ ᴜᴘᴛɪᴍᴇ » {}\n\n"
    "╔═════════╗\n"
    "║ ➻ ʀᴇᴘᴏ ➪ [Cʟɪᴄᴋ Hᴇʀᴇ](https://github.com/kalahume6-lgtm/YASHIKA-CHAT-BOT)\n"
    f"║ ➻ ᴄʀᴇᴀᴛᴏʀ ➪ [Oᴡɴᴇʀ](https://t.me/{_owner_uname()})\n"
    "╚═════════╝\n"
    "**"
)

HELP_READ = (
    "**\n"
    "Cʟɪᴄᴋ ᴏɴ ᴛʜᴇ ʙᴜᴛᴛᴏɴs ʙᴇʟᴏᴡ ғᴏʀ ᴍᴏʀᴇ ɪɴғᴏʀᴍᴀᴛɪᴏɴ.\n"
    f"Iғ ʏᴏᴜ'ʀᴇ ғᴀᴄɪɴɢ ᴀɴʏ ᴘʀᴏʙʟᴇᴍ ᴀsᴋ ɪɴ [sᴜᴘᴘᴏʀᴛ](https://t.me/{_support()}).\n\n"
    "Aʟʟ ᴄᴏᴍᴍᴀɴᴅs ᴄᴀɴ ʙᴇ ᴜsᴇᴅ ᴡɪᴛʜ: /**\n"
    "**"
)

SOURCE_READ = (
    "**ʜᴇʏ, ᴛʜᴇ sᴏᴜʀᴄᴇ ᴄᴏᴅᴇ ɪs ɢɪᴠᴇɴ ʙᴇʟᴏᴡ.**\n"
    "**ᴘʟᴇᴀsᴇ ғᴏʀᴋ ᴛʜᴇ ʀᴇᴘᴏ & ɢɪᴠᴇ ᴛʜᴇ sᴛᴀʀ ✯**\n"
    "**──────────────────**\n"
    "**ʜᴇʀᴇ ɪs ᴛʜᴇ [sᴏᴜʀᴄᴇ ᴄᴏᴅᴇ](https://github.com/kalahume6-lgtm/YASHIKA-CHAT-BOT)**\n"
    "**──────────────────**\n"
    f"**ɪғ ʏᴏᴜ ғᴀᴄᴇ ᴀɴʏ ᴘʀᴏʙʟᴇᴍ ᴄᴏɴᴛᴀᴄᴛ [sᴜᴘᴘᴏʀᴛ](https://t.me/{_support()}).**\n"
    f"**||📡 ᴍᴀᴅᴇ ʙʏ ➪ [Oᴡɴᴇʀ](https://t.me/{_owner_uname()}) 💞||**"
)


def get_tools_data_read():
    return (
        f"**\n"
        f"๏ Commands for {YASHIKA.mention}:\n\n"
        "➻ /start - Wake up the bot\n"
        "──────────────\n"
        "➻ /help - All commands & features\n"
        "──────────────\n"
        "➻ /ping - Check response time\n"
        "──────────────\n"
        "➻ /id - Get User ID, Chat ID, Message ID\n"
        "──────────────\n"
        "➻ /broadcast - Broadcast message (Owner only)\n"
        "──────────────\n"
        "➻ /shayri - Random Shayri\n"
        "──────────────\n"
        "➻ /repo - Source code\n"
        "──────────────\n"
        f"๏ Made by ➪ [Owner](https://t.me/{_owner_uname()}) 💞**"
    )


def get_chatbot_read():
    return (
        f"**\n"
        f"๏ Chatbot Commands for {YASHIKA.mention}:\n\n"
        "➻ /chatbot - Enable or Disable chatbot\n"
        "──────────────\n"
        "➻ /lang /language /setlang - Select chat language\n"
        "──────────────\n"
        "➻ /resetlang /nolang - Reset to mixed language\n"
        "──────────────\n"
        "➻ /status - Check chatbot status\n"
        "──────────────\n"
        f"📡 Made by ➪ [Owner](https://t.me/{_owner_uname()}) 💞**"
    )


def get_about_read():
    return (
        f"**\n"
        f"➻ [{YASHIKA.name}](https://t.me/{YASHIKA.username}) is an advanced chat-bot.\n"
        f"➻ Automatically replies to users by learning.\n"
        "➻ Helps activate your groups.\n"
        "➻ Written in Python with **SQLite** as database (No MongoDB needed)\n"
        "──────────────\n"
        f"➻ Click buttons below for help and info about [{YASHIKA.name}](https://t.me/{YASHIKA.username})\n"
        "**"
    )
