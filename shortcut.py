from telethon import events, Button
from shortcut import *
from ABH import *
STATE_KEY = "channels"
FORCED_KEY = "forced_channels"
BANNED_KEY = "banned_users"
USERS_KEY = "save_users"
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
@ABH.on(events.CallbackQuery)
async def settings_callback(e):
    if not can(e.sender_id):
        return await e.answer("ليس لك صلاحية", alert=True)
    data = e.data.decode("utf-8")
    if data == "back_to_settings":
        await main_settings(e)
    elif data == "set_channel":
        r.hset(STATE_KEY, e.sender_id, "add_channel")
        await e.edit("📥 أرسل الآن ايدي أو يوزر القناة", buttons=[Button.inline("⬅️ إلغاء", data="back_to_settings")])
    elif data == "show_channels":
        channels = r.smembers(FORCED_KEY)
        if not channels:
            return await e.answer("⚠️ لا توجد قنوات.", alert=True)
        text = "📌 القنوات:\n" + "\n".join([f"`{ch}`" for ch in channels])
        await e.edit(text, buttons=[Button.inline("⬅️ عودة", data="back_to_settings")])
    elif data == "del_channel":
        channels = r.smembers(FORCED_KEY)
        if not channels:
            return await e.answer("⚠️ لا توجد قنوات حالياً", alert=True)
        buttons = []
        for ch in channels:
            ch_id = ch.decode("utf-8") if isinstance(ch, bytes) else str(ch)
            buttons.append([Button.inline(f"❌ حذف: {ch_id}", data=f"remove_{ch_id}")])
        buttons.append([Button.inline("⬅️ عودة", data="back_to_settings")])
        await e.edit("🗑 اختر القناة لحذفها:", buttons=buttons)
    elif data.startswith("remove_"):
        ch_id = data.replace("remove_", "")
        r.srem(FORCED_KEY, ch_id)
        await e.answer(f"✅ تم حذف {ch_id}", alert=True)
        await main_settings(e) 
    elif data == "list_users":
        users = r.smembers(USERS_KEY)
        if not users:
            return await e.answer("⚠️ لا يوجد مستخدمين مخزنين", alert=True)
        await e.answer("🔄 جاري تحضير القائمة...")
        all_users = list(users)
        for i in range(0, len(all_users), 20):
            chunk = all_users[i:i + 20]
            lines = []
            num = i + 1
            for u in chunk:
                user_link = await mention(u) 
                lines.append(f"{num}- ( {user_link} ) -- ( `{u}` )")
                num += 1
            msg = "👥 **قائمة المستخدمين:**\n\n" + "\n".join(lines)
            if i == 0:
                await e.edit(msg, buttons=[Button.inline("⬅️ عودة", data="back_to_settings")])
            else:
                await e.respond(msg)
    elif data == "ban_user":
        r.hset(STATE_KEY, e.sender_id, "step_ban")
        await e.edit("🚫 أرسل الآن ID الشخص المراد حظره من البوت:", buttons=[Button.inline("⬅️ إلغاء", data="back_to_settings")])
    elif data == "count_users":
        count = r.scard(USERS_KEY)
        await e.answer(f"📊 إجمالي المستخدمين: {count}", alert=True)
    elif data == "del_add_session":
        r.hdel(STATE_KEY, e.sender_id)
        await e.edit("✅ تم إنهاء الجلسة.", buttons=[Button.inline("⬅️ القائمة الرئيسية", data="back_to_settings")])
@ABH.on(events.NewMessage)
async def inputs_handler(e):
    if r.sismember(BANNED_KEY, str(e.sender_id)):
        return 
    state = r.hget(STATE_KEY, e.sender_id)
    if not state: return
    state = state.decode("utf-8") if isinstance(state, bytes) else state
    if state == "step_ban":
        user_id = e.text.strip()
        if user_id.isdigit():
            r.sadd(BANNED_KEY, user_id)
            await e.reply(f"✅ تم حظر المستخدم `{user_id}` بنجاح.")
            r.hdel(STATE_KEY, e.sender_id)
        else:
            await e.reply("⚠️ يرجى إرسال ID صحيح (أرقام فقط).")
    elif state == "add_channel":
        channel = e.text.strip()
        try:
            entity = await ABH.get_entity(channel)
            r.sadd(FORCED_KEY, str(entity.id))
            await e.reply(f"✅ تم إضافة القناة `{entity.id}`")
            r.hdel(STATE_KEY, e.sender_id)
        except Exception as ex:
            await e.reply(f"❌ خطأ: {str(ex)}")
