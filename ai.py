from ABH import *
from telethon import Button, events
from datetime import datetime
from ddgs import DDGS
import httpx
def search_web(query):
    with DDGS() as ddgs:
        results = list(ddgs.text(query, max_results=3))
        if results:
            context = ""
            links = "\n\n**🌐 المصادر والنتائج المتقدمة:**"
            for i, r in enumerate(results, 1):
                context += f"[{i}] {r['body']}\n"
                links += f"\n{i}. [{r['title']}]({r['href']})"
            return context, links
    return "", ""
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
        full_prompt = f"المعلومات المجلوبة من الويب (حديثة):\n{web_info}\n\nالسؤال: {q}\nاجب بناءً على المعلومات أعلاه بلهجة عراقية."
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
                if response_data:
                    return response_data
                return "ماكو رد واضح من السيرفر، جرب مرة ثانية."
            return "السيرفر حالياً ثقيل، ثواني وارجع جرب."
    except Exception as e:
        return f"صار خطأ تقني: {str(e)}"
@ABH.on(events.NewMessage(pattern=r"^ميكارو(\s+.*|$)"))
async def bot_handler(event):
    user_q = event.pattern_match.group(1).strip()    
    if not user_q:
        return await event.reply("🙂")
    async with event.client.action(event.chat_id, "typing"):
        ai_res = await ask_ai(user_q)
        buttons = [Button.inline("🔍 بحث عميق بمصادر الويب", data=f"search_{event.id}")]
        await event.reply(ai_res, buttons=buttons)
@ABH.on(events.CallbackQuery(pattern=r"search_(\d+)"))
async def search_callback(event):
    msg = await event.get_message()
    if not msg.reply_to_msg_id:
        return await event.answer("ما گدرت ألقى السؤال الأصلي.", alert=True)
    original_msg = await msg.get_reply_message()
    query = original_msg.text.replace("مخفي", "").strip()
    await event.edit("**جاري البحث في الويب وتحليل البيانات... 🔎**")    
    web_info, sources = search_web(query)    
    if web_info:
        advanced_res = await ask_ai(query, web_info=web_info)
        final_text = f"**📌 نتيجة البحث المتقدم:**\n\n{advanced_res}\n\n{sources}"
        await event.edit(final_text, buttons=None, link_preview=False)
    else:
        await event.answer("ما لگيت نتائج إضافية مفيدة بالويب.", alert=True)
