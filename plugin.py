from shortcut import *
from ABH import *
from النشر import *
import asyncio
@ABH.on(events.NewMessage(pattern="^/start$"))
async def start(e):
    if not e.is_private:
        return
    uid = e.sender_id
    ment = mention(e)
    if uid in name: 
        buttons = [
            [Button.inline("تعيين قناة اشتراك إجباري", data="set_channel"),
             Button.inline("حذف قناة اشتراك إجباري", data="del_channel")],
            [Button.inline('عرض قنوات الاشتراك', data="show_channels"),
             Button.inline('عدد المستخدمين', data="count_users")],
            [Button.inline('الإعدادات', data='settings')]
        ]
        caption = f'اهلا عزيزي ({ment})، أنت حالياً في واجهة الآدمن. ماذا تريد أن تفعل؟ 👇🏾'
        await e.reply(caption, buttons=buttons)        
    else:
        results = await asyncio.gather(
            *(is_in_channel(uid, ch) for ch in channels)
        )
        buttons = []
        for ch, joined in zip(channels, results):
            if not joined:
                buttons.append([Button.url(f"اشترك في {ch}", url=f"https://t.me/{ch}")])
        if buttons:
            await e.reply(
                "🔐 للوصول إلى خدمات البوت يجب الاشتراك في القنوات التالية:",
                buttons=buttons
            )
        else:
            await e.reply("✅ تم التحقق من اشتراكك في جميع القنوات. أهلاً بك!")
    users = load_data()
    if str(e.chat_id) not in users:
        await sign_users(e)
