import os

from dotenv import load_dotenv

load_dotenv()

DEBUG = os.getenv('DEBUG')

TOKEN = os.getenv('TELEGRAM_TOKEN')
OWM_TOKEN = os.getenv('OWM_TOKEN')

# webhook settings
WEBHOOK_HOST = os.getenv('HEROKU_APP_URL')
WEBHOOK_PATH = '/'
WEBHOOK_URL = f"{WEBHOOK_HOST}{WEBHOOK_PATH}"

# webserver settings
WEBAPP_HOST = '0.0.0.0'  # or ip
WEBAPP_PORT = os.getenv('WEBHOOK_PORT', default=3001)


async def on_startup(dp):
    await dp.bot.set_webhook(WEBHOOK_URL, drop_pending_updates=True)
    print("Bot started")


async def on_shutdown(dp):
    print("Bot stopped")
    await dp.bot.delete_webhook()

    # Close DB connection (if used)
    await dp.storage.close()
    await dp.storage.wait_closed()
