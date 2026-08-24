"""
SQLite Database Layer (No MongoDB)
Uses aiosqlite for full async support.
"""

import aiosqlite
import os
from typing import Optional, List, Dict, Any
import config
from YASHIKA import LOGGER

DB_PATH = config.DB_PATH


async def _get_db():
    os.makedirs(os.path.dirname(DB_PATH) if os.path.dirname(DB_PATH) else ".", exist_ok=True)
    db = await aiosqlite.connect(DB_PATH)
    db.row_factory = aiosqlite.Row
    return db


async def init_db():
    """Create all tables if they don't exist."""
    db = await _get_db()
    try:
        await db.executescript(
            """
            CREATE TABLE IF NOT EXISTS users (
                user_id INTEGER PRIMARY KEY
            );

            CREATE TABLE IF NOT EXISTS chats (
                chat_id INTEGER PRIMARY KEY
            );

            CREATE TABLE IF NOT EXISTS chatbot_status (
                chat_id INTEGER PRIMARY KEY,
                status TEXT DEFAULT 'disabled'
            );

            CREATE TABLE IF NOT EXISTS chat_lang (
                chat_id INTEGER PRIMARY KEY,
                language TEXT DEFAULT 'en'
            );

            CREATE TABLE IF NOT EXISTS word_replies (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                word TEXT NOT NULL,
                text TEXT NOT NULL,
                check_type TEXT DEFAULT 'none'
            );

            CREATE INDEX IF NOT EXISTS idx_word ON word_replies(word);
            """
        )
        await db.commit()
        LOGGER.info("SQLite database initialized successfully.")
    finally:
        await db.close()


# ==================== USERS ====================

async def add_served_user(user_id: int):
    db = await _get_db()
    try:
        await db.execute(
            "INSERT OR IGNORE INTO users (user_id) VALUES (?)", (user_id,)
        )
        await db.commit()
    finally:
        await db.close()


async def get_served_users() -> List[Dict]:
    db = await _get_db()
    try:
        cursor = await db.execute("SELECT user_id FROM users WHERE user_id > 0")
        rows = await cursor.fetchall()
        return [{"user_id": row["user_id"]} for row in rows]
    finally:
        await db.close()


async def is_served_user(user_id: int) -> bool:
    db = await _get_db()
    try:
        cursor = await db.execute(
            "SELECT 1 FROM users WHERE user_id = ?", (user_id,)
        )
        return await cursor.fetchone() is not None
    finally:
        await db.close()


# ==================== CHATS ====================

async def add_served_chat(chat_id: int):
    db = await _get_db()
    try:
        await db.execute(
            "INSERT OR IGNORE INTO chats (chat_id) VALUES (?)", (chat_id,)
        )
        await db.commit()
    finally:
        await db.close()


async def get_served_chats() -> List[Dict]:
    db = await _get_db()
    try:
        cursor = await db.execute("SELECT chat_id FROM chats WHERE chat_id < 0")
        rows = await cursor.fetchall()
        return [{"chat_id": row["chat_id"]} for row in rows]
    finally:
        await db.close()


async def is_served_chat(chat_id: int) -> bool:
    db = await _get_db()
    try:
        cursor = await db.execute(
            "SELECT 1 FROM chats WHERE chat_id = ?", (chat_id,)
        )
        return await cursor.fetchone() is not None
    finally:
        await db.close()


async def remove_served_chat(chat_id: int):
    db = await _get_db()
    try:
        await db.execute("DELETE FROM chats WHERE chat_id = ?", (chat_id,))
        await db.commit()
    finally:
        await db.close()


# ==================== CHATBOT STATUS ====================

async def get_chatbot_status(chat_id: int) -> Optional[str]:
    db = await _get_db()
    try:
        cursor = await db.execute(
            "SELECT status FROM chatbot_status WHERE chat_id = ?", (chat_id,)
        )
        row = await cursor.fetchone()
        return row["status"] if row else None
    finally:
        await db.close()


async def set_chatbot_status(chat_id: int, status: str):
    db = await _get_db()
    try:
        await db.execute(
            """
            INSERT INTO chatbot_status (chat_id, status) VALUES (?, ?)
            ON CONFLICT(chat_id) DO UPDATE SET status = excluded.status
            """,
            (chat_id, status),
        )
        await db.commit()
    finally:
        await db.close()


# ==================== LANGUAGE ====================

async def get_chat_language(chat_id: int) -> str:
    db = await _get_db()
    try:
        cursor = await db.execute(
            "SELECT language FROM chat_lang WHERE chat_id = ?", (chat_id,)
        )
        row = await cursor.fetchone()
        return row["language"] if row else "en"
    finally:
        await db.close()


async def set_chat_language(chat_id: int, language: str):
    db = await _get_db()
    try:
        await db.execute(
            """
            INSERT INTO chat_lang (chat_id, language) VALUES (?, ?)
            ON CONFLICT(chat_id) DO UPDATE SET language = excluded.language
            """,
            (chat_id, language),
        )
        await db.commit()
    finally:
        await db.close()


# ==================== WORD REPLIES (Learning) ====================

async def save_reply(word: str, text: str, check_type: str = "none"):
    """Save a learned reply. Avoid exact duplicates."""
    if not word or not text:
        return
    db = await _get_db()
    try:
        cursor = await db.execute(
            "SELECT 1 FROM word_replies WHERE word = ? AND text = ? AND check_type = ?",
            (word, text, check_type),
        )
        if await cursor.fetchone():
            return
        await db.execute(
            "INSERT INTO word_replies (word, text, check_type) VALUES (?, ?, ?)",
            (word, text, check_type),
        )
        await db.commit()
    finally:
        await db.close()


async def get_reply(word: str) -> Optional[Dict[str, Any]]:
    """
    Get a random reply for the given word.
    1. Exact match first
    2. Partial / contains match as fallback
    """
    if not word:
        return None
    db = await _get_db()
    try:
        # Exact match
        cursor = await db.execute(
            "SELECT text, check_type FROM word_replies WHERE word = ? ORDER BY RANDOM() LIMIT 1",
            (word,),
        )
        row = await cursor.fetchone()
        if row:
            return {"text": row["text"], "check": row["check_type"]}

        # Partial match (word contains or is contained)
        cursor = await db.execute(
            """
            SELECT text, check_type FROM word_replies
            WHERE word LIKE ? OR ? LIKE '%' || word || '%'
            ORDER BY RANDOM() LIMIT 1
            """,
            (f"%{word}%", word),
        )
        row = await cursor.fetchone()
        if row:
            return {"text": row["text"], "check": row["check_type"]}

        return None
    finally:
        await db.close()
