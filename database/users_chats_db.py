import motor.motor_asyncio
import datetime
from info import ALL_SHORT_LINK_OFF, WELCOME_TEXT, AUTH_CHANNEL, VERIFY_LOG, TUTORIAL, SHORTLINK_URL, SHORTLINK_API, SHORTLINK_URL2, SHORTLINK_API2, CUSTOM_FILE_CAPTION, IS_VERIFY, DATABASE_NAME, DATABASE_URI, IMDB, IMDB_TEMPLATE, MELCOW_NEW_USERS, P_TTI_SHOW_OFF, SINGLE_BUTTON, SPELL_CHECK_REPLY, PROTECT_CONTENT, AUTO_DELETE, MAX_BTN, AUTO_FFILTER, SHORTLINK_API, SHORTLINK_URL, IS_SHORTLINK, IS_TUTORIAL
import pytz

class Database:
    
    def __init__(self, uri, database_name):
        self._client = motor.motor_asyncio.AsyncIOMotorClient(uri)
        self.db = self._client[database_name]
        self.col = self.db.users
        self.grp = self.db.groups
        self.users = self.db.uersz
        self.verify_id = self.db.verify_id
        self.misc = self.db.misc
       

    def new_user(self, id, name):
        return dict(
            id = id,
            name = name,
            ban_status=dict(
                is_banned=False,
                ban_reason="",
            ),
        )

    def new_group(self, id, title):
        return dict(
            id = id,
            title = title, 
            verify2 = False,
            chat_status=dict(
                is_disabled=False,
                reason="",
            ),
        )
    
    async def add_user(self, id, name):
        user = self.new_user(id, name)
        await self.col.insert_one(user)
    
    async def is_user_exist(self, id):
        user = await self.col.find_one({'id':int(id)})
        return bool(user)
    
    async def total_users_count(self):
        count = await self.col.count_documents({})
        return count
    
    async def remove_ban(self, id):
        ban_status = dict(
            is_banned=False,
            ban_reason=''
        )
        await self.col.update_one({'id': id}, {'$set': {'ban_status': ban_status}})
    
    async def ban_user(self, user_id, ban_reason="No Reason"):
        ban_status = dict(
            is_banned=True,
            ban_reason=ban_reason
        )
        await self.col.update_one({'id': user_id}, {'$set': {'ban_status': ban_status}})

    async def get_ban_status(self, id):
        default = dict(
            is_banned=False,
            ban_reason=''
        )
        user = await self.col.find_one({'id':int(id)})
        if not user:
            return default
        return user.get('ban_status', default)

    async def get_all_users(self):
        return self.col.find({})
    
    async def delete_user(self, user_id):
        await self.col.delete_many({'id': int(user_id)})
    async def delete_chat(self, grp):
        await self.grp.delete_many({'id': int(grp)})

    async def get_banned(self):
        users = self.col.find({'ban_status.is_banned': True})
        chats = self.grp.find({'chat_status.is_disabled': True})
        b_chats = [chat['id'] async for chat in chats]
        b_users = [user['id'] async for user in users]
        return b_users, b_chats
    
    async def add_chat(self, chat, title):
        chat = self.new_group(chat, title)
        await self.grp.insert_one(chat)   

    async def get_chat(self, chat):
        chat = await self.grp.find_one({'id':int(chat)})
        return False if not chat else chat.get('chat_status')
    
    async def re_enable_chat(self, id):
        chat_status=dict(
            is_disabled=False,
            reason="",
            )
        await self.grp.update_one({'id': int(id)}, {'$set': {'chat_status': chat_status}})
        
    async def update_settings(self, id, settings):
        await self.grp.update_one({'id': int(id)}, {'$set': {'settings': settings}})
           
    async def get_settings(self, id):
        default = {
            'button': SINGLE_BUTTON,
            'botpm': P_TTI_SHOW_OFF,
            'file_secure': PROTECT_CONTENT,
            'imdb': IMDB,
            'spell_check': SPELL_CHECK_REPLY,
            'welcome': MELCOW_NEW_USERS,
            'auto_delete': AUTO_DELETE,
            'auto_ffilter': AUTO_FFILTER,
            'max_btn': MAX_BTN,
            'template': IMDB_TEMPLATE,
            'shortlink': SHORTLINK_URL,
            'shortlink_api': SHORTLINK_API,
            'is_shortlink': IS_SHORTLINK,
            'is_verify': IS_VERIFY, 
            'tutorial': TUTORIAL,
            'tutorial2': TUTORIAL,
            'shortlink': SHORTLINK_URL,
            'shortlink_api': SHORTLINK_API,
            'shortlink2': SHORTLINK_URL2,
            'shortlink_api2': SHORTLINK_API2,  
            'log_channel': VERIFY_LOG,
            'fsub': AUTH_CHANNEL,
            'caption': CUSTOM_FILE_CAPTION,
            'welcome_text': WELCOME_TEXT,
            'verify_short': ALL_SHORT_LINK_OFF,
            'is_tutorial': IS_TUTORIAL
        }
        chat = await self.grp.find_one({'id':int(id)})
        if chat:
            return chat.get('settings', default)
        return default
    
    async def disable_chat(self, chat, reason="No Reason"):
        chat_status=dict(
            is_disabled=True,
            reason=reason,
            )
        await self.grp.update_one({'id': int(chat)}, {'$set': {'chat_status': chat_status}})  

    async def total_chat_count(self):
        count = await self.grp.count_documents({})
        return count
    
    async def get_all_chats(self):
        return self.grp.find({})

    async def get_user(self, user_id):
        user_data = await self.users.find_one({"id": user_id})
        return user_data
    async def update_user(self, user_data):
        await self.users.update_one({"id": user_data["id"]}, {"$set": user_data}, upsert=True)

    async def has_premium_access(self, user_id):
        user_data = await self.get_user(user_id)
        if user_data:
            expiry_time = user_data.get("expiry_time")
            if expiry_time is None:
                # User previously used the free trial, but it has ended.
                return False
            elif isinstance(expiry_time, datetime.datetime) and datetime.datetime.now() <= expiry_time:
                return True
            else:
                await self.users.update_one({"id": user_id}, {"$set": {"expiry_time": None}})
        return False
        
    async def update_user(self, user_data):
        await self.users.update_one({"id": user_data["id"]}, {"$set": user_data}, upsert=True)

    async def update_one(self, filter_query, update_data):
        try:
            # Assuming self.client and self.users are set up properly
            result = await self.users.update_one(filter_query, update_data)
            return result.matched_count == 1
        except Exception as e:
            print(f"Error updating document: {e}")
            return False


    async def get_grp_info(self, group_id: int):
        g = await self.grp.find_one({'id': group_id})
        if not g:
            await self.add_chat(group_id, "Custom Group")
            
        return await self.grp.find_one({"id": group_id}) or {}

    async def get_group_info(self, group_id):
        return await self.get_grp_info(group_id)

    async def update_group(self, group_id, value):
        g = await self.grp.find_one({'id': group_id})
        if not g:
            await self.add_chat(group_id, "Custom Group")

        await self.grp.update_one({'id': group_id}, {'$set': value}, upsert=True)
    

    
    async def get_expired(self, current_time):
        expired_users = []
        if data := self.users.find({"expiry_time": {"$lt": current_time}}):
            async for user in data:
                expired_users.append(user)
        return expired_users

    async def remove_premium_access(self, user_id):
        return await self.update_one(
            {"id": user_id}, {"$set": {"expiry_time": None}}
        )

    async def get_db_size(self):
        return (await self.db.command("dbstats"))['dataSize']

    async def get_notcopy_user(self, user_id):
        user_id = int(user_id)

        user = await self.misc.find_one({"user_id": user_id})
        ist_timezone = pytz.timezone('Asia/Kolkata')

        if not user:
            res = {
                "user_id": user_id,
                "last_verified": datetime.datetime(2020, 5, 17, 0, 0, 0, tzinfo=ist_timezone),
                "second_time_verified": datetime.datetime(2019, 5, 17, 0, 0, 0, tzinfo=ist_timezone),
            }

            user = await self.misc.insert_one(res)

        return user

    async def update_notcopy_user(self, user_id, value:dict):
        user_id = int(user_id)
        myquery = {"user_id": user_id}
        newvalues = {"$set": value}
        return await self.misc.update_one(myquery, newvalues)

    async def is_user_verified(self, user_id):
        """
        The user object is retrieved using the get_notcopy_user() method, which takes a user_id as an argument and returns a user object containing information about the user.
        The pastDate variable is set to the value of the last_verified field in the user object. If this field is not present in the user object, an Exception is raised and the user object is retrieved again using the get_notcopy_user() method.
        The ist_timezone variable is set to the time zone for India Standard Time.
        The pastDate variable is converted to the India Standard Time time zone using the .astimezone() method.
        The current_time variable is set to the current time in the India Standard Time time zone using the datetime.now() method.
        The seconds_since_midnight variable is set to the total number of seconds since midnight of the current day in the India Standard Time time zone. This is calculated by taking the difference between the current time and a datetime instance representing midnight of the current day in the India Standard Time time zone.
        The time_diff variable is set to the difference between the current_time and the pastDate variables. This is a timedelta instance representing the amount of time that has elapsed between the two times.
        The total_seconds variable is set to the total number of seconds represented by the time_diff timedelta instance. This is calculated using the .total_seconds() method.
        The code returns True if the total_seconds is less than or equal to the seconds_since_midnight, and False otherwise. This indicates whether the pastDate time is within the same day as the current time.

        :param user_id: The user's ID
        :return: The number of seconds since the user was last verified.
        """
        user = await self.get_notcopy_user(user_id)

        try:
            pastDate = user["last_verified"]
        except Exception:
            user = await self.get_notcopy_user(user_id)
            pastDate = user["last_verified"]

        ist_timezone = pytz.timezone('Asia/Kolkata')
        pastDate = pastDate.astimezone(ist_timezone)
        current_time = datetime.datetime.now(tz=ist_timezone)

        seconds_since_midnight = (current_time - datetime.datetime(current_time.year, current_time.month, current_time.day, 0, 0, 0, tzinfo=ist_timezone)).total_seconds()

        # Calculate the difference between the two times
        time_diff = current_time - pastDate

        # Get the total number of seconds between the two times
        total_seconds = time_diff.total_seconds()
        return total_seconds <= seconds_since_midnight

    async def use_second_shortener(self, user_id, grp_id): 
        group = await self.get_group_info(int(grp_id))
        status = group.get('verify2')
        if status==False:        
            user = await self.get_notcopy_user(user_id)
            if not user.get("second_time_verified"):
                ist_timezone = pytz.timezone('Asia/Kolkata')
                await self.update_notcopy_user(user_id, {"second_time_verified":datetime.datetime(2019, 5, 17, 0, 0, 0, tzinfo=ist_timezone)})
                user = await self.get_notcopy_user(user_id)

            if await self.is_user_verified(user_id):

                try:
                    pastDate = user["last_verified"]
                except Exception:
                    user = await self.get_notcopy_user(user_id)
                    pastDate = user["last_verified"]

                ist_timezone = pytz.timezone('Asia/Kolkata')
                pastDate = pastDate.astimezone(ist_timezone)
                current_time = datetime.datetime.now(tz=ist_timezone)
                time_difference = current_time - pastDate
                if time_difference > datetime.timedelta(seconds=14400):
                    pastDate = user["last_verified"].astimezone(ist_timezone)
                    second_time = user["second_time_verified"].astimezone(ist_timezone)
                    return second_time < pastDate

            return False 
        else:
            return False 

    async def create_verify_id(self, user_id: int, hash):
        res = {"user_id": user_id, "hash":hash, "verified":False}
        return await self.verify_id.insert_one(res)

    async def get_verify_id_info(self, user_id: int, hash):
        return await self.verify_id.find_one({"user_id": user_id, "hash": hash})
    
    async def update_verify_id_info(self, user_id, hash, value: dict):
        myquery = {"user_id": user_id, "hash": hash}
        newvalues = { "$set": value }
        return await self.verify_id.update_one(myquery, newvalues)


db = Database(DATABASE_URI, DATABASE_NAME)
