from telethon.tl.functions.channels import GetParticipantRequest
from ABH import *
import asyncio
# wfffp = 1910015590
owner = 575441333
name = {wfffp: 'ابن هاشم', owner: 'احمد'}
name = { owner: 'احمد'}
can = lambda user_id: user_id in r.smembers("save_users")
isprof = lambda user_id: user_id in (wfffp, owner)
async def mention(entity):
    try:
        if hasattr(entity, 'sender') and entity.sender:
            user = entity.sender
        elif hasattr(entity, 'sender_id') and entity.sender_id:
            user = await ABH.get_entity(entity.sender_id)
        else:
            user = await ABH.get_entity(int(entity))        
        if user:
            name = getattr(user, 'first_name', "مستخدم")
            if not name or name.strip() == "":
                name = "مستخدم"
            return f"[{name}](tg://user?id={user.id})"
        return "مستخدم"
    except:
        return "مستخدم"
async def ment(ids_list: list):
    tasks = [mention(u) for u in ids_list]
    return await asyncio.gather(*tasks)
async def is_in_channel(user_id, channel_username):
    try:
        return await ABH(GetParticipantRequest(channel_username, user_id))
    except:
        return False
channels = {
    "ANYMOUSupdate": "https://t.me/ANYMOUSupdate",
    "x04ou": "https://t.me/x04ou"
}
async def hint(caption, b=None):
    return await ABH.send_message(wfffp, message=caption, buttons=b)
async def main_settings(e, caption=None):
    buttons = [
        [Button.inline("➕ إضافة قناة", data="set_channel"), Button.inline("🗑 حذف قناة", data="del_channel")],
        [Button.inline("📋 عرض القنوات", data="show_channels"), Button.inline("📊 الإحصائيات", data="count_users")],
        [Button.inline("👥 قائمة المستخدمين", data="list_users"), Button.inline("🚫 حظر مستخدم", data="ban_user")],
        [Button.inline("⚙️ إنهاء الجلسة", data="del_add_session")]
    ]
    text = "🛠 **إعدادات البوت والتحكم:**" if caption is None else caption
    if hasattr(e, 'edit') and not isinstance(e, events.NewMessage.Event):
        await e.edit(text, buttons=buttons)
    else:
        await e.respond(text, buttons=buttons)
unicode = "\u200f"
