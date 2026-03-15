from telethon.tl.functions.channels import GetParticipantRequest
from ABH import *
wfffp = 1910015590
owner = 7941637237
name = {wfffp: 'ابن هاشم', owner: 'ابراهيم'}
can = lambda user_id: user_id in [wfffp, owner]
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
