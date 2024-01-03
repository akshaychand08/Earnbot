from datetime import timedelta
import pytz
import asyncio
from utils import get_size, get_settings, temp
import datetime, time
from database.users_chats_db import db 
from pyrogram.types import InlineKeyboardButton, InlineKeyboardMarkup


async def send_all_files(client, message, files, chat_id):
    for msg in files:
        title = msg.file_name
        size=get_size(msg.file_size)
        f_caption=msg.caption
        user = message.from_user.mention 
        settings = await get_settings(int(chat_id))
        CAPTION = settings['caption']
        f_caption = CAPTION.format(
            file_name='' if title is None else title,
            file_size='' if size is None else size,
            file_caption='' if f_caption is None else f_caption,
            user='' if user is None else user
        )
        await client.send_cached_media(
            chat_id=message.from_user.id,
            file_id=msg.file_id,
            caption=f_caption,    #<b>📝 NAME ➠ : <a href=https://t.me/OnlineTubeFiles>{msg.file_name}</a>\n\n⚙️ SIZE ➠ : {get_size(msg.file_size)}</b>",	    
            protect_content=False,
            reply_markup=InlineKeyboardMarkup([[InlineKeyboardButton("👨‍👩‍👧‍👦 ᴘʟᴇᴀsᴇ sʜᴀʀᴇ & sᴜᴘᴘᴏʀᴛ 🧲", url=f"https://t.me/share/url?url=https://t.me/{temp.U_NAME}"),]]))
        



async def send_files(client, message, files, chat_id):
    file = files
    title = file.file_name
    size=get_size(file.file_size)
    f_caption=file.caption    
    file_id=file.file_id
    user = message.from_user.mention 
    settings = await get_settings(int(chat_id))
    CAPTION = settings['caption']
    f_caption = CAPTION.format(
        file_name='' if title is None else title,
        file_size='' if size is None else size,
        file_caption='' if f_caption is None else f_caption,
        user='' if user is None else user
    )    
    await client.send_cached_media(
        chat_id=message.from_user.id,
        file_id=file.file_id,
        caption=f_caption,     #f"<b>📝 NAME ➠ : <a href=https://t.me/OnlineTubeFiles>{file.file_name}</a>\n\n⚙️ SIZE ➠ : {get_size(file.file_size)}</b>",
        protect_content=False, #if pre == 'filep' else False,
        reply_markup=InlineKeyboardMarkup([[InlineKeyboardButton("👨‍👩‍👧‍👦 ᴘʟᴇᴀsᴇ sʜᴀʀᴇ & sᴜᴘᴘᴏʀᴛ 🧲", url=f"https://t.me/share/url?url=https://t.me/{temp.U_NAME}"),]]))
