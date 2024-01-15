import os
import logging
import random
import asyncio
import string
import pytz
import datetime
from datetime import datetime
from .sendall import  send_all_files, send_files
from Script import script, SECOND_VERIFY_COMPLETE_TEXT, SECOND_VERIFICATION_TEXT, VERIFY_TEXT, VERIFY_COMPLETE_TEXT, VERIFIED_TXT
from pyrogram import Client, filters, enums
from pyrogram.errors import ChatAdminRequired, FloodWait
from pyrogram.types import *
from pyrogram.errors.exceptions.bad_request_400 import MessageTooLong
from database.ia_filterdb import Media, get_file_details, unpack_new_file_id, get_bad_files
from database.users_chats_db import db
from info import FSUBOFF, PICS_1, ALL_SHORT_LINK_OFF, AUTO_FFILTER, AUTO_DELETE, IMDB_TEMPLATE, VERIFY_LOG, IS_VERIFY, TUTORIAL_LINK_2, TUTORIAL_LINK_1, VERIFY_LOG, VERIFY_IMG, USERNAME, CHANNELS, ADMINS, AUTH_CHANNEL, LOG_CHANNEL, PICS, BATCH_FILE_CAPTION, CUSTOM_FILE_CAPTION, PROTECT_CONTENT, CHNL_LNK, GRP_LNK, REQST_CHANNEL, SUPPORT_CHAT_ID, SUPPORT_CHAT, MAX_B_TN, VERIFY, SHORTLINK_API, SHORTLINK_URL, TUTORIAL, IS_TUTORIAL, REQST_CHANNEL
from utils import is_int, is_bot_admin, get_vr_shortlink, get_settings, get_size, is_subscribed, save_group_settings, temp, get_shortlink, get_tutorial
from database.connections_mdb import active_connection
from shortzy import Shortzy 
import re, asyncio, os, sys
import json
import base64
logger = logging.getLogger(__name__)

BATCH_FILES = {}

@Client.on_message(filters.command("start") & filters.incoming)
async def start(client, message):
    m = message
    user_id = m.from_user.id
    if len(m.command) == 2 and m.command[1].startswith('notcopy'):
        user_id = int(m.command[1].split("_")[1])
        verify_id = m.command[1].split("_")[2]
        file_id = m.command[1].split("_")[3] if len(m.command[1].split("_")) > 3 else None
        verify_id_info = await db.get_verify_id_info(user_id, verify_id)
        if not verify_id_info or verify_id_info["verified"]:
            await message.reply("Invalid link. Link has already verified or has wrong hash. Try Again")
            return

        ist_timezone = pytz.timezone('Asia/Kolkata')
        
        key = "second_time_verified" if await db.is_user_verified(user_id) else "last_verified"
        current_time = datetime.now(tz=ist_timezone)

        result = await db.update_notcopy_user(user_id, {key:current_time})
        grpids = temp.GET_ID.get(user_id)
        settings = await get_settings(int(grpids))
        VERIFY_LOGS = settings['log_channel']	
        await db.update_verify_id_info(user_id, verify_id, {"verified":True})
        num =  2 if key == "second_time_verified" else 1	
        txt = SECOND_VERIFY_COMPLETE_TEXT if key == "second_time_verified" else VERIFY_COMPLETE_TEXT
        await client.send_message(VERIFY_LOGS, VERIFIED_TXT.format(m.from_user.mention, user_id, datetime.now(pytz.timezone('Asia/Kolkata')).strftime('%d %B %Y'), num))
        dmm = await m.reply_photo(
        photo=(VERIFY_IMG), 
        caption=(txt.format(message.from_user.mention)), 
        reply_markup=InlineKeyboardMarkup([[InlineKeyboardButton("♻️ ᴄʟɪᴄᴋ ʜᴇʀᴇ ᴛᴏ ɢᴇᴛ ғɪʟᴇ ♻️", url=f"https://telegram.me/{temp.U_NAME}?start=files_{int(grpids)}_{file_id}"),]]),parse_mode=enums.ParseMode.HTML)
        return		
	    
    if message.chat.type in [enums.ChatType.GROUP, enums.ChatType.SUPERGROUP]:
        buttons = [[
                    InlineKeyboardButton('ᴀᴅᴅ ᴍᴇ ᴛᴏ ʏᴏᴜʀ ɢʀᴏᴜᴘ', url=f'http://t.me/{temp.U_NAME}?startgroup=true')
                  ],[
                    InlineKeyboardButton('ᴜᴘᴅᴀᴛᴇs', url='https://t.me/arsOfficial10'),
                    InlineKeyboardButton('sᴜᴘᴘᴏʀᴛ', url='https://t.me/iPapdiscussion')
                  ],[
                    InlineKeyboardButton('ʜᴇʟᴘ', url=f"https://t.me/{temp.U_NAME}?start=help")
                  ]]
        reply_markup = InlineKeyboardMarkup(buttons)
        kd = await message.reply_photo(
        photo=random.choice(PICS_1),
        caption=script.START_TXT.format(message.from_user.mention if message.from_user else message.chat.title, temp.U_NAME, temp.B_NAME), reply_markup=reply_markup)
        await asyncio.sleep(25)
        await kd.delete()
        await message.delete()
        if not await db.get_chat(message.chat.id):
            total=await client.get_chat_members_count(message.chat.id)
            await client.send_message(LOG_CHANNEL, script.LOG_TEXT_G.format(message.chat.title, message.chat.id, total, "Unknown"))       
            await db.add_chat(message.chat.id, message.chat.title)
        return 
    if not await db.is_user_exist(message.from_user.id):
        await db.add_user(message.from_user.id, message.from_user.first_name)
        await client.send_message(LOG_CHANNEL, script.LOG_TEXT_P.format(message.from_user.id, message.from_user.mention))
    if len(message.command) != 2:
        buttons = [[
                    InlineKeyboardButton('➕ Aᴅᴅ Mᴇ Tᴏ Yᴏᴜʀ Gʀᴏᴜᴘ ➕', url=f'http://t.me/{temp.U_NAME}?startgroup=true')
                ],[
                    InlineKeyboardButton('🔱 SUPPORT CHANNEL 🔱', url= 'https://t.me/arsOfficial10')
                ],[
		    InlineKeyboardButton('〄 Hᴇʟᴘ', callback_data='help'),
                    InlineKeyboardButton('ABOUT', callback_data='about')
                  ]]
        reply_markup = InlineKeyboardMarkup(buttons)
        await message.reply_photo(
            photo=random.choice(PICS),
            caption=script.START_TXT.format(message.from_user.mention, temp.U_NAME, temp.B_NAME),
            reply_markup=reply_markup,
            parse_mode=enums.ParseMode.HTML
        )
        return
	    
    data = message.command[1]
    try:
        pre, grp_id, file_id = data.split('_', 2)
    except:
        file_id = data
        pre = ""

    temp.GET_ID[message.from_user.id] = grp_id
	
    settings = await get_settings(int(grp_id))
    if settings['fsub'] and not await is_subscribed(client, message, grp_id):
        try:
            invite_link = await client.create_chat_invite_link(settings['fsub'])
        except ChatAdminRequired:
            logger.error("Make sure Bot is admin in Forcesub channel")
            return
        btn = [
            [
                InlineKeyboardButton(
                    "‼️ ᴜᴘᴅᴀᴛᴇ ᴄʜᴀɴɴᴇʟ ‼️", url=invite_link.invite_link
                )
            ]
        ]

        if message.command[1] != "subscribe":
            try:
                kk, file_id = message.command[1].split("_", 1)
                pre = 'checksubp' if kk == 'filep' else 'checksub' 
                btn.append([InlineKeyboardButton("  ♻️ ᴛʀʏ ᴀɢᴀɪɴ ♻️", callback_data=f"{pre}#{file_id}")])
            except (IndexError, ValueError):
                btn.append([InlineKeyboardButton("  ♻️ ᴛʀʏ ᴀɢᴀɪɴ ♻️", url=f"https://t.me/{temp.U_NAME}?start={message.command[1]}")])
        await client.send_message(
            chat_id=message.from_user.id,
            text="**ᴘʟᴇᴀsᴇ ᴊᴏɪɴ ᴍʏ ᴜᴘᴅᴀᴛᴇs ᴄʜᴀɴɴᴇʟ\nᴛʜᴇɴ ᴄʟɪᴄᴋ ᴏɴ ᴛʀʏ ᴀɢᴀɪɴ ʙᴜᴛᴛᴏɴ 👇🏼**",
            reply_markup=InlineKeyboardMarkup(btn),
            parse_mode=enums.ParseMode.MARKDOWN
            )
        return
    if len(message.command) == 2 and message.command[1] in ["subscribe", "error", "okay", "help"]:
        buttons = [[
            InlineKeyboardButton('× ᴀᴅᴅ ᴍᴇ ᴛᴏ ʏᴏᴜʀ ɢʀᴏᴜᴘs ×', url=f'http://t.me/{temp.U_NAME}?startgroup=true')
        ]]
        reply_markup = InlineKeyboardMarkup(buttons)
        await message.reply_photo(
            photo=random.choice(PICS),
            caption=script.SUR_TXT.format(message.from_user.mention, temp.U_NAME, temp.B_NAME),
            reply_markup=reply_markup,
            parse_mode=enums.ParseMode.HTML
        )
        return
	 
    if data.startswith("short"):
        user = message.from_user.id
        chat_id = int(grp_id)
        files_ = await get_file_details(file_id)
        files = files_[0]      
        if not settings['verify_short']: 
            if settings['is_shortlink']:	
                files_ = await get_file_details(file_id)
                files = files_[0]		    
                g = await get_shortlink(chat_id, f"https://telegram.me/{temp.U_NAME}?start=file_{chat_id}_{file_id}")
                await client.send_message(chat_id=user,text=f"<b>📝 NAME ➠ : <code>{files.file_name}</code> \n\n⚙️ SIZE ➠ : {get_size(files.file_size)}\n\n📂 FILE LINK ➠ : {g}\n\n<i>Note: ⚠️ ᴛʜɪs ᴍᴇssᴀɢᴇ ᴡɪʟʟ ʙᴇ ᴀᴜᴛᴏ ᴅᴇʟᴇᴛᴇᴅ ᴀғᴛᴇʀ 𝟹𝟶 ᴍɪɴᴜᴛᴇs.</i></b>", reply_markup=InlineKeyboardMarkup(
                        [
                            [
                                InlineKeyboardButton('📂 ᴍᴏᴠɪᴇ ᴅᴏᴡɴʟᴏᴀᴅ ʟɪɴᴋ 📂', url=g)
                            ], [
                                InlineKeyboardButton('🤔 Hᴏᴡ Tᴏ Dᴏᴡɴʟᴏᴀᴅ 🤔', url=await get_tutorial(chat_id))
                        ]
                    ]
                )
            )
                return	 	
		    
    # User Verifying features 

    grpid = grp_id 
    settings = await get_settings(int(grp_id))
    TUTORIAL_LINK2 = settings['tutorial2']
    TUTORIAL_LINK1 = settings['tutorial']

    if settings['verify_short']: 
        pass
        #m = await message.reply_text('please wait') 
        #await m.delete()	         	    
    else:
        if not settings['is_shortlink']:
            user_verified = await db.is_user_verified(user_id)
            is_second_shortener = await db.use_second_shortener(user_id, grp_id)
            ist_timezone = pytz.timezone('Asia/Kolkata')
            how_to_download_link = TUTORIAL_LINK2 if is_second_shortener else TUTORIAL_LINK1
            if not user_verified or is_second_shortener:
                verify_id = ''.join(random.choices(string.ascii_uppercase + string.digits, k=7))
                await db.create_verify_id(user_id, verify_id)
                buttons = [[InlineKeyboardButton(text="♨️ ᴠᴇʀɪꜰʏ ♨️", url=await get_vr_shortlink(grpid, f"https://telegram.me/{temp.U_NAME}?start=notcopy_{user_id}_{verify_id}_{file_id}", is_second_shortener),),], [InlineKeyboardButton(text="⁉️ ʜᴏᴡ ᴛᴏ ᴠᴇʀɪꜰʏ ⁉️", url=how_to_download_link)]]
                reply_markup=InlineKeyboardMarkup(buttons)
                num = 2 if is_second_shortener else 1
                bin_text = SECOND_VERIFICATION_TEXT if is_second_shortener else VERIFY_TEXT
                dmb = await m.reply_text(
                    text=(bin_text.format(message.from_user.mention)),
                    reply_markup=reply_markup,
                    parse_mode=enums.ParseMode.HTML
                )
                await asyncio.sleep(120) 
                await dmb.delete()
                return   
		    
	# verify features ended 

	
	
    files_ = await get_file_details(file_id)           
    if not files_:
        pre, file_id = ((base64.urlsafe_b64decode(data + "=" * (-len(data) % 4))).decode("ascii")).split("_", 1)
        return await message.reply('No such file exist.')

    files = files_[0]
    title = ' '.join(filter(lambda x: not x.startswith('[') and not x.startswith('@'), files.file_name.split()))
    size=get_size(files.file_size)
    f_caption=files.caption
    user = message.from_user.mention 
    settings = await get_settings(int(grp_id))
    CAPTION = settings['caption']
    f_caption = CAPTION.format(
        file_name='' if title is None else title,
        file_size='' if size is None else size,
        file_caption='' if f_caption is None else f_caption,
	user='' if user is None else user
    )
    await client.send_cached_media(
        chat_id=message.from_user.id,
        file_id=file_id,
        caption=f_caption,       #<b>📝 NAME ➠ : <a href=https://t.me/OnlineTubeFiles>{files.file_name}</a>\n\n⚙️ SIZE ➠ : {get_size(files.file_size)}</b>",    
        protect_content=True if pre == 'filep' else False,
        reply_markup=InlineKeyboardMarkup([[InlineKeyboardButton("👨‍👩‍👧‍👦 ᴘʟᴇᴀsᴇ sʜᴀʀᴇ & sᴜᴘᴘᴏʀᴛ 🧲", url=f"https://t.me/share/url?url=https://t.me/{temp.U_NAME}"),]]))


@Client.on_message(filters.command('channel') & filters.user(ADMINS))
async def channel_info(bot, message):
           
    """Send basic information of channel"""
    if isinstance(CHANNELS, (int, str)):
        channels = [CHANNELS]
    elif isinstance(CHANNELS, list):
        channels = CHANNELS
    else:
        raise ValueError("Unexpected type of CHANNELS")

    text = '📑 **Indexed channels/groups**\n'
    for channel in channels:
        chat = await bot.get_chat(channel)
        if chat.username:
            text += '\n@' + chat.username
        else:
            text += '\n' + chat.title or chat.first_name

    text += f'\n\n**Total:** {len(CHANNELS)}'

    if len(text) < 4096:
        await message.reply(text)
    else:
        file = 'Indexed channels.txt'
        with open(file, 'w') as f:
            f.write(text)
        await message.reply_document(file)
        os.remove(file)


@Client.on_message(filters.command('logs') & filters.user(ADMINS))
async def log_file(bot, message):
    """Send log file"""
    try:
        await message.reply_document('TelegramBot.log')
    except Exception as e:
        await message.reply(str(e))

@Client.on_message(filters.command('delete') & filters.user(ADMINS))
async def delete(bot, message):
    """Delete file from database"""
    reply = message.reply_to_message
    if reply and reply.media:
        msg = await message.reply("Processing...⏳", quote=True)
    else:
        await message.reply('Reply to file with /delete which you want to delete', quote=True)
        return

    for file_type in ("document", "video", "audio"):
        media = getattr(reply, file_type, None)
        if media is not None:
            break
    else:
        await msg.edit('This is not supported file format')
        return
    
    file_id, file_ref = unpack_new_file_id(media.file_id)

    result = await Media.collection.delete_one({
        '_id': file_id,
    })
    if result.deleted_count:
        await msg.edit('File is successfully deleted from database')
    else:
        file_name = re.sub(r"(_|\-|\.|\+)", " ", str(media.file_name))
        result = await Media.collection.delete_many({
            'file_name': file_name,
            'file_size': media.file_size,
            'mime_type': media.mime_type
            })
        if result.deleted_count:
            await msg.edit('File is successfully deleted from database')
        else:
            # files indexed before https://github.com/EvamariaTG/EvaMaria/commit/f3d2a1bcb155faf44178e5d7a685a1b533e714bf#diff-86b613edf1748372103e94cacff3b578b36b698ef9c16817bb98fe9ef22fb669R39 
            # have original file name.
            result = await Media.collection.delete_many({
                'file_name': media.file_name,
                'file_size': media.file_size,
                'mime_type': media.mime_type
            })
            if result.deleted_count:
                await msg.edit('File is successfully deleted from database')
            else:
                await msg.edit('File not found in database')


@Client.on_message(filters.command('deleteall') & filters.user(ADMINS))
async def delete_all_index(bot, message):
    await message.reply_text(
        'This will delete all indexed files.\nDo you want to continue??',
        reply_markup=InlineKeyboardMarkup(
            [
                [
                    InlineKeyboardButton(
                        text="YES", callback_data="autofilter_delete"
                    )
                ],
                [
                    InlineKeyboardButton(
                        text="CANCEL", callback_data="close_data"
                    )
                ],
            ]
        ),
        quote=True,
    )


@Client.on_callback_query(filters.regex(r'^autofilter_delete'))
async def delete_all_index_confirm(bot, message):
    await Media.collection.drop()
    await message.answer('Piracy Is Crime')
    await message.message.edit('Succesfully Deleted All The Indexed Files.')


@Client.on_message(filters.command('settings'))
async def settings(client, message):
    userid = message.from_user.id if message.from_user else None
    if not userid:
        return await message.reply(f"You are anonymous admin. Use /connect {message.chat.id} in PM")
    chat_type = message.chat.type

    if chat_type == enums.ChatType.PRIVATE:
        grpid = await active_connection(str(userid))
        if grpid is not None:
            grp_id = grpid
            try:
                chat = await client.get_chat(grpid)
                title = chat.title
            except:
                await message.reply_text("Make sure I'm present in your group!!", quote=True)
                return
        else:
            await message.reply_text("I'm not connected to any groups!", quote=True)
            return

    elif chat_type in [enums.ChatType.GROUP, enums.ChatType.SUPERGROUP]:
        grp_id = message.chat.id
        title = message.chat.title

    else:
        return

    st = await client.get_chat_member(grp_id, userid)
    if (
            st.status != enums.ChatMemberStatus.ADMINISTRATOR
            and st.status != enums.ChatMemberStatus.OWNER
            and str(userid) not in ADMINS
    ):
        return
    
    settings = await get_settings(grp_id)

    try:
        if settings['max_btn']:
            settings = await get_settings(grp_id)
    except KeyError:
        await save_group_settings(grp_id, 'max_btn', False)
        settings = await get_settings(grp_id)
    if 'is_shortlink' not in settings.keys():
        await save_group_settings(grp_id, 'is_shortlink', False)
    else:
        pass

    if settings is not None:
        buttons = [
            [
                InlineKeyboardButton(
                    'Rᴇsᴜʟᴛ Pᴀɢᴇ',
                    callback_data=f'setgs#button#{settings["button"]}#{grp_id}',
                ),
                InlineKeyboardButton(
                    'Bᴜᴛᴛᴏɴ' if settings["button"] else 'Tᴇxᴛ',
                    callback_data=f'setgs#button#{settings["button"]}#{grp_id}',
                ),
            ],
            [
                InlineKeyboardButton(
                    'Aᴜᴛᴏ-Dᴇʟᴇᴛᴇ',
                    callback_data=f'setgs#auto_delete#{settings["auto_delete"]}#{grp_id}',
                ),
                InlineKeyboardButton(
                    '10 Mɪɴs' if settings["auto_delete"] else '✘ Oғғ',
                    callback_data=f'setgs#auto_delete#{settings["auto_delete"]}#{grp_id}',
                ),
            ],
            [
                InlineKeyboardButton(
                    'sʜᴏʀᴛʟɪɴᴋ ᴍᴏᴅ',
                    callback_data=f'setgs#is_shortlink#{settings["is_shortlink"]}#{grp_id}',
                ),
                InlineKeyboardButton(
                    'ᴘᴍ ʟɪɴᴋ' if settings["is_shortlink"] else 'ᴠᴇʀɪғʏ',
                    callback_data=f'setgs#is_shortlink#{settings["is_shortlink"]}#{grp_id}',
                ),
            ],
        ]
        btn = [[
                InlineKeyboardButton("Oᴘᴇɴ Hᴇʀᴇ ↓", callback_data=f"opnsetgrp#{grp_id}"),
                InlineKeyboardButton("Oᴘᴇɴ Iɴ PM ⇲", callback_data=f"opnsetpm#{grp_id}")
              ]]

        reply_markup = InlineKeyboardMarkup(buttons)
        if chat_type in [enums.ChatType.GROUP, enums.ChatType.SUPERGROUP]:
            await message.reply_text(
                text="<b>Dᴏ ʏᴏᴜ ᴡᴀɴᴛ ᴛᴏ ᴏᴘᴇɴ sᴇᴛᴛɪɴɢs ʜᴇʀᴇ ?</b>",
                reply_markup=InlineKeyboardMarkup(btn),
                disable_web_page_preview=True,
                parse_mode=enums.ParseMode.HTML,
                reply_to_message_id=message.id
            )
        else:
            await message.reply_text(
                text=f"<b>Cʜᴀɴɢᴇ Yᴏᴜʀ Sᴇᴛᴛɪɴɢs Fᴏʀ {title} As Yᴏᴜʀ Wɪsʜ ⚙</b>",
                reply_markup=reply_markup,
                disable_web_page_preview=True,
                parse_mode=enums.ParseMode.HTML,
                reply_to_message_id=message.id
            )


@Client.on_message(filters.command("deletefiles") & filters.user(ADMINS))
async def deletemultiplefiles(bot, message):
    chat_type = message.chat.type
    if chat_type != enums.ChatType.PRIVATE:
        return await message.reply_text(f"<b>Hey {message.from_user.mention}, This command won't work in groups. It only works on my PM !</b>")
    else:
        pass
    try:
        keyword = message.text.split(" ", 1)[1]
    except:
        return await message.reply_text(f"<b>Hey {message.from_user.mention}, Give me a keyword along with the command to delete files.</b>")
    k = await bot.send_message(chat_id=message.chat.id, text=f"<b>Fetching Files for your query {keyword} on DB... Please wait...</b>")
    files, total = await get_bad_files(keyword)
    await k.delete()
    btn = [[
       InlineKeyboardButton("Yes, Continue !", callback_data=f"killfilesdq#{keyword}")
       ],[
       InlineKeyboardButton("No, Abort operation !", callback_data="close_data")
    ]]
    await message.reply_text(
        text=f"<b>Found {total} files for your query {keyword} !\n\nDo you want to delete?</b>",
        reply_markup=InlineKeyboardMarkup(btn),
        parse_mode=enums.ParseMode.HTML
    )




@Client.on_message(filters.command('set_caption'))
async def save_caption(client, message):
    userid = message.from_user.id if message.from_user else None
    if not userid:
        return await message.reply(f"You are anonymous admin. Use /connect {message.chat.id} in PM")
    chat_type = message.chat.type
    if chat_type == enums.ChatType.PRIVATE:
        grpid = await active_connection(str(userid))
        if grpid is not None:
            grp_id = grpid
            try:
                chat = await client.get_chat(grpid)
                title = chat.title
            except:
                await message.reply_text("Make sure I'm present in your group!!", quote=True)
                return
        else:
            await message.reply_text("I'm not connected to any groups!", quote=True)
            return
    elif chat_type in [enums.ChatType.GROUP, enums.ChatType.SUPERGROUP]:
        grp_id = message.chat.id
        title = message.chat.title
    else:
        return
    st = await client.get_chat_member(grp_id, userid)
    if (
            st.status != enums.ChatMemberStatus.ADMINISTRATOR
            and st.status != enums.ChatMemberStatus.OWNER
            and str(userid) not in ADMINS
    ):
        return
    try:
        caption = message.text.split(" ", 1)[1]
    except:
        return await message.reply_text("<b>Command Incomplete!!\n\nuse like this -</b>\nfor file name <code>{{file_name}}</code>\nfor file size <code>{{file_size}}</code>")
    
    await save_group_settings(grp_id, 'caption', caption)
    await message.reply_text(f"Successfully changed caption for {title} to\n\n{caption}")

@Client.on_message(filters.command("set_shortlink"))
async def set_shortlink(bot, message):
    sts = await message.reply("Please wait")
    chat_type = message.chat.type
    grp_id = message.chat.id
    userid = message.from_user.id
    if chat_type not in [enums.ChatType.GROUP, enums.ChatType.SUPERGROUP]:
        return await message.reply_text("<b>You can use this command only on groups.</b>")
    user = await bot.get_chat_member(grp_id, userid)
    if user.status != enums.ChatMemberStatus.ADMINISTRATOR and user.status != enums.ChatMemberStatus.OWNER and str(userid) not in ADMINS:
        return await message.reply_text("You are not authorised to use this command")
    content = message.text
    try:
        num, url, api = str(content).split(" ")[1:]
    except:
        return await sts.edit("<b>Hey, Use the correct format. \n\nExample:\n/set_shortlink 1 <a href=https://publicearn.com/ref/AkshayChand10>publicearn.com</a> 4b392f8eb6ad711be589ae36\n\nHere the first parameter is the number which decides the input shortlink is primary or secondary. Give 1 for setting it as primary. Give 2 for setting it as secondary.\n\nThe second parameter is the url of the shortlink website.\n\nThe third parameter is the api for the shortlink.</b>")

    try:
        shortzy = Shortzy(api_key=api, base_site=url)
        link = f'https://t.me/{temp.U_NAME}'
        await shortzy.convert(link)
    except:            
          btn = [[
          InlineKeyboardButton('owner', url="https://t.me/AkshayChand08")
          ]]
          delt=await sts.edit(f"𝗛𝗲𝘆 {message.from_user.mention}\n\n𝗬𝗼𝘂𝗿 𝘄𝗲𝗯𝘀𝗶𝘁𝗲 𝗮𝗻𝗱 𝗔𝗣𝗜 𝗶𝘀 𝘄𝗿𝗼𝗻𝗴 𝗼𝗿 𝘁𝗵𝗶𝘀 𝘄𝗲𝗯𝘀𝗶𝘁𝗲 𝗶𝘀 𝗱𝗼𝘄𝗻 𝗻𝗼𝘄 𝗽𝗹𝗲𝗮𝘀𝗲 𝗰𝗵𝗲𝗰𝗸 𝗮𝗴𝗮𝗶𝗻 𝗮𝗻𝗱 𝗮𝗱𝗱...\n\n𝙖𝙣𝙙 𝙋𝙡𝙚𝙖𝙨𝙚 𝙙𝙤𝙣'𝙩 𝙪𝙨𝙚:   𝗵𝘁𝘁𝗽𝘀://.\n\n𝗮𝗱𝗱 𝘁𝗵𝗶𝘀 𝘁𝘆𝗽𝗲: <code>/set_shortlink 1 <a href=https://publicearn.com/ref/AkshayChand10>publicearn.com</a> 4b392f8eb6ad711be589ae36\n\n𝗔𝗻𝘆 𝗶𝘀𝘀𝘂𝗲 𝗰𝗼𝗻𝘁𝗮𝗰𝘁 𝗺𝘆 𝗼𝘄𝗻𝗲𝗿 👇", disable_web_page_preview=True, reply_markup=InlineKeyboardMarkup(btn))        
          async def del_func():
              await asyncio.sleep(30)
              await delt.delete()
              await message.delete()
          await asyncio.create_task(del_func())
          return
        
    settings = await get_settings(int(grp_id))
    if int(num) == 1:
        await save_group_settings(grp_id, 'shortlink', url)
        await save_group_settings(grp_id, 'shortlink_api', api)    
        return await sts.edit(f"Successfully set as primary shortner.\n\nCurrent Status:\n\nPrimary Shortner URL: {settings['shortlink']}\n\nPrimary API: {settings['shortlink_api']}")
    elif int(num) == 2:
        await save_group_settings(grp_id, 'shortlink2', url)
        await save_group_settings(grp_id, 'shortlink_api2', api)  
        return await sts.edit(f"Successfully set as secondary shortner Only Verify.\n\nCurrent Status Verify Mode:\n\nSecondary URL: {settings['shortlink2']}\n\nSecondary API: {settings['shortlink_api2']}\n\nPrimary URL: {settings['shortlink']}\n\nPrimary API: {settings['shortlink_api']}") 
    else:
        return await sts.edit("Give valid number as the first parameter. Eg: 1 or 2")



@Client.on_message(filters.command("set_tutorial"))
async def set_tutorial(bot, message):
    chat_type = message.chat.type
    grp_id = message.chat.id
    userid = message.from_user.id
    if chat_type not in [enums.ChatType.GROUP, enums.ChatType.SUPERGROUP]:
        return await message.reply_text("<b>You can use this command only on groups.</b>")
    user = await bot.get_chat_member(grp_id, userid)
    if user.status != enums.ChatMemberStatus.ADMINISTRATOR and user.status != enums.ChatMemberStatus.OWNER and str(userid) not in ADMINS:
        return await message.reply_text("You are not authorised to use this command")
    content = message.text
    try:
        num, tutorial = str(content).split(" ")[1:]
    except:
        return await message.reply_text("<b>Hey, Use the correct format. \n\nExample:\n/set_tutorial 1 https://t.me/Howtodownlod\n\nHere the first parameter is the number which decides the input tutorial is primary or secondary. Give 1 for setting it as primary. Give 2 for setting it as secondary.\nThe second parameter is the url of the tutorial.</b>")
    settings = await get_settings(int(grp_id))
    if int(num) == 1:
        await save_group_settings(grp_id, 'tutorial', tutorial)        
        return await message.reply_text(f"Successfully set as secondary tutorial.\n\nCurrent Status:\n\nPrimary tutorial: {settings['tutorial']}\nSecondary tutorial: {settings['tutorial2']}") 
    elif int(num) == 2:
        await save_group_settings(grp_id, 'tutorial2', tutorial)        
        return await message.reply_text(f"Successfully set as secondary tutorial.\n\nCurrent Status:\n\nSecondary tutorial: {settings['tutorial2']}\nPrimary tutorial: {settings['tutorial']}") 
    else:
        return await message.reply_text("Give valid number as the first parameter. Eg: 1 or 2")


@Client.on_message(filters.command('set_fsub'))
async def set_fsub(client, message):
    if message.chat.type == enums.ChatType.PRIVATE:
        am = await message.reply_text('This command only working in groups\n\n ye commands keval groups me kaam karti hai')
        async def del_func():
            await asyncio.sleep(7)
            await am.delete()  
            await m.delete()  
        await asyncio.create_task(del_func())     
        return
    userid = message.from_user.id if message.from_user else None
    if not userid:
        return await message.reply("You are anonymous admin")
    sts= await message.reply("please wait....")
    grp_id = message.chat.id
    st = await client.get_chat_member(grp_id, userid)
    if st.status not in [
        enums.ChatMemberStatus.ADMINISTRATOR,
        enums.ChatMemberStatus.OWNER,
    ]:
        return await sts.edit("You are anonymous admin")

    if len(message.command) != 2:
        await sts.edit("⚠️ Invalid format\n\nuse like this: /set_fsub -100××××××")
        return

    elif is_int(message.command[1]):
        fsub = int(message.command[1])

        bot_admin = await is_bot_admin(client, fsub)
        if not bot_admin:
            await sts.edit(f"⚠️ Make sure this bot admin that channel\n\nMake @{temp.U_NAME} admin in given channel {fsub}")
            return
        await save_group_settings(grp_id, 'fsub', fsub)
        await sts.edit(f"<b>sᴜᴄᴄᴇꜱғᴜʟʟʏ ꜱᴇᴛ ʏᴏᴜʀ ғꜱᴜʙ ᴄʜᴀɴɴᴇʟ ғᴏʀ<b> {message.chat.title}\n\n<b>ɪᴅ</b>:- `{fsub}`")
		
    else:
        await sts.edit("⚠️ Channel ID invalid. plz add only channel id\n\nLike this /set_fsub -100××××××")
    return

@Client.on_message(filters.command('set_log_channel'))
async def save_logs_channel(client, message):
    if message.chat.type == enums.ChatType.PRIVATE:
        am = await message.reply_text('This command only working in groups\n\n ye commands keval groups me kaam karti hai')
        async def del_func():
            await asyncio.sleep(7)
            await am.delete()  
            await m.delete()  
        await asyncio.create_task(del_func())     
        return
    userid = message.from_user.id if message.from_user else None
    if not userid:
        return await message.reply("You are anonymous admin")
    sts= await message.reply("please wait....")
    grp_id = message.chat.id
    st = await client.get_chat_member(grp_id, userid)
    if st.status not in [
        enums.ChatMemberStatus.ADMINISTRATOR,
        enums.ChatMemberStatus.OWNER,
    ]:
        return await sts.edit("You are anonymous admin")

    if len(message.command) != 2:
        await sts.edit("⚠️ Invalid format\n\nuse like this: /set_log_channel -100××××××")
        return

    elif is_int(message.command[1]):
        log_channel = int(message.command[1])

        bot_admin = await is_bot_admin(client, log_channel)
        if not bot_admin:
            await sts.edit(f"⚠️ Make sure this bot admin that channel\n\nMake @{temp.U_NAME} admin in given channel {log_channel}")
            return
        await save_group_settings(grp_id, 'log_channel', log_channel)
        await sts.edit(f"✅ <b>sᴜᴄᴄᴇssꜰᴜʟʟʏ sᴇᴛ ʏᴏᴜʀ ʟᴏɢ ᴄʜᴀɴɴᴇʟ ꜰᴏʀ</b> {message.chat.title}\n\n<b>ɪᴅ</b> `{log_channel}`")
		
    else:
        await sts.edit("⚠️ Channel ID invalid. plz add only channel id\n\nLike this /set_log_channel -100××××××")
    return



@Client.on_message(filters.command("offfsub"))
async def offfsub(client, message):
    grpid = message.chat.id
    userid = message.from_user.id
    fsuboff = FSUBOFF
    chat_type = message.chat.type
    if chat_type == enums.ChatType.PRIVATE:
        return await message.reply_text("I will Work Only in group")
    elif chat_type in [enums.ChatType.GROUP, enums.ChatType.SUPERGROUP]:
        grpid = message.chat.id
        title = message.chat.title
    else:
        return
    st = await client.get_chat_member(grpid, userid)
    if st.status not in [
        enums.ChatMemberStatus.ADMINISTRATOR,
        enums.ChatMemberStatus.OWNER,
    ]:
        return await message.reply_text("You are anonymous admin")
    	    
    settings = await get_settings(int(grpid))
    await save_group_settings(grpid, 'fsub', fsuboff)
    return await message.reply_text(f"Successfully removed fsub channel")


@Client.on_message(filters.command("checkfsub"))
async def checkfsub(client, message):
    grpid = message.chat.id
    userid = message.from_user.id
    chat_type = message.chat.type
    if chat_type == enums.ChatType.PRIVATE:
        return await message.reply_text("I will Work Only in group")
    elif chat_type in [enums.ChatType.GROUP, enums.ChatType.SUPERGROUP]:
        grpid = message.chat.id
        title = message.chat.title
    else:
        return
    st = await client.get_chat_member(grpid, userid)
    if st.status not in [
        enums.ChatMemberStatus.ADMINISTRATOR,
        enums.ChatMemberStatus.OWNER,
    ]:
        return await message.reply_text("You are anonymous admin")
    	    
    settings = await get_settings(int(grpid))
    fsub = settings['fsub']
    return await message.reply_text(f"Active fsub channe.\n\n{fsub}")


@Client.on_message(filters.command('details'))
async def get_details(client, message):
    chat_type = message.chat.type
    if chat_type not in [enums.ChatType.GROUP, enums.ChatType.SUPERGROUP]:
        return await message.reply_text("Use this command in group.")
    grp_id = message.chat.id
    userid = message.from_user.id 
    title = message.chat.title
    st = await client.get_chat_member(grp_id, userid)
    if st.status not in [
        enums.ChatMemberStatus.ADMINISTRATOR,
        enums.ChatMemberStatus.OWNER,
    ]:
        return await message.reply_text("You are anonymous admin")
    
    settings = await get_settings(grp_id)
    un = message.from_user.mention
    u1 = settings["shortlink"]
    a1 = settings["shortlink_api"]
    u2 = settings["shortlink2"]
    a2 = settings["shortlink_api2"]
    t1 = settings['tutorial']
    t2 = settings['tutorial2']
    fs = settings['fsub']
    it = settings['template']
    fc = settings['caption']	
    btn = [[
        InlineKeyboardButton(text="Close", callback_data="close_data")
    ]]
    await message.reply(script.CUSTOM_DETAILS.format(un, title, u1, a1, t1, u2, a2, t2, fs, it, fc), reply_markup=InlineKeyboardMarkup(btn), disable_web_page_preview=True)


@Client.on_message(filters.command("verify2") & filters.incoming)
async def verify2(c: Client, m):
    userid = m.from_user.id if m.from_user else None
    if not userid:
        return await m.reply("You are anonymous admin")
    chat_type = m.chat.type
    if chat_type == enums.ChatType.PRIVATE:
        grpid = await active_connection(str(userid))
        if grpid is not None:
            grp_id = grpid
            try:
                chat = await client.get_chat(grpid)
                title = chat.title
            except:
                await m.reply_text("Make sure I'm present in your group!!", quote=True)
                return
        else:
            await m.reply_text("I'm not connected to any groups!", quote=True)
            return

    elif chat_type in [enums.ChatType.GROUP, enums.ChatType.SUPERGROUP]:
        grp_id = m.chat.id
        title = m.chat.title
    else:
        return
    grp_id = m.chat.id
    st = await c.get_chat_member(grp_id, userid)
    if st.status not in [
        enums.ChatMemberStatus.ADMINISTRATOR,
        enums.ChatMemberStatus.OWNER,
    ]:
        return 
    if m.command[1] in ["True", "False"]:
        contact = m.command[1] == "True"
        await db.update_group(grp_id, {"verify2": contact})
        text = "Updated Successfully"

    await m.reply_text(text)


