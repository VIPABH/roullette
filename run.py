from ABH import *
from plugin import *
from التخزين import *
from النشر import *
from الاعدادات import *
from ai import *
import asyncio, sys
async def main():
    try:
        r.ping()
        print("✅ اتصال Redis: مستقر")
    except redis.ConnectionError:
        print("❌ فشل الاتصال بـ Redis! تأكد من تشغيل السيرفر.")
        return
    await ABH.start(bot_token=BOT_TOKEN)
    print("🚀 bot is running.")    
    await ABH.run_until_disconnected()
if __name__ == '__main__':
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print("\nتم إيقاف البوت يدوياً.")
async def run_cmd(command: str):
    process = await asyncio.create_subprocess_shell(
        command,
        stdout=asyncio.subprocess.PIPE,
        stderr=asyncio.subprocess.PIPE
    )
    stdout, stderr = await process.communicate()
    return stdout.decode().strip(), stderr.decode().strip(), process.returncode
@ABH.on(events.NewMessage(pattern="^(تحديث|up)$", from_users=[1910015590]))
async def update_repo(event):
    try:
        stdout, stderr, code = await run_cmd("git pull")
        if code == 0:
            await event.reply(f" تم تحديث السورس بنجاح\n\n{stdout or 'لا توجد تحديثات'}")
            os.execv(sys.executable, [sys.executable, os.path.abspath("run.py")])
        else:
            await hint(f" حدث خطأ أثناء التحديث:\n\n{stderr}")
    except Exception as e:
        await hint(f"⚠️ خطأ غير متوقع:\n\n{e}")
