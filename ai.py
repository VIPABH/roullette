from shortcut import can
from ABH import *
import google.generativeai as genai
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
        if "429" in str(e):
            return "عيني هواي أسئلة جايتني حالياً! اصبرلي ثواني وارجع اسألني. ⏳"
        return f"صار عندي خلل فني بسيط: {str(e)}"
globalbutton = lambda id: [
    Button.inline("ذكاء عادي", data=f"ai:{id}"),
    Button.inline("ذكاء ومصادر", data=f"ai-serach:{id}"),
    Button.inline("بحث يوتيوب", data=f"ai-youtube:{id}"),
    Button.inline("بحث تيكتوك", data=f"ai-google:{id}"),
    Button.inline("مصادر اخرى", data=f"other-ai:{id}"),
]
ask = {}
@ABH.on(events.NewMessage(pattern='^ميكارو'))
async def mikaru(e):
    id = e.sender_id
    if not can(id): return await e.reply("لا تستطيع استخدام هذا الامر\n جرب ترسل `/start` بالخاص")
    t = e.text
    if t == "ميكارو":
        await e.respond("🙂")
    else:
        x = t.replace('ميكارو', '')
        b = globalbutton(id)
        await e.reply(f"البحث عن **{x}ّ**:", buttons=b)
        ask[id] = x
@ABH.on(events.CallbackQuery(pattern=rb'^(ai|ai-serach|ai-youtube|ai-google|other-ai):(.*)'))
async def ai(e):
    id = e.sender_id
    if not can(id): return await e.answer("لا تستطيع استخدام هذا الامر\n جرب ترسل `/start` بالخاص")
    data_parts = e.data.decode('utf-8').split(':')
    ai_type = data_parts[0]
    user_id = data_parts[1]
    if id != int(user_id): return await e.answer("الامر ما يخصك")
    if ai_type == "ai":
        await e.answer("جاري التحميل..."), await e.edit("الذكاء عادي")
    ai_response = await ask_makhfi_ai(ask[id])    
    await e.edit(f"**مخفي يقول لك:**\n\n{ai_response}\n\n---\nبخدمتكم - مطور البوت: ابن هاشم")
