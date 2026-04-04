from ABH import *
from plugin import *
from التخزين import *
from النشر import *
from الاعدادات import *
from ai import *
save_data(owner), save_data(wfffp)
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
