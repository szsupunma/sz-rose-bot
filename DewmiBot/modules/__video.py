# Copyright (C) 2021 By VeezMusicProject
# thank you i get your codes for my szrosebot 

from __future__ import unicode_literals

import asyncio
import math
import os
import time
import wget
from random import randint
from urllib.parse import urlparse

import aiofiles
import aiohttp
import requests
import youtube_dl
from yt_dlp import YoutubeDL
from pyrogram import Client, filters
from pyrogram.errors import FloodWait, MessageNotModified
from pyrogram.types import *
from youtube_search import YoutubeSearch

from DewmiBot.config import get_str_key
from DewmiBot import pbot

@pbot.on_message(filters.command(["video"]))
async def vsong(pbot, message):
    ydl_opts = {
        'format':'best',
        'keepvideo':True,
        'prefer_ffmpeg':False,
        'geo_bypass':True,
        'outtmpl':'%(title)s.%(ext)s',
        'quite':True
    }
    query = " ".join(message.command[1:])
    try:
        results = YoutubeSearch(query, max_results=1).to_dict()
        link = f"https://youtube.com{results[0]['url_suffix']}"
        title = results[0]["title"][:40]
        thumbnail = results[0]["thumbnails"][0]
        thumb_name = f"thumb{title}.jpg"
        thumb = requests.get(thumbnail, allow_redirects=True)
        open(thumb_name, "wb").write(thumb.content)
        duration = results[0]["duration"]
        results[0]["url_suffix"]
        results[0]["views"]
        rby = message.from_user.mention
    except Exception as e:
        print(e)
    try:
        msg = await message.reply("📥 **downloading video...**")
        with YoutubeDL(ydl_opts) as ytdl:
            ytdl_data = ytdl.extract_info(link, download=True)
            file_name = ytdl.prepare_filename(ytdl_data)
    except Exception as e:
        return await msg.edit(f"❌**YouTube Download Error !*** {str(e)}\n\n Go support chat👉 @slbotzone")
    preview = wget.download(thumbnail)
    await msg.edit("📤 **uploading video...**")
    await message.reply_video(
        file_name,
        duration=int(ytdl_data["duration"]),
        thumb=preview,
        caption=ytdl_data['title'],
        reply_markup=InlineKeyboardMarkup([[InlineKeyboardButton("Join updates", url=f"https://t.me/szroseupdates")]]))
    try:
        os.remove(file_name)
        await msg.delete()
    except Exception as e:
        print(e)

        
