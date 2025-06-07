import os, pytz, re, datetime, logging, asyncio, math, time
from pyrogram import Client, filters, enums
from pyrogram.errors import FloodWait
from pyrogram.errors.exceptions.bad_request_400 import ChannelInvalid, ChatAdminRequired, UsernameInvalid, UsernameNotModified
from info import ADMINS, LOG_CHANNEL, DATABASE_URI, DATABASE_NAME
from database.ia_filterdb import save_file2, save_file3, save_file4, check_file, get_readable_time
from pyrogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from utils import temp
logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)
lock = asyncio.Lock()
import pymongo

inclient = pymongo.MongoClient(DATABASE_URI)
indb = inclient[DATABASE_NAME]
incol = indb['index']

@Client.on_callback_query(filters.regex(r'^index'))
async def index_files(bot, query):
    if query.data.startswith('index_cancel'):
        temp.CANCEL = True
        return await query.answer("Cancelling Indexing")
    _, raju, chat, lst_msg_id, from_user = query.data.split("#")
    if raju == 'reject':
        await query.message.delete()
        await bot.send_message(int(from_user),
                               f'Your Submission for indexing {chat} has been decliened by our moderators.',
                               reply_to_message_id=int(lst_msg_id))
        return
    if raju == 'accept1':
        if lock.locked():
            return await query.answer('Wait until previous process complete.', show_alert=True)
        msg = query.message

        await query.answer('Processing...⏳', show_alert=True)
        if int(from_user) not in ADMINS:
            await bot.send_message(int(from_user),
                                   f'Your Submission for indexing {chat} has been accepted by our moderators and will be added soon.',
                                   reply_to_message_id=int(lst_msg_id))
        await msg.edit(
            "Starting Indexing",
            reply_markup=InlineKeyboardMarkup(
                [[InlineKeyboardButton('Cancel', callback_data='index_cancel')]]
            )
        )
        try:
            chat = int(chat)
        except:
            chat = chat
        await index_files_to_db1(int(lst_msg_id), chat, msg, bot)
    elif raju == 'accept2':
        if lock.locked():
            return await query.answer('Wait until previous process complete.', show_alert=True)
        msg = query.message

        await query.answer('Processing...⏳', show_alert=True)
        if int(from_user) not in ADMINS:
            await bot.send_message(int(from_user),
                                   f'Your Submission for indexing {chat} has been accepted by our moderators and will be added soon.',
                                   reply_to_message_id=int(lst_msg_id))
        await msg.edit(
            "Starting Indexing",
            reply_markup=InlineKeyboardMarkup(
                [[InlineKeyboardButton('Cancel', callback_data='index_cancel')]]
            )
        )
        try:
            chat = int(chat)
        except:
            chat = chat
        await index_files_to_db2(int(lst_msg_id), chat, msg, bot)
    elif raju == 'accept3':
        if lock.locked():
            return await query.answer('Wait until previous process complete.', show_alert=True)
        msg = query.message

        await query.answer('Processing...⏳', show_alert=True)
        if int(from_user) not in ADMINS:
            await bot.send_message(int(from_user),
                                   f'Your Submission for indexing {chat} has been accepted by our moderators and will be added soon.',
                                   reply_to_message_id=int(lst_msg_id))
        await msg.edit(
            "Starting Indexing",
            reply_markup=InlineKeyboardMarkup(
                [[InlineKeyboardButton('Cancel', callback_data='index_cancel')]]
            )
        )
        try:
            chat = int(chat)
        except:
            chat = chat
        await index_files_to_db3(int(lst_msg_id), chat, msg, bot)    
    elif raju == 'accept5':
        if lock.locked():
            return await query.answer('Wait until previous process complete.', show_alert=True)
        msg = query.message

        await query.answer('Processing...⏳', show_alert=True)
        if int(from_user) not in ADMINS:
            await bot.send_message(int(from_user),
                                   f'Your Submission for indexing {chat} has been accepted by our moderators and will be added soon.',
                                   reply_to_message_id=int(lst_msg_id))
        await msg.edit(
            "Starting Indexing",
            reply_markup=InlineKeyboardMarkup(
                [[InlineKeyboardButton('Cancel', callback_data='index_cancel')]]
            )
        )
        try:
            chat = int(chat)
        except:
            chat = chat
        await index_files_to_db(int(lst_msg_id), chat, msg, bot)


@Client.on_message((filters.forwarded | (filters.regex("(https://)?(t\.me/|telegram\.me/|telegram\.dog/)(c/)?(\d+|[a-zA-Z_0-9]+)/(\d+)$")) & filters.text ) & filters.private & filters.incoming)
async def send_for_index(bot, message):
    if message.text:
        regex = re.compile("(https://)?(t\.me/|telegram\.me/|telegram\.dog/)(c/)?(\d+|[a-zA-Z_0-9]+)/(\d+)$")
        match = regex.match(message.text)
        if not match:
            return await message.reply('Invalid link')
        chat_id = match.group(4)
        last_msg_id = int(match.group(5))
        if chat_id.isnumeric():
            chat_id  = int(("-100" + chat_id))
    elif message.forward_from_chat.type == enums.ChatType.CHANNEL:
        last_msg_id = message.forward_from_message_id
        chat_id = message.forward_from_chat.username or message.forward_from_chat.id
    else:
        return
    try:
        await bot.get_chat(chat_id)
    except ChannelInvalid:
        return await message.reply('This may be a private channel / group. Make me an admin over there to index the files.')
    except (UsernameInvalid, UsernameNotModified):
        return await message.reply('Invalid Link specified.')
    except Exception as e:
        logger.exception(e)
        return await message.reply(f'Errors - {e}')
    try:
        k = await bot.get_messages(chat_id, last_msg_id)
    except:
        return await message.reply('Make Sure That Iam An Admin In The Channel, if channel is private')
    if k.empty:
        return await message.reply('This may be group and iam not a admin of the group.')

    if message.from_user.id in ADMINS:
        buttons = [
            [
                InlineKeyboardButton('Index To DB1',
                                     callback_data=f'index#accept1#{chat_id}#{last_msg_id}#{message.from_user.id}')
            ],
            [
                InlineKeyboardButton('Index To DB2',
                                     callback_data=f'index#accept2#{chat_id}#{last_msg_id}#{message.from_user.id}')
            ],
            [
                InlineKeyboardButton('Index To DB3',
                                     callback_data=f'index#accept3#{chat_id}#{last_msg_id}#{message.from_user.id}')
            ],            
            [
                InlineKeyboardButton('Index To all DB',
                                     callback_data=f'index#accept5#{chat_id}#{last_msg_id}#{message.from_user.id}')
            ],
            [
                InlineKeyboardButton('close', callback_data='close_data'),
            ]
        ]
        reply_markup = InlineKeyboardMarkup(buttons)
        return await message.reply(
            f'Do you Want To Index This Channel/ Group ?\n\nChat ID/ Username: <code>{chat_id}</code>\nLast Message ID: <code>{last_msg_id}</code>',
            reply_markup=reply_markup)

    if type(chat_id) is int:
        try:
            link = (await bot.create_chat_invite_link(chat_id)).invite_link
        except ChatAdminRequired:
            return await message.reply('Make sure iam an admin in the chat and have permission to invite users.')
    else:
        link = f"@{message.forward_from_chat.username}"
    buttons = [
        [
            InlineKeyboardButton('Index To DB1',
                                 callback_data=f'index#accept1#{chat_id}#{last_msg_id}#{message.from_user.id}')
        ],
        [
            InlineKeyboardButton('Index To DB2',
                                 callback_data=f'index#accept2#{chat_id}#{last_msg_id}#{message.from_user.id}')
        ],
        [
            InlineKeyboardButton('Index To DB3',
                                 callback_data=f'index#accept3#{chat_id}#{last_msg_id}#{message.from_user.id}')
        ],
        [
            InlineKeyboardButton('Index To DB4',
                                 callback_data=f'index#accept4#{chat_id}#{last_msg_id}#{message.from_user.id}')
        ],
        [
            InlineKeyboardButton('Index To both DB',
                                 callback_data=f'index#accept5#{chat_id}#{last_msg_id}#{message.from_user.id}')
        ],
        [
            InlineKeyboardButton('Reject Index',
                                 callback_data=f'index#reject#{chat_id}#{message.id}#{message.from_user.id}'),
        ]
    ]
    reply_markup = InlineKeyboardMarkup(buttons)
    await bot.send_message(LOG_CHANNEL,
                           f'#IndexRequest\n\nBy : {message.from_user.mention} (<code>{message.from_user.id}</code>)\nChat ID/ Username - <code> {chat_id}</code>\nLast Message ID - <code>{last_msg_id}</code>\nInviteLink - {link}',
                           reply_markup=reply_markup)
    await message.reply('ThankYou For the Contribution, Wait For My Moderators to verify the files.')


@Client.on_message(filters.command('setskip') & filters.user(ADMINS))
async def set_skip_number(bot, message):
    if ' ' in message.text:
        _, skip = message.text.split(" ")
        try:
            skip = int(skip)
        except:
            return await message.reply("Skip number should be an integer.")
        await message.reply(f"Successfully set SKIP number as {skip}")
        temp.CURRENT = int(skip)
    else:
        await message.reply("Give me a skip number")
        
async def index_files_to_db1(lst_msg_id, chat, msg, bot):
    total_files = 0
    duplicate = 0
    no_media = 0
    fst_msg_id = temp.CURRENT
    start_time = time.time()
    remaining_time_str = "N/A"
    async with lock:
        try:
            current = temp.CURRENT
            tz = pytz.timezone('Asia/Kolkata')
            today = datetime.date.today()
            now = datetime.datetime.now(tz)
            ttime = now.strftime("%I:%M:%S %p - %d %b, %Y")
            temp.CANCEL = False
            elapsed_time = 0
            remaining_index = 0
            async for message in bot.iter_messages(chat, lst_msg_id, temp.CURRENT):
                if temp.CANCEL:
                    await msg.edit(f"<b>❌ Successfully Cancelled!!</b>\n\n<b>├ ▸ Last Updated: <i>{ttime}</i></b>\n\n<b>╭ ▸ Fetched:</b> <code>{current}</code>\n<b>├ ▸ Saved:</b> <code>{total_files}</code>\n<b>├ ▸ Duplicate:</b> <code>{duplicate}</code>\n<b>╰ ▸ Non:</b> <code>{no_media}</code>\n")
                    break
                current += 1
                tz = pytz.timezone('Asia/Kolkata')
                today = datetime.date.today()
                now = datetime.datetime.now(tz)
                ttime = now.strftime("%I:%M:%S %p - %d %b, %Y")
                if current % 250 == 0:
                    can = [[InlineKeyboardButton('Cancel', callback_data='index_cancel')]]
                    reply = InlineKeyboardMarkup(can)
                    await asyncio.sleep(1)
                    elapsed_time = time.time() - start_time
                    remaining_time = (lst_msg_id - current - 1) * elapsed_time / (current - fst_msg_id + 1)
                    remaining_time_str = get_readable_time(remaining_time)
                    elapsed_time_str = get_readable_time(elapsed_time)
                    remaining_index = lst_msg_id - current
                    await msg.edit_text(
                        text=f"<b>╭ ▸ ETC: </b>{remaining_time_str} ❙ Remaining:</b> <code>{remaining_index}</code>\n<b>├ ▸ Last Updated: <i>{ttime}</i></b>\n<b>╰ ▸ Time Taken: </b>{elapsed_time_str} <b>\n\n<b>╭ ▸ Fetched:</b> <code>{current}</code>\n<b>├ ▸ Saved:</b> <code>{total_files}</code>\n<b>├ ▸ Duplicate:</b> <code>{duplicate}</code>\n<b>╰ ▸ Non:</b> <code>{no_media}</code>\n",
                        reply_markup=reply)
                if message.empty:
                    no_media += 1
                    continue
                elif not message.media:
                    no_media += 1
                    continue
                elif message.media not in [enums.MessageMediaType.VIDEO, enums.MessageMediaType.DOCUMENT]:
                    no_media += 1
                    continue
                media = getattr(message, message.media.value, None)
                if not media:
                    no_media += 1
                    continue
                if media.mime_type not in ['video/mp4', 'video/x-matroska']:
                    no_media += 1
                    continue
                media.file_type = message.media.value
                media.caption = message.caption
                tz = pytz.timezone('Asia/Kolkata')
                today = datetime.date.today()
                now = datetime.datetime.now(tz)
                ttime = now.strftime("%I:%M:%S %p - %d %b, %Y")
                tru = await check_file(media)
                if tru == "okda":
                    aynav, vnay = await save_file2(media) 
                    if aynav:
                        total_files += 1
                    elif vnay == 0:
                        duplicate += 1
                    elif vnay == 2:
                        errors += 1
                else:
                    duplicate += 1                
        except Exception as e:
            logger.exception(e)
            return await bot.send_message(msg.chat.id, f'<b>🚫 Error:</b> {e}\n\n<b>╭ ▸ ETC: </b>{remaining_time_str} ❙ Remaining:</b> <code>{remaining_index}</code>\n<b>├ ▸ Last Updated: <i>{ttime}</i></b>\n<b>╰ ▸ Time Taken: </b>{elapsed_time_str} <b>\n\n<b>╭ ▸ Fetched:</b> <code>{current}</code>\n<b>├ ▸ Saved:</b> <code>{total_files}</code>\n<b>├ ▸ Duplicate:</b> <code>{duplicate}</code>\n<b>╰ ▸ Non:</b> <code>{no_media}</code>\n')
        else:
            await bot.send_message(msg.chat.id, f'<b>✅ Successfully Completed!!</b>\n\n<b>╭ ▸ ETC: </b>{remaining_time_str} ❙ Remaining:</b> <code>{remaining_index}</code>\n<b>├ ▸ Last Updated: <i>{ttime}</i></b>\n<b>╰ ▸ Time Taken: </b>{elapsed_time_str} <b>\n\n<b>╭ ▸ Fetched:</b> <code>{current}</code>\n<b>├ ▸ Saved:</b> <code>{total_files}</code>\n<b>├ ▸ Duplicate:</b> <code>{duplicate}</code>\n<b>╰ ▸ Non:</b> <code>{no_media}</code>\n')


async def index_files_to_db2(lst_msg_id, chat, msg, bot):
    total_files = 0
    duplicate = 0
    no_media = 0
    fst_msg_id = temp.CURRENT
    start_time = time.time()
    remaining_time_str = "N/A"
    async with lock:
        try:
            current = temp.CURRENT
            tz = pytz.timezone('Asia/Kolkata')
            today = datetime.date.today()
            now = datetime.datetime.now(tz)
            ttime = now.strftime("%I:%M:%S %p - %d %b, %Y")
            temp.CANCEL = False
            elapsed_time = 0
            remaining_index = 0
            async for message in bot.iter_messages(chat, lst_msg_id, temp.CURRENT):
                if temp.CANCEL:
                    await msg.edit(f"<b>❌ Successfully Cancelled!!</b>\n\n<b>├ ▸ Last Updated: <i>{ttime}</i></b>\n\n<b>╭ ▸ Fetched:</b> <code>{current}</code>\n<b>├ ▸ Saved:</b> <code>{total_files}</code>\n<b>├ ▸ Duplicate:</b> <code>{duplicate}</code>\n<b>╰ ▸ Non:</b> <code>{no_media}</code>\n")
                    break
                current += 1
                tz = pytz.timezone('Asia/Kolkata')
                today = datetime.date.today()
                now = datetime.datetime.now(tz)
                ttime = now.strftime("%I:%M:%S %p - %d %b, %Y")
                if current % 250 == 0:
                    can = [[InlineKeyboardButton('Cancel', callback_data='index_cancel')]]
                    reply = InlineKeyboardMarkup(can)
                    await asyncio.sleep(1)
                    elapsed_time = time.time() - start_time
                    remaining_time = (lst_msg_id - current - 1) * elapsed_time / (current - fst_msg_id + 1)
                    remaining_time_str = get_readable_time(remaining_time)
                    elapsed_time_str = get_readable_time(elapsed_time)
                    remaining_index = lst_msg_id - current
                    await msg.edit_text(
                        text=f"<b>╭ ▸ ETC: </b>{remaining_time_str} ❙ Remaining:</b> <code>{remaining_index}</code>\n<b>├ ▸ Last Updated: <i>{ttime}</i></b>\n<b>╰ ▸ Time Taken: </b>{elapsed_time_str} <b>\n\n<b>╭ ▸ Fetched:</b> <code>{current}</code>\n<b>├ ▸ Saved:</b> <code>{total_files}</code>\n<b>├ ▸ Duplicate:</b> <code>{duplicate}</code>\n<b>╰ ▸ Non:</b> <code>{no_media}</code>\n",
                        reply_markup=reply)
                if message.empty:
                    no_media += 1
                    continue
                elif not message.media:
                    no_media += 1
                    continue
                elif message.media not in [enums.MessageMediaType.VIDEO, enums.MessageMediaType.DOCUMENT]:
                    no_media += 1
                    continue
                media = getattr(message, message.media.value, None)
                if not media:
                    no_media += 1
                    continue
                if media.mime_type not in ['video/mp4', 'video/x-matroska']:
                    no_media += 1
                    continue
                media.file_type = message.media.value
                media.caption = message.caption
                tz = pytz.timezone('Asia/Kolkata')
                today = datetime.date.today()
                now = datetime.datetime.now(tz)
                ttime = now.strftime("%I:%M:%S %p - %d %b, %Y")
                tru = await check_file(media)
                if tru == "okda":
                    aynav, vnay = await save_file3(media) 
                    if aynav:
                        total_files += 1
                    elif vnay == 0:
                        duplicate += 1
                    elif vnay == 2:
                        errors += 1
                else:
                    duplicate += 1                
        except Exception as e:
            logger.exception(e)
            return await bot.send_message(msg.chat.id, f'<b>🚫 Error:</b> {e}\n\n<b>╭ ▸ ETC: </b>{remaining_time_str} ❙ Remaining:</b> <code>{remaining_index}</code>\n<b>├ ▸ Last Updated: <i>{ttime}</i></b>\n<b>╰ ▸ Time Taken: </b>{elapsed_time_str} <b>\n\n<b>╭ ▸ Fetched:</b> <code>{current}</code>\n<b>├ ▸ Saved:</b> <code>{total_files}</code>\n<b>├ ▸ Duplicate:</b> <code>{duplicate}</code>\n<b>╰ ▸ Non:</b> <code>{no_media}</code>\n')
        else:
            await bot.send_message(msg.chat.id, f'<b>✅ Successfully Completed!!</b>\n\n<b>╭ ▸ ETC: </b>{remaining_time_str} ❙ Remaining:</b> <code>{remaining_index}</code>\n<b>├ ▸ Last Updated: <i>{ttime}</i></b>\n<b>╰ ▸ Time Taken: </b>{elapsed_time_str} <b>\n\n<b>╭ ▸ Fetched:</b> <code>{current}</code>\n<b>├ ▸ Saved:</b> <code>{total_files}</code>\n<b>├ ▸ Duplicate:</b> <code>{duplicate}</code>\n<b>╰ ▸ Non:</b> <code>{no_media}</code>\n')
          
async def index_files_to_db3(lst_msg_id, chat, msg, bot):
    total_files = 0
    duplicate = 0
    no_media = 0
    fst_msg_id = temp.CURRENT
    start_time = time.time()
    remaining_time_str = "N/A"
    async with lock:
        try:
            current = temp.CURRENT
            tz = pytz.timezone('Asia/Kolkata')
            today = datetime.date.today()
            now = datetime.datetime.now(tz)
            ttime = now.strftime("%I:%M:%S %p - %d %b, %Y")
            temp.CANCEL = False
            elapsed_time = 0
            remaining_index = 0
            async for message in bot.iter_messages(chat, lst_msg_id, temp.CURRENT):
                if temp.CANCEL:
                    await msg.edit(f"<b>❌ Successfully Cancelled!!</b>\n\n<b>├ ▸ Last Updated: <i>{ttime}</i></b>\n\n<b>╭ ▸ Fetched:</b> <code>{current}</code>\n<b>├ ▸ Saved:</b> <code>{total_files}</code>\n<b>├ ▸ Duplicate:</b> <code>{duplicate}</code>\n<b>╰ ▸ Non:</b> <code>{no_media}</code>\n")
                    break
                current += 1
                tz = pytz.timezone('Asia/Kolkata')
                today = datetime.date.today()
                now = datetime.datetime.now(tz)
                ttime = now.strftime("%I:%M:%S %p - %d %b, %Y")
                if current % 250 == 0:
                    can = [[InlineKeyboardButton('Cancel', callback_data='index_cancel')]]
                    reply = InlineKeyboardMarkup(can)
                    await asyncio.sleep(1)
                    elapsed_time = time.time() - start_time
                    remaining_time = (lst_msg_id - current - 1) * elapsed_time / (current - fst_msg_id + 1)
                    remaining_time_str = get_readable_time(remaining_time)
                    elapsed_time_str = get_readable_time(elapsed_time)
                    remaining_index = lst_msg_id - current
                    await msg.edit_text(
                        text=f"<b>╭ ▸ ETC: </b>{remaining_time_str} ❙ Remaining:</b> <code>{remaining_index}</code>\n<b>├ ▸ Last Updated: <i>{ttime}</i></b>\n<b>╰ ▸ Time Taken: </b>{elapsed_time_str} <b>\n\n<b>╭ ▸ Fetched:</b> <code>{current}</code>\n<b>├ ▸ Saved:</b> <code>{total_files}</code>\n<b>├ ▸ Duplicate:</b> <code>{duplicate}</code>\n<b>╰ ▸ Non:</b> <code>{no_media}</code>\n",
                        reply_markup=reply)
                if message.empty:
                    no_media += 1
                    continue
                elif not message.media:
                    no_media += 1
                    continue
                elif message.media not in [enums.MessageMediaType.VIDEO, enums.MessageMediaType.DOCUMENT]:
                    no_media += 1
                    continue
                media = getattr(message, message.media.value, None)
                if not media:
                    no_media += 1
                    continue
                if media.mime_type not in ['video/mp4', 'video/x-matroska']:
                    no_media += 1
                    continue
                media.file_type = message.media.value
                media.caption = message.caption
                tz = pytz.timezone('Asia/Kolkata')
                today = datetime.date.today()
                now = datetime.datetime.now(tz)
                ttime = now.strftime("%I:%M:%S %p - %d %b, %Y")
                tru = await check_file(media)
                if tru == "okda":
                    aynav, vnay = await save_file4(media) 
                    if aynav:
                        total_files += 1
                    elif vnay == 0:
                        duplicate += 1
                    elif vnay == 2:
                        errors += 1
                else:
                    duplicate += 1                
        except Exception as e:
            logger.exception(e)
            return await bot.send_message(msg.chat.id, f'<b>🚫 Error:</b> {e}\n\n<b>╭ ▸ ETC: </b>{remaining_time_str} ❙ Remaining:</b> <code>{remaining_index}</code>\n<b>├ ▸ Last Updated: <i>{ttime}</i></b>\n<b>╰ ▸ Time Taken: </b>{elapsed_time_str} <b>\n\n<b>╭ ▸ Fetched:</b> <code>{current}</code>\n<b>├ ▸ Saved:</b> <code>{total_files}</code>\n<b>├ ▸ Duplicate:</b> <code>{duplicate}</code>\n<b>╰ ▸ Non:</b> <code>{no_media}</code>\n')
        else:
            await bot.send_message(msg.chat.id, f'<b>✅ Successfully Completed!!</b>\n\n<b>╭ ▸ ETC: </b>{remaining_time_str} ❙ Remaining:</b> <code>{remaining_index}</code>\n<b>├ ▸ Last Updated: <i>{ttime}</i></b>\n<b>╰ ▸ Time Taken: </b>{elapsed_time_str} <b>\n\n<b>╭ ▸ Fetched:</b> <code>{current}</code>\n<b>├ ▸ Saved:</b> <code>{total_files}</code>\n<b>├ ▸ Duplicate:</b> <code>{duplicate}</code>\n<b>╰ ▸ Non:</b> <code>{no_media}</code>\n')

async def index_files_to_db(lst_msg_id, chat, msg, bot):
    start_time = time.time()
    elapsed_time_str = "0s"  # default fallback to prevent UnboundLocalError
    total_files = 0
    duplicate = 0
    no_media = 0
    fst_msg_id = temp.CURRENT
    remaining_time_str = "N/A"
    async with lock:
        try:
            current = temp.CURRENT
            tz = pytz.timezone('Asia/Kolkata')
            today = datetime.date.today()
            now = datetime.datetime.now(tz)
            ttime = now.strftime("%I:%M:%S %p - %d %b, %Y")
            temp.CANCEL = False
            elapsed_time = 0
            remaining_index = 0
            async for message in bot.iter_messages(chat, lst_msg_id, temp.CURRENT):
                if temp.CANCEL:
                    await msg.edit(f"<b>❌ Successfully Cancelled!!</b>\n\n<b>├ ▸ Last Updated: <i>{ttime}</i></b>\n\n<b>╭ ▸ Fetched:</b> <code>{current}</code>\n<b>├ ▸ Saved:</b> <code>{total_files}</code>\n<b>├ ▸ Duplicate:</b> <code>{duplicate}</code>\n<b>╰ ▸ Non:</b> <code>{no_media}</code>\n")
                    break
                current += 1
                tz = pytz.timezone('Asia/Kolkata')
                today = datetime.date.today()
                now = datetime.datetime.now(tz)
                ttime = now.strftime("%I:%M:%S %p - %d %b, %Y")              
                if current % 500 == 0:
                    can = [[InlineKeyboardButton('Cancel', callback_data='index_cancel')]]
                    reply = InlineKeyboardMarkup(can)
                    await asyncio.sleep(1)
                    elapsed_time = time.time() - start_time
                    remaining_time = (lst_msg_id - current - 1) * elapsed_time / (current - fst_msg_id + 1)
                    remaining_time_str = get_readable_time(remaining_time)
                    elapsed_time_str = get_readable_time(elapsed_time)
                    remaining_index = lst_msg_id - current
                    incol.update_one(
                        {"_id": "index_progress"},
                        {"$set": {"last_indexed_file": current, "last_msg_id": lst_msg_id, "chat_id": chat}},
                        upsert=True
                    )
                    await msg.edit_text(
                        text=f"<b>╭ ▸ ETC: </b>{remaining_time_str} ❙ Remaining:</b> <code>{remaining_index}</code>\n<b>├ ▸ Last Updated: <i>{ttime}</i></b>\n<b>╰ ▸ Time Taken: </b>{elapsed_time_str} <b>\n\n<b>╭ ▸ Fetched:</b> <code>{current}</code>\n<b>├ ▸ Saved:</b> <code>{total_files}</code>\n<b>├ ▸ Duplicate:</b> <code>{duplicate}</code>\n<b>╰ ▸ Non:</b> <code>{no_media}</code>\n",
                        reply_markup=reply)                   
                if message.empty:
                    no_media += 1
                    continue
                elif not message.media:
                    no_media += 1
                    continue
                elif message.media not in [enums.MessageMediaType.VIDEO, enums.MessageMediaType.DOCUMENT]:
                    no_media += 1
                    continue
                media = getattr(message, message.media.value, None)
                if not media:
                    no_media += 1
                    continue
                if media.mime_type not in ['video/mp4', 'video/x-matroska']:
                    no_media += 1
                    continue
                media.file_type = message.media.value
                media.caption = message.caption
                tz = pytz.timezone('Asia/Kolkata')
                today = datetime.date.today()
                now = datetime.datetime.now(tz)
                ttime = now.strftime("%I:%M:%S %p - %d %b, %Y")
                if current % 3 == 0:   
                    tru = await check_file(media)
                    if tru == "okda":
                        aynav, vnay = await save_file2(media) 
                        if aynav:
                            total_files += 1
                        elif vnay == 0:
                            duplicate += 1
                        elif vnay == 2:
                            errors += 1
                    else:
                        duplicate += 1
                elif current % 3 == 1:   
                    tru = await check_file(media)
                    if tru == "okda":
                        aynav, vnay = await save_file3(media) 
                        if aynav:
                            total_files += 1
                        elif vnay == 0:
                            duplicate += 1
                        elif vnay == 2:
                            errors += 1
                    else:
                        duplicate += 1                
                else:  
                    tru = await check_file(media)
                    if tru:
                        aynav, vnay = await save_file4(media)                    
                        if aynav:
                            total_files += 1
                        elif vnay == 0:
                            duplicate += 1
                        elif vnay == 2:
                            errors += 1
                    else:
                        duplicate += 1
        except Exception as e:
            logger.exception(e)
            return await bot.send_message(msg.chat.id, f'<b>🚫 Error:</b> {e}\n\n<b>╭ ▸ ETC: </b>{remaining_time_str} ❙ Remaining:</b> <code>{remaining_index}</code>\n<b>├ ▸ Last Updated: <i>{ttime}</i></b>\n<b>\n\n<b>╭ ▸ Fetched:</b> <code>{current}</code>\n<b>├ ▸ Saved:</b> <code>{total_files}</code>\n<b>├ ▸ Duplicate:</b> <code>{duplicate}</code>\n<b>╰ ▸ Non:</b> <code>{no_media}</code>\n')
        else:
            elapsed_time = time.time() - start_time
            elapsed_time_str = f"{elapsed_time:.2f}s"
            
            await bot.send_message(msg.chat.id, f'<b>✅ Successfully Completed!!</b>\n\n<b>╭ ▸ ETC: </b>{remaining_time_str} ❙ Remaining:</b> <code>{remaining_index}</code>\n<b>├ ▸ Last Updated: <i>{ttime}</i></b>\n<b>╰ ▸ Time Taken: </b>{elapsed_time_str} <b>\n\n<b>╭ ▸ Fetched:</b> <code>{current}</code>\n<b>├ ▸ Saved:</b> <code>{total_files}</code>\n<b>├ ▸ Duplicate:</b> <code>{duplicate}</code>\n<b>╰ ▸ Non:</b> <code>{no_media}</code>\n')
            incol.delete_one({"_id": "index_progress"})
