from telethon.tl.functions.messages import ExportChatInviteRequest
from التخزين import *
from shortcut import *
from ABH import *
async def sign_users(e):
    if e.is_private:
        user_id = e.sender_id
        b = Button.url(
            "بروفايلة",
            f"tg://user?id={user_id}"
        )
        caption = f"""
تم تفعيل البوت بواسطة
المستخدم {mention(e)}
ايديه `{user_id}`
"""
    else:
        if e.chat.username:
            group_link = f"https://t.me/{e.chat.username}"
        else:
            group = await e.client.get_entity(e.chat_id)
            full = await e.client(ExportChatInviteRequest(
                peer=group
            ))
            group_link = full.link
        b = Button.url("رابط المجموعة", group_link)
        caption = f"""
تم تشغيل البوت داخل المجموعة
{e.chat.title}
ايدي المجموعة `{e.chat_id}`
"""
    data = load_data()
    if e.chat_id not in data:
        save_data(e.chat_id)
        await hint(caption, buttons=[[b]])
