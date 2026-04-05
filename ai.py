import os
import asyncio
from shortcut import can
from ABH import *
import google.generativeai as genai
from telethon import Button, events
API_KEY = "AIzaSyDZngGFlslfMKZw18bhKSUmcaQ6PjWyvfc"
genai.configure(api_key=API_KEY)
model = genai.GenerativeModel(
    model_name="gemini-1.5-flash",
    system_instruction=(
        "أنت ذكاء اصطناعي متطور واسمك 'مخفي'. "
        "مطورك هو المبرمج المبدع 'ابن هاشم'. "
        "تتحدث باللهجة العراقية الودودة والذكية (مثلاً: عيني، تدلل، خادم ربك). "
        "إذا سألك أحد منو صنعك، جاوبه بفخر إنه 'ابن هاشم'. "
        "إجاباتك لازم تكون دقيقة ومختصرة ومفيدة للمستخدم العراقي."
    )
)
async def ask_makhfi_ai(prompt):
    try:
        response = await model.generate_content_async(prompt)
        if response and response.text:
            return response.text
        return "اعتذر منك عيني، ماكدرت أطلع جواب حالياً."
    except Exception as e:
        err_msg = str(e)
        if "429" in err_msg:
            return "عيني هواي أسئلة جايتني حالياً! اصبرلي ثواني وارجع اسألني. ⏳"
        if "404" in err_msg:
            return "عيني الموديل حالياً بيه تحديث بسيط، ثواني ويرجع."
        return f"صار عندي خلل فني بسيط: {err_msg}"
globalbutton = lambda id: [
    [Button.inline("ذكاء عادي 🧠", data=f"ai:{id}"), Button.inline("ذكاء ومصادر 🌐", data=f"ai-search:{id}")],
    [Button.inline("بحث يوتيوب 🎬", data=f"ai-youtube:{id}"), Button.inline("بحث تيكتوك 📱", data=f"ai-google:{id}")],
    [Button.inline("مصادر اخرى 📂", data=f"other-ai:{id}")]
]
ask = {}
@ABH.on(events.NewMessage(pattern='^ميكارو'))
async def mikaru(e):
    user_id = e.sender_id    
    # if not can(user_id): 
    #     return await e.reply("لا تستطيع استخدام هذا الامر\n جرب ترسل `/start` بالخاص")    
    text = e.text
    if text == "ميكارو":
        await e.respond("🙂 تؤمرني بشيء؟ أرسل سؤالك ويه كلمة ميكارو.")
    else:
        query = text.replace('ميكارو', '').strip()
        if not query:
            return await e.reply("عيني أرسل السؤال ويه كلمة ميكارو.")
        ask[user_id] = query
        buttons = globalbutton(user_id)
        await e.reply(f"البحث عن: **{query}**\n\nاختار نوع الذكاء اللي تريده:", buttons=buttons)
@ABH.on(events.CallbackQuery(pattern=rb'^(ai|ai-search|ai-youtube|ai-google|other-ai):(.*)'))
async def ai_callback(e):
    sender_id = e.sender_id
    data_parts = e.data.decode('utf-8').split(':')
    ai_type = data_parts[0]
    target_user_id = int(data_parts[1])
    if sender_id != target_user_id: 
        return await e.answer("هذا البحث مو إلك عيني! ✋", alert=True)
    user_query = ask.get(sender_id)
    if not user_query:
        return await e.edit("عيني انتهت الجلسة، ارجع أرسل السؤال من جديد.")
    if ai_type == "ai":
        await e.answer("جاري التفكير... 🧠")
        await e.edit(f"⏳ جاري معالجة: **{user_query}**")        
        ai_response = await ask_makhfi_ai(user_query)
        final_text = f"**مخفي يقول لك:**\n\n{ai_response}\n\n---\nبخدمتكم - مطور البوت: ابن هاشم"
        await e.edit(final_text)
    else:
        await e.answer("هذا القسم قيد التطوير حالياً.. قريباً يكمل! 🛠", alert=True)
