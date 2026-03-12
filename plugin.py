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
        notjoind_names = []
        buttons = []
        for ch in channels:
            link = channels[ch]            
            is_joined = await is_in_channel(uid, ch)            
            if not is_joined:
                notjoind_names.append(f"@{ch}") 
                buttons.append([Button.url(f"اضغط للاشتراك في {ch}", link)])
        if buttons:
            names_str = "، ".join(notjoind_names)
            caption = f"⚠️ عزيزي، أنت غير مشترك في القنوات التالية:\n{names_str}\n\nيرجى الاشتراك ثم الضغط على /start مرة أخرى."
            return await e.reply(caption, buttons=buttons)
        await e.reply(f"✅ أهلاً بك يا {ment}\nتم التحقق من اشتراكك، يمكنك الآن استخدام البوت!")
