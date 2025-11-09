from aiogram.types import ReplyKeyboardMarkup
from aiogram.utils.keyboard import ReplyKeyboardBuilder
import pandas as pd
import os
import time
import json


def get_start_kb() -> ReplyKeyboardMarkup:
    kb = ReplyKeyboardBuilder()
    kb.button(text="🌍 Мировые компании")
    kb.button(text="🇷🇺 Российские компании")
    kb.adjust(2)
    return kb.as_markup(resize_keyboard=True)


def get_world_kb() -> ReplyKeyboardMarkup:
    kb = ReplyKeyboardBuilder()
    kb.button(text="📈 Данные по тикеру")
    kb.button(text="⏳ Лидеры роста и снижения S&P 500")
    kb.adjust(2)
    return kb.as_markup(resize_keyboard=True)


def load_tickers():
    df = pd.read_csv("data/sp500.csv")
    return df['Ticker'].tolist()


def load_from_cache():
    CACHE_FILE = 'data/cache.json'
    CACHE_EXPIRATION_TIME = 3600
    if os.path.exists(CACHE_FILE):
        with open(CACHE_FILE, 'r') as f:
            data = json.load(f)
            if time.time() - data['timestamp'] < CACHE_EXPIRATION_TIME:
                return data['result']
    return None


def save_to_cache(result):
    CACHE_FILE = 'data/cache.json'
    with open(CACHE_FILE, 'w') as f:
        json.dump({'timestamp': time.time(), 'result': result}, f)
