from ABH import *
from telethon import Button, events
from datetime import datetime
from ddgs import DDGS
import httpx
def universal_search(query, mode="web"):
    try:
        with DDGS() as ddgs:
            if mode == "web":
                results = list(ddgs.text(query, max_results=3))
                if not results: return "", ""
                context = "\n".join([f"[{i+1}] {r['body']}" for i, r in enumerate(results)])
                links = "\n\n**🌐 المصادر:**\n" + "\n".join([f"{i+1}. [{r['title']}]({r['href']})" for i, r in enumerate(results)])
                return context, links            
            search_query = f"site:youtube.com {query}" if mode == "youtube" else f"site:tiktok.com {query}"
            results = list(ddgs.videos(search_query, max_results=3)) if mode == "youtube" else list(ddgs.text(search_query, max_results=3))            
            if results:
                context = ""
                for i, r in enumerate(results):
                    url = r.get('content') or r.get('href')
                    context += f"ID: {i+1}\nالعنوان: {r['title']}\nالرابط: {url}\nالوصف الخام: {r.get('description') or r.get('body', 'لا يوجد')}\n\n"
                return context, ""
    except: pass
    return "", ""
async def ask_ai(q, system_extra=""):
    system_instruction = (
        f"أنت 'ميكارو'، مطورك 'ابن هاشم'. تتحدث بالعراقي. تاريخ اليوم: {datetime.now().strftime('%Y-%m-%d')}. "
        f"{system_extra}"
    )
    headers = {"User-Agent": "Dart/3.3 (dart:io)", "content-type": "application/json; charset=utf-8"}
    data = {
        "action": "send_message", "model": "gpt-4o-mini", "secret_token": "AIChatPowerBrain123@2024",
        "messages": [{"role": "system", "content": system_instruction}, {"role": "user", "content": q}]
    }
    try:
        async with httpx.AsyncClient() as client:
            res = await client.post("https://powerbrainai.com/app/backend/api/api.php", headers=headers, json=data, timeout=20.0)
            return res.json().get("data", "") if res.status_code == 200 else "السيرفر ثقيل."
    except: return "خطأ تقني."
@ABH.on(events.NewMessage(pattern=r"^(ميكارو|يوتيوب|تيكتوك)(\s+.*|$)"))
async def main_handler(event):
    cmd = event.pattern_match.group(1)
    query = event.pattern_match.group(2).strip()
    if not query: return await event.reply("شنو نكتب؟")    
    async with event.client.action(event.chat_id, "typing"):
        mode_map = {"ميكارو": "web", "يوتيوب": "youtube", "تيكتوك": "tiktok"}
        context, extra = universal_search(query, mode=mode_map[cmd])
        if not context: return await event.reply("ماكو نتائج. 😕")
        system_extra = (
            "حلل النتائج ورتبها. لكل فيديو/مقطع، استخرج 'short_title' و 'explanation' (الشرح) و 'summary' (الوصف المختصر بالعراقي). "
            "التنسيق النهائي للمستخدم:\nاسم الفيديو\n\"الشرح\"\nالوصف المختصر\n(الرابط)"
        )        
        prompt = f"المعلومات:\n{context}\n\nالسؤال/البحث: {query}"
        ai_res = await ask_ai(prompt, system_extra)
        if cmd == "ميكارو":
            buttons = [Button.inline("🔍 بحث عميق", data=f"search_{event.id}")]
            await event.reply(ai_res, buttons=buttons)
        else:
            await event.reply(f"**🎬 نتائج {cmd}:**\n\n{ai_res}", link_preview=False)
@ABH.on(events.CallbackQuery(pattern=r"search_(\d+)"))
async def search_callback(event):
    msg = await event.get_message()
    if not msg.reply_to_msg_id: return
    original = await msg.get_reply_message()
    query = original.text.split(maxsplit=1)[1]
    await event.edit("**جاري البحث العميق... 🔎**")
    context, sources = universal_search(query, "web")
    if context:
        res = await ask_ai(f"سوي بحث عميق لـ: {query}\nالمعلومات: {context}")
        await event.edit(f"{res}{sources}", link_preview=False)
