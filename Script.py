import os
class script(object):
    
    START_TXT = """<b>Hᴇʟʟᴏ {},
Mʏ Nᴀᴍᴇ Is <a href=https://t.me/{}>{}</a>, I Cᴀɴ Pʀᴏᴠɪᴅᴇ Mᴏᴠɪᴇs, Jᴜsᴛ Aᴅᴅ Mᴇ Tᴏ Yᴏᴜʀ Gʀᴏᴜᴘ As Aᴅᴍɪɴ Aɴᴅ Eɴᴊᴏʏ 😍</b></b>"""

    HELP_TXT = """<b>Hᴇʏ {}
Hᴇʀᴇ Is Tʜᴇ Hᴇʟᴘ Fᴏʀ Mʏ Cᴏᴍᴍᴀɴᴅs.</b>"""

    ABOUT_TXT = """<b>⚜️ MY NAME : {}</b>
<b>⚜️ MY OWNER : <a href=https://t.me/AkshayChand08>Akshay Chand</a></b>
               : <a href=https://t.me/Rutuja78>Rutuja</a></b>
<b>⚜️ UPDATES : <a href=https://t.me/arsOfficial10>ARS Official</a></b>"""

    MANUELFILTER_TXT = """Hii"""

    BUTTON_TXT = """Hii"""

    AUTOFILTER_TXT = """Hii"""

    CONNECTION_TXT = """ʜᴇʟᴘ: <b>ᴄᴏɴɴᴇᴄᴛɪᴏɴꜱ</b>
- ᴜꜱᴇᴅ ᴛᴏ ᴄᴏɴɴᴇᴄᴛ ʙᴏᴛ ᴛᴏ ᴘᴍ ꜰᴏʀ ᴍᴀɴᴀɢɪɴɢ ꜰɪʟᴛᴇʀꜱ 
- ɪᴛ ʜᴇʟᴘꜱ ᴛᴏ ᴀᴠᴏɪᴅ ꜱᴘᴀᴍᴍɪɴɢ ɪɴ ɢʀᴏᴜᴘꜱ.
<b>ɴᴏᴛᴇ:</b>
1. ᴏɴʟʏ ᴀᴅᴍɪɴꜱ ᴄᴀɴ ᴀᴅᴅ ᴀ ᴄᴏɴɴᴇᴄᴛɪᴏɴ.
2. ꜱᴇɴᴅ <code>/ᴄᴏɴɴᴇᴄᴛ</code> ꜰᴏʀ ᴄᴏɴɴᴇᴄᴛɪɴɢ ᴍᴇ ᴛᴏ ʏᴏᴜʀ ᴘᴍ
Cᴏᴍᴍᴀɴᴅs Aɴᴅ Usᴀɢᴇ:
• /connect  - <code>ᴄᴏɴɴᴇᴄᴛ ᴀ ᴘᴀʀᴛɪᴄᴜʟᴀʀ ᴄʜᴀᴛ ᴛᴏ ʏᴏᴜʀ ᴘᴍ</code>
• /disconnect  - <code>ᴅɪꜱᴄᴏɴɴᴇᴄᴛ ꜰʀᴏᴍ ᴀ ᴄʜᴀᴛ</code>
• /connections - <code>ʟɪꜱᴛ ᴀʟʟ ʏᴏᴜʀ ᴄᴏɴɴᴇᴄᴛɪᴏɴꜱ</code>"""

    EXTRAMOD_TXT = """ʜᴇʟᴘ: Exᴛʀᴀ Mᴏᴅᴜʟᴇs
<b>ɴᴏᴛᴇ:</b>
ᴛʜᴇꜱᴇ ᴀʀᴇ ᴛʜᴇ ᴇxᴛʀᴀ ꜰᴇᴀᴛᴜʀᴇꜱ ᴏꜰ ᴛʜɪꜱ ʙᴏᴛ
Cᴏᴍᴍᴀɴᴅs Aɴᴅ Usᴀɢᴇ:
• /id - <code>ɢᴇᴛ ɪᴅ ᴏꜰ ᴀ ꜱᴘᴇᴄɪꜰɪᴇᴅ ᴜꜱᴇʀ.</code>
• /info  - <code>ɢᴇᴛ ɪɴꜰᴏʀᴍᴀᴛɪᴏɴ ᴀʙᴏᴜᴛ ᴀ ᴜꜱᴇʀ.</code>"""

    ADMIN_TXT = """ʜᴇʟᴘ: Aᴅᴍɪɴ Mᴏᴅs
<b>ɴᴏᴛᴇ:</b>
Tʜɪs Mᴏᴅᴜʟᴇ Oɴʟʏ Wᴏʀᴋs Fᴏʀ Mʏ Aᴅᴍɪɴs
Cᴏᴍᴍᴀɴᴅs Aɴᴅ Usᴀɢᴇ:
• /logs - <code>ᴛᴏ ɢᴇᴛ ᴛʜᴇ ʀᴇᴄᴇɴᴛ ᴇʀʀᴏʀꜱ</code>
• /stats - <code>ᴛᴏ ɢᴇᴛ ꜱᴛᴀᴛᴜꜱ ᴏꜰ ꜰɪʟᴇꜱ ɪɴ ᴅʙ. [Tʜɪs Cᴏᴍᴍᴀɴᴅ Cᴀɴ Bᴇ Usᴇᴅ Bʏ Aɴʏᴏɴᴇ]</code>
• /delete - <code>ᴛᴏ ᴅᴇʟᴇᴛᴇ ᴀ ꜱᴘᴇᴄɪꜰɪᴄ ꜰɪʟᴇ ꜰʀᴏᴍ ᴅʙ.</code>
• /users - <code>ᴛᴏ ɢᴇᴛ ʟɪꜱᴛ ᴏꜰ ᴍʏ ᴜꜱᴇʀꜱ ᴀɴᴅ ɪᴅꜱ.</code>
• /chats - <code>ᴛᴏ ɢᴇᴛ ʟɪꜱᴛ ᴏꜰ ᴍʏ ᴄʜᴀᴛꜱ ᴀɴᴅ ɪᴅꜱ</code>
• /leave  - <code>ᴛᴏ ʟᴇᴀᴠᴇ ꜰʀᴏᴍ ᴀ ᴄʜᴀᴛ.</code>
• /disable  -  <code>ᴛᴏ ᴅɪꜱᴀʙʟᴇ ᴀ ᴄʜᴀᴛ.</code>
• /ban  - <code>ᴛᴏ ʙᴀɴ ᴀ ᴜꜱᴇʀ.</code>
• /unban  - <code>ᴛᴏ ᴜɴʙᴀɴ ᴀ ᴜꜱᴇʀ.</code>
• /channel - <code>ᴛᴏ ɢᴇᴛ ʟɪꜱᴛ ᴏꜰ ᴛᴏᴛᴀʟ ᴄᴏɴɴᴇᴄᴛᴇᴅ ᴄʜᴀɴɴᴇʟꜱ</code>
• /broadcast - <code>ᴛᴏ ʙʀᴏᴀᴅᴄᴀꜱᴛ ᴀ ᴍᴇꜱꜱᴀɢᴇ ᴛᴏ ᴀʟʟ ᴜꜱᴇʀꜱ</code>
• /grp_broadcast - <code>Tᴏ ʙʀᴏᴀᴅᴄᴀsᴛ ᴀ ᴍᴇssᴀɢᴇ ᴛᴏ ᴀʟʟ ᴄᴏɴɴᴇᴄᴛᴇᴅ ɢʀᴏᴜᴘs.</code>
• /gfilter - <code>ᴛᴏ ᴀᴅᴅ ɢʟᴏʙᴀʟ ғɪʟᴛᴇʀs</code>
• /gfilters - <code>ᴛᴏ ᴠɪᴇᴡ ʟɪsᴛ ᴏғ ᴀʟʟ ɢʟᴏʙᴀʟ ғɪʟᴛᴇʀs</code>
• /delg - <code>ᴛᴏ ᴅᴇʟᴇᴛᴇ ᴀ sᴘᴇᴄɪғɪᴄ ɢʟᴏʙᴀʟ ғɪʟᴛᴇʀ</code>
• /request - <code>Tᴏ sᴇɴᴅ ᴀ Mᴏᴠɪᴇ/Sᴇʀɪᴇs ʀᴇᴏ̨ᴜᴇsᴛ ᴛᴏ ʙᴏᴛ ᴀᴅᴍɪɴs. Oɴʟʏ ᴡᴏʀᴋs ᴏɴ sᴜᴘᴘᴏʀᴛ ɢʀᴏᴜᴘ. [Tʜɪs Cᴏᴍᴍᴀɴᴅ Cᴀɴ Bᴇ Usᴇᴅ Bʏ Aɴʏᴏɴᴇ]</code>
• /delallg - <code>Tᴏ ᴅᴇʟᴇᴛᴇ ᴀʟʟ Gғɪʟᴛᴇʀs ғʀᴏᴍ ᴛʜᴇ ʙᴏᴛ's ᴅᴀᴛᴀʙᴀsᴇ.</code>
• /deletefiles - <code>Tᴏ ᴅᴇʟᴇᴛᴇ CᴀᴍRɪᴘ ᴀɴᴅ PʀᴇDVD Fɪʟᴇs ғʀᴏᴍ ᴛʜᴇ ʙᴏᴛ's ᴅᴀᴛᴀʙᴀsᴇ.</code>"""

    STATUS_TXT = """<b>🗂 Total Files: <code>{}</code>
👤 Total Users: <code>{}</code>
🔮 Total Chats: <code>{}</code>
🗃 Storage: <code>{}</code>
🗃 Free Storage: <code>{}</code></b>"""

    LOG_TEXT_G = """#NewGroup
Gʀᴏᴜᴘ = {}(<code>{}</code>)
Tᴏᴛᴀʟ Mᴇᴍʙᴇʀs = <code>{}</code>
Aᴅᴅᴇᴅ Bʏ - {}"""

    LOG_TEXT_P = """#NewUser
ID - <code>{}</code>
Nᴀᴍᴇ - {}"""

    ALRT_TXT = """ʜᴇʟʟᴏ {},
ᴛʜɪꜱ ɪꜱ ɴᴏᴛ ʏᴏᴜʀ ᴍᴏᴠɪᴇ ʀᴇQᴜᴇꜱᴛ,
ʀᴇQᴜᴇꜱᴛ ʏᴏᴜʀ'ꜱ..."""

    OLD_ALRT_TXT = """ʜᴇʏ {},
ʏᴏᴜ ᴀʀᴇ ᴜꜱɪɴɢ ᴏɴᴇ ᴏꜰ ᴍʏ ᴏʟᴅ ᴍᴇꜱꜱᴀɢᴇꜱ, 
ᴘʟᴇᴀꜱᴇ ꜱᴇɴᴅ ᴛʜᴇ ʀᴇQᴜᴇꜱᴛ ᴀɢᴀɪɴ."""

    CUDNT_FND = """<b>Sᴘᴇʟʟɪɴɢ Mɪꜱᴛᴀᴋᴇ Bʀᴏ ‼️
Dᴏɴ'ᴛ Wᴏʀʀʏ 😊 Cʜᴏᴏꜱᴇ Tʜᴇ Cᴏʀʀᴇᴄᴛ Oɴᴇ Bᴇʟᴏᴡ 👇🏼</b>"""

    I_CUDNT = """<b>sᴏʀʀʏ ʙʀᴏ ɴᴏ ꜰɪʟᴇs ꜰᴏᴜɴᴅ ᴍʏ ᴅᴀᴛᴀʙᴀsᴇ

ᴄʜᴇᴄᴋ ʏᴏᴜʀ sᴘᴇʟʟɪɴɢ ɪɴ ɢᴏᴏɢʟᴇ ᴀɴᴅ ᴛʀʏ ᴀɢᴀɪɴ ‼️

ᴛᴀᴘ ᴛᴏ ɢᴏᴏɢʟᴇ ᴀɴᴅ ᴄᴏᴘʏ ʀɪɢʜᴛ sᴘᴇʟʟɪɴɢ</b>"""

    I_CUD_NT = """ɪ ᴄᴏᴜʟᴅɴ'ᴛ ꜰɪɴᴅ ᴀɴʏ ᴍᴏᴠɪᴇ ʀᴇʟᴀᴛᴇᴅ ᴛᴏ {}.
ᴘʟᴇᴀꜱᴇ ᴄʜᴇᴄᴋ ᴛʜᴇ ꜱᴘᴇʟʟɪɴɢ ᴏɴ ɢᴏᴏɢʟᴇ ᴏʀ ɪᴍᴅʙ..."""

    MVE_NT_FND = """<b>𝐌𝐎𝐕𝐈𝐄 𝐍𝐎𝐓 𝐀𝐕𝐀𝐈𝐋𝐀𝐁𝐋𝐄 𝐑𝐄𝐀𝐒𝐎𝐍

1 𝐎.𝐓.𝐓 𝐎𝐑 𝐃𝐕𝐃 𝐍𝐎𝐓 𝐑𝐄𝐋𝐄𝐀𝐒𝐄𝐃

2 𝐓𝐘𝐏𝐄 𝐍𝐀𝐌𝐄 𝐖𝐈𝐓𝐇 𝐘𝐄𝐀𝐑

3 𝐌𝐎𝐕𝐈𝐄 𝐈𝐒 𝐍𝐎𝐓 𝐀𝐕𝐀𝐈𝐋𝐀𝐁𝐋𝐄 𝐈𝐍 𝐓𝐇𝐄 𝐃𝐀𝐓𝐀𝐁𝐀𝐒𝐄 𝐑𝐄𝐏𝐎𝐑𝐓 𝐓𝐎 𝐀𝐃𝐌𝐈𝐍👇🏼👇🏼</b>"""

    TOP_ALRT_MSG = """Cʜᴇᴄᴋɪɴɢ Fᴏʀ Mᴏᴠɪᴇ Iɴ Dᴀᴛᴀʙᴀsᴇ..."""

    MELCOW_ENG = """<b>Hᴇʟʟᴏ {} 😍, Aɴᴅ Wᴇʟᴄᴏᴍᴇ Tᴏ {} Gʀᴏᴜᴘ ❤️</b>"""

    REQINFO = """
⚠ ɪɴꜰᴏʀᴍᴀᴛɪᴏɴ ⚠

ᴀꜰᴛᴇʀ 5 ᴍɪɴᴜᴛᴇꜱ ᴛʜɪꜱ ᴍᴇꜱꜱᴀɢᴇ ᴡɪʟʟ ʙᴇ ᴀᴜᴛᴏᴍᴀᴛɪᴄᴀʟʟʏ ᴅᴇʟᴇᴛᴇᴅ

ɪꜰ ʏᴏᴜ ᴅᴏ ɴᴏᴛ ꜱᴇᴇ ᴛʜᴇ ʀᴇǫᴜᴇsᴛᴇᴅ ᴍᴏᴠɪᴇ / sᴇʀɪᴇs ꜰɪʟᴇ, ʟᴏᴏᴋ ᴀᴛ ᴛʜᴇ ɴᴇxᴛ ᴘᴀɢᴇ"""

    SELECT = """
MOVIES ➢ Sᴇʟᴇᴄᴛ "Lᴀɴɢᴜᴀɢᴇs"

SERIES ➢ Sᴇʟᴇᴄᴛ "Sᴇᴀsᴏɴs"

Tɪᴘ: Sᴇʟᴇᴄᴛ "Lᴀɴɢᴜᴀɢᴇs" ᴏʀ "Sᴇᴀsᴏɴs" Bᴜᴛᴛᴏɴ ᴀɴᴅ Cʟɪᴄᴋ "Sᴇɴᴅ Aʟʟ" Tᴏ ɢᴇᴛ Aʟʟ Fɪʟᴇ Lɪɴᴋs ɪɴ ᴀ Sɪɴɢʟᴇ ᴄʟɪᴄᴋ"""

    SINFO = """Hii"""

    NORSLTS = """
★ #𝗡𝗼𝗥𝗲𝘀𝘂𝗹𝘁𝘀 ★

𝗜𝗗 <b>: {}</b>

𝗡𝗮𝗺𝗲 <b>: {}</b>

𝗠𝗲𝘀𝘀𝗮𝗴𝗲 <b>: {}</b>"""

    CAPTION = """<b>📝 NAME ➠ {file_name}

⚙️ SIZE ➠ : {file_size}</b>"""

    IMDB_TEMPLATE_TXT = """

🏷 Title: <a href={url}>{title}</a>
🎭 Genres: {genres}
📆 Year: <a href={url}/releaseinfo>{year}</a>
⏱️ Result Shown in: {remaining_seconds} <i>seconds</i> 🔥
🌟 Rating: <a href={url}/ratings>{rating}</a> / 10</b>"""
    
    ALL_FILTERS = """
<b>Hᴇʏ {}, Tʜᴇsᴇ ᴀʀᴇ ᴍʏ ᴛʜʀᴇᴇ ᴛʏᴘᴇs ᴏғ ғɪʟᴛᴇʀs.</b>"""
    
    GFILTER_TXT = """Hii"""
    
    FILE_STORE_TXT = """Hii"""


    RESTART_TXT = """
<b>Bᴏᴛ Rᴇsᴛᴀʀᴛᴇᴅ !

📅 Dᴀᴛᴇ : <code>{}</code>
⏰ Tɪᴍᴇ : <code>{}</code>
🌐 Tɪᴍᴇᴢᴏɴᴇ : <code>Asia/Kolkata</code>
⚜️ BUILD STATUS: <code>V1.9.7 [STABLE]</code></b>"""

    LOGO = """Bot Started successfully, no any error"""
    
    PREMIUM_TEXT = """Hii"""

    ADULT_TEXT = """hii"""

    FSUB_TXT = """
<b>‼️ʜᴏᴡ ᴛᴏ ᴇɴᴀʙʟᴇ ғᴏʀᴄᴇ sᴜʙsᴄʀɪʙᴇ‼️


⁉️ ᴍᴀᴋᴇ ʙᴏᴛ ᴀᴅᴍɪɴ ɪɴ ʏᴏᴜʀ ɢʀᴏᴜᴘ ᴀɴᴅ ᴄᴀʜɴɴᴇʟ


⁉️ sᴇɴᴅ ʏᴏᴜʀ ᴄᴀʜɴɴᴇʟ ɪᴅ /set_fsub -100**** ɪᴅ ɪɴ ʏᴏᴜʀ ɢʀᴏᴜᴘ


⁉️ ᴛᴏ sᴛᴏᴘ ꜰᴏʀᴄᴇ sᴜʙ
sᴇɴᴅ /offfsub -100**** ɪᴅ ɪɴ ʏᴏᴜʀ ɢʀᴏᴜᴘ


⁉️ ᴛᴏ ᴄʜᴇᴄᴋ ᴄᴏɴɴᴇᴄᴛᴇᴅ ꜰᴏʀᴄᴇsᴜʙ ᴄʜᴀɴɴᴇʟ sᴇɴᴅ /checkfsub ɪɴ ʏᴏᴜʀ ɢʀᴏᴜᴘ


💯 ɴᴏᴛᴇ - ᴛʜɪs ʙᴏᴛ ɪs ꜰʀᴇᴇ ᴛᴏ ᴀʟʟ, ʏᴏᴜ ᴄᴀɴ ᴜsᴇ ᴛʜɪs ʙᴏᴛ ɪɴ ʏᴏᴜʀ ɢʀᴏᴜᴘs</b>"""   
    
    CAPTION_TXT = """
ᴇxᴀᴍᴘʟᴇ 👇🏼 ᴀᴅᴅ ʏᴏᴜʀ ɢʀᴏᴜᴘ ʟɪɴᴋ ᴛʜɪs ғᴏʀᴍᴀᴛ

👉 /set_caption <b>Join [Here](https://t.me/arsOfficial10)</b> 

FILE : <code>{file_name}</code> 
Size : <i>{file_size}</i>"""
    
    ERN_MONY_S = """
<b>🀄 ʜᴏᴡ ᴛᴏ sᴇᴛ sʜᴏʀᴛʟɪɴᴋ ᴍᴏᴅᴇ 🀄

ᴛʜɪs ᴄᴏᴍᴍᴀɴᴅ ᴏɴʟʏ ᴡᴏʀᴋ ᴏɴ sʜᴏʀᴛʟɪɴᴋ ᴍᴏᴅᴇ

❗ sᴛᴇᴘ 1 : ʏᴏᴜ ᴍᴜsᴛ ʜᴀᴠᴇ ᴀᴛʟᴇᴀsᴛ ᴏɴᴇ ɢʀᴏᴜᴘ ᴡɪᴛʜ ᴍɪɴɪᴍᴜᴍ 𝟷𝟶𝟶 ᴍᴇᴍʙᴇʀs.

❗ sᴛᴇᴘ 2 : ᴍᴀᴋᴇ ᴀᴄᴄᴏᴜɴᴛ ᴏɴ ♻️ TNLINK ʏᴏᴜ ᴄᴀɴ ᴀʟsᴏ ᴜsᴇᴅ ᴏᴛʜᴇʀ sʜᴏʀᴛɴᴇʀ ᴡᴇʙsɪᴛᴇ 

❗ sᴛᴇᴘ 3 : ᴛʜᴇɴ sᴇᴛ ʏᴏᴜʀ sʜᴏʀᴛɴᴇʀ ᴅᴇᴛᴀɪʟs ʙʏ ᴛʜɪs ꜰᴏʀᴍᴀᴛ ᴇxᴀᴍᴘʟᴇ👇🏼

/shortlink tnshort.net 6ee7840bdaf0103a11214c62c83

💯 ɴᴏᴛᴇ - ᴛʜɪs ʙᴏᴛ ɪs ꜰʀᴇᴇ ᴛᴏ ᴀʟʟ, ʏᴏᴜ ᴄᴀɴ ᴜsᴇ ᴛʜɪs ʙᴏᴛ ɪɴ ʏᴏᴜʀ ɢʀᴏᴜᴘs ᴀɴᴅ ᴇᴀʀɴ ᴜɴʟɪᴍɪᴛᴇᴅ ᴍᴏɴᴇʏ.</b>"""
    
    ERN_MONY_V = """
<b> Step 1: make admin this <a href=https://t.me/{}>{}</a> bot your group  

Step 2: Add your website and API

Exp: /set_shortlink 1</code> <a href=https://publicearn.com/ref/AkshayChand10>publicearn.com</a> 4b392f8eb6ad711be589ae36 (verify & page)

On Second Verify (only Group) /verify2 True</code>
Off Second Verify /verify2 False</code>

#Note second verification 4 Hours will happen after.
/set_shortlink 2</code> <a href=https://link2paisa.com/ref/AkshayChand10>link2paisa.com</a> 4b392f8eb6ad711be589ae36 (Second Verify)

Step 3: add your how to verify & download video

    👇 how to add 👇

Exp:  /set_tutorial 1 video link</code> (verify & page)
       /set_tutorial 2 video link</code> (Second Verify)
      
Step 4: Check Your All Details 
        command /details (Work Only Group)</b>"""

    CUSTOM_DETAILS = """Hey {}. welcome 
    
<b>ᴄᴜꜱᴛᴏᴍ ꜱᴇᴛᴛɪɴɢꜱ ғᴏʀ</b>: <b>{}</b>

━━━━•❅•°•❈•°•❅•━━━━

✅️ 1sᴛ ᴠᴇʀɪꜰʏ sʜᴏʀᴛɴᴇʀ ɴᴀᴍᴇ/ᴀᴘɪ

<b>ɴᴀᴍᴇ</b>:- `{}`
<b>ᴀᴘɪ</b>:- `{}`

📍 <b>ᴛᴜᴛᴏʀɪᴀʟ ʟɪɴᴋ</b>:- `{}`

━━━━•❅•°•❈•°•❅•━━━━

✅️ 2ɴᴅ ᴠᴇʀɪꜰʏ sʜᴏʀᴛɴᴇʀ ɴᴀᴍᴇ/ᴀᴘɪ

<b>ɴᴀᴍᴇ</b>:- `{}`
<b>ᴀᴘɪ</b>:- `{}`

📍 <b>ᴛᴜᴛᴏʀɪᴀʟ ʟɪɴᴋ</b>:- `{}`

━━━━•❅•°•❈•°•❅•━━━━
🧳 ᴍᴏʀᴇ ᴅᴇᴛᴀɪʟꜱ:

<b>ғꜱᴜʙ ᴄʜᴀɴɴᴇʟ</b>:- `{}`

<b>ғɪʟᴇ ᴄᴀᴘᴛɪᴏɴ</b>: `{}`
"""
    WELCOME_TEXT = """👋 Hello {user}, Welcome to {group} group"""


VERIFY_TEXT = """<b>Hᴇʏ {}

ʏᴏᴜ ᴀʀᴇ ɴᴏᴛ ᴠᴇʀɪꜰɪᴇᴅ ꜰɪʀsᴛ ᴠᴇʀɪꜰɪᴄᴀᴛɪᴏɴ ᴛᴏᴅᴀʏ ᴛᴀᴘ ᴏɴ ᴛʜᴇ ᴠᴇʀɪꜰʏ ʙᴜᴛᴛᴏɴ ᴀɴᴅ ɢᴇᴛ ᴜɴʟɪᴍɪᴛᴇᴅ ᴀᴄᴄᴇss ᴅɪʀᴇᴄᴛ ꜰɪʟᴇs ɴᴏ ʟɪɴᴋ sᴛɪʟʟ ɴᴇxᴛ ᴠᴇʀɪꜰɪᴄᴀᴛɪᴏɴ ⏳

ᴇxᴘɪʀᴇ ᴏɴ 𝟷 ʜᴏᴜʀs ⌛

इस  बॉट को  इस्तेमाल  करने  के  लिए  आपको  ᴠᴇʀɪꜰʏ  करना  होगा  नहीं  तो  आप  इसका  इस्तेमाल  नहीं  कर  पाएंगे ।

#Vᴇʀɪꜰɪᴄᴀᴛɪᴏɴ:- 1/2
</b>"""
SECOND_VERIFICATION_TEXT = """<b>Hᴇʏ. {}. 

ʏᴏᴜ ᴀʀᴇ ɴᴏᴛ ᴠᴇʀɪꜰɪᴇᴅ sᴇᴄᴏɴᴅ ᴠᴇʀɪꜰɪᴄᴀᴛɪᴏɴ ᴛᴏᴅᴀʏ, ᴘʟᴇᴀsᴇ ᴠᴇʀɪꜰʏ ɴᴏᴡ ᴀɴᴅ ɢᴇᴛ ᴜɴʟɪᴍɪᴛᴇᴅ ᴀᴄᴄᴇss ᴀɴᴅ ᴅɪʀᴇᴄᴛ ꜰɪʟᴇs ɴᴏ ʟɪɴᴋ 🔗 😊

ᴇxᴘɪʀᴇ ᴏɴ 𝟷𝟸:𝟶𝟶 ᴀᴍ ⌛

इस  बॉट को  इस्तेमाल  करने  के  लिए  आपको  ᴠᴇʀɪꜰʏ  करना  होगा  नहीं  तो  आप  इसका  इस्तेमाल  नहीं  कर  पाएंगे ।


#Vᴇʀɪꜰɪᴄᴀᴛɪᴏɴ:- 2/2
</b>"""


SECOND_VERIFICATION_TEXT = os.environ.get('SECOND_VERIFICATION_TEXT', SECOND_VERIFICATION_TEXT)


VERIFY_COMPLETE_TEXT = """<b>ʜᴇʏ {}

ʏᴏᴜ ʜᴀᴠᴇ ᴄᴏᴍᴘʟᴇᴛᴇᴅ ᴛʜᴇ 1st ᴠᴇʀɪꜰɪᴄᴀᴛɪᴏɴ ✅️...

ɴᴏᴡ ʏᴏᴜ ʜᴀᴠᴇ ᴜɴʟɪᴍɪᴛᴇᴅ ᴀᴄᴄᴇss ꜰᴏʀ ᴛɪʟʟ ɴᴇxᴛ ᴠᴇʀɪꜰɪᴄᴀᴛɪᴏɴ ❤️‍🔥...</b>"""



SECOND_VERIFY_COMPLETE_TEXT = """Hay. {}. 

ʏᴏᴜ ᴀʀᴇ ɴᴏᴡ ᴠᴇʀɪғɪᴇᴅ ғᴏʀ ᴛᴏɴɪɢʜᴛ 12:00ᴀᴍ ... ᴇɴɪᴏʏ ʏᴏᴜʀ ᴜɴʟɪᴍɪᴛᴇᴅ ᴀᴄᴄᴇꜱꜱ ғᴏʀ ʏᴏᴜʀ ᴇɴᴛᴇʀᴛᴀɪɴᴍᴇɴᴛ🧑‍🎤 ..."""

VERIFIED_TXT = """
<b><u>☄ ᴜsᴇʀ ᴠᴇʀɪꜰɪᴇᴅ sᴜᴄᴄᴇssꜰᴜʟʟʏ ☄</u>

⚡️ ɴᴀᴍᴇ:- {} [ <code>{}</code> ] 
📆 ᴅᴀᴛᴇ:- <code>{} </code></b>

#verified_{}_completed
"""
