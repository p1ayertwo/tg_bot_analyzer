from dotenv import load_dotenv
import os

load_dotenv()
TELEGRAM_API_KEY = os.getenv('TELEGRAM_API')