#    Hitsuki (A telegram bot project)

#    This program is free software: you can redistribute it and/or modify
#    it under the terms of the GNU General Public License as published by
#    the Free Software Foundation, either version 3 of the License, or
#    (at your option) any later version.

#    This program is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU General Public License for more details.

#    You should have received a copy of the GNU General Public License
#    along with this program.  If not, see <https://www.gnu.org/licenses/>.


import re
from random import choice

import requests
from bs4 import BeautifulSoup
from DewmiBot import pbot
from pyrogram import Client, filters
from pyrogram.types import Update


@pbot.on_message(filters.command("direct"))
async def direct_link_generator(c: Client, update: Update):
    if not len(update.command) == 2:
        m = "Usage: `/direct <url>`"
        await update.reply_text(
            parse_mode="md",
            text=m)
        return

    text = update.command[1]
    if text:
        links = re.findall(r'\bhttps?://.*\.\S+', text)
    else:
        return
    reply = []
    if not links:
        await update.reply_text("No links found!")
        return
    for link in links:
        if 'sourceforge.net' in link:
            reply.append(sourceforge(link))
        else:
            reply.append(re.findall(
                r"\bhttps?://(.*?[^/]+)", link)[0] + ' is not supported')

    await update.reply_text("\n".join(reply))


def sourceforge(url: str) -> str:
    try:
        link = re.findall(r'\bhttps?://.*sourceforge\.net\S+', url)[0]
    except IndexError:
        reply = "No SourceForge links found\n"
        return reply
    file_path = re.findall(r'/files(.*)/download', link)
    if not file_path:
        file_path = re.findall(r'/files(.*)', link)
    file_path = file_path[0]
    reply = f"Mirrors for <code>{file_path.split('/')[-1]}</code>\n"
    project = re.findall(r'projects?/(.*?)/files', link)[0]
    mirrors = f'https://sourceforge.net/settings/mirror_choices?' \
        f'projectname={project}&filename={file_path}'
    page = BeautifulSoup(requests.get(mirrors).content, 'lxml')
    info = page.find('ul', {'id': 'mirrorList'}).findAll('li')
    for mirror in info[1:]:
        name = re.findall(r'\((.*)\)', mirror.text.strip())[0]
        dl_url = f'https://{mirror["id"]}.dl.sourceforge.net/project/{project}/{file_path}'
        reply += f'<a href="{dl_url}">{name}</a> '
    return reply


def useragent():
    useragents = BeautifulSoup(
        requests.get(
            'https://developers.whatismybrowser.com/'
            'useragents/explore/operating_system_name/android/').content,
        'lxml').findAll('td', {'class': 'useragent'})
    user_agent = choice(useragents)
    return user_agent.text


__help__ = """
@szrosebot🇱🇰
 ❍ /direct - get any file useing link
"""
__mod_name__ = "ᴅ-ʟɪɴᴋ🖇️"
