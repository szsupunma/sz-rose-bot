from DewmiBot import pbot 
import random
from DewmiBot.function.dbfun import (
    update_karma,
    get_karma,
    get_karmas,
    int_to_alpha,
    alpha_to_int,
)
from DewmiBot.utils.filter_groups import karma_positive_group, karma_negative_group
from pyrogram import filters


regex_upvote = r"^((?i)\+|\+\+|\+1|thx|tnx|ty|thank you|thanx|thanks|pro|cool|good|👍)$"
regex_downvote = r"^(\-|\-\-|\-1|👎)$"


@pbot.on_message(
    filters.text
    & filters.group
    & filters.incoming
    & filters.reply
    & filters.regex(regex_upvote)
    & ~filters.via_bot
    & ~filters.bot
    & ~filters.edited,
    group=karma_positive_group,
)
async def upvote(_, message):
    if message.reply_to_message.from_user.id == message.from_user.id:
        return
    chat_id = message.chat.id
    user_id = message.reply_to_message.from_user.id
    user_mention = message.reply_to_message.from_user.mention
    current_karma = await get_karma(chat_id, await int_to_alpha(user_id))
    if current_karma:
        current_karma = current_karma["karma"]
        karma = current_karma + 1
        new_karma = {"karma": karma}
        await update_karma(chat_id, await int_to_alpha(user_id), new_karma)
    else:
        karma = 1
        new_karma = {"karma": karma}
        await update_karma(chat_id, await int_to_alpha(user_id), new_karma)
    await message.reply_text(
        f"Incremented Karma of {user_mention} By 1 \nTotal Points: {karma}"
    )


@pbot.on_message(
    filters.text
    & filters.group
    & filters.incoming
    & filters.reply
    & filters.regex(regex_downvote)
    & ~filters.via_bot
    & ~filters.bot
    & ~filters.edited,
    group=karma_negative_group,
)
async def downvote(_, message):
    if message.reply_to_message.from_user.id == message.from_user.id:
        return
    chat_id = message.chat.id
    user_id = message.reply_to_message.from_user.id
    user_mention = message.reply_to_message.from_user.mention
    current_karma = await get_karma(chat_id, await int_to_alpha(user_id))
    if current_karma:
        current_karma = current_karma["karma"]
        karma = current_karma - 1
        new_karma = {"karma": karma}
        await update_karma(chat_id, await int_to_alpha(user_id), new_karma)
    else:
        karma = 1
        new_karma = {"karma": karma}
        await update_karma(chat_id, await int_to_alpha(user_id), new_karma)
    await message.reply_text(
        f"Decremented Karma Of {user_mention} By 1 \nTotal Points: {karma}"
    )


@pbot.on_message(filters.command("karma") & filters.group)
async def command_karma(_, message):
    chat_id = message.chat.id
    
    if not message.reply_to_message:
        m = await message.reply_text("Analyzing Karma...")
        karma = await get_karmas(chat_id)
        if not karma:
            return await m.edit("No karma in DB for this chat.")
        msg = f"Karma list of {message.chat.title}"
        limit = 0
        karma_dicc = {}
        for i in karma:
            user_id = await alpha_to_int(i)
            user_karma = karma[i]["karma"]
            karma_dicc[str(user_id)] = user_karma
            karma_arranged = dict(
                sorted(
                    karma_dicc.items(),
                    key=lambda item: item[1],
                    reverse=True,
                )
            )
        if not karma_dicc:
            return await m.edit("No karma in DB for this chat.")
        userdb = await get_user_id_and_usernames(pbot)
        karma = {}
        for user_idd, karma_count in karma_arranged.items():
            if limit > 15:
                break
            if int(user_idd) not in list(userdb.keys()):
                continue
            username = userdb[int(user_idd)]
            karma[karma_count] = ["@" + username]
            limit += 1
        await m.edit(section(msg, karma))
    else:
        if not message.reply_to_message.from_user:
            return await message.reply("Anon user hash no karma.")

        user_id = message.reply_to_message.from_user.id
        karma = await get_karma(chat_id, await int_to_alpha(user_id))
        if karma:
            karma = karma["karma"]
            await message.reply_text(f"**Total Points**: __{karma}__")
        else:
            karma = 0
            await message.reply_text(f"**Total Points**: __{karma}__")
      

__help__ = """
@szrosebot🇱🇰
[UPVOTE] - Use upvote keywords like "+", "+1", "thanks" etc to upvote a cb.message.
[DOWNVOTE] - Use downvote keywords like "-", "-1", etc to downvote a cb.message.

❍ /karma[ON/OFF]: Enable/Disable karma in group. (don't give space)
❍ /karma [Reply to a message]: Check user's karma
❍ /karma: Chek karma list of top 10 users

"""
__mod_name__ = "ᴋᴀʀᴍᴀ🎪"            

