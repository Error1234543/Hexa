import os
import asyncio
import aiohttp
import time
import subprocess
from pyrogram import Client, filters
from pyrogram.types import Message
from utils import *

API_ID = int(os.getenv("API_ID", ""))
API_HASH = os.getenv("API_HASH", "")
BOT_TOKEN = os.getenv("BOT_TOKEN", "")
OWNER_ID = int(os.getenv("OWNER_ID", ""))
ALLOWED_GROUP = int(os.getenv("ALLOWED_GROUP", ""))
START_TEXT = "engine start successful ☠️  🍫🍫 eat do 🚫"

authorized_users = set()

app = Client("bot", api_id=API_ID, api_hash=API_HASH, bot_token=BOT_TOKEN)

@app.on_message(filters.command("start"))
async def start(client, message: Message):
    await message.reply_text(START_TEXT)

@app.on_message(filters.command("sonic"))
async def authorize_user(client, message: Message):
    if message.from_user.id != OWNER_ID:
        return await message.reply("You are not authorized to use this command.")
    try:
        user_id = int(message.text.split(" ", 1)[1])
        add_authorized_user(user_id, authorized_users)
        await message.reply(f"User {user_id} authorized ✅")
    except:
        await message.reply("Format: /sonic <user_id>")

@app.on_message(filters.command("yl"))
async def m3u8_handler(client, message: Message):
    if not is_authorized(message.from_user.id, message.chat.id, OWNER_ID, ALLOWED_GROUP, authorized_users):
        return await message.reply("You are not authorized.")
    url = message.text.split(" ", 1)[1]
    filename = extract_filename(url) + ".mp4"
    output_path = f"./{filename}"
    cmd = ["yt-dlp", "-o", output_path, url]
    proc = await asyncio.create_subprocess_exec(*cmd)
    await proc.wait()
    await message.reply_video(video=output_path, caption="Uploaded ✅")
    os.remove(output_path)

@app.on_message(filters.command("l"))
async def pdf_handler(client, message: Message):
    if not is_authorized(message.from_user.id, message.chat.id, OWNER_ID, ALLOWED_GROUP, authorized_users):
        return await message.reply("You are not authorized.")
    url = message.text.split(" ", 1)[1]
    filename = extract_filename(url) + ".pdf"
    async with aiohttp.ClientSession() as session:
        async with session.get(url) as resp:
            with open(filename, "wb") as f:
                f.write(await resp.read())
    await message.reply_document(document=filename, caption="Uploaded ✅")
    os.remove(filename)

@app.on_message(filters.command("stats"))
async def stats_handler(client, message: Message):
    uptime = format_time(time.time() - psutil.boot_time())
    cpu = psutil.cpu_percent()
    ram = psutil.virtual_memory().percent
    await message.reply(f"🖥️ CPU: {cpu}%
💾 RAM: {ram}%
⏱️ Uptime: {uptime}")

@app.on_message(filters.command("cancel"))
async def cancel_handler(client, message: Message):
    await message.reply("Cancel not implemented in this version.")

app.run()
