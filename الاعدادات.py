from telethon import events, Button
from telethon.tl.functions.channels import GetParticipantRequest
from telethon.errors import ChatAdminRequiredError
from shortcut import *
from ABH import *
@ABH.on(events.CallbackQuery)
async def settings(e):
    if not can(e.sender_id):
        return await e.answer("ليس لك صلاحية", alert=True)
    data = e.data.decode("utf-8")
    if data == "set_channel":
        r.hset(STATE_KEY, e.sender_id, "add_channel")
        await e.edit("📥 أرسل الآن ايدي أو يوزر القناة")
    elif data == "del_channel":
        r.hset(STATE_KEY, e.sender_id, "del_channel")
        await e.edit("📤 أرسل الآن ايدي أو يوزر القناة")
    elif data == "show_channels":
        channels = r.smembers(FORCED_KEY)
        if not channels:
            return await e.edit("لا توجد قنوات مضافة حالياً.")
        text = "📌 قنوات الاشتراك الإجباري:\n\n"
        for ch in channels:
            text += f"• `{ch}`\n"
        await e.edit(text)
    elif data == "count_users":
        count = r.scard(USERS_KEY)
        await e.answer(f"عدد المستخدمين: {count}", alert=True)
STATE_KEY = "channels"
FORCED_KEY = "forced_channels"
USERS_KEY = "users"
@ABH.on(events.NewMessage)
async def channel_handler(e):
    r.delete(USERS_KEY)
    state = r.hget(STATE_KEY, e.sender_id)
    if not state:
        return
    channel = e.text.strip()
    try:
        entity = await ABH.get_entity(channel)
        me = await ABH.get_me()
        perms = await ABH.get_permissions(entity, me)
        if not perms.is_admin:
            return await e.reply("❌ يجب أن يكون البوت مشرف داخل القناة أولاً")
    except ChatAdminRequiredError:
        return await e.reply("❌ البوت ليس لديه صلاحيات داخل القناة")
    except Exception:
        return await e.reply("❌ تأكد من إدخال يوزر أو ايدي صحيح")
    if state == "add_channel":
        r.sadd(FORCED_KEY, str(entity.id))
        await e.reply("✅ تم إضافة القناة إلى الاشتراك الإجباري")
        r.hdel(STATE_KEY, e.sender_id)
    elif state == "del_channel":
        r.srem(FORCED_KEY, str(entity.id))
        await e.reply("❌ تم حذف القناة من الاشتراك الإجباري")
        r.hdel(STATE_KEY, e.sender_id)
