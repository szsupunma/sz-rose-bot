import github  # pyGithub
from pyrogram import filters

from DewmiBot.services.pyrogram import pbot as client

  
    
@client.on_message(filters.command("contributors") & ~filters.edited)
async def give_cobtribs(c, m):
    g = github.Github()
    co = ""
    n = 0
    repo = g.get_repo("youtubeslgeekshow/sz-rose-bot")
    for i in repo.get_contributors():
        n += 1
        co += f"{n}. [{i.login}](https://github.com/{i.login})\n"
    t = f"**Szrosebot Contributors**\n\n{co}\n\n\nA Powerful BOT to Make Your Groups Secured and Organized ! ✨"
    await m.reply(t, disable_web_page_preview=True)
    
__help__ = """
@szrosebot🇱🇰
Contributor
 ❍ /contributors : contributors using this bot  
"""
__mod_name__ = "ᴄᴏɴᴛʀɪʙᴜᴛᴇ🪗"
