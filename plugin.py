from shortcut import *
from ABH import *
from النشر import *
import asyncio
channels = r.get("forced_channels")
@ABH.on(events.NewMessage(pattern="^/start$"))
async def start(e):
    if not e.is_private:
        return
    uid = e.sender_id
    ment = await mention(e)
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
            await e.reply(f"اهلا اخي ( {await mention(e)} ) حياك الله \n اني ميكارو مساعدك المجاني في بوابة الذكاء الصناعي\n تكدر تستخدمني بالكروبات وبالخاص شوكت ما تحتاج شيء راح تلكاني يمك \n \help")
            users = load_data()
            if str(e.sender_id) not in users:
                await sign_users(e)
@ABH.on(events.NewMessage(pattern="^/help$"))
async def help(e):
    await e.reply(f"""
اهلا صديقي ( {await mention(e)} )
اوامر البوت كآلاتي
1 ↔ {unicode}/start لتفعيل البوت بالطريقة الصحيحه
2 ↔ `تسجيل الدخول` للوصول الى معلوماتك في البوت
3 ↔ `اوامر الذكاء` ل استعراض كل الاوامر التي يمكنك استخدامها في البوت
""")
