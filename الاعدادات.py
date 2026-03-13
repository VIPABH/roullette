from telethon.errors import ChatAdminRequiredError
from telethon.tl.functions.channels import GetParticipantRequest
from telethon.tl.types import ChannelParticipantAdmin, ChannelParticipantCreator
from shortcut import *
from ABH import *
STATE_KEY = "channels"
@ABH.on(events.CallbackQuery)
async def settings(e):
    if not can(e.sender_id):
        return await e.answer("ليس لك صلاحية", alert=True)
    data = e.data.decode("utf-8")
    if data == "set_channel":
        r.hset(STATE_KEY, e.sender_id, "add_channel")
        await e.edit("أرسل الآن ايدي أو يوزر القناة")
    elif data == "del_channel":
        r.hset(STATE_KEY, e.sender_id, "del_channel")
        await e.edit("أرسل الآن ايدي أو يوزر القناة")
    elif data == "show_channels":
        await e.edit("قنوات الاشتراك الاجباري 👇")
    elif data == "count_users":
        count = r.scard("users")
        await e.edit(f"عدد المستخدمين حالياً: {count}")
@ABH.on(events.NewMessage)
async def channel_handler(e):
    state = r.hget(STATE_KEY, e.sender_id)
    if not state:
        return
    state = state.decode().strip()
    channel = e.text.strip()
    try:
        entity = await ABH.get_entity(channel)
        me = await ABH.get_me()
        participant = await ABH(GetParticipantRequest(entity, me.id))
        if not isinstance(participant.participant, (ChannelParticipantAdmin)):
            return await e.reply("❌ البوت يجب أن يكون مشرف داخل القناة أولاً")
    except ChatAdminRequiredError:
        return await e.reply("❌ البوت ليس لديه صلاحيات داخل القناة")
    except Exception:
        return await e.reply("❌ تأكد من إدخال يوزر أو ايدي صحيح للقناة")
    if state == "add_channel":
        r.sadd("forced_channels", str(entity.id))
        await e.reply("✅ تم إضافة القناة إلى الاشتراك الإجباري")
        r.hdel(STATE_KEY, e.sender_id)
    elif state == "del_channel":
        r.srem("forced_channels", str(entity.id))
        await e.reply("❌ تم حذف القناة من الاشتراك الإجباري")
        r.hdel(STATE_KEY, e.sender_id)
