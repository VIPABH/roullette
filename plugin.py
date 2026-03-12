from shortcut import *
from ABH import *
import asyncio
@ABH.on(events.NewMessage(pattern="^/start$"))
async def start(e):
    if not e.is_private:
        return
    uid = e.sender_id
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
