from telethon import events, Button
from shortcut import *
from ABH import *
STATE_KEY = "channels"
FORCED_KEY = "forced_channels"
BANNED_KEY = "banned_users"
USERS_KEY = "save_users"
@ABH.on(events.CallbackQuery)
async def settings_callback(e):
    data = e.data.decode("utf-8")
    if data == "del_add_session":
        r.hdel(STATE_KEY, e.sender_id)
        await e.edit("✅ تم إنهاء الجلسة.", buttons=[Button.inline("⬅️ القائمة الرئيسية", data="back_to_settings")])
    if not isprof(e.sender_id):
        return await e.answer("ليس لك صلاحية", alert=True)
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
        users = list(r.smembers(USERS_KEY))
        if not users:
            return await e.answer("⚠️ لا يوجد مستخدمين", alert=True)
        await e.answer("🔄 جاري جلب البيانات...")        
        for i in range(0, len(users), 20):
            chunk = users[i:i + 20]
            mentions = await ment(chunk)
            lines = []
            for idx, user_mention in enumerate(mentions):
                u_id = chunk[idx]
                lines.append(f"{i + idx + 1}- ( {user_mention} ) -- ( `{u_id}` )")
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
    elif data == 'post':
        count = r.scard(USERS_KEY)
        b = [
            Button.inline(f'عدد المستخدمين ( {count} )🧮', data='count_users'),
            Button.inline(f'قائمة المستخدمين🧑‍🤝‍🧑', data='list_users'),
             ]
        await e.edit('قائمة النشر والاعضاء', buttons=b)
    elif data == 'banned_stuff':
        b = [
            Button.inline('حظر عضو⛔', data='ban_user'),
            Button.inline('الغاء حظر عضو❗', data='unban_user'),
            Button.inline('المحظورين', data='banned'),
            ]
        await e.edit('قائمة الحظر والمحظورين', buttons=b)
b = Button.inline("حذف الجلسة", data="del_add_session")
@ABH.on(events.NewMessage)
async def inputs_handler(e):
    if r.sismember(BANNED_KEY, str(e.sender_id)):
        await e.reply("⚠️ لا يمكنك استخدام البوت حالياً.")
        raise events.StopPropagation 
    raw_state = r.hget(STATE_KEY, e.sender_id)
    if not raw_state: 
        return
    state = raw_state.decode("utf-8") if isinstance(raw_state, bytes) else raw_state
    user_input = e.text.strip()
    if state == "step_ban":
        if user_input.isdigit():
            r.sadd(BANNED_KEY, user_input)
            await e.reply(f"✅ تم حظر المستخدم `{user_input}` بنجاح.")
            r.hdel(STATE_KEY, e.sender_id)
        else:
            await e.reply("⚠️ يرجى إرسال ID صحيح (أرقام فقط).")
    elif state == "add_channel":
            channel_input = e.text.strip()
            if channel_input.replace('-', '').isdigit():
                target = int(channel_input)
            else:
                target = channel_input 
            try:
                entity = await ABH.get_entity(target)
                me = await ABH.get_me()            
                permissions = await ABH.get_permissions(entity, me)
                if not permissions.is_admin:
                    return await e.reply("❌ البوت ليس مشرفاً في هذه القناة.")
                r.sadd(FORCED_KEY, str(entity.id))
                await e.reply(f"✅ تم الإضافة: {entity.title}")
                r.hdel(STATE_KEY, e.sender_id)
            except Exception as ex:
                await e.reply(f"❌ فشل العثور على القناة.\nتأكد من معرف القناة (Username) أو الـ ID الصحيح.\nالخطأ: `{str(ex)}`")
                r.hdel(STATE_KEY, e.sender_id)
