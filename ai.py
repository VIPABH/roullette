from telethon import Button, events
from datetime import datetime
from ddgs import DDGS
from ABH import *
import httpx
def universal_search(query, mode="web"):
    try:
        with DDGS() as ddgs:
            if mode == "web":
                results = list(ddgs.text(query, max_results=3))
            elif mode == "youtube":
                results = list(ddgs.videos(f"site:youtube.com {query}", max_results=3))
            elif mode == "tiktok":
                results = list(ddgs.text(f"site:tiktok.com {query}", max_results=3))
            elif mode == "wiki":
                results = list(ddgs.text(f"site:wikipedia.org {query}", max_results=3))
            if not results: return "", ""            
            context = ""
            links = []
            for i, r in enumerate(results):
                url = r.get('content') or r.get('href')
                title = r.get('title', 'بدون عنوان')
                body = r.get('description') or r.get('body', '')
                context += f"المصدر {i+1}:\nالعنوان: {title}\nالوصف: {body}\nالرابط: {url}\n\n"
                links.append(f"{i+1}. [{title}]({url})")
            sources_text = "\n\n**🌐 المصادر:**\n" + "\n".join(links)
            return context, sources_text
    except Exception as e:
        print(f"Search Error: {e}")
        return "", ""
async def ask_ai(q, system_extra=""):
    system_instruction = (
        f"أنت 'ميكارو'، مطورك 'ابن هاشم'. تتحدث بالعراقي فقط وبأسلوب ذكي ومختصر. "
        f"تاريخ اليوم: {datetime.now().strftime('%Y-%m-%d')}. {system_extra}"
    )
    headers = {"User-Agent": "Dart/3.3 (dart:io)", "content-type": "application/json; charset=utf-8"}
    data = {
        "action": "send_message", "model": "gpt-4o-mini", "secret_token": "AIChatPowerBrain123@2024",
        "messages": [{"role": "system", "content": system_instruction}, {"role": "user", "content": q}]
    }
    try:
        async with httpx.AsyncClient() as client:
            res = await client.post("https://powerbrainai.com/app/backend/api/api.php", headers=headers, json=data, timeout=20.0)
            return res.json().get("data", "") if res.status_code == 200 else "السيرفر ثقيل حالياً."
    except: return "صار عندي خطأ تقني، جرب شوية ثانية."
@ABH.on(events.NewMessage(pattern=r"^(ميكارو|يوتيوب|تيكتوك|ويكيبيديا)(\s+.*|$)"))
async def main_handler(event):
    cmd = event.pattern_match.group(1)
    query = event.pattern_match.group(2).strip()
    if not query:
        return await event.reply(f"اكتب شي وية كلمة {cmd} حتى أبحث لك عنه!")
    async with event.client.action(event.chat_id, "typing"):
        mode_map = {
            "ميكارو": "web", 
            "يوتيوب": "youtube", 
            "تيكتوك": "tiktok", 
            "ويكيبيديا": "wiki"
        }
        context, sources = universal_search(query, mode=mode_map[cmd])        
        if cmd == "ميكارو":
            system_extra = "أجب على السؤال بشكل مباشر وذكي بناءً على المعلومات المتاحة."
        elif cmd in ["يوتيوب", "تيكتوك"]:
            system_extra = "رتب الفيديوهات المذكورة. لكل فيديو: الاسم، شرح مختصر جداً عنه، والرابط."
        else:
            system_extra = "لخص المعلومات من ويكيبيديا بأسلوب موسوعي لكن بلهجة عراقية مفهومة."
        prompt = f"المعلومات المتاحة:\n{context}\n\nسؤال المستخدم: {query}"
        ai_res = await ask_ai(prompt, system_extra)
        if not context and cmd != "ميكارو":
            return await event.reply("للاسف ما لكيت نتائج دقيقة عن هذا الموضوع.")
        buttons = []
        if cmd == "ميكارو":
            buttons = [Button.inline("🔍 بحث عميق", data=f"deep_{event.id}")]
        final_text = f"{ai_res}"
        if cmd != "ميكارو":
            final_text += f"\n{sources}"
        await event.reply(final_text, buttons=buttons, link_preview=False)
@ABH.on(events.CallbackQuery(pattern=r"deep_(\d+)"))
async def deep_search_callback(event):
    original = await event.get_reply_message()
    if not original or not original.text: 
        return await event.answer("ما لكيت الرسالة الأصلية.")    
    query = original.text.split(maxsplit=1)[1]
    await event.edit("**جاري التعمق في المصادر وتحليلها... 🧐**")
    context, sources = universal_search(query, "web") 
    deep_prompt = f"قم بعمل تحليل مفصل وشامل لـ: {query}\nالمعلومات: {context}"
    res = await ask_ai(deep_prompt, "أنت الآن خبير وباحث، قدم تقريراً مفصلاً بالعراقي.")
    await event.edit(f"**نتائج البحث العميق:**\n\n{res}{sources}", link_preview=False)
