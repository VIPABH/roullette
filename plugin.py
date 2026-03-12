from shortcut import *
from ABH import *
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
        if channels: 
            results = await asyncio.gather(
                *(is_in_channel(uid, ch) for ch in channels)
            )
            check_buttons = []
            for (ch_name, link) in zip(channels.items(), results):
                joined = is_in_channel(uid, ch_name)
                print(ch_name, link, joined)
                if not joined:
                    check_buttons.append([Button.url(f"اشترك في {ch_name}", link)])            
            if check_buttons:
                check_buttons.append([Button.inline("تحقق من الاشتراك ✅", data="check_again")])
                await e.reply(
                    "🔐 للوصول إلى خدمات البوت، يجب الاشتراك في القنوات التالية أولاً:",
                    buttons=check_buttons
                )
                return
        await e.reply(f"✅ أهلاً بك يا {ment}\nتم التحقق من اشتراكك، يمكنك الآن استخدام البوت!")
