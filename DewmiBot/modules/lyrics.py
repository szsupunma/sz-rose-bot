import io
import os
import requests
from pyrogram import filters

from pyrogram import Client
from pyrogram import Client as pbot

#dont edit credits i will fuck you 🤣 Made by me for @szrosebot ~ youtubeslgeekshow



@pbot.on_message(filters.command(["lyric", "lyrics"]))
async def liri(client, message):
    try:
        if len(message.command) < 2:
            await message.reply_text("**give a lyric name too !**")
            return
        query = message.text.split(None, 1)[1]
        rep = await message.reply_text("🔎 **searching lyrics...**")
        resp = requests.get(f"https://api-tede.herokuapp.com/api/lirik?l={query}").json()
        result = f"{resp['data']}"
        await rep.edit(result)
    except Exception:
        await rep.edit("**Lyrics not found.** please give a valid song name !!!")
