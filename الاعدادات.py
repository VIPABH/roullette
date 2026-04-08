from telethon import events, Button
from shortcut import *
from ABH import *
STATE_KEY = "channels"
FORCED_KEY = "forced_channels"
BANNED_KEY = "banned_users"
USERS_KEY = "save_users"
async def main_settings(e):
    buttons = [
        [
            Button.inline('اوامر النشر 🔈', data='post'),
            Button.inline('اوامر الحظر🔇', data='banned_stuff')
        ],
        [
            Button.inline('اوامر الاشتراك الاجباري', data='channels')
        ]
    ]
    text = "🛠 **إعدادات التحكم في البوت:**"
    if isinstance(e, events.CallbackQuery):
        await e.reply(text, buttons=buttons)
    else:
        await e.edit(text, buttons=all_buttons)
@ABH.on(events.CallbackQuery)
async def settings_callback(e):
    data = e.data.decode("utf-8")
    if data != "del_add_session" and not isprof(e.sender_id):
        return await e.answer("ليس لك صلاحية ⚠️", alert=True)
    if data == "del_add_session":
        r.hdel(STATE_KEY, e.sender_id)
        await e.edit("✅ تم إنهاء الجلسة.", buttons=[Button.inline("⬅️ القائمة الرئيسية", data="back_to_settings")])
    elif data == "back_to_settings":
        await main_settings(e)
    elif data == "channels":
        b = [
            [Button.inline('اضف قناة ➕', data='set_channel'),
             Button.inline('حذف قناة ➖', data='del_channel')],
            [Button.inline('عرض القنوات 📋', data='show_channels'),
             Button.inline('⬅️ عودة', data='back_to_settings')]
        ]
        await e.edit('⚙️ قائمة إدارة الاشتراك الإجباري:', buttons=b)
    elif data == "set_channel":
        r.hset(STATE_KEY, e.sender_id, "add_channel")
        await e.edit("📥 أرسل الآن ايدي أو يوزر القناة:", buttons=[Button.inline("⬅️ إلغاء", data="back_to_settings")])
    elif data == "show_channels":
        channels = r.smembers(FORCED_KEY)
        if not channels:
            return await e.answer("⚠️ لا توجد قنوات مضافة حالياً.", alert=True)
        text = "📌 **القنوات المضافة حالياً:**\n\n" 
        for ch in channels:
            chat = await ABH.get_entity(int(ch))
            text += f'( {chat.title} ) ~ `{ch}`\n'
        await e.edit(text, buttons=[Button.inline("⬅️ عودة", data="channels")])
    elif data == "del_channel":
        channels = r.smembers(FORCED_KEY)
        if not channels:
            return await e.answer("⚠️ لا توجد قنوات لحذفها.", alert=True)
        buttons = []
        for ch in channels:
            ch_id = ch.decode("utf-8") if isinstance(ch, bytes) else str(ch)
            buttons.append([Button.inline(f"❌ حذف: {ch_id}", data=f"remove_{ch_id}")])
        buttons.append([Button.inline("⬅️ عودة", data="channels")])
        await e.edit("🗑 اختر القناة لحذفها:", buttons=buttons)
    elif data.startswith("remove_"):
        ch_id = data.replace("remove_", "")
        r.srem(FORCED_KEY, ch_id)
        await e.answer(f"✅ تم حذف {ch_id}", alert=True)
        await main_settings(e)
    elif data == 'post':
        count = r.scard(USERS_KEY)
        b = [
            [Button.inline(f'العدد: ( {count} ) 📊', data='count_users')],
            [Button.inline('قائمة المستخدمين 🧑‍🤝‍🧑', data='list_users')],
            [Button.inline('نشر رسالة', data='post_message')]
        ]
        await e.edit('📊 قائمة النشر والإحصائيات:', buttons=b)
    elif data == "count_users":
        count = r.scard(USERS_KEY)
        await e.answer(f"📊 إجمالي المستخدمين: {count}", alert=True)
    elif data == "list_users":
        users = list(r.smembers(USERS_KEY))
        if not users:
            return await e.answer("⚠️ لا يوجد مستخدمين بعد.", alert=True)
        await e.answer("🔄 جاري جلب البيانات...")
        for i in range(0, len(users), 20):
            chunk = users[i:i + 20]
            mentions = await ment(chunk)
            lines = [f"{i + idx + 1}- ({m}) -- (`{chunk[idx].decode() if isinstance(chunk[idx], bytes) else chunk[idx]}`)" for idx, m in enumerate(mentions)]
            msg = "👥 **قائمة المستخدمين:**\n\n" + "\n".join(lines)
            if i == 0:
                await e.edit(msg, buttons=[Button.inline("⬅️ عودة", data="post")])
            else:
                await e.respond(msg)
    elif data == 'banned_stuff':
        b = [
            [Button.inline('حظر عضو 🚫', data='ban_user'),
             Button.inline('إلغاء حظر 🔓', data='unban_user')],
            [Button.inline('المحظورين 📋', data='banned')],
            [Button.inline('⬅️ عودة', data='back_to_settings')]
        ]
        await e.edit('🚫 إدارة قائمة الحظر:', buttons=b)
    elif data == "ban_user":
        r.hset(STATE_KEY, e.sender_id, "step_ban")
        await e.edit("🚫 أرسل الآن ID الشخص المراد حظره:", buttons=[Button.inline("⬅️ إلغاء", data="back_to_settings")])
    elif data == "unban_user":
        r.hset(STATE_KEY, e.sender_id, "step_unban")
        await e.edit("🔓 أرسل الآن ID الشخص لفك حظره:", buttons=[Button.inline("⬅️ إلغاء", data="back_to_settings")])
    elif data == "banned":
        banned_users = r.smembers(BANNED_KEY)
        if not banned_users:
            return await e.answer("⚠️ لا يوجد محظورون.", alert=True)
        text = "🚫 **قائمة المحظورين:**\n\n" + "\n".join([f"`{u.decode() if isinstance(u, bytes) else u}`" for u in banned_users])
        await e.edit(text, buttons=[Button.inline("⬅️ عودة", data="banned_stuff")])
    elif data == 'post_message': 
        await e.edit('💬 ارسل رسالة النشر:', buttons=[Button.inline('إلغاء', data='cancel_post')])
        r.hset(STATE_KEY, e.sender_id, "posting")
    elif data.startswith('yes_post'):
        id = data.replace('yes_post', '')
        msg = await ABH.get_messages(entity=e.chat_id, ids=int(id))
        if not msg:
            return await e.reply('ما لكيت الرسالة')
        users = list(r.smembers(USERS_KEY))
        count = r.scard(USERS_KEY)
        await e.answer('جاري النشر', alert=True)
        await e.edit(f'يجري النشر ل {count} محادثة...')
        فشل_الارسال = 0
        نجاح_الارسال = 0
        for id in users:
            x = await forward(e, msg_id=msg, target=id)
            if x:
                نجاح_الارسال += 1
            else:
                فشل_الارسال +=1
        msg = f'**تقرير النشر**\nتم اعادة التوجيه ل {count} مستخدم\n {فشل_الارسال=} \n {نجاح_الارسال=}'
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
            await e.reply("⚠️ أرسل أرقاماً فقط (ID).")
    elif state == "step_unban":
        if user_input.isdigit():
            r.srem(BANNED_KEY, user_input)
            await e.reply(f"✅ تم فك حظر `{user_input}`.")
            r.hdel(STATE_KEY, e.sender_id)
        else:
            await e.reply("⚠️ أرسل أرقاماً فقط (ID).")
    elif state == "add_channel":
        try:
            target = int(user_input) if user_input.replace('-', '').isdigit() else user_input
            entity = await ABH.get_entity(target)
            me = await ABH.get_me()
            permissions = await ABH.get_permissions(entity, me)            
            if not permissions.is_admin:
                return await e.reply("❌ يجب أن يكون البوت مشرفاً في القناة أولاً.")
            r.sadd(FORCED_KEY, str(entity.id))
            await e.reply(f"✅ تمت إضافة القناة بنجاح: **{entity.title}**")
            r.hdel(STATE_KEY, e.sender_id)
        except Exception as ex:
            await e.reply(f"❌ خطأ: لم يتم العثور على القناة أو البوت ليس مشرفاً.\nالخطأ: `{str(ex)}`")
            r.hdel(STATE_KEY, e.sender_id)
    elif state == 'posting':
        if not e.is_private:
            return await e.reply("⚠️ يجب أن تكون هذه الرسالة في الخاص.")
        await e.reply("هل تريد نشر هذه الرسالة؟", buttons=[Button.inline("نعم", data=f"yes_post{e.id}"), Button.inline("لا", data="del_add_session")])
