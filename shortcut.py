from telethon.tl.functions.channels import GetParticipantRequest
from ABH import *
wfffp = 1910015590
owner = 7941637237
name = {wfffp: 'ابن هاشم', owner: 'ابراهيم'}
can = lambda user_id: user_id in [wfffp, owner]
def mention(entity):
    try:
        if hasattr(entity, 'sender') and entity.sender:
            user = entity.sender
        elif hasattr(entity, 'sender_id') and entity.sender_id:
            user = ABH.get_entity(entity.sender_id)
        else:
            user = ABH.get_entity(entity)
        name = getattr(user, 'first_name', "مستخدم")
        if not name or name.strip() == "":
            name = "مستخدم"
        return f"[{name}](tg://user?id={user.id})"
    except Exception:
        return "مستخدم"
async def is_in_channel(user_id, channel_username):
    try:
        return await ABH(GetParticipantRequest(channel_username, user_id))
    except:
        return False
channels = {
    "ANYMOUSupdate": "https://t.me/ANYMOUSupdate",
    "x04ou": "https://t.me/x04ou"
}
