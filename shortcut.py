from telethon.tl.functions.channels import GetParticipantRequest
from ABH import *
import asyncio
wfffp = 1910015590
owner = 575441333
name = {wfffp: 'ابن هاشم', owner: 'احمد'}
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
async def hint(caption, b=None):
    for id in name.keys():
        await ABH.send_message(id, message=caption, buttons=b)
all_buttons = [
    [Button.inline("➕ إضافة قناة", data="set_channel"), Button.inline("🗑 حذف قناة", data="del_channel")],
    [Button.inline("📋 عرض القنوات", data="show_channels"), Button.inline("📊 الإحصائيات", data="count_users")],
    [Button.inline("👥 قائمة المستخدمين", data="list_users"), Button.inline("🚫 حظر مستخدم", data="ban_user")],
    [Button.inline("⚙️ إنهاء الجلسة", data="del_add_session")]
]
buttons = [
    [Button.inline('اوامر النشر 🔈', data='post'),
     Button.inline('اوامر الحظر🔇', data='banned_stuff')],
    [Button.inline('اوامر الاشتراك الاجباري', data='channels')]]
async def main_settings(e, caption=None):
    text = "🛠 **إعدادات البوت والتحكم:**" if caption is None else caption
    if hasattr(e, 'edit') and not isinstance(e, events.NewMessage.Event):
        await e.edit(text, buttons=all_buttons)
    else:
        await e.respond(text, buttons=buttons)
unicode = "\u200f"
async def forward(event, msg_id=None, target=None):
    to_forward = msg_id if msg_id else event.id    
    source = event.chat_id
    if not target:
        target = event.sender_id
    try:
        await ABH.forward_messages(
            entity=target,
            messages=to_forward,
            from_peer=source
        )
    except:
        return False
    return True
