from shortcut import *
from الاعدادات import *
from ABH import *
from النشر import *
import asyncio
@ABH.on(events.NewMessage(pattern="^/start$"))
async def start(e):
    if not e.is_private:
        return
    # if r.sismember(BANNED_KEY, str(e.sender_id)):
    #     return 
    uid = e.sender_id
    ment = mention(e)
    if uid in name: 
        caption = f'اهلا عزيزي ({ment})، أنت حالياً في واجهة الآدمن. ماذا تريد أن تفعل؟ 👇🏾'
        await main_settings(e, caption)
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
