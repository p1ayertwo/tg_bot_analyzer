from aiogram import Bot, Router, F
from aiogram.types import Message, ReplyKeyboardRemove, FSInputFile
from aiogram.filters import Command
import os
from config import TELEGRAM_API_KEY
from bot.utils import get_start_kb, get_world_kb
from bot.commands import generate_stock_price_chart, get_stock_info, get_and_format_top_movers, generate_stock_price_chart_ru, get_stock_info_ru

router = Router()

@router.message(Command("start"))
async def cmd_start(message : Message):
    await message.answer(
        "Привет! Я бот для анализа финансовых рынков за последний день от @play3rtwo",
        reply_markup=get_start_kb()
    )

@router.message(F.text.contains("Мировые компании"))
async def world(message: Message):
    await message.answer(
        "Выбери действие",
        reply_markup=get_world_kb()
    )

@router.message(F.text.contains("Данные по тикеру"))
async def world_ticker(message: Message):
    await message.answer(
        "Отправь мне интересующий тебя тикер в формате 'W <тикер>'",
        reply_markup=ReplyKeyboardRemove()
    )

@router.message(F.text.contains("W "))
async def world_ticker_ans(message: Message):
    bot = Bot(token=TELEGRAM_API_KEY)
    ticker = message.text[2:].strip().upper()
    file_path = f'data/{ticker}.png'
    chart_path = generate_stock_price_chart(ticker, file_path)
    if chart_path:
        await bot.send_photo(
            chat_id=message.chat.id,
            photo=FSInputFile(chart_path)
        )
        os.remove(chart_path)
        await message.answer(
            get_stock_info(ticker),
            reply_markup=get_start_kb()
        )
    else:
        await message.answer(
            f'Нет данных для {ticker}',
            reply_markup=get_start_kb()
        )

@router.message(F.text.contains("Лидеры роста и снижения S&P 500"))
async def world_sp500(message: Message):
    await message.answer(
        get_and_format_top_movers(),
        reply_markup=get_start_kb()
    )

@router.message(F.text.contains("Российские компании"))
async def ru_ticker(message: Message):
    await message.answer(
        "Отправь мне интересующий тебя тикер в формате 'R <тикер>'",
        reply_markup=ReplyKeyboardRemove()
    )

@router.message(F.text.contains("R "))
async def ru_ticker_ans(message: Message):
    bot = Bot(token=TELEGRAM_API_KEY)
    ticker = message.text[2:].strip().upper()
    file_path = f'data/{ticker}.png'
    chart_path = generate_stock_price_chart_ru(ticker, file_path)
    if chart_path:
        await bot.send_photo(
            chat_id=message.chat.id,
            photo=FSInputFile(chart_path)
        )
        os.remove(chart_path)
        await message.answer(
            get_stock_info_ru(ticker),
            reply_markup=get_start_kb()
        )
    else:
        await message.answer(
            f'Нет данных для {ticker}',
            reply_markup=get_start_kb()
        )