import asyncio
import time

from telethon import events
from telethon.errors.rpcerrorlist import MessageDeleteForbiddenError
from telethon.tl.types import ChannelParticipantsAdmins

from DewmiBot import DEV_USERS, telethn
from DewmiBot.modules.helper_funcs.telethn.chatstatus import (
    can_delete_messages,
    user_is_admin,
)


# Check if user has admin rights
async def is_administrator(user_id: int, message):
    admin = False
    async for user in telethn.iter_participants(
        message.chat_id, filter=ChannelParticipantsAdmins
    ):
        if user_id == user.id or user_id in DEV_USERS:
            admin = True
            break
    return admin


@telethn.on(events.NewMessage(pattern="^[!/]purge$"))
async def purge(event):
    chat = event.chat_id
    start = time.perf_counter()
    msgs = []

    if not await is_administrator(
        user_id=event.sender_id, message=event
    ) and event.from_id not in [1087968824]:
        await event.reply("You're Not An Admin!")
        return

    msg = await event.get_reply_message()
    if not msg:
        await event.reply("Reply to a message to select where to start purging from.")
        return

    try:
        msg_id = msg.id
        count = 0
        to_delete = event.message.id - 1
        await event.client.delete_messages(chat, event.message.id)
        msgs.append(event.reply_to_msg_id)
        for m_id in range(to_delete, msg_id - 1, -1):
            msgs.append(m_id)
            count += 1
            if len(msgs) == 100:
                await event.client.delete_messages(chat, msgs)
                msgs = []

        await event.client.delete_messages(chat, msgs)
        time_ = time.perf_counter() - start
        del_res = await event.client.send_message(
            event.chat_id, f"Purged {count} Messages In {time_:0.2f} Secs."
        )

        await asyncio.sleep(4)
        await del_res.delete()

    except MessageDeleteForbiddenError:
        text = "Failed to delete messages.\n"
        text += "Messages maybe too old or I'm not admin! or dont have delete rights!"
        del_res = await event.respond(text, parse_mode="md")
        await asyncio.sleep(5)
        await del_res.delete()


@telethn.on(events.NewMessage(pattern="^[!/]del$"))
async def delete_messages(event):
    if event.from_id is None:
        return

    if not await user_is_admin(
        user_id=event.sender_id, message=event
    ) and event.from_id not in [1087968824]:
        await event.reply("Only Admins are allowed to use this command")
        return

    if not await can_delete_messages(message=event):
        await event.reply("Can't seem to delete this?")
        return

    message = await event.get_reply_message()
    if not message:
        await event.reply("Whadya want to delete?")
        return
    chat = await event.get_input_chat()
    del_message = [message, event.message]
    await event.client.delete_messages(chat, del_message)


__help__ = """
@szrosebot🇱🇰
*Admin only:*
 ❍ /del*:* deletes the message you replied to.
 ❍ /purge*:* deletes all messages between this and the replied to message.
 ❍ /purge <integer X>*:* deletes the replied message, and X messages following it if replied to a message.
 
"""

__mod_name__ = "ᴘᴜʀɢᴇ❌"
