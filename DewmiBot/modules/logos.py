from DewmiBot.events import register
from DewmiBot import OWNER_ID
from DewmiBot import telethn as tbot
import os 
from PIL import Image, ImageDraw, ImageFont
import shutil 
import random, re
import glob

import time
from telethon.tl.types import InputMessagesFilterPhotos



TELEGRAPH_MEDIA_LINKS = ["./DewmiBot/resources/download (1).jfif", 
                         "./DewmiBot/resources/download (1).png", 
                         "./DewmiBot/resources/download (2).jfif",
                         "./DewmiBot/resources/download (2).png",
                         "./DewmiBot/resources/download (3).jfif",    
                         "./DewmiBot/resources/download (4).jfif", 
                         "./DewmiBot/resources/download (5).jfif",
                         "./DewmiBot/resources/download (7).jfif",
                         "./DewmiBot/resources/download.jfif",
                         "./DewmiBot/resources/download.png", 
                         "./DewmiBot/resources/images (1).jfif",
                         "./DewmiBot/resources/images (2).jfif",
                         "./DewmiBot/resources/images (3).jfif",
                         "./DewmiBot/resources/images (4).jfif", 
                         "./DewmiBot/resources/images (5).jfif",
                         "./DewmiBot/resources/images (6).jfif",
                         "./DewmiBot/resources/images (7).jfif",     
                         "./DewmiBot/resources/images (8).jfif", 
                         "./DewmiBot/resources/images (9).jfif",
                         "./DewmiBot/resources/images.jfif",
                         "./DewmiBot/resources/images.png"
                         ]

@register(pattern="^/logo ?(.*)")
async def lego(event):
 quew = event.pattern_match.group(1)
 if event.sender_id == OWNER_ID:
     pass
 else:

    if not quew:
       await event.reply('Provide Some Text To Draw!')
       return
    else:
       pass
 await event.reply('Wait..now ok!')
 try:
    text = event.pattern_match.group(1)
    img = Image.open(random.choice(TELEGRAPH_MEDIA_LINKS))
    draw = ImageDraw.Draw(img)
    image_widthz, image_heightz = img.size
    pointsize = 25
    fillcolor = "gold"
    shadowcolor = "blue"
    font = ImageFont.truetype("./DewmiBot/resources/font.otf",40)
    w, h = draw.textsize(text, font=font)
    h += int(h*0.21)
    image_width, image_height = img.size
    draw.text(((image_widthz-w)/2, (image_heightz-h)/2), text, font=font, fill=(255, 255, 255))
    x = (image_widthz-w)/2
    y= ((image_heightz-h)/2+6)
    draw.text((x, y), text, font=font, fill="black", stroke_width=2, stroke_fill="yellow")
    fname2 = "Logo.png"
    img.save(fname2, "png")
    await tbot.send_file(event.chat_id, fname2, caption="Made By @szrosebot🇱🇰")
    if os.path.exists(fname2):
            os.remove(fname2)
 except Exception as e:
   await event.reply(f'Join with us ~ @sl_bot_zone to use this, {e}')


@register(pattern="^/wlogo ?(.*)")
async def logo(event):
 quew = event.pattern_match.group(1)
 if event.sender_id == OWNER_ID:
     pass
 else:

    if not quew:
       await event.reply('Provide Some Text To Draw!')
       return
    else:
       pass
 await event.reply('Creating your logo...wait!')
 try:
    text = event.pattern_match.group(1)
    img = Image.open('./DewmiBot/resources/photo_2021-08-21_23-14-49.png')
    draw = ImageDraw.Draw(img)
    image_widthz, image_heightz = img.size
    pointsize = 500
    fillcolor = "white"
    shadowcolor = "blue"
    font = ImageFont.truetype("./DewmiBot/resources/Maghrib.ttf", 1000)
    w, h = draw.textsize(text, font=font)
    h += int(h*0.21)
    image_width, image_height = img.size
    draw.text(((image_widthz-w)/2, (image_heightz-h)/2), text, font=font, fill=(255, 255, 255))
    x = (image_widthz-w)/2
    y= ((image_heightz-h)/2+6)
    draw.text((x, y), text, font=font, fill="white", stroke_width=0, stroke_fill="white")
    fname2 = "Logo.png"
    img.save(fname2, "png")
    await tbot.send_file(event.chat_id, fname2, caption="Made By @szrosebot🇱🇰")
    if os.path.exists(fname2):
            os.remove(fname2)
 except Exception as e:
   await event.reply(f'Join with us ~ @sl_bot_zone to use this, {e}')

  

@register(pattern="^/pandalogo ?(.*)")
async def lego(event):
 quew = event.pattern_match.group(1)
 if event.sender_id == OWNER_ID:
     pass
 else:

    if not quew:
       await event.reply('Provide Some Text To Draw!')
       return
    else:
       pass
 await event.reply('Creating your logo...wait!')
 try:
    text = event.pattern_match.group(1)
    img = Image.open('./DewmiBot/resources/pandabg.png')
    draw = ImageDraw.Draw(img)
    image_widthz, image_heightz = img.size
    pointsize = 25
    fillcolor = "gold"
    shadowcolor = "blue"
    font = ImageFont.truetype("./DewmiBot/resources/font.otf", 100)
    w, h = draw.textsize(text, font=font)
    h += int(h*0.21)
    image_width, image_height = img.size
    draw.text(((image_widthz-w)/2, (image_heightz-h)/2), text, font=font, fill=(255, 255, 255))
    x = (image_widthz-w)/2
    y= ((image_heightz-h)/2+6)
    draw.text((x, y), text, font=font, fill="black", stroke_width=25, stroke_fill="yellow")
    fname2 = "Logo.png"
    img.save(fname2, "png")
    await tbot.send_file(event.chat_id, fname2, caption="Made By @szrosebot🇱🇰")
    if os.path.exists(fname2):
            os.remove(fname2)
 except Exception as e:
   await event.reply(f'Join with us ~ @sl_bot_zone to use this, {e}')
  
file_help = os.path.basename(__file__)
file_help = file_help.replace(".py", "")
file_helpo = file_help.replace("_", " ")


__help__ = """
@szrosebot🇱🇰
 ❍ /logo text :  Create your logo with your name
 ❍ /wlogo text :  Create your logo with your name
 ❍ /pandalogo :  Create your logo with your name
 """
__mod_name__ = "Logo Maker"
