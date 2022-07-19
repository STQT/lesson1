import os

from dotenv import load_dotenv

load_dotenv()

TOKEN = os.getenv('TELEGRAM_TOKEN')
OWM_TOKEN = os.getenv('OWM_TOKEN')