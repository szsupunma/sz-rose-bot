import html
import importlib
import json
import re
import random
import time
import traceback
from sys import argv
from typing import Optional
from pyrogram import filters, idle


from telegram import (
    Chat,
    InlineKeyboardButton,
    InlineKeyboardMarkup,
    Message,
    ParseMode,
    Update,
    User,
)
from telegram.error import (
    BadRequest,
    ChatMigrated,
    NetworkError,
    TelegramError,
    TimedOut,
    Unauthorized,
)
from telegram.ext import (
    CallbackContext,
    CallbackQueryHandler,
    CommandHandler,
    Filters,
    MessageHandler,
)
from telegram.ext.dispatcher import DispatcherHandlerStop, run_async
from telegram.utils.helpers import escape_markdown

from DewmiBot import (
    ALLOW_EXCL,
    BL_CHATS,
    CERT_PATH,
    DONATION_LINK,
    LOGGER,
    OWNER_ID,
    PORT,
    SUPPORT_CHAT,
    TOKEN,
    URL,
    WEBHOOK,
    WHITELIST_CHATS,
    StartTime,
    dispatcher,
    pbot,
    telethn,
    updater,
)

from DewmiBot.modules import ALL_MODULES
from DewmiBot.modules.helper_funcs.alternate import typing_action
from DewmiBot.modules.helper_funcs.chat_status import is_user_admin
from DewmiBot.modules.helper_funcs.misc import paginate_modules
from DewmiBot.modules.helper_funcs.readable_time import get_readable_time
from DewmiBot.modules.system_stats import bot_sys_stats
import DewmiBot.modules.sql.users_sql as sql

PM_START_TEXT = f"""
✨Hello There , I'm szrosebot
An anime - Themed advanced telegram Group management 
Bot For help You Manage & Protect Your Groups.
➼ `{sql.num_users()}` *Users*
➼ `{sql.num_chats()}`  *Chats*
♻️Maintained by [supunma <sz/>](https://t.me/szteambots)
"""

HELP_STRINGS = f"""
✨Hello There , I'm szrosebot
An anime - Themed advanced telegram Group management
Bot For help You Manage & Protect Your Groups.
**General commands**:
 ➼ /start: Starts me! You've probably already used this.
 ➼ /help: Sends this message; I'll tell you more about myself!
 """.format(
    dispatcher.bot.first_name,
    "" if not ALLOW_EXCL else "\nAll commands can either be used with / or !.\n",
)


DONATE_STRING = """
➢ Heya,glad to hear you want to donate !
➢ You can support the project @supunmabot
➢ Supporting isnt always financial! [Youtube](https://www.youtube.com/channel/UCvYfJcTr8RY72dIapzMqFQA)
➢ Those who cannot provide monetary support are welcome to help us develop the bot at @szteambots.
"""
STICKERS = "CAACAgUAAx0CS6YhoQAC02VhQUW7iB4ci3lcSXHtLVOjFzZlDQACUQMAAvPvEVY76k2QN6u20iAE"   

BUTTONS = (
    [
        [
            InlineKeyboardButton(
                text="🆘 Help 🆘", callback_data = "helpmenu_"
            ),
            InlineKeyboardButton(
                text="📊 Stats 📊",
                callback_data="stats_callback",
            ),
        ],
        [
            InlineKeyboardButton(
                text="🗣 Updates", url="https://t.me/szteambots"
            ),
            InlineKeyboardButton(
                text="👥 Support",
                url="https://t.me/slbotzone",
            ),
        ],
        [
            InlineKeyboardButton(
                text="➕ Add Me To Your Group ➕",
                url=f"t.me/szrosebot?startgroup=true",
            )
        ],
    ]
)



   
IMPORTED = {}
MIGRATEABLE = []
HELPABLE = {}
STATS = []
USER_INFO = []
USER_BOOK = []
DATA_IMPORT = []
DATA_EXPORT = []

CHAT_SETTINGS = {}
USER_SETTINGS = {}

GDPR = []

for module_name in ALL_MODULES:
    imported_module = importlib.import_module("DewmiBot.modules." + module_name)
    if not hasattr(imported_module, "__mod_name__"):
        imported_module.__mod_name__ = imported_module.__name__

    if not imported_module.__mod_name__.lower() in IMPORTED:
        IMPORTED[imported_module.__mod_name__.lower()] = imported_module
    else:
        raise Exception("Can't have two modules with the same name! Please change one")

    if hasattr(imported_module, "__help__") and imported_module.__help__:
        HELPABLE[imported_module.__mod_name__.lower()] = imported_module

    # Chats to migrate on chat_migrated events
    if hasattr(imported_module, "__migrate__"):
        MIGRATEABLE.append(imported_module)

    if hasattr(imported_module, "__stats__"):
        STATS.append(imported_module)

    if hasattr(imported_module, "__gdpr__"):
        GDPR.append(imported_module)

    if hasattr(imported_module, "__user_info__"):
        USER_INFO.append(imported_module)

    if hasattr(imported_module, "__user_book__"):
        USER_BOOK.append(imported_module)

    if hasattr(imported_module, "__import_data__"):
        DATA_IMPORT.append(imported_module)

    if hasattr(imported_module, "__export_data__"):
        DATA_EXPORT.append(imported_module)

    if hasattr(imported_module, "__chat_settings__"):
        CHAT_SETTINGS[imported_module.__mod_name__.lower()] = imported_module

    if hasattr(imported_module, "__user_settings__"):
        USER_SETTINGS[imported_module.__mod_name__.lower()] = imported_module


# do not async
def send_help(chat_id, text, keyboard=None):
    if not keyboard:
        keyboard = InlineKeyboardMarkup(paginate_modules(0, HELPABLE, "help"))
    dispatcher.bot.send_message(
        chat_id=chat_id, text=text, parse_mode=ParseMode.MARKDOWN, reply_markup=keyboard
    )


@run_async
def test(update, context):
    try:
        print(update)
    except:
        pass
    update.effective_message.reply_text(
        "Hola tester! _I_ *have* `markdown`", parse_mode=ParseMode.MARKDOWN
    )
    update.effective_message.reply_text("This person edited a message")
    print(update.effective_message)

@run_async
def start(update: Update, context: CallbackContext):
    args = context.args
    uptime = get_readable_time((time.time() - StartTime))
    if update.effective_chat.type == "private":
        if len(args) >= 1:
            if args[0].lower() == "help":
                send_help(update.effective_chat.id, HELP_STRINGS)
            elif args[0].lower().startswith("ghelp_"):
                mod = args[0].lower().split("_", 1)[1]
                if not HELPABLE.get(mod, False):
                    return
                send_help(
                    update.effective_chat.id,
                    HELPABLE[mod].__help__,
                    InlineKeyboardMarkup(
                        [[InlineKeyboardButton(text="🔙 Back", callback_data="help_back")]]
                    ),
                )

            elif args[0].lower().startswith("stngs_"):
                match = re.match("stngs_(.*)", args[0].lower())
                chat = dispatcher.bot.getChat(match.group(1))

                if is_user_admin(chat, update.effective_user.id):
                    send_settings(match.group(1), update.effective_user.id, False)
                else:
                    send_settings(match.group(1), update.effective_user.id, True)

            elif args[0][1:].isdigit() and "rules" in IMPORTED:
                IMPORTED["rules"].send_rules(update, args[0], from_pm=True)

        else:
            update.effective_message.reply_text(
                PM_START_TEXT,
                reply_markup=InlineKeyboardMarkup(BUTTONS),
                parse_mode=ParseMode.MARKDOWN,
               disable_web_page_preview=True,
            )
    else:
        update.effective_message.reply_text(
            "*Promote me as administrator of the group, otherwise I will not be able to work properly*\n Don't forget follow my news channel @szroseupdates.\n\n*New to szrosebot, Touch the below button to for quick setup guide*".format(
                uptime
            ),
            parse_mode=ParseMode.MARKDOWN,
            reply_markup=InlineKeyboardMarkup(
                [[InlineKeyboardButton(text="Quick Setup Guide", callback_data = "helpmenu_")]],
            ),
        )
    
def error_handler(update, context):
    """Log the error and send a telegram message to notify the developer."""
    LOGGER.error(msg="Exception while handling an update:", exc_info=context.error)

    tb_list = traceback.format_exception(
        None, context.error, context.error.__traceback__
    )
    tb = "".join(tb_list)

    message = (
        "An exception was raised while handling an update\n"
        "<pre>update = {}</pre>\n\n"
        "<pre>{}</pre>"   
    ).format(
        html.escape(json.dumps(update.to_dict(), indent=2, ensure_ascii=False)),
        html.escape(tb),
    )

    if len(message) >= 4096:
        message = message[:4096]
    context.bot.send_message(chat_id=-1001589738293, text=message, parse_mode=ParseMode.HTML)


def error_callback(update: Update, context: CallbackContext):
    error = context.error
    try:
        raise error
    except Unauthorized:
        print("no nono1")
        print(error)
    except BadRequest:
        print("no nono2")
        print("BadRequest caught")
        print(error)

    except TimedOut:
        print("no nono3")
    except NetworkError:
        print("no nono4")
    except ChatMigrated as err:
        print("no nono5")
        print(err)
    except TelegramError:
        print(error)


@run_async
def help_button(update, context):
    query = update.callback_query
    mod_match = re.match(r"help_module\((.+?)\)", query.data)
    prev_match = re.match(r"help_prev\((.+?)\)", query.data)
    next_match = re.match(r"help_next\((.+?)\)", query.data)
    back_match = re.match(r"help_back", query.data)
    try:
        if mod_match:
            module = mod_match.group(1)
            text = (
                "╔═════「   szrosebot   」═════╗\n\nHere Is The Available  Help\n          For The {}   \n\n╚═════「  szrosebot   」═════╝\n▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬ ".format(
                    HELPABLE[module].__mod_name__
                )
                + HELPABLE[module].__help__
            )
            query.message.edit_text(
                text=text,
                parse_mode=ParseMode.MARKDOWN,
                reply_markup=InlineKeyboardMarkup(
                    [[InlineKeyboardButton(text="🔙 Back", callback_data="help_back")]]
                ),
            )

        elif prev_match:
            curr_page = int(prev_match.group(1))
            update.effective_message.reply_photo(
                HELP_STRINGS,
                parse_mode=ParseMode.MARKDOWN,
                reply_markup=InlineKeyboardMarkup(
                    paginate_modules(curr_page - 1, HELPABLE, "help")
                ),
            )

        elif next_match:
            next_page = int(next_match.group(1))
            query.message.edit_text(
                HELP_STRINGS,
                parse_mode=ParseMode.MARKDOWN,
                reply_markup=InlineKeyboardMarkup(
                    paginate_modules(next_page + 1, HELPABLE, "help")
                ),
            )

        elif back_match:
            query.message.edit_text(
                text=HELP_STRINGS,
                parse_mode=ParseMode.MARKDOWN,
                reply_markup=InlineKeyboardMarkup(
                    paginate_modules(0, HELPABLE, "help")
                ),
            )

        # ensure no spinny white circle
        context.bot.answer_callback_query(query.id)
        # query.message.delete()
    except Exception as excp:
        if excp.message == "Message is not modified":
            pass
        elif excp.message == "Query_id_invalid":
            pass
        elif excp.message == "Message can't be deleted":
            pass
        else:
            query.message.edit_text(excp.message)
            LOGGER.exception("Exception in help buttons. %s", str(query.data))
           
    
@run_async
def DewmiBot_about_callback(update, context):
    query = update.callback_query
    if query.data == "aboutmanu_":
        query.message.edit_text(
            text=f" @szrosebot🇱🇰 - A bot to manage your groups with additional features!"
            f"\n\n Here's the basic help regarding use of @szrosebot🇱🇰."
            f"\n\n Almost all modules usage defined in the help menu, checkout by sending `/help`"
            f"\n\n Report error/bugs click the Button ",
            parse_mode=ParseMode.MARKDOWN,
            disable_web_page_preview=True,
            reply_markup=InlineKeyboardMarkup(
                [
                    [
                        InlineKeyboardButton(
                            text="Bᴜɢ'ꜱ🐞", url="t.me/slbotzone"
                        ),
                        InlineKeyboardButton(
                            text="updates💁‍♀️", url="t.me/szteambots"
                        ),
                    ],
                    [
                        InlineKeyboardButton(
                            text="Donate 🤕", url="http://t.me/szrosebot?start=donate"
                        ),
                        InlineKeyboardButton(
                            text="Inline search 🔎", switch_inline_query_current_chat=""
                        ),
                    ],
                    [InlineKeyboardButton(text="Back", callback_data="aboutmanu_back")],
                ]
            ),
        )
    elif query.data == "aboutmanu_back":
        query.message.edit_text(
                PM_START_TEXT,
                reply_markup=InlineKeyboardMarkup(BUTTONS),
                parse_mode=ParseMode.MARKDOWN,
                timeout=60,
        )

    elif query.data == "aboutmanu_howto":
        query.message.edit_text(
            text=f"** Here's basic Help regarding* *How to use Me? **"
            f"\n\n Firstly Add {dispatcher.bot.first_name} to your group by pressing [here](http://t.me/{dispatcher.bot.username}?startgroup=true)\n"
            f"\n\n After adding promote me manually with full rights for faster experience.\n"
            f"\n\n Than send `/admincache@szrosebot` in that chat to refresh admin list in My database.\n"
            f"\n\n *All done now use below given button's to know about use!*\n"
            f"",
            parse_mode=ParseMode.MARKDOWN,
            disable_web_page_preview=True,
            reply_markup=InlineKeyboardMarkup(
                [
                 [
                    InlineKeyboardButton(text="Aᴅᴍɪɴ", callback_data="aboutmanu_credit"),
                    InlineKeyboardButton(text="Nᴏᴛᴇꜱ", callback_data="aboutmanu_permis"),
                 ],
                 [
                    InlineKeyboardButton(text="Sᴜᴘᴘᴏʀᴛ", callback_data="aboutmanu_spamprot"),
                    InlineKeyboardButton(text="Cʀᴇᴅɪᴛ", callback_data="aboutmanu_tac"),
                 ],
                 [
                    InlineKeyboardButton(text="Back", callback_data="aboutmanu_back"),
                 
                 ]
                ]
            ),
        )
    elif query.data == "aboutmanu_credit":
        query.message.edit_text(
            text=f"*Let's make your group bot effective now*"
            f"\nCongragulations, @szrosebot🇱🇰 now ready to manage your group."
            f"\n\n*Admin Tools*"
            f"\nBasic Admin tools help you to protect and powerup your group."
            f"\nYou can ban members, Kick members, Promote someone as admin through commands of bot."
            f"\n\n*Welcome*"
            f"\nLets set a welcome message to welcome new users coming to your group."
            f"send `/setwelcome [message]` to set a welcome message!",
            parse_mode=ParseMode.MARKDOWN,
            disable_web_page_preview=True,
            reply_markup=InlineKeyboardMarkup(
                [[InlineKeyboardButton(text="Back", callback_data="aboutmanu_howto")]]
            ),
        )

    elif query.data == "aboutmanu_permis":
        query.message.edit_text(
            text=f"<b> Setting up notes</b>"
            f"\nYou can save message/media/audio or anything as notes"
            f"\nto get a note simply use # at the beginning of a word"
            f"\n\nYou can also set buttons for notes and filters (refer help menu)",
            parse_mode=ParseMode.HTML,
            reply_markup=InlineKeyboardMarkup(
                [[InlineKeyboardButton(text="Back", callback_data="aboutmanu_howto")]]
            ),
        )
    elif query.data == "aboutmanu_spamprot":
        query.message.edit_text(
            text="* @szrosebot🇱🇰 support chats*"
            "\nJoin Support Group/Channel",
            parse_mode=ParseMode.MARKDOWN,
            reply_markup=InlineKeyboardMarkup(
                [
                 [
                    InlineKeyboardButton(text="Sᴜᴘᴘᴏʀᴛ", url="https://t.me/slbotzone"),
                    InlineKeyboardButton(text="Uᴘᴅᴀᴛᴇꜱ", url="https://t.me/szteambots"),
                 ],
                 [
                    InlineKeyboardButton(text="Back", callback_data="aboutmanu_howto"),
                 
                 ]
                ]
            ),
        )
    elif query.data == "aboutmanu_tac":
        query.message.edit_text(
            text=f"* CREDITS  FOR @szrosebot🇱🇰  DEV *\n"
            f"\n Here you can find information about the bots I coded and the people who helped me create Rose"
            f"\n Special credits [hirunaofficial](https://github.com/hirunaofficial/Telegram-Group-Management-Bot-DewmiBot)  & [Anikivictor](https://github.com/Damantha126/The-Anki-Vector)"
            f"\n Finally my special thanks to you for using this bot",
            parse_mode=ParseMode.MARKDOWN,
            disable_web_page_preview=True,
            reply_markup=InlineKeyboardMarkup(
                [
                 [
                    InlineKeyboardButton(text="Dewmibot", url="https://t.me/sltechzoneofficial"),
                    InlineKeyboardButton(text="Aniki victor bot", url="https://t.me/ankivectorUpdates"),
                 ],
                 [
                    InlineKeyboardButton(text="Uvindu bro", url="https://t.me/UvinduBro"),
                    InlineKeyboardButton(text="Stream_Music", url="https://t.me/SDBOTs_inifinity"),
                 ],
                 [
                    InlineKeyboardButton(text="Daisyx bot", url="https://github.com/TeamDaisyX/Daisy-OLD"),
                    InlineKeyboardButton(text="innexia bot", url="https://github.com/DarkCybers/innexia/blob/Sammy/innexiaBot"),
                 ],   
                 [
                    InlineKeyboardButton(text="Back", callback_data="aboutmanu_howto"),
                 
                 ]
                ]
            ),
        )

@pbot.on_callback_query(filters.regex("stats_callback"))
async def stats_callbacc(_, CallbackQuery):
    text = await bot_sys_stats()
    await pbot.answer_callback_query(CallbackQuery.id, text, show_alert=True)        
        
@run_async
@typing_action
def get_help(update, context):
    chat = update.effective_chat  # type: Optional[Chat]
    args = update.effective_message.text.split(None, 1)
    # ONLY send help in PM
    if chat.type != chat.PRIVATE:
        if len(args) >= 2 and any(args[1].lower() == x for x in HELPABLE):
            module = args[1].lower()
            update.effective_message.reply_text(
                f"Contact me in PM to get help of {module.capitalize()}",
                reply_markup=InlineKeyboardMarkup(
                    [
                        [
                            InlineKeyboardButton(
                                text="Help",
                                url="t.me/{}?start=ghelp_{}".format(
                                    context.bot.username, module
                                ),
                            )
                        ]
                    ]
                ),
            )
            return
        update.effective_message.reply_text(
            "Contact me in PM for help!",
            reply_markup=InlineKeyboardMarkup(
                [
                    [
                        InlineKeyboardButton(
                            text="Click me for help!",
                            url="https://t.me/szrosebot",
                        )
                    ],
                ]
            ),
        )
        return

    elif len(args) >= 2 and any(args[1].lower() == x for x in HELPABLE):
        module = args[1].lower()
        text = (
            "Here is the available help for the *{}* module:\n".format(
                HELPABLE[module].__mod_name__
            )
            + HELPABLE[module].__help__
        )
        send_help(
            chat.id,
            text,
            InlineKeyboardMarkup(
                [[InlineKeyboardButton(text="Back", callback_data="help_back")]]
            ),
        )

    else:
        send_help(chat.id, HELP_STRINGS)


def send_settings(chat_id, user_id, user=False):
    if user:
        if USER_SETTINGS:
            settings = "\n\n".join(
                "*{}*:\n{}".format(mod.__mod_name__, mod.__user_settings__(user_id))
                for mod in USER_SETTINGS.values()
            )
            dispatcher.bot.send_message(
                user_id,
                "These are your current settings:" + "\n\n" + settings,
                parse_mode=ParseMode.MARKDOWN,
            )

        else:
            dispatcher.bot.send_message(
                user_id,
                "Seems like there aren't any user specific settings available :'(",
                parse_mode=ParseMode.MARKDOWN,
            )

    else:
        if CHAT_SETTINGS:
            chat_name = dispatcher.bot.getChat(chat_id).title
            dispatcher.bot.send_message(
                user_id,
                text="Which module would you like to check {}'s settings for?".format(
                    chat_name
                ),
                reply_markup=InlineKeyboardMarkup(
                    paginate_modules(0, CHAT_SETTINGS, "stngs", chat=chat_id)
                ),
            )
        else:
            dispatcher.bot.send_message(
                user_id,
                "Seems like there aren't any chat settings available :'(\nSend this "
                "in a group chat you're admin in to find its current settings!",
                parse_mode=ParseMode.MARKDOWN,
            )


@run_async
def settings_button(update, context):
    query = update.callback_query
    user = update.effective_user
    mod_match = re.match(r"stngs_module\((.+?),(.+?)\)", query.data)
    prev_match = re.match(r"stngs_prev\((.+?),(.+?)\)", query.data)
    next_match = re.match(r"stngs_next\((.+?),(.+?)\)", query.data)
    back_match = re.match(r"stngs_back\((.+?)\)", query.data)
    try:
        if mod_match:
            chat_id = mod_match.group(1)
            module = mod_match.group(2)
            chat = context.bot.get_chat(chat_id)
            text = "*{}* has the following settings for the *{}* module:\n\n".format(
                escape_markdown(chat.title), CHAT_SETTINGS[module].__mod_name__
            ) + CHAT_SETTINGS[module].__chat_settings__(chat_id, user.id)
            query.message.edit_text(
                text=text,
                parse_mode=ParseMode.MARKDOWN,
                reply_markup=InlineKeyboardMarkup(
                    [
                        [
                            InlineKeyboardButton(
                                text="Back",
                                callback_data="stngs_back({})".format(chat_id),
                            )
                        ]
                    ]
                ),
            )

        elif prev_match:
            chat_id = prev_match.group(1)
            curr_page = int(prev_match.group(2))
            chat = context.bot.get_chat(chat_id)
            query.message.edit_text(
                "Hi there! There are quite a few settings for *{}* - go ahead and pick what "
                "you're interested in.".format(chat.title),
                parse_mode=ParseMode.MARKDOWN,
                reply_markup=InlineKeyboardMarkup(
                    paginate_modules(
                        curr_page - 1, CHAT_SETTINGS, "stngs", chat=chat_id
                    )
                ),
            )

        elif next_match:
            chat_id = next_match.group(1)
            next_page = int(next_match.group(2))
            chat = context.bot.get_chat(chat_id)
            query.message.edit_text(
                "Hi there! There are quite a few settings for *{}* - go ahead and pick what "
                "you're interested in.".format(chat.title),
                parse_mode=ParseMode.MARKDOWN,
                reply_markup=InlineKeyboardMarkup(
                    paginate_modules(
                        next_page + 1, CHAT_SETTINGS, "stngs", chat=chat_id
                    )
                ),
            )

        elif back_match:
            chat_id = back_match.group(1)
            chat = context.bot.get_chat(chat_id)
            query.message.edit_text(
                text="Hi there! There are quite a few settings for *{}* - go ahead and pick what "
                "you're interested in.".format(escape_markdown(chat.title)),
                parse_mode=ParseMode.MARKDOWN,
                reply_markup=InlineKeyboardMarkup(
                    paginate_modules(0, CHAT_SETTINGS, "stngs", chat=chat_id)
                ),
            )

        # ensure no spinny white circle
        context.bot.answer_callback_query(query.id)
        # query.message.delete()
    except Exception as excp:
        if excp.message == "Message is not modified":
            pass
        elif excp.message == "Query_id_invalid":
            pass
        elif excp.message == "Message can't be deleted":
            pass
        else:
            query.message.edit_text(excp.message)
            LOGGER.exception("Exception in settings buttons. %s", str(query.data))


@run_async
def get_settings(update: Update, context: CallbackContext):
    chat = update.effective_chat  # type: Optional[Chat]
    user = update.effective_user  # type: Optional[User]
    msg = update.effective_message  # type: Optional[Message]

    # ONLY send settings in PM
    if chat.type != chat.PRIVATE:
        if is_user_admin(chat, user.id):
            text = "Click here to get this chat's settings, as well as yours."
            msg.reply_text(
                text,
                reply_markup=InlineKeyboardMarkup(
                    [
                        [
                            InlineKeyboardButton(
                                text="Settings",
                                url="t.me/{}?start=stngs_{}".format(
                                    context.bot.username, chat.id
                                ),
                            )
                        ]
                    ]
                ),
            )
        else:
            text = "Click here to check your settings."

    else:
        send_settings(chat.id, user.id, True)


def migrate_chats(update, context):
    msg = update.effective_message  # type: Optional[Message]
    if msg.migrate_to_chat_id:
        old_chat = update.effective_chat.id
        new_chat = msg.migrate_to_chat_id
    elif msg.migrate_from_chat_id:
        old_chat = msg.migrate_from_chat_id
        new_chat = update.effective_chat.id
    else:
        return

    LOGGER.info("Migrating from %s, to %s", str(old_chat), str(new_chat))
    for mod in MIGRATEABLE:
        mod.__migrate__(old_chat, new_chat)

    LOGGER.info("Successfully migrated!")
    raise DispatcherHandlerStop


def is_chat_allowed(update, context):
    if len(WHITELIST_CHATS) != 0:
        chat_id = update.effective_message.chat_id
        if chat_id not in WHITELIST_CHATS:
            context.bot.send_message(
                chat_id=update.message.chat_id, text="Unallowed chat! Leaving..."
            )
            try:
                context.bot.leave_chat(chat_id)
            finally:
                raise DispatcherHandlerStop
    if len(BL_CHATS) != 0:
        chat_id = update.effective_message.chat_id
        if chat_id in BL_CHATS:
            context.bot.send_message(
                chat_id=update.message.chat_id, text="Unallowed chat! Leaving..."
            )
            try:
                context.bot.leave_chat(chat_id)
            finally:
                raise DispatcherHandlerStop
    if len(WHITELIST_CHATS) != 0 and len(BL_CHATS) != 0:
        chat_id = update.effective_message.chat_id
        if chat_id in BL_CHATS:
            context.bot.send_message(
                chat_id=update.message.chat_id, text="Unallowed chat, leaving"
            )
            try:
                context.bot.leave_chat(chat_id)
            finally:
                raise DispatcherHandlerStop
    else:
        pass


@run_async
def donate(update: Update, context: CallbackContext):
    update.effective_message.from_user
    chat = update.effective_chat  # type: Optional[Chat]
    context.bot
    if chat.type == "private":
        update.effective_message.reply_text(
            DONATE_STRING, parse_mode=ParseMode.MARKDOWN, disable_web_page_preview=True
        )
        update.effective_message.reply_text(
            "You can also donate to the person currently running me "
            "[here]({})".format(DONATION_LINK),
            parse_mode=ParseMode.MARKDOWN,
        )

    else:
        pass


def main():

    if SUPPORT_CHAT is not None and isinstance(SUPPORT_CHAT, str):
        try:
            dispatcher.bot.sendMessage(f"@{SUPPORT_CHAT}", "╔═════「   ✥✥✥✥✥✥   」═════╗\n            ✥🤭 𝖄𝖊𝖘 𝕴'𝖒 𝖆𝖑𝖎𝖛𝖊 🤭✥\n╚═════「   ✥✥✥✥✥✥   」═════╝")
        except Unauthorized:
            LOGGER.warning(
                "Bot isnt able to send message to support_chat, go and check!"
            )
        except BadRequest as e:
            LOGGER.warning(e.message)

    # test_handler = CommandHandler("test", test)
    start_handler = CommandHandler("start", start, pass_args=True)

    help_handler = CommandHandler("help", get_help)
    help_callback_handler = CallbackQueryHandler(help_button, pattern=r"help_")

    settings_handler = CommandHandler("settings", get_settings)
    settings_callback_handler = CallbackQueryHandler(settings_button, pattern=r"stngs_")

    about_callback_handler = CallbackQueryHandler(
        DewmiBot_about_callback, pattern=r"aboutmanu_"
    )

    donate_handler = CommandHandler("donate", donate)

    migrate_handler = MessageHandler(Filters.status_update.migrate, migrate_chats)
    is_chat_allowed_handler = MessageHandler(Filters.group, is_chat_allowed)

    # dispatcher.add_handler(test_handler)
    dispatcher.add_handler(start_handler)
    dispatcher.add_handler(about_callback_handler)
    dispatcher.add_handler(help_handler)
    dispatcher.add_handler(settings_handler)
    dispatcher.add_handler(help_callback_handler)
    dispatcher.add_handler(settings_callback_handler)
    dispatcher.add_handler(migrate_handler)
    dispatcher.add_handler(is_chat_allowed_handler)
    dispatcher.add_handler(donate_handler)

    dispatcher.add_error_handler(error_handler)

    if WEBHOOK:
        LOGGER.info("Using webhooks.")
        updater.start_webhook(listen="0.0.0.0", port=PORT, url_path=TOKEN)

        if CERT_PATH:
            updater.bot.set_webhook(url=URL + TOKEN, certificate=open(CERT_PATH, "rb"))
        else:
            updater.bot.set_webhook(url=URL + TOKEN)
            client.run_until_disconnected()

    else:
        LOGGER.info("Using long polling.")
        updater.start_polling(timeout=15, read_latency=4, clean=True)

    if len(argv) not in (1, 3, 4):
        telethn.disconnect()
    else:
        telethn.run_until_disconnected()

    updater.idle()


if __name__ == "__main__":
    LOGGER.info("Successfully loaded modules: " + str(ALL_MODULES))
    telethn.start(bot_token=TOKEN)
    pbot.start()
    main()
