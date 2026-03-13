from telethon import events
from shortcut import *
from ABH import *
STATE_KEY = "channels"
async def settings(e):
    if not can(e.sender_id):
        return await e.reply("ليس لك صلاحية الدخول هنا")
    data = e.data.decode("utf-8")
    if data == "set_channel":
        r.hset(STATE_KEY, e.sender_id, "add_channel")
        await e.reply("ارسل الان ايدي او يوزر القناة")
    elif data == "del_channel":
        r.hset(STATE_KEY, e.sender_id, "del_channel")
        await e.reply("ارسل الان ايدي او يوزر القناة")
    elif data == "show_channels":
        await e.reply("قنوات الاشتراك الاجباري 👇🏾")
@ABH.on(events.NewMessage)
async def channel_handler(e):
    state = r.hget(STATE_KEY, e.sender_id)
    if not state:
        return
    if state == "add_channel":
        await e.reply("تم اضافة القناة الى الاشتراك الاجباري")
        r.hdel(STATE_KEY, e.sender_id)
    elif state == "del_channel":
        await e.reply("تم حذف القناة من الاشتراك الاجباري")
        r.hdel(STATE_KEY, e.sender_id)
