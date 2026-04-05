from ABH import *
from telethon import Button, events
from datetime import datetime
from ddgs import DDGS
import httpx
def search_web(query):
    try:
        with DDGS() as ddgs:
            results = list(ddgs.text(query, max_results=3))
            if results:
                context = ""
                links = "\n\n**🌐 المصادر والنتائج المتقدمة:**"
                for i, r in enumerate(results, 1):
                    context += f"[{i}] {r['body']}\n"
                    links += f"\n{i}. [{r['title']}]({r['href']})"
                return context, links
    except:
        pass
    return "", ""
def search_youtube(query):
    try:
        with DDGS() as ddgs:
            results = list(ddgs.videos(f"site:youtube.com {query}", max_results=3))
            if results:
                context = ""
                for i, r in enumerate(results, 1):
                    context += f"فيديو {i}:\nالعنوان: {r['title']}\nالرابط: {r['content']}\nالوصف: {r.get('description', 'لا يوجد وصف')}\n\n"
                return context
    except:
        pass
    return ""
def search_tiktok(query):
    try:
        with DDGS() as ddgs:
            results = list(ddgs.text(f"site:tiktok.com {query}", max_results=3))
            if results:
                context = ""
                for i, r in enumerate(results, 1):
                    context += f"مقطع {i}:\nالعنوان: {r['title']}\nالرابط: {r['href']}\nالوصف: {r.get('body', 'لا يوجد وصف')}\n\n"
                return context
    except:
        pass
    return ""
AI_SECRET = "AIChatPowerBrain123@2024"
API_URL = "https://powerbrainai.com/app/backend/api/api.php"
async def ask_ai(q, web_info=None):
    current_date = datetime.now().strftime("%Y-%m-%d")
    system_instruction = (
        f"أنت ذكاء اصطناعي اسمك 'ميكارو'. "
        f"مطورك هو المبدع 'ابن هاشم'. "
        f"تتحدث باللهجة العراقية الودودة والذكية. "
        f"تاريخ اليوم هو {current_date}. "
        "عند الإجابة، كن مطلعاً على الأحداث الحديثة ودقيقاً جداً. "
        "إذا سألك أحد منو صنعك أو منو مطورك، جاوبه بفخر إنه 'ابن هاشم'."
    )
    full_prompt = q
    if web_info:
        full_prompt = f"المعلومات المجلوبة (حديثة):\n{web_info}\n\nالسؤال: {q}\nاجب بناءً على المعلومات أعلاه بلهجة عراقية."

    headers = {
        "User-Agent": "Dart/3.3 (dart:io)",
        "content-type": "application/json; charset=utf-8"
    }
    data = {
        "action": "send_message",
        "model": "gpt-4o-mini", 
        "secret_token": AI_SECRET,
        "messages": [
            {"role": "system", "content": system_instruction},
            {"role": "user", "content": full_prompt}
        ]
    }
    try:
        async with httpx.AsyncClient() as client:
            res = await client.post(API_URL, headers=headers, json=data, timeout=20.0)
            if res.status_code == 200:
                response_data = res.json().get("data", "")
                return response_data if response_data else "ماكو رد واضح من السيرفر، جرب مرة ثانية."
            return "السيرفر حالياً ثقيل، ثواني وارجع جرب."
    except Exception as e:
        return f"صار خطأ تقني: {str(e)}"
@ABH.on(events.NewMessage(pattern=r"^ميكارو(\s+.*|$)"))
async def bot_handler(event):
    user_q = event.pattern_match.group(1).strip()    
    if not user_q: return await event.reply("🙂")
    async with event.client.action(event.chat_id, "typing"):
        ai_res = await ask_ai(user_q)
        buttons = [Button.inline("🔍 بحث عميق بمصادر الويب", data=f"search_{event.id}")]
        await event.reply(ai_res, buttons=buttons)
@ABH.on(events.NewMessage(pattern=r"^يوتيوب(\s+.*|$)"))
async def youtube_handler(event):
    query = event.pattern_match.group(1).strip()
    if not query: return await event.reply("شنو تريد أبحثلك باليوتيوب؟")
    async with event.client.action(event.chat_id, "typing"):
        yt_context = search_youtube(query)
        if yt_context:
            prompt = f"إليك نتائج يوتيوب عن '{query}':\n\n{yt_context}\nصغ النتيجة لكل فيديو بهذا الشكل:\nاسم الفيديو (مختصر)\n\"الشرح\"\nالوصف المختصر (بالعراقي)\n[(الرابط)](رابط الفيديو)"
            ai_res = await ask_ai(prompt)
            await event.reply(ai_res, link_preview=False)
        else:
            await event.reply("ماكو نتائج يوتيوب حالياً. 😕")
@ABH.on(events.NewMessage(pattern=r"^تيكتوك(\s+.*|$)"))
async def tiktok_handler(event):
    query = event.pattern_match.group(1).strip()
    if not query: return await event.reply("شنو تريد أبحثلك بالتيكتوك؟")
    async with event.client.action(event.chat_id, "typing"):
        tk_context = search_tiktok(query)
        if tk_context:
            prompt = f"إليك نتائج تيكتوك عن '{query}':\n\n{tk_context}\nصغ النتيجة لكل فيديو بهذا الشكل:\nاسم المقطع (مختصر)\n\"الشرح\"\nالوصف المختصر (بالعراقي)\n[(الرابط)](رابط الفيديو)"
            ai_res = await ask_ai(prompt)
            await event.reply(ai_res, link_preview=False)
        else:
            await event.reply("ماكو نتائج تيكتوك حالياً. 😕")
@ABH.on(events.CallbackQuery(pattern=r"search_(\d+)"))
async def search_callback(event):
    msg = await event.get_message()
    if not msg.reply_to_msg_id: return await event.answer("ما لگيت السؤال الأصلي.", alert=True)
    original_msg = await msg.get_reply_message()
    query = original_msg.text.replace("ميكارو", "").strip()
    await event.edit("**جاري البحث العميق... 🔎**")    
    web_info, sources = search_web(query)    
    if web_info:
        advanced_res = await ask_ai(query, web_info=web_info)
        await event.edit(f"**📌 نتيجة البحث المتقدم:**\n\n{advanced_res}\n\n{sources}", link_preview=False)
    else:
        await event.answer("ماكو نتائج إضافية بالويب.", alert=True)
