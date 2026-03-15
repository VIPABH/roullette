from telethon.errors import ChatAdminRequiredError
from telethon.errors import ChatAdminRequiredError
from telethon import events, Button
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
        channels = r.smembers(FORCED_KEY)
        if not channels:
            return await e.answer("⚠️ لا توجد قنوات مضافة لحذفها", alert=True)        
        buttons = []
        for ch in channels:
            ch_id = ch.decode("utf-8") if isinstance(ch, bytes) else str(ch)
            buttons.append([Button.inline(f"❌ حذف: {ch_id}", data=f"remove_{ch_id}")])
        buttons.append([Button.inline("⬅️ رجوع", data="back_to_settings")]) # اختياري
        await e.edit("🗑 اختر القناة التي تريد حذفها من القائمة:", buttons=buttons)
    elif data.startswith("remove_"):
        channel_to_del = data.replace("remove_", "")
        r.srem(FORCED_KEY, channel_to_del)
        await e.answer(f"✅ تم حذف القناة {channel_to_del}", alert=True)        
        await settings(e) 
    elif data == "show_channels":
        channels = r.smembers(FORCED_KEY)
        if not channels:
            return await e.edit("لا توجد قنوات مضافة حالياً.")
        text = "📌 قنوات الاشتراك الإجباري:\n\n"
        for ch in channels:
            ch_id = ch.decode("utf-8") if isinstance(ch, bytes) else str(ch)
            text += f"• `{ch_id}`\n"
        await e.edit(text, buttons=[Button.inline("⬅️ رجوع", data="back_to_settings")])
    elif data == "count_users":
        count = r.scard('save_users')
        await e.answer(f"عدد المستخدمين: {count}", alert=True)
    elif data == "del_add_session":
        r.hdel(STATE_KEY, e.sender_id)
        await e.edit("✅ تم حذف الجلسة")
STATE_KEY = "channels"
FORCED_KEY = "forced_channels"
@ABH.on(events.NewMessage)
async def channel_handler(e):
    state = r.hget(STATE_KEY, e.sender_id)
    if not state:
        return
    b = Button.inline('حذف الجلسة', data='del_add_session')
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
        return await e.reply("❌ تأكد من إدخال يوزر أو ايدي صحيح", buttons=b)
    if state == "add_channel":
        r.sadd(FORCED_KEY, str(entity.id))
        await e.reply("✅ تم إضافة القناة إلى الاشتراك الإجباري")
        r.hdel(STATE_KEY, e.sender_id)
    elif state == "del_channel":
        r.srem(FORCED_KEY, str(entity.id))
        await e.reply("❌ تم حذف القناة من الاشتراك الإجباري")
        r.hdel(STATE_KEY, e.sender_id)
