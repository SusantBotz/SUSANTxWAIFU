from pymongo import ReturnDocument
from NOBITA import app gaming_group_total
from pyrogram import filters
from pyrogram.types import Message
from NOBITA.pro import sudo_filter


# In-memory dictionary to track message counts per user per chat
chat_message_counts = {}  # {chat_id: {user_id: count}}

@app.on_message(filters.command("ctime") & sudo_filter)
async def change_time_sudo(client, message: Message):
    try:
        args = message.text.split(maxsplit=1)[1:]
        if len(args) != 1 or not args[0].isdigit():
            await message.reply_text('❌ Incorrect format. Please use: /ctime NUMBER')
            return

        new_frequency = int(args[0])
        if new_frequency < 1:
            await message.reply_text('❌ The message frequency must be greater than or equal to 1.')
            return
        if new_frequency > 10000:
            await message.reply_text('❌ The message frequency must be below 10,000.')
            return

        # Update the message_frequency in MongoDB for this chat
        await gaming_group_total.find_one_and_update(
            {'chat_id': message.chat.id},
            {'$set': {'message_frequency': new_frequency}},
            upsert=True,
            return_document=ReturnDocument.AFTER
        )

        await message.reply_text(f'✅ Successfully changed character appearance frequency to every {new_frequency} messages.')
    except Exception as e:
        await message.reply_text(f'❌ Failed to change character appearance frequency.\nError: {str(e)}')


@app.on_message(filters.chat & ~filters.command)
async def track_user_messages(client, message: Message):
    chat_id = message.chat.id
    user_id = message.from_user.id

    # Fetch chat settings from DB or default to frequency=1
    chat_settings = await gaming_group_total.find_one({'chat_id': chat_id}) or {}
    message_frequency = chat_settings.get('message_frequency', 1)

    if chat_id not in chat_message_counts:
        chat_message_counts[chat_id] = {}

    user_count = chat_message_counts[chat_id].get(user_id, 0) + 1
    chat_message_counts[chat_id][user_id] = user_count

    # When user reaches the message frequency, reset count and spawn character
    if user_count >= message_frequency:
        chat_message_counts[chat_id][user_id] = 0
        # Your spawn character logic here, e.g.:
        # await spawn_character_for_user(chat_id, user_id)
        print(f"Spawn character for user {user_id} in chat {chat_id}")
