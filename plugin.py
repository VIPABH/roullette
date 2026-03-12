from shortcut import *
from ABH import *
import asyncio
@ABH.on(events.NewMessage(pattern="^/start$"))
async def start(e):
    if not e.is_private:
        return
    uid = e.sender_id
    ment = mention(e)
    if id in name:
        b =[Button.inline("تعيين قناة اشتراك اجباري", data=f"set_channel"), 
            Button.inline("حذف قناة اشتراك اجباري", data=f"del_channel"), 
            Button.inline('عرض قنوات الاشتراك الاجباري', data=f"show_channels"), 
            Button.inline('عدد مستخدمين البوت', data=f"count_users"),
            Button.inline('الاعدادات', data='settings'),
            ]
        caption = f'اهلا عزيزي( {ment} ) انت حاليا ب واجهه الادمن , شنو تحب تسوي 👇🏾👇🏾'
    else:
        results = await asyncio.gather(
            *(is_in_channel(uid, ch) for ch in channels)
        )
        buttons = []
        for (ch, link), joined in zip(channels.items(), results):
            if not joined:
                buttons.append([Button.url(f"اشترك في {ch}", link)])
        if buttons:
            await e.reply(
                "🔐 للوصول إلى خدمات البوت يجب الاشتراك في القنوات التالية:",
                buttons=buttons
            )
        else:
            await e.reply("✅ تم التحقق من اشتراكك في جميع القنوات. أهلاً بك!")
