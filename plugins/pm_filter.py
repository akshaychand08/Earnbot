import asyncio
import re
import ast
import math
import random
import pytz
from urllib.parse import quote_plus
from datetime import datetime, timedelta, date, time
lock = asyncio.Lock()
from pyrogram.errors.exceptions.bad_request_400 import MediaEmpty, PhotoInvalidDimensions, WebpageMediaEmpty
from Script import script
import pyrogram
from database.connections_mdb import active_connection, all_connections, delete_connection, if_active, make_active, \
    make_inactive
from info import GEN_URL, BIN_CHANNEL, ADMINS, AUTH_CHANNEL, AUTH_USERS, SUPPORT_CHAT_ID, CUSTOM_FILE_CAPTION, MSG_ALRT, PICS, AUTH_GROUPS, P_TTI_SHOW_OFF, GRP_LNK, CHNL_LNK, NOR_IMG, LOG_CHANNEL, SPELL_IMG, MAX_B_TN, IMDB, \
    SINGLE_BUTTON, USERNAME, SPELL_CHECK_REPLY, IMDB_TEMPLATE, NO_RESULTS_MSG, TUTORIAL, REQST_CHANNEL, IS_TUTORIAL, SUPPORT_CHAT, PREMIUM_USER
from pyrogram.types import InlineKeyboardMarkup, InlineKeyboardButton, CallbackQuery, InputMediaPhoto
from pyrogram import Client, filters, enums
from pyrogram.errors import FloodWait, UserIsBlocked, MessageNotModified, PeerIdInvalid
from utils import replace_words, get_size, is_subscribed, get_poster, temp, get_settings, save_group_settings, get_shortlink, get_tutorial
from database.users_chats_db import db
from database.ia_filterdb import Media, get_file_details, get_search_results, get_bad_files
from database.filters_mdb import (
    del_all,
    find_filter,
    get_filters,
)


import logging

logger = logging.getLogger(__name__)
logger.setLevel(logging.ERROR)

BUTTON = {}
BUTTONS = {}
FRESH = {}
BUTTONS0 = {}
BUTTONS1 = {}
BUTTONS2 = {}
SPELL_CHECK = {}
CAP = {}

@Client.on_callback_query(filters.regex(r"^next"))
async def next_page(bot, query):
    ident, req, key, offset, = query.data.split("_")
    curr_time = datetime.now(pytz.timezone('Asia/Kolkata')).time()
    if int(req) not in [query.from_user.id, 0]:
        return await query.answer(script.ALRT_TXT.format(query.from_user.first_name), show_alert=True)
    try:
        offset = int(offset)
    except:
        offset = 0
    if BUTTONS.get(key)!=None:
        search = BUTTONS.get(key)
    else:
        search = FRESH.get(key)
    cap = CAP.get(key)
    if not search:
        await query.answer(script.OLD_ALRT_TXT.format(query.from_user.first_name),show_alert=True)
        return

    files, n_offset, total = await get_search_results(search, offset=offset, filter=True)
    try:
        n_offset = int(n_offset)
    except:
        n_offset = 0

    if not files:
        return
    user = query.from_user.id 
    settings = await get_settings(query.message.chat.id)
    pre = 'filep' if settings['file_secure'] else 'file'
    chat_id = query.message.chat.id 
    is_lang = False
    is_series = False 
    text_link = "\n\n"
    if settings["button"]:
        btn = []
        for file in files:        
            if "s0" in str(file.caption).lower() or "season" in str(file.caption).lower():
                is_series = True  
            if "hindi" in str(file.caption).lower() or "tamil" in str(file.caption).lower() or "telugu" in str(file.caption).lower() or "kannada" in str(file.caption).lower() or "malayalam" in str(file.caption).lower() or "telugu" in str(file.caption).lower() or "english" in str(file.caption).lower():
                is_lang = True                
            btn.append([
                InlineKeyboardButton(text=f"[{get_size(file.file_size)}] {' '.join(filter(lambda x: not x.startswith('[') and not x.startswith('@') and not x.startswith('www.'), file.file_name.split()))}", url=f'https://telegram.dog/{temp.U_NAME}?start=short_{chat_id}_{file.file_id}')
            ])
    else:
        btn = []
        for file in files:    
            if "s0" in str(file.caption).lower() or "season" in str(file.caption).lower():
                is_series = True  
            if "hindi" in str(file.caption).lower() or "tamil" in str(file.caption).lower() or "telugu" in str(file.caption).lower() or "kannada" in str(file.caption).lower() or "malayalam" in str(file.caption).lower() or "telugu" in str(file.caption).lower() or "english" in str(file.caption).lower():
                is_lang = True     
            text_link += f"<b>📽 <a href='https://telegram.me/{temp.U_NAME}?start=short_{chat_id}_{file.file_id}'>[{get_size(file.file_size)}] {' '.join(filter(lambda x: not x.startswith('[') and not x.startswith('@') and not x.startswith('www.'), file.file_name.split()))}\n\n</a></b>"         
            
    if is_series:
        btn.insert(0, [
            InlineKeyboardButton("🥶 Cʜᴏᴏsᴇ Sᴇᴀsᴏɴ 🥶", callback_data=f"season#{key}#0#{offset}")
        ])
    if is_lang:
        btn.insert(0, [
            InlineKeyboardButton("‼️ Cʜᴏᴏsᴇ Lᴀɴɢᴜᴀɢᴇ ‼️", callback_data=f"languages#{key}#0#{offset}"),
        ])  

        if 0 < offset <= int(MAX_B_TN):
            off_set = 0
        elif offset == 0:
            off_set = None
        else:
            off_set = offset - int(MAX_B_TN)
        if n_offset == 0:
            btn.append(
                [InlineKeyboardButton("⌫ 𝐁𝐀𝐂𝐊", callback_data=f"next_{req}_{key}_{off_set}"), InlineKeyboardButton(f"{math.ceil(int(offset)/int(MAX_B_TN))+1} / {math.ceil(total/int(MAX_B_TN))}", callback_data="pages")]
            )
        elif off_set is None:
            btn.append([InlineKeyboardButton("𝐏𝐀𝐆𝐄", callback_data="pages"), InlineKeyboardButton(f"{math.ceil(int(offset)/int(MAX_B_TN))+1} / {math.ceil(total/int(MAX_B_TN))}", callback_data="pages"), InlineKeyboardButton("𝐍𝐄𝐗𝐓 ➪", callback_data=f"next_{req}_{key}_{n_offset}")])
        else:
            btn.append(
                [
                    InlineKeyboardButton("⌫ 𝐁𝐀𝐂𝐊", callback_data=f"next_{req}_{key}_{off_set}"),
                    InlineKeyboardButton(f"{math.ceil(int(offset)/int(MAX_B_TN))+1} / {math.ceil(total/int(MAX_B_TN))}", callback_data="pages"),
                    InlineKeyboardButton("𝐍𝐄𝐗𝐓 ➪", callback_data=f"next_{req}_{key}_{n_offset}")
                ],
            )

    if not settings["button"]:
        await query.message.edit_text(cap + text_link, disable_web_page_preview=True, reply_markup=InlineKeyboardMarkup(btn))
        return        
    try:
        await query.edit_message_reply_markup(
            reply_markup=InlineKeyboardMarkup(btn)
        )
    except MessageNotModified:
        pass
    await query.answer()

@Client.on_callback_query(filters.regex(r"^sp"))
async def advantage_spoll_choker(bot, query):
    _, us, movie_ = query.data.split('#')
    movies = SPELL_CHECK.get(query.message.reply_to_message.id)
    if not movies:
        return await query.answer(script.OLD_ALRT_TXT.format(query.from_user.first_name), show_alert=True)
    if int(us) != 0 and query.from_user.id != int(us):
        return await query.answer(script.ALRT_TXT.format(query.from_user.first_name), show_alert=True)
    if movie_ == "cl_sl":
        return await query.message.delete()
    movie = movies[(int(movie_))]
    movie = re.sub(r"[:\-]", " ", movie)
    movie = re.sub(r"\s+", " ", movie).strip()
    await query.answer(script.TOP_ALRT_MSG)
    k = await manual_filters(bot, query.message, text=movie)
    if k == False:
        files, offset, total_results = await get_search_results(movie, offset=0, filter=True)
        if files:
            k = (movie, files, offset, total_results)
            await auto_filter(bot, query, k)
        else: 
            reply = movie.replace(" ", '+')  
            btn = [[
                InlineKeyboardButton("🔍 𝗖𝗹𝗶𝗰𝗸 𝗧𝗼 𝗖𝗵𝗲𝗰𝗸 𝗦𝗽𝗶𝗹𝗹𝗶𝗻𝗴 ✅", url=f"https://www.google.com/search?q={reply}+movie")
                ],[
                InlineKeyboardButton("🔍 𝗖𝗹𝗶𝗰𝗸 𝗧𝗼 𝗖𝗵𝗲𝗰𝗸 𝗥𝗲𝗹𝗲𝗮𝘀𝗲 𝗗𝗮𝘁𝗲 📅", url=f"https://www.google.com/search?q={reply}+release+date")
            ]]                
            k = await query.message.edit(script.MVE_NT_FND, reply_markup=InlineKeyboardMarkup(btn))
            await asyncio.sleep(30)
            await k.delete()


#languages code started here
@Client.on_callback_query(filters.regex(r"^languages#"))
async def languages_cb_handler(client: Client, query: CallbackQuery):

    if int(query.from_user.id) not in [query.message.reply_to_message.from_user.id, 0]:
        return await query.answer(
            f"⚠️ 𝗛𝗲𝘆, {query.from_user.first_name}.. \n\n𝗦𝗲𝗮𝗿𝗰𝗵 𝗬𝗼𝘂𝗿 𝗢𝘄𝗻𝗲𝗿 𝗙𝗶𝗹𝗲,\n\n⚠️𝗗𝗼𝗻'𝘁 𝗖𝗹𝗶𝗰𝗸 𝗢𝘁𝗵𝗲𝗿𝘀 𝗥𝗲𝘀𝘂𝗹𝘁𝘀 😬",
            show_alert=True,
        )
    
    _, key, offset, orginal_offset = query.data.split("#")
    orginal_offset = int(orginal_offset)

    btn = [[
        InlineKeyboardButton("ʜɪɴᴅɪ", callback_data=f"fl#hindi#{key}#{offset}#{orginal_offset}"),
        InlineKeyboardButton("ᴇɴɢʟɪꜱʜ", callback_data=f"fl#english#{key}#{offset}#{orginal_offset}")
        ],[
        InlineKeyboardButton("ᴛᴀᴍɪʟ", callback_data=f"fl#tamil#{key}#{offset}#{orginal_offset}"),
        InlineKeyboardButton("ᴛᴇʟᴜɢᴜ", callback_data=f"fl#telugu#{key}#{offset}#{orginal_offset}")
        ],[
        InlineKeyboardButton("ᴍᴀʟᴀʏᴀʟᴀᴍ", callback_data=f"fl#malayalam#{key}#{offset}#{orginal_offset}"),
        InlineKeyboardButton("ᴋᴀɴɴᴀᴅᴀ", callback_data=f"fl#kannada#{key}#{offset}#{orginal_offset}")
        ],[
        InlineKeyboardButton("ᴘᴜɴɪᴀʙɪ", callback_data=f"fl#punjabi#{key}#{offset}#{orginal_offset}"),
        InlineKeyboardButton("ᴍᴀʀᴀᴛʜɪ", callback_data=f"fl#marathi#{key}#{offset}#{orginal_offset}")
        ],[
        InlineKeyboardButton("ʙᴇɴɢᴏʟɪ", callback_data=f"fl#bengoli#{key}#{offset}#{orginal_offset}"),
        InlineKeyboardButton("ɢᴜɪʀᴀᴛɪ", callback_data=f"fl#gujrati#{key}#{offset}#{orginal_offset}")
        ],[
        InlineKeyboardButton("ᴅᴜᴀʟ", callback_data=f"fl#dual#{key}#{offset}#{orginal_offset}"),
        InlineKeyboardButton("ᴍᴜʟᴛɪ", callback_data=f"fl#multi#{key}#{offset}#{orginal_offset}")
    ]]

    btn.insert(
        0,
        [
            InlineKeyboardButton(
                text="👇 sᴇʟᴇᴄᴛ ʏᴏᴜʀ ʟᴀɴɢᴜᴀɢᴇꜱ 👇", callback_data="ident"
            )
        ],
    )
    req = query.from_user.id
    offset = 0
    btn.append([InlineKeyboardButton(text="🏃‍♀ ʙᴀᴄᴋ ᴛᴏ ғɪʟᴇꜱ", callback_data=f"next_{req}_{key}_{offset}")])
    await query.edit_message_reply_markup(InlineKeyboardMarkup(btn))

@Client.on_callback_query(filters.regex(r"^fl#"))
async def filter_languages_cb_handler(client: Client, query: CallbackQuery):
    _, lang, key, offset, orginal_offset = query.data.split("#")
    offset = int(offset)
    search = BUTTONS.get(key)
    cap = CAP.get(key)

    if not search:
        await query.answer("You are clicking on an old button which is expired.", show_alert=True)
        return

    print(search)
    search = search.replace("_", " ")
    req = query.from_user.id

    if int(req) not in [query.message.reply_to_message.from_user.id, 0]:
        return await query.answer(
            f"⚠️ 𝗛𝗲𝘆, {query.from_user.first_name}.. \n\n𝗦𝗲𝗮𝗿𝗰𝗵 𝗬𝗼𝘂𝗿 𝗢𝘄𝗻𝗲𝗿 𝗙𝗶𝗹𝗲,\n\n⚠️𝗗𝗼𝗻'𝘁 𝗖𝗹𝗶𝗰𝗸 𝗢𝘁𝗵𝗲𝗿𝘀 𝗥𝗲𝘀𝘂𝗹𝘁𝘀 😬",
            show_alert=True,
        )
    chat_id = query.message.chat.id
    max_btn = int(MAX_B_TN)
    files, n_offset, total = await get_search_results(f"{search} {lang}", max_results=max_btn, offset=offset)
    try:
        n_offset = int(n_offset)
    except:
        n_offset = 0

    files = [file for file in files if re.search(lang, file.file_name, re.IGNORECASE)]
    if not files:
        await query.answer(f"No files were found {search} in {lang}", show_alert=1)
        return    
    temp.GETALL[key] = files
    settings = await get_settings(query.message.chat.id)
    chat_id = query.message.chat.id 
    is_lang = True
    is_series = False 
    text_link = "\n\n"
    if settings["button"]:
        btn = []
        for file in files:        
            if "s0" in str(file.caption).lower() or "season" in str(file.caption).lower():
                is_series = True  
            if "hindi" in str(file.caption).lower() or "tamil" in str(file.caption).lower() or "telugu" in str(file.caption).lower() or "kannada" in str(file.caption).lower() or "malayalam" in str(file.caption).lower() or "telugu" in str(file.caption).lower() or "english" in str(file.caption).lower():
                is_lang = True                
            btn.append([
                InlineKeyboardButton(text=f"[{get_size(file.file_size)}] {' '.join(filter(lambda x: not x.startswith('[') and not x.startswith('@') and not x.startswith('www.'), file.file_name.split()))}", url=f'https://telegram.dog/{temp.U_NAME}?start=short_{chat_id}_{file.file_id}')
            ])
    else:
        btn = []
        for file in files:    
            if "s0" in str(file.caption).lower() or "season" in str(file.caption).lower():
                is_series = True  
            if "hindi" in str(file.caption).lower() or "tamil" in str(file.caption).lower() or "telugu" in str(file.caption).lower() or "kannada" in str(file.caption).lower() or "malayalam" in str(file.caption).lower() or "telugu" in str(file.caption).lower() or "english" in str(file.caption).lower():
                is_lang = True     
            text_link += f"<b>📽 <a href='https://telegram.me/{temp.U_NAME}?start=short_{chat_id}_{file.file_id}'>[{get_size(file.file_size)}] {' '.join(filter(lambda x: not x.startswith('[') and not x.startswith('@') and not x.startswith('www.'), file.file_name.split()))}\n\n</a></b>"         
            
    if is_series:
        btn.insert(0, [
            InlineKeyboardButton("🥶 Cʜᴏᴏsᴇ Sᴇᴀsᴏɴ 🥶", callback_data=f"season#{key}#{offset}#{offset}")
        ])
    if is_lang:
        btn.insert(0, [
            InlineKeyboardButton("‼️ Cʜᴏᴏsᴇ Lᴀɴɢᴜᴀɢᴇ ‼️", callback_data=f"languages#{key}#{offset}#{offset}"),
        ])  
    if n_offset == 0:
        btn.append(
            [
                InlineKeyboardButton(
                    f"ᴘᴀɢᴇꜱ {math.ceil(offset / max_btn) + 1} / {math.ceil(total / max_btn)}",
                    callback_data="pages",
                ),
            ]
        )
    elif offset:
        btn.append(
            [
                InlineKeyboardButton(
                    "~ ʙᴀᴄᴋ", callback_data=f"fl#{lang}#{key}#{offset-max_btn}#{orginal_offset}"
                ),
                InlineKeyboardButton(
                    f" {math.ceil(offset / max_btn) + 1} / {math.ceil(total / max_btn)}",
                    callback_data="pages",
                ),
                InlineKeyboardButton(
                    "ɴᴇxᴛ ~", callback_data=f"fl#{lang}#{key}#{n_offset}#{orginal_offset}"
                ),
            ]
        )     
    else:
        btn.append(
            [
                InlineKeyboardButton(
                    f" {math.ceil(offset / max_btn) + 1} / {math.ceil(total / max_btn)}",
                    callback_data="pages",
                ),
                InlineKeyboardButton(
                    "ɴᴇxᴛ ~", callback_data=f"fl#{lang}#{key}#{n_offset}#{orginal_offset}"
                ),
            ]
        )
    btn.append([
            InlineKeyboardButton(
                text="~ ʙᴀᴄᴋ ᴛᴏ ᴍᴀɪɴ ᴘᴀɢᴇ",
                callback_data=f"next_{req}_{key}_{orginal_offset}"
                ),
        ])
    
    if not settings["button"]:
        await query.message.edit_text(cap + text_link, disable_web_page_preview=True, reply_markup=InlineKeyboardMarkup(btn))
        return        
    
    await query.edit_message_reply_markup(
        reply_markup=InlineKeyboardMarkup(btn)
    )

#languages code started here

@Client.on_callback_query(filters.regex(r"^season#"))
async def season_cb_handler(client: Client, query: CallbackQuery):

    if int(query.from_user.id) not in [query.message.reply_to_message.from_user.id, 0]:
        return await query.answer(
            f"⚠️ 𝗛𝗲𝘆, {query.from_user.first_name}.. \n\n𝗦𝗲𝗮𝗿𝗰𝗵 𝗬𝗼𝘂𝗿 𝗢𝘄𝗻𝗲𝗿 𝗙𝗶𝗹𝗲,\n\n⚠️𝗗𝗼𝗻'𝘁 𝗖𝗹𝗶𝗰𝗸 𝗢𝘁𝗵𝗲𝗿𝘀 𝗥𝗲𝘀𝘂𝗹𝘁𝘀 😬",
            show_alert=True,
        )
    
    _, key, offset, orginal_offset = query.data.split("#")
    orginal_offset = int(orginal_offset)
    
    btn = [[
        InlineKeyboardButton("ꜱᴇᴀꜱᴏɴ 1", callback_data=f"sl#S01#{key}#{offset}#{orginal_offset}"),
        InlineKeyboardButton("ꜱᴇᴀꜱᴏɴ 2", callback_data=f"sl#S02#{key}#{offset}#{orginal_offset}")
        ],[
        InlineKeyboardButton("ꜱᴇᴀꜱᴏɴ 3", callback_data=f"sl#S03#{key}#{offset}#{orginal_offset}"),
        InlineKeyboardButton("ꜱᴇᴀꜱᴏɴ 4", callback_data=f"sl#S04#{key}#{offset}#{orginal_offset}")
        ],[
        InlineKeyboardButton("ꜱᴇᴀꜱᴏɴ 5", callback_data=f"sl#S05#{key}#{offset}#{orginal_offset}"),
        InlineKeyboardButton("ꜱᴇᴀꜱᴏɴ 6", callback_data=f"sl#S06#{key}#{offset}#{orginal_offset}")
        ],[
        InlineKeyboardButton("ꜱᴇᴀꜱᴏɴ 7", callback_data=f"sl#S07#{key}#{offset}#{orginal_offset}"),
        InlineKeyboardButton("ꜱᴇᴀꜱᴏɴ 8", callback_data=f"sl#S08#{key}#{offset}#{orginal_offset}")
        ],[
        InlineKeyboardButton("ꜱᴇᴀꜱᴏɴ 9", callback_data=f"sl#S09#{key}#{offset}#{orginal_offset}"),
        InlineKeyboardButton("ꜱᴇᴀꜱᴏɴ 10", callback_data=f"sl#S10#{key}#{offset}#{orginal_offset}")
        ],[
        InlineKeyboardButton("ꜱᴇᴀꜱᴏɴ 11", callback_data=f"sl#S11#{key}#{offset}#{orginal_offset}"),
        InlineKeyboardButton("ꜱᴇᴀꜱᴏɴ 12", callback_data=f"sl#S12#{key}#{offset}#{orginal_offset}")
    ]]
    
    btn.insert(
        0,
        [
            InlineKeyboardButton(
                text="👇 sᴇʟᴇᴄᴛ ʏᴏᴜʀ ꜱᴇᴀꜱᴏɴ 👇", callback_data="ident"
            )
        ],
    )
    req = query.from_user.id
    offset = 0
    btn.append([InlineKeyboardButton(text="🏃‍♀ ʙᴀᴄᴋ ᴛᴏ ғɪʟᴇꜱ", callback_data=f"next_{req}_{key}_{offset}")])
    await query.edit_message_reply_markup(InlineKeyboardMarkup(btn))

@Client.on_callback_query(filters.regex(r"^sl#"))
async def filter_season_cb_handler(client: Client, query: CallbackQuery):
    _, lang, key, offset, orginal_offset = query.data.split("#")
    offset = int(offset)
    search = BUTTONS.get(key)
    cap = CAP.get(key)

    if not search:
        await query.answer("You are clicking on an old button which is expired.", show_alert=True)
        return

    print(search)
    search = search.replace("_", " ")
    req = query.from_user.id

    if int(req) not in [query.message.reply_to_message.from_user.id, 0]:
        return await query.answer(
            f"⚠️ 𝗛𝗲𝘆, {query.from_user.first_name}.. \n\n𝗦𝗲𝗮𝗿𝗰𝗵 𝗬𝗼𝘂𝗿 𝗢𝘄𝗻𝗲𝗿 𝗙𝗶𝗹𝗲,\n\n⚠️𝗗𝗼𝗻'𝘁 𝗖𝗹𝗶𝗰𝗸 𝗢𝘁𝗵𝗲𝗿𝘀 𝗥𝗲𝘀𝘂𝗹𝘁𝘀 😬",
            show_alert=True,
        )
    chat_id = query.message.chat.id
    max_btn = int(MAX_B_TN)
    files, n_offset, total = await get_search_results(f"{search} {lang}", max_results=max_btn, offset=offset)
    try:
        n_offset = int(n_offset)
    except:
        n_offset = 0

    files = [file for file in files if re.search(lang, file.file_name, re.IGNORECASE)]
    if not files:
        await query.answer(f"No files were found {search} {lang}", show_alert=1)
        return    
    temp.GETALL[key] = files
    settings = await get_settings(query.message.chat.id)
    chat_id = query.message.chat.id 
    is_lang = True
    is_series = False 
    text_link = "\n\n"
    if settings["button"]:
        btn = []
        for file in files:        
            if "s0" in str(file.caption).lower() or "season" in str(file.caption).lower():
                is_series = True  
            if "hindi" in str(file.caption).lower() or "tamil" in str(file.caption).lower() or "telugu" in str(file.caption).lower() or "kannada" in str(file.caption).lower() or "malayalam" in str(file.caption).lower() or "telugu" in str(file.caption).lower() or "english" in str(file.caption).lower():
                is_lang = True                
            btn.append([
                InlineKeyboardButton(text=f"[{get_size(file.file_size)}] {' '.join(filter(lambda x: not x.startswith('[') and not x.startswith('@') and not x.startswith('www.'), file.file_name.split()))}", url=f'https://telegram.dog/{temp.U_NAME}?start=short_{chat_id}_{file.file_id}')
            ])
    else:
        btn = []
        for file in files:    
            if "s0" in str(file.caption).lower() or "season" in str(file.caption).lower():
                is_series = True  
            if "hindi" in str(file.caption).lower() or "tamil" in str(file.caption).lower() or "telugu" in str(file.caption).lower() or "kannada" in str(file.caption).lower() or "malayalam" in str(file.caption).lower() or "telugu" in str(file.caption).lower() or "english" in str(file.caption).lower():
                is_lang = True     
            text_link += f"<b>📽 <a href='https://telegram.me/{temp.U_NAME}?start=short_{chat_id}_{file.file_id}'>[{get_size(file.file_size)}] {' '.join(filter(lambda x: not x.startswith('[') and not x.startswith('@') and not x.startswith('www.'), file.file_name.split()))}\n\n</a></b>"         
            
    if is_series:
        btn.insert(0, [
            InlineKeyboardButton("🥶 Cʜᴏᴏsᴇ Sᴇᴀsᴏɴ 🥶", callback_data=f"season#{key}#{offset}#{offset}")
        ])
    if is_lang:
        btn.insert(0, [
            InlineKeyboardButton("‼️ Cʜᴏᴏsᴇ Lᴀɴɢᴜᴀɢᴇ ‼️", callback_data=f"languages#{key}#{offset}#{offset}"),
        ])  
    if n_offset == 0:
        btn.append(
            [
                InlineKeyboardButton(
                    f"ᴘᴀɢᴇꜱ {math.ceil(offset / max_btn) + 1} / {math.ceil(total / max_btn)}",
                    callback_data="pages",
                ),
            ]
        )
    elif offset:
        btn.append(
            [
                InlineKeyboardButton(
                    "~ ʙᴀᴄᴋ", callback_data=f"fl#{lang}#{key}#{offset-max_btn}#{orginal_offset}"
                ),
                InlineKeyboardButton(
                    f" {math.ceil(offset / max_btn) + 1} / {math.ceil(total / max_btn)}",
                    callback_data="pages",
                ),
                InlineKeyboardButton(
                    "ɴᴇxᴛ ~", callback_data=f"fl#{lang}#{key}#{n_offset}#{orginal_offset}"
                ),
            ]
        )     
    else:
        btn.append(
            [
                InlineKeyboardButton(
                    f" {math.ceil(offset / max_btn) + 1} / {math.ceil(total / max_btn)}",
                    callback_data="pages",
                ),
                InlineKeyboardButton(
                    "ɴᴇxᴛ ~", callback_data=f"fl#{lang}#{key}#{n_offset}#{orginal_offset}"
                ),
            ]
        )
    btn.append([
            InlineKeyboardButton(
                text="~ ʙᴀᴄᴋ ᴛᴏ ᴍᴀɪɴ ᴘᴀɢᴇ",
                callback_data=f"next_{req}_{key}_{orginal_offset}"
                ),
        ])
    
    if not settings["button"]:
        await query.message.edit_text(cap + text_link, disable_web_page_preview=True, reply_markup=InlineKeyboardMarkup(btn))
        return        
    
    await query.edit_message_reply_markup(
        reply_markup=InlineKeyboardMarkup(btn)
    )



@Client.on_callback_query()
async def cb_handler(client: Client, query: CallbackQuery):
    #link = await client.create_chat_invite_link(int(REQST_CHANNEL))
    if query.data == "close_data":
        await query.message.delete()
    elif query.data.startswith("checksub"):
        ident, file_id = query.data.split("#")
        grp_id = temp.GET_ID.get(query.from_user.id)
        settings = await get_settings(int(grp_id))
        if settings['fsub'] and not await is_subscribed(client, query, grp_id):
            await query.answer(f"I Like Your Smartness, But Don't Be Oversmart Go And Join Update Channel 😒", show_alert=True)
            return        
        if not settings['is_shortlink']:
            await query.answer(url=f"https://telegram.me/{temp.U_NAME}?start=files_{file_id}")
            return 
        else:
            await query.answer(url=f"https://telegram.me/{temp.U_NAME}?start=short_{file_id}")
            return 
            
    elif query.data.startswith("opnsetgrp"):
        ident, grp_id = query.data.split("#")
        userid = query.from_user.id if query.from_user else None
        st = await client.get_chat_member(grp_id, userid)
        if (
                st.status != enums.ChatMemberStatus.ADMINISTRATOR
                and st.status != enums.ChatMemberStatus.OWNER
                and str(userid) not in ADMINS
        ):
            await query.answer("Yᴏᴜ Dᴏɴ'ᴛ Hᴀᴠᴇ Tʜᴇ Rɪɢʜᴛs Tᴏ Dᴏ Tʜɪs !", show_alert=True)
            return
        title = query.message.chat.title
        settings = await get_settings(grp_id)
        if settings is not None:
            buttons = [
                [
                    InlineKeyboardButton('ʀᴇsᴜʟᴛ ᴘᴀɢᴇ ',
                                         callback_data=f'setgs#button#{settings["button"]}#{str(grp_id)}'),
                    InlineKeyboardButton('ʙᴜᴛᴛᴏɴ' if settings["button"] else 'ᴛᴇxᴛ',
                                         callback_data=f'setgs#button#{settings["button"]}#{str(grp_id)}')
                ],
                [
                    InlineKeyboardButton('sᴘᴇʟʟ ᴄʜᴇᴄᴋ',
                                         callback_data=f'setgs#spell_check#{settings["spell_check"]}#{str(grp_id)}'),
                    InlineKeyboardButton('ᴇɴᴀʙʟᴇ' if settings["spell_check"] else 'ᴅɪsᴀʙʟᴇ',
                                         callback_data=f'setgs#spell_check#{settings["spell_check"]}#{str(grp_id)}')
                ],
                [
                    InlineKeyboardButton('ᴀᴜᴛᴏ ᴅᴇʟᴇᴛᴇ',
                                         callback_data=f'setgs#auto_delete#{settings["auto_delete"]}#{str(grp_id)}'),
                    InlineKeyboardButton('15 ᴍɪɴs' if settings["auto_delete"] else 'ᴅɪsᴀʙʟᴇ',
                                         callback_data=f'setgs#auto_delete#{settings["auto_delete"]}#{str(grp_id)}')
                ],
                [
                    InlineKeyboardButton('ᴀᴜᴛᴏ ꜰɪʟᴛᴇʀ',
                                         callback_data=f'setgs#auto_ffilter#{settings["auto_ffilter"]}#{str(grp_id)}'),
                    InlineKeyboardButton('ᴇɴᴀʙʟᴇ'  if settings["auto_ffilter"] else 'ᴅɪsᴀʙʟᴇ',
                                         callback_data=f'setgs#auto_ffilter#{settings["auto_ffilter"]}#{str(grp_id)}')
                ],
                [
                    InlineKeyboardButton('sʜᴏʀᴛʟɪɴᴋ ᴍᴏᴅ',
                                         callback_data=f'setgs#is_shortlink#{settings["is_shortlink"]}#{str(grp_id)}'),
                    InlineKeyboardButton('sʜᴏʀᴛʟɪɴᴋ' if settings["is_shortlink"] else 'ᴠᴇʀɪꜰʏ',
                                         callback_data=f'setgs#is_shortlink#{settings["is_shortlink"]}#{str(grp_id)}')  
                ],
                [
                    InlineKeyboardButton('ʟɪɴᴋ ᴍᴏᴅ',
                                         callback_data=f'setgs#verify_short#{settings["verify_short"]}#{str(grp_id)}'),
                    InlineKeyboardButton('ᴅɪsᴀʙʟᴇ' if settings["verify_short"] else 'ᴇɴᴀʙʟᴇ',
                                         callback_data=f'setgs#verify_short#{settings["verify_short"]}#{str(grp_id)}')            
                ]
            ]
            reply_markup = InlineKeyboardMarkup(buttons)
            await query.message.edit_text(
                text=f"<b>Cʜᴀɴɢᴇ Yᴏᴜʀ Sᴇᴛᴛɪɴɢs Fᴏʀ {title} As Yᴏᴜʀ Wɪsʜ ⚙</b>",
                disable_web_page_preview=True,
                parse_mode=enums.ParseMode.HTML
            )
            await query.message.edit_reply_markup(reply_markup)
        
    elif query.data.startswith("opnsetpm"):
        ident, grp_id = query.data.split("#")
        userid = query.from_user.id if query.from_user else None
        st = await client.get_chat_member(grp_id, userid)
        if (
                st.status != enums.ChatMemberStatus.ADMINISTRATOR
                and st.status != enums.ChatMemberStatus.OWNER
                and str(userid) not in ADMINS
        ):
            await query.answer("Yᴏᴜ Dᴏɴ'ᴛ Hᴀᴠᴇ Tʜᴇ Rɪɢʜᴛs Tᴏ Dᴏ Tʜɪs !", show_alert=True)
            return
        title = query.message.chat.title
        settings = await get_settings(grp_id)
        btn2 = [[
                 InlineKeyboardButton("Cʜᴇᴄᴋ PM", url=f"telegram.me/{temp.U_NAME}")
               ]]
        reply_markup = InlineKeyboardMarkup(btn2)
        await query.message.edit_text(f"<b>Yᴏᴜʀ sᴇᴛᴛɪɴɢs ᴍᴇɴᴜ ғᴏʀ {title} ʜᴀs ʙᴇᴇɴ sᴇɴᴛ ᴛᴏ ʏᴏᴜʀ PM</b>")
        await query.message.edit_reply_markup(reply_markup)
        if settings is not None:
            buttons = [
                [
                    InlineKeyboardButton('ʀᴇsᴜʟᴛ ᴘᴀɢᴇ ',
                                         callback_data=f'setgs#button#{settings["button"]}#{str(grp_id)}'),
                    InlineKeyboardButton('ʙᴜᴛᴛᴏɴ' if settings["button"] else 'ᴛᴇxᴛ',
                                         callback_data=f'setgs#button#{settings["button"]}#{str(grp_id)}')
                ],
                [
                    InlineKeyboardButton('sᴘᴇʟʟ ᴄʜᴇᴄᴋ',
                                         callback_data=f'setgs#spell_check#{settings["spell_check"]}#{str(grp_id)}'),
                    InlineKeyboardButton('ᴇɴᴀʙʟᴇ' if settings["spell_check"] else 'ᴅɪsᴀʙʟᴇ',
                                         callback_data=f'setgs#spell_check#{settings["spell_check"]}#{str(grp_id)}')
                ],
                [
                    InlineKeyboardButton('ᴀᴜᴛᴏ ᴅᴇʟᴇᴛᴇ',
                                         callback_data=f'setgs#auto_delete#{settings["auto_delete"]}#{str(grp_id)}'),
                    InlineKeyboardButton('15 ᴍɪɴs' if settings["auto_delete"] else 'ᴅɪsᴀʙʟᴇ',
                                         callback_data=f'setgs#auto_delete#{settings["auto_delete"]}#{str(grp_id)}')
                ],
                [
                    InlineKeyboardButton('ᴀᴜᴛᴏ ꜰɪʟᴛᴇʀ',
                                         callback_data=f'setgs#auto_ffilter#{settings["auto_ffilter"]}#{str(grp_id)}'),
                    InlineKeyboardButton('ᴇɴᴀʙʟᴇ'  if settings["auto_ffilter"] else 'ᴅɪsᴀʙʟᴇ',
                                         callback_data=f'setgs#auto_ffilter#{settings["auto_ffilter"]}#{str(grp_id)}')
                ],
                [
                    InlineKeyboardButton('sʜᴏʀᴛʟɪɴᴋ ᴍᴏᴅ',
                                         callback_data=f'setgs#is_shortlink#{settings["is_shortlink"]}#{str(grp_id)}'),
                    InlineKeyboardButton('sʜᴏʀᴛʟɪɴᴋ' if settings["is_shortlink"] else 'ᴠᴇʀɪꜰʏ',
                                         callback_data=f'setgs#is_shortlink#{settings["is_shortlink"]}#{str(grp_id)}')  
                ],
                [
                    InlineKeyboardButton('ʟɪɴᴋ ᴍᴏᴅ',
                                         callback_data=f'setgs#verify_short#{settings["verify_short"]}#{str(grp_id)}'),
                    InlineKeyboardButton('ᴅɪsᴀʙʟᴇ' if settings["verify_short"] else 'ᴇɴᴀʙʟᴇ',
                                         callback_data=f'setgs#verify_short#{settings["verify_short"]}#{str(grp_id)}')            
                ]
            ]
            reply_markup = InlineKeyboardMarkup(buttons)
            await client.send_message(
                chat_id=userid,
                text=f"<b>Cʜᴀɴɢᴇ Yᴏᴜʀ Sᴇᴛᴛɪɴɢs Fᴏʀ {title} As Yᴏᴜʀ Wɪsʜ ⚙</b>",
                reply_markup=reply_markup,
                disable_web_page_preview=True,
                parse_mode=enums.ParseMode.HTML,
                reply_to_message_id=query.message.id
            )


    elif query.data == "reqinfo":
        await query.answer(text=script.REQINFO, show_alert=True)

    elif query.data == "premium_Alert":
        return await query.answer(f"Hay bro this features only available in Premium user\n\nYou can go premium if you want access to it", show_alert=True)

    elif query.data == "select":
        await query.answer(text=script.SELECT, show_alert=True)

    elif query.data == "sinfo":
        await query.answer(text=script.SINFO, show_alert=True)

    elif query.data == "start":
        buttons = [[
                    InlineKeyboardButton('➕ Aᴅᴅ Mᴇ Tᴏ Yᴏᴜʀ Gʀᴏᴜᴘ ➕', url=f'http://t.me/{temp.U_NAME}?startgroup=true')
                ],[
                    InlineKeyboardButton('🔱 SUPPORT CHANNEL 🔱', url= 'https://t.me/FoxyBotSupport')
                ],[
                    InlineKeyboardButton('FEATURES', callback_data='help'),
                    InlineKeyboardButton('ABOUT', callback_data='about')
                ],[
                    InlineKeyboardButton('💲 Eᴀʀɴ Moɴᴇʏ Wɪᴛʜ Bᴏᴛ 💲', callback_data='ern_mony')
                  ]]
        
        reply_markup = InlineKeyboardMarkup(buttons)
        await client.edit_message_media(
            query.message.chat.id, 
            query.message.id, 
            InputMediaPhoto(random.choice(PICS))
        )
        await query.message.edit_text(
            text=script.START_TXT.format(query.from_user.mention, temp.U_NAME, temp.B_NAME),
            reply_markup=reply_markup,
            parse_mode=enums.ParseMode.HTML
        )
        await query.answer(MSG_ALRT)

    elif query.data == "filters":
        buttons = [[
            InlineKeyboardButton('Mᴀɴᴜᴀʟ FIʟᴛᴇʀ', callback_data='manuelfilter'),
            InlineKeyboardButton('Aᴜᴛᴏ FIʟᴛᴇʀ', callback_data='autofilter')
        ],[
            InlineKeyboardButton('⟸ Bᴀᴄᴋ', callback_data='help'),
            InlineKeyboardButton('Gʟᴏʙᴀʟ Fɪʟᴛᴇʀs', callback_data='global_filters')
        ]]
        
        reply_markup = InlineKeyboardMarkup(buttons)
        await client.edit_message_media(
            query.message.chat.id, 
            query.message.id, 
            InputMediaPhoto(random.choice(PICS))
        )
        await query.message.edit_text(
            text=script.ALL_FILTERS.format(query.from_user.mention),
            reply_markup=reply_markup,
            parse_mode=enums.ParseMode.HTML
        )

    elif query.data == "global_filters":
        buttons = [[
            InlineKeyboardButton('⟸ Bᴀᴄᴋ', callback_data='filters')
        ]]
        await client.edit_message_media(
            query.message.chat.id, 
            query.message.id, 
            InputMediaPhoto(random.choice(PICS))
        )
        reply_markup = InlineKeyboardMarkup(buttons)
        await query.message.edit_text(
            text=script.GFILTER_TXT,
            reply_markup=reply_markup,
            parse_mode=enums.ParseMode.HTML
        )
    
    elif query.data == "help":
        if query.from_user.id in ADMINS:
            buttons = [[InlineKeyboardButton('FSUB', callback_data='fsub'),InlineKeyboardButton('CUSTOM CAPTION', callback_data='caption'),], [InlineKeyboardButton('EXTRA MODS', callback_data='extra'),InlineKeyboardButton('Sᴛᴀᴛᴜs', callback_data='stats'),],[InlineKeyboardButton('Back', callback_data='start'),]]
        else:          
            buttons = [[InlineKeyboardButton('FSUB', callback_data='fsub'),InlineKeyboardButton('CUSTOM CAPTION', callback_data='caption'),], [InlineKeyboardButton('EXTRA MODS', callback_data='extra'),],[InlineKeyboardButton('Back', callback_data='start'),]]
        reply_markup = InlineKeyboardMarkup(buttons)
        await client.edit_message_media(
            query.message.chat.id, 
            query.message.id, 
            InputMediaPhoto(random.choice(PICS))
        )
        await query.message.edit_text(
            text=script.HELP_TXT.format(query.from_user.mention),
            reply_markup=reply_markup,
            parse_mode=enums.ParseMode.HTML
        )
    elif query.data == "ern_mony":
        buttons = [[
            InlineKeyboardButton('VERIFY', callback_data="ern_mony_v"),
            InlineKeyboardButton('SHORTLINK', callback_data="ern_mony_s"),
            ],[
            InlineKeyboardButton('BACK', callback_data='start')
        ]]
        await client.edit_message_media(
            query.message.chat.id, 
            query.message.id, 
            InputMediaPhoto(random.choice(PICS))
        )
        reply_markup = InlineKeyboardMarkup(buttons)
        await query.message.edit_text(
            text=('💲 Eᴀʀɴ Mᴏɴᴇʏ Wɪᴛʜ Bᴏᴛ 💲'),
            reply_markup=reply_markup,
            parse_mode=enums.ParseMode.HTML
        )               
    elif query.data == "ern_mony_v":
        buttons = [[
            InlineKeyboardButton('SUPPORT CHANNEL', url=USERNAME),
            InlineKeyboardButton('Back', callback_data='ern_mony')
        ]]
        await client.edit_message_media(
            query.message.chat.id, 
            query.message.id, 
            InputMediaPhoto(random.choice(PICS))
        )
        reply_markup = InlineKeyboardMarkup(buttons)
        await query.message.edit_text(
            text=script.ERN_MONY_V.format(temp.B_NAME, temp.U_NAME),
            reply_markup=reply_markup,
            parse_mode=enums.ParseMode.HTML
        )       

    elif query.data == "ern_mony_s":
        buttons = [[
            InlineKeyboardButton('SUPPORT CHANNEL', url=USERNAME),
            InlineKeyboardButton('Back', callback_data='ern_mony')
        ]]
        await client.edit_message_media(
            query.message.chat.id, 
            query.message.id, 
            InputMediaPhoto(random.choice(PICS))
        )
        reply_markup = InlineKeyboardMarkup(buttons)
        await query.message.edit_text(
            text=script.ERN_MONY_S.format(temp.B_NAME, temp.U_NAME),
            reply_markup=reply_markup,
            parse_mode=enums.ParseMode.HTML
        )      

    elif query.data == "caption":
        buttons = [[
            InlineKeyboardButton('SUPPORT CHANNEL', url=USERNAME),
            InlineKeyboardButton('Back', callback_data='help')
        ]]
        await client.edit_message_media(
            query.message.chat.id, 
            query.message.id, 
            InputMediaPhoto(random.choice(PICS))
        )
        reply_markup = InlineKeyboardMarkup(buttons)
        await query.message.edit_text(
            text=script.CAPTION_TXT,
            reply_markup=reply_markup,
            parse_mode=enums.ParseMode.HTML
        )
    elif query.data == "fsub":
        buttons = [[
            InlineKeyboardButton('SUPPORT CHANNEL', url=USERNAME),
            InlineKeyboardButton('Back', callback_data='help')
        ]]
        reply_markup = InlineKeyboardMarkup(buttons)
        await client.edit_message_media(
            query.message.chat.id, 
            query.message.id, 
            InputMediaPhoto(random.choice(PICS))
        )
        await query.message.edit_text(
            text=script.FSUB_TXT,
            reply_markup=reply_markup,
            parse_mode=enums.ParseMode.HTML
        )
    
    elif query.data == "about":
        buttons = [[
            InlineKeyboardButton('SUPPORT CHANNEL', url='https://t.me/FoxyBotSupport')
        ]]
        await client.edit_message_media(
            query.message.chat.id, 
            query.message.id, 
            InputMediaPhoto(random.choice(PICS))
        )
        reply_markup = InlineKeyboardMarkup(buttons)
        await query.message.edit_text(
            text=script.ABOUT_TXT.format(temp.B_NAME),
            reply_markup=reply_markup,
            parse_mode=enums.ParseMode.HTML
        )
    elif query.data == "source":
        buttons = [[
            InlineKeyboardButton('⟸ Bᴀᴄᴋ', callback_data='about')
        ]]
        reply_markup = InlineKeyboardMarkup(buttons)
        await client.edit_message_media(
            query.message.chat.id, 
            query.message.id, 
            InputMediaPhoto(random.choice(PICS))
        )
        await query.message.edit_text(
            text=script.SOURCE_TXT,
            reply_markup=reply_markup,
            parse_mode=enums.ParseMode.HTML
        )
    elif query.data == "manuelfilter":
        buttons = [[
            InlineKeyboardButton('⟸ Bᴀᴄᴋ', callback_data='filters'),
            InlineKeyboardButton('Bᴜᴛᴛᴏɴs', callback_data='button')
        ]]
        reply_markup = InlineKeyboardMarkup(buttons)
        await client.edit_message_media(
            query.message.chat.id, 
            query.message.id, 
            InputMediaPhoto(random.choice(PICS))
        )
        await query.message.edit_text(
            text=script.MANUELFILTER_TXT,
            reply_markup=reply_markup,
            parse_mode=enums.ParseMode.HTML
        )
    elif query.data == "button":
        buttons = [[
            InlineKeyboardButton('⟸ Bᴀᴄᴋ', callback_data='manuelfilter')
        ]]
        await client.edit_message_media(
            query.message.chat.id, 
            query.message.id, 
            InputMediaPhoto(random.choice(PICS))
        )
        reply_markup = InlineKeyboardMarkup(buttons)
        await query.message.edit_text(
            text=script.BUTTON_TXT,
            reply_markup=reply_markup,
            parse_mode=enums.ParseMode.HTML
        )
    elif query.data == "sendreqst":
        user_Rqt = USER_SPELL_CHECK.get(query.message.reply_to_message.id)
        await client.edit_message_media(
            query.message.chat.id, 
            query.message.id, 
            InputMediaPhoto("https://telegra.ph/file/121c805157214ac354b18.jpg")
        )
        await query.message.edit(f"ʜᴇʏ {query.from_user.mention}\n\nʏᴏᴜʀ ʀᴇǫᴜᴇꜱᴛ ʜᴀꜱ ʙᴇᴇɴ ᴀᴄᴄᴇᴘᴛᴇᴅ! ᴘʟᴇᴀꜱᴇ ᴡᴀɪᴛ ғᴏʀ ᴏᴜʀ ᴀᴅᴍɪɴꜱ ᴛᴏ ʀᴇꜱᴘᴏɴᴅ.")
        await client.send_message(REQST_CHANNEL, f"<b>#RequestContent🔻</b>\n<b>CONTENT -> `<code>{user_Rqt}</code>`</b>\n\n<b>ID -> `{query.from_user.id}`</b>\n<b>Name -> {query.from_user.first_name}</b>") 
        return
    
    elif query.data == "autofilter":
        buttons = [[
            InlineKeyboardButton('⟸ Bᴀᴄᴋ', callback_data='filters')
        ]]
        await client.edit_message_media(
            query.message.chat.id, 
            query.message.id, 
            InputMediaPhoto(random.choice(PICS))
        )
        reply_markup = InlineKeyboardMarkup(buttons)
        await query.message.edit_text(
            text=script.AUTOFILTER_TXT,
            reply_markup=reply_markup,
            parse_mode=enums.ParseMode.HTML
        )
    
    elif query.data == "coct":
        buttons = [[
            InlineKeyboardButton('⟸ Bᴀᴄᴋ', callback_data='help')
        ]]
        await client.edit_message_media(
            query.message.chat.id, 
            query.message.id, 
            InputMediaPhoto(random.choice(PICS))
        )
        reply_markup = InlineKeyboardMarkup(buttons)
        await query.message.edit_text(
            text=script.CONNECTION_TXT,
            reply_markup=reply_markup,
            parse_mode=enums.ParseMode.HTML
        )
    elif query.data == "extra":
        buttons = [[
            InlineKeyboardButton('⟸ Bᴀᴄᴋ', callback_data='help'),
            InlineKeyboardButton('Aᴅᴍɪɴ', callback_data='admin')
        ]]
        await client.edit_message_media(
            query.message.chat.id, 
            query.message.id, 
            InputMediaPhoto(random.choice(PICS))
        )
        reply_markup = InlineKeyboardMarkup(buttons)
        await query.message.edit_text(
            text=script.EXTRAMOD_TXT,
            reply_markup=reply_markup,
            parse_mode=enums.ParseMode.HTML
        )
    
    elif query.data == "store_file":
        buttons = [[
            InlineKeyboardButton('⟸ Bᴀᴄᴋ', callback_data='help')
        ]]
        await client.edit_message_media(
            query.message.chat.id, 
            query.message.id, 
            InputMediaPhoto(random.choice(PICS))
        )
        reply_markup = InlineKeyboardMarkup(buttons)
        await query.message.edit_text(
            text=script.FILE_STORE_TXT,
            reply_markup=reply_markup,
            parse_mode=enums.ParseMode.HTML
        )
    
    elif query.data == "admin":
        buttons = [[
            InlineKeyboardButton('⟸ Bᴀᴄᴋ', callback_data='extra')
        ]]
        await client.edit_message_media(
            query.message.chat.id, 
            query.message.id, 
            InputMediaPhoto(random.choice(PICS))
        )
        reply_markup = InlineKeyboardMarkup(buttons)
        await query.message.edit_text(
            text=script.ADMIN_TXT,
            reply_markup=reply_markup,
            parse_mode=enums.ParseMode.HTML
        )
    elif query.data == "stats":
        buttons = [[
            InlineKeyboardButton('⟸ Bᴀᴄᴋ', callback_data='help'),
            InlineKeyboardButton('⟲ Rᴇғʀᴇsʜ', callback_data='rfrsh')
        ]]
        await client.edit_message_media(
            query.message.chat.id, 
            query.message.id, 
            InputMediaPhoto(random.choice(PICS))
        )
        reply_markup = InlineKeyboardMarkup(buttons)
        total = await Media.count_documents()
        users = await db.total_users_count()
        chats = await db.total_chat_count()
        monsize = await db.get_db_size()
        free = 536870912 - monsize
        monsize = get_size(monsize)
        free = get_size(free)
        await query.message.edit_text(
            text=script.STATUS_TXT.format(total, users, chats, monsize, free),
            reply_markup=reply_markup,
            parse_mode=enums.ParseMode.HTML
        )
    elif query.data == "rfrsh":
        await query.answer("Fetching MongoDb DataBase")
        buttons = [[
            InlineKeyboardButton('⟸ Bᴀᴄᴋ', callback_data='help'),
            InlineKeyboardButton('⟲ Rᴇғʀᴇsʜ', callback_data='rfrsh')
        ]]
        await client.edit_message_media(
            query.message.chat.id, 
            query.message.id, 
            InputMediaPhoto(random.choice(PICS))
        )
        reply_markup = InlineKeyboardMarkup(buttons)
        total = await Media.count_documents()
        users = await db.total_users_count()
        chats = await db.total_chat_count()
        monsize = await db.get_db_size()
        free = 536870912 - monsize
        monsize = get_size(monsize)
        free = get_size(free)
        await query.message.edit_text(
            text=script.STATUS_TXT.format(total, users, chats, monsize, free),
            reply_markup=reply_markup,
            parse_mode=enums.ParseMode.HTML
        )

    elif query.data == "p_text":
        btn = [[
            InlineKeyboardButton('❗Bᴜʏ Pʀᴇᴍɪᴜᴍ Pʟᴀɴ / Cᴏɴᴛᴀᴄᴛ ❗', url=USERNAME)
        ],[
            InlineKeyboardButton('📤 Cʟᴏsᴇ Tʜɪs Mᴇssᴀɢᴇ 📤', callback_data='close_data')
        ]]
        reply_markup = InlineKeyboardMarkup(btn)
        await query.message.reply_text(
            text=script.PREMIUM_TEXT.format(query.from_user.mention),
            reply_markup=reply_markup,
            parse_mode=enums.ParseMode.HTML
        )
        
    elif query.data.startswith("setgs"):
        ident, set_type, status, grp_id = query.data.split("#")
        grpid = await active_connection(str(query.from_user.id))

        if str(grp_id) != str(grpid):
            await query.message.edit("Yᴏᴜʀ Aᴄᴛɪᴠᴇ Cᴏɴɴᴇᴄᴛɪᴏɴ Hᴀs Bᴇᴇɴ Cʜᴀɴɢᴇᴅ. Gᴏ Tᴏ /connections ᴀɴᴅ ᴄʜᴀɴɢᴇ ʏᴏᴜʀ ᴀᴄᴛɪᴠᴇ ᴄᴏɴɴᴇᴄᴛɪᴏɴ.")
            return await query.answer(MSG_ALRT)
            
        if set_type == 'verify_short' and query.from_user.id not in ADMINS:
            return await query.answer(text=f"Hey {query.from_user.first_name}, You can't change shortlink settings for your group !\n\nIt's an admin only setting !", show_alert=True)
        
        if status == "True":
            await save_group_settings(grpid, set_type, False)
        else:
            await save_group_settings(grpid, set_type, True)

        settings = await get_settings(grpid)

        if settings is not None:
            buttons = [
                [
                    InlineKeyboardButton('ʀᴇsᴜʟᴛ ᴘᴀɢᴇ ',
                                         callback_data=f'setgs#button#{settings["button"]}#{str(grp_id)}'),
                    InlineKeyboardButton('ʙᴜᴛᴛᴏɴ' if settings["button"] else 'ᴛᴇxᴛ',
                                         callback_data=f'setgs#button#{settings["button"]}#{str(grp_id)}')
                ],
                [
                    InlineKeyboardButton('sᴘᴇʟʟ ᴄʜᴇᴄᴋ',
                                         callback_data=f'setgs#spell_check#{settings["spell_check"]}#{str(grp_id)}'),
                    InlineKeyboardButton('ᴇɴᴀʙʟᴇ' if settings["spell_check"] else 'ᴅɪsᴀʙʟᴇ',
                                         callback_data=f'setgs#spell_check#{settings["spell_check"]}#{str(grp_id)}')
                ],
                [
                    InlineKeyboardButton('ᴀᴜᴛᴏ ᴅᴇʟᴇᴛᴇ',
                                         callback_data=f'setgs#auto_delete#{settings["auto_delete"]}#{str(grp_id)}'),
                    InlineKeyboardButton('15 ᴍɪɴs' if settings["auto_delete"] else 'ᴅɪsᴀʙʟᴇ',
                                         callback_data=f'setgs#auto_delete#{settings["auto_delete"]}#{str(grp_id)}')
                ],
                [
                    InlineKeyboardButton('ᴀᴜᴛᴏ ꜰɪʟᴛᴇʀ',
                                         callback_data=f'setgs#auto_ffilter#{settings["auto_ffilter"]}#{str(grp_id)}'),
                    InlineKeyboardButton('ᴇɴᴀʙʟᴇ'  if settings["auto_ffilter"] else 'ᴅɪsᴀʙʟᴇ',
                                         callback_data=f'setgs#auto_ffilter#{settings["auto_ffilter"]}#{str(grp_id)}')
                ],
                [
                    InlineKeyboardButton('sʜᴏʀᴛʟɪɴᴋ ᴍᴏᴅ',
                                         callback_data=f'setgs#is_shortlink#{settings["is_shortlink"]}#{str(grp_id)}'),
                    InlineKeyboardButton('sʜᴏʀᴛʟɪɴᴋ' if settings["is_shortlink"] else 'ᴠᴇʀɪꜰʏ',
                                         callback_data=f'setgs#is_shortlink#{settings["is_shortlink"]}#{str(grp_id)}')  
                ],
                [
                    InlineKeyboardButton('ʟɪɴᴋ ᴍᴏᴅ',
                                         callback_data=f'setgs#verify_short#{settings["verify_short"]}#{str(grp_id)}'),
                    InlineKeyboardButton('ᴅɪsᴀʙʟᴇ' if settings["verify_short"] else 'ᴇɴᴀʙʟᴇ',
                                         callback_data=f'setgs#verify_short#{settings["verify_short"]}#{str(grp_id)}')                    
                ]
            ]
            reply_markup = InlineKeyboardMarkup(buttons)
            await query.message.edit_reply_markup(reply_markup)
            
    elif query.data.startswith("batchfiles"):
        ident, group_id, message_id, user = query.data.split("#")
        chat_id = query.message.chat.id
        group_id = int(group_id)
        message_id = int(message_id)
        user = int(user)
        if user != query.from_user.id:
            await query.answer("🥷 ᴛʜᴀᴛ ɪꜱ ɴᴏᴛ ғᴏʀ ʏᴏᴜʀ ᴘʟᴢ ꜱᴇᴀʀᴄʜ ʏᴏᴜʀ",show_alert=True)
            return
        link = f"https://telegram.me/{temp.U_NAME}?start=sendallfiles_{query.message.chat.id}_{group_id}-{message_id}"
        await query.answer(url=link)   
        return 

    await query.answer(MSG_ALRT)    

    
async def auto_filter(client, msg, spoll=False):
    curr_time = datetime.now(pytz.timezone('Asia/Kolkata')).time()
    # reqstr1 = msg.from_user.id if msg.from_user else 0
    # reqstr = await client.get_users(reqstr1)
    
    if not spoll:
        message = msg
        chat_id = message.chat.id
        settings = await get_settings(message.chat.id)
        if message.text.startswith("/"): return  # ignore commands
        if re.findall("((^\/|^,|^!|^\.|^[\U0001F600-\U000E007F]).*)", message.text):
            return
        if 2 < len(message.text) < 100:

            search = await replace_words(message.text)            
            files, offset, total_results = await get_search_results(search.lower(), offset=0, filter=True)
            if not files:
    
                if settings["spell_check"]:
                    return await advantage_spell_chok(msg)
                else:
                    return
        else:
            return
    else:
        message = msg.message.reply_to_message  # msg will be callback query
        search, files, offset, total_results = spoll
        settings = await get_settings(message.chat.id)
        await msg.message.delete()
    user = message.from_user.id
    chat_id = message.chat.id 
    pre = 'filep' if settings['file_secure'] else 'file'
    key = f"{message.chat.id}-{message.id}"
    chat_id = message.chat.id 
    is_lang = False
    is_series = False 
    text_link = "\n\n"
    if settings["button"]:
        btn = []
        for file in files:        
            if "s0" in str(file.caption).lower() or "season" in str(file.caption).lower():
                is_series = True  
            if "hindi" in str(file.caption).lower() or "tamil" in str(file.caption).lower() or "telugu" in str(file.caption).lower() or "kannada" in str(file.caption).lower() or "malayalam" in str(file.caption).lower() or "telugu" in str(file.caption).lower() or "english" in str(file.caption).lower():
                is_lang = True                
            btn.append([
                InlineKeyboardButton(text=f"[{get_size(file.file_size)}] {' '.join(filter(lambda x: not x.startswith('[') and not x.startswith('@') and not x.startswith('www.'), file.file_name.split()))}",  url=f'https://telegram.dog/{temp.U_NAME}?start=short_{chat_id}_{file.file_id}')
            ])
    else:
        btn = []
        for file in files:    
            if "s0" in str(file.caption).lower() or "season" in str(file.caption).lower():
                is_series = True  
            if "hindi" in str(file.caption).lower() or "tamil" in str(file.caption).lower() or "telugu" in str(file.caption).lower() or "kannada" in str(file.caption).lower() or "malayalam" in str(file.caption).lower() or "telugu" in str(file.caption).lower() or "english" in str(file.caption).lower():
                is_lang = True     
            text_link += f"<b>📽 <a href='https://telegram.me/{temp.U_NAME}?start=short_{chat_id}_{file.file_id}'>[{get_size(file.file_size)}] {' '.join(filter(lambda x: not x.startswith('[') and not x.startswith('@') and not x.startswith('www.'), file.file_name.split()))}\n\n</a></b>"         
     
    BUTTONS[key] = search
    try:
        offset = int(offset) 
    except:
        offset = 10    
    if is_series:
        btn.insert(0, [
            InlineKeyboardButton("🥶 Cʜᴏᴏsᴇ Sᴇᴀsᴏɴ 🥶", callback_data=f"season#{key}#0#{offset-10 or 0}")
        ])
    if is_lang:
        btn.insert(0, [
            InlineKeyboardButton("‼️ Cʜᴏᴏsᴇ Lᴀɴɢᴜᴀɢᴇ ‼️", callback_data=f"languages#{key}#0#{offset-10 or 0}"),
        ]) 
    if offset != "":
        req = message.from_user.id if message.from_user else 0

        btn.append(
            [InlineKeyboardButton("𝐏𝐀𝐆𝐄", callback_data="pages"), InlineKeyboardButton(text=f"1/{math.ceil(int(total_results)/int(MAX_B_TN))}",callback_data="pages"), InlineKeyboardButton(text="𝐍𝐄𝐗𝐓 ➪",callback_data=f"next_{req}_{key}_{offset}")]
        )

    else:

        btn.append(
            [InlineKeyboardButton(text="𝐍𝐎 𝐌𝐎𝐑𝐄 𝐏𝐀𝐆𝐄𝐒 𝐀𝐕𝐀𝐈𝐋𝐀𝐁𝐋𝐄",callback_data="pages")]
        ) 

    cap = f"<b>🍿 Hᴇʏ {message.from_user.mention},\n♨️ ʜᴇʀᴇ ɪ ꜰᴏᴜɴᴅ ꜰᴏʀ ʏᴏᴜʀ sᴇᴀʀᴄʜ {search}...</b>"
    CAP[key] = cap
    if settings['auto_delete']:
        k = await message.reply_text(cap + text_link, reply_markup=InlineKeyboardMarkup(btn), disable_web_page_preview=True)
        await asyncio.sleep(600)
        await k.delete()
    else:
        await message.reply_text(cap + text_link, reply_markup=InlineKeyboardMarkup(btn), disable_web_page_preview=True)
        

async def advantage_spell_chok(msg):
    us = msg.from_user.id if msg.from_user else 0
    query = re.sub(
        r"\b(pl(i|e)*?(s|z+|ease|se|ese|(e+)s(e)?)|((send|snd|giv(e)?|gib)(\sme)?)|movie(s)?|new|latest|br((o|u)h?)*|^h(e|a)?(l)*(o)*|mal(ayalam)?|t(h)?amil|file|that|find|und(o)*|kit(t(i|y)?)?o(w)?|thar(u)?(o)*w?|kittum(o)*|aya(k)*(um(o)*)?|full\smovie|any(one)|with\ssubtitle(s)?)",
        "", msg.text, flags=re.IGNORECASE)  # plis contribute some common words

    query = query.strip()
    try:
        movies = await get_poster(msg.text, bulk=True)
    except Exception as e:
        logger.exception(e)
        reply = query.replace(" ", '+')  
        reply_markup = InlineKeyboardMarkup([[
        InlineKeyboardButton("🔍 𝗖𝗹𝗶𝗰𝗸 𝗧𝗼 𝗖𝗵𝗲𝗰𝗸 𝗦𝗽𝗶𝗹𝗹𝗶𝗻𝗴 ✅", url=f"https://www.google.com/search?q={reply}+movie")
        ],[
        InlineKeyboardButton("🔍 𝗖𝗹𝗶𝗰𝗸 𝗧𝗼 𝗖𝗵𝗲𝗰𝗸 𝗥𝗲𝗹𝗲𝗮𝘀𝗲 𝗗𝗮𝘁𝗲 📅", url=f"https://www.google.com/search?q={reply}+release+date")
        ]]  
        )    
        a = await msg.reply_text(
            text=script.I_CUDNT.format(query),
            reply_markup=reply_markup                 
        )
        async def del_func():
            await asyncio.sleep(38)
            await a.delete()
            await msg.delete()         
        await asyncio.create_task(del_func())
        return
    movielist = [] #error fixed
    if not movies:
        reply = query.replace(" ", '+')  
        reply_markup = InlineKeyboardMarkup([[
        InlineKeyboardButton("🔍 Click To Check Spilling ✅", url=f"https://www.google.com/search?q={reply}+movie")
        ],[
        InlineKeyboardButton("🔍 Click To Check Release Date 📅", url=f"https://www.google.com/search?q={reply}+release+date")
        ]]  
        )    
        ab = await msg.reply_text(
            text=script.I_CUDNT.format(query),
            reply_markup=reply_markup                 
        )
        async def del_func():
            await asyncio.sleep(38)
            await ab.delete()
            await msg.delete()            
        await asyncio.create_task(del_func())   
        return

    movielist += [movie.get('title') for movie in movies]
    movielist += [f"{movie.get('title')} {movie.get('year')}" for movie in movies] 
    movielist = movielist[:5]
    
    SPELL_CHECK[msg.id] = movielist
    btn = [[
        InlineKeyboardButton(
            text=movie.strip(),
            callback_data=f"sp#{us}#{k}",
        )
    ] for k, movie in enumerate(movielist)]
    btn.append([InlineKeyboardButton(text="Close", callback_data=f'sp#{us}#cl_sl')])
    dll = await msg.reply_text(
        text=(script.CUDNT_FND.format(query)),
        reply_markup=InlineKeyboardMarkup(btn), reply_to_message_id=msg.id)

    async def del_func():
        await asyncio.sleep(120)
        await dll.delete()
        await msg.delete()
    await asyncio.create_task(del_func())
    

async def manual_filters(client, message, text=False):
    group_id = message.chat.id
    name = text or message.text
    reply_id = message.reply_to_message.id if message.reply_to_message else message.id
    keywords = await get_filters(group_id)
    for keyword in reversed(sorted(keywords, key=len)):
        pattern = r"( |^|[^\w])" + re.escape(keyword) + r"( |$|[^\w])"
        if re.search(pattern, name, flags=re.IGNORECASE):
            reply_text, btn, alert, fileid = await find_filter(group_id, keyword)

            if reply_text:
                reply_text = reply_text.replace("\\n", "\n").replace("\\t", "\t")

            if btn is not None:
                try:
                    if fileid == "None":
                        if btn == "[]":
                            await client.send_message(group_id, reply_text, disable_web_page_preview=True)
                        else:
                            button = eval(btn)
                            await client.send_message(
                                group_id,
                                reply_text,
                                disable_web_page_preview=True,
                                reply_markup=InlineKeyboardMarkup(button),
                                reply_to_message_id=reply_id
                            )
                    elif btn == "[]":
                        await client.send_cached_media(
                            group_id,
                            fileid,
                            caption=reply_text or "",
                            reply_to_message_id=reply_id
                        )
                    else:
                        button = eval(btn)
                        await message.reply_cached_media(
                            fileid,
                            caption=reply_text or "",
                            reply_markup=InlineKeyboardMarkup(button),
                            reply_to_message_id=reply_id
                        )
                except Exception as e:
                    logger.exception(e)
                break
    else:
        return False
