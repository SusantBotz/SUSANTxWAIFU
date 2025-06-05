from NOBITA import *
from telegram import Update
from telegram.ext import CommandHandler, CallbackContext, MessageHandler, filters, ContextTypes
import asyncio
import time

# Global in-memory storage (in production, consider persistent cache)
warned_users = {}
user_cooldowns = {}
last_user = {}
normal_message_counts = {}
locks = {}

async def message_counter(update: Update, context: CallbackContext) -> None:
    chat_id = str(update.effective_chat.id)
    user_id = update.effective_user.id
    current_time = time.time()

    # Fetch or initialize group ctime setting
    existing_group = await group_user_totals_collection.find_one({"group_id": chat_id})
    if not existing_group:
        await group_user_totals_collection.update_one(
            {"group_id": chat_id},
            {"$set": {"group_id": chat_id, "ctime": 80}},  # default ctime
            upsert=True
        )
        ctime = 80
    else:
        ctime = existing_group.get("ctime", 80)

    # Lock per group
    if chat_id not in locks:
        locks[chat_id] = asyncio.Lock()
    lock = locks[chat_id]

    async with lock:
        # Cooldown logic
        if user_id in user_cooldowns:
            if current_time < user_cooldowns[user_id]:
                return
            else:
                del user_cooldowns[user_id]

        # Anti-spam check
        if chat_id in last_user and last_user[chat_id]['user_id'] == user_id:
            last_user[chat_id]['count'] += 1
            if last_user[chat_id]['count'] >= 10:
                if user_id not in warned_users or current_time - warned_users[user_id] >= 600:
                    user_cooldowns[user_id] = current_time + 600  # 10 minutes cooldown
                    warned_users[user_id] = current_time
                    await update.message.reply_text(
                        f"⚠️ Don't spam {update.effective_user.first_name}...\n"
                        "Your messages will be ignored for 10 minutes."
                    )
                return
        else:
            last_user[chat_id] = {'user_id': user_id, 'count': 1}

        # Message counting
        normal_message_counts[chat_id] = normal_message_counts.get(chat_id, 0) + 1

        if normal_message_counts[chat_id] % ctime == 0:
            await send_image(update, context)
            normal_message_counts[chat_id] = 0

# Add message handler
application.add_handler(MessageHandler(~filters.COMMAND, message_counter))
