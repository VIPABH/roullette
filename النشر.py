from telethon.tl.functions.messages import ExportChatInviteRequest
from التخزين import *
from shortcut import *
from ABH import *
async def sign_users(e):
    if e.is_private:
        id = e.sender_id
        b = Button.url(
            "بروفايلة",
            f"tg://user?id={id}"
        )
        caption = f"""
تم تفعيل البوت بواسطة
المستخدم {await mention(e)}
ايديه `{id}`
"""
    else:
        if e.chat.username:
            group_link = f"https://t.me/{e.chat.username}"
        else:
            group = await e.client.get_entity(id)
            full = await e.client(ExportChatInviteRequest(
                peer=group
            ))
            group_link = full.link
        b = Button.url("رابط المجموعة", group_link)
        caption = f"""
تم تشغيل البوت داخل المجموعة
{e.chat.title}
ايدي المجموعة `{id}`
"""
    data = load_data()
    if str(id) not in data:
        save_data(id)
        await hint(caption, b)
