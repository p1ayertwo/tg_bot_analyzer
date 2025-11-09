import pytest
import os
from bot.commands import (
    generate_stock_price_chart,
    get_stock_info,
    get_top_movers,
    generate_stock_price_chart_ru,
    get_stock_info_ru
)


# Фикстуры


@pytest.fixture
def us_ticker_list():
    return ["NVDA", "MSFT", "AAPL"]


@pytest.fixture
def ru_ticker_list():
    return ["SBER", "ROSN", "LKOH"]


# Тесты для generate_stock_price_chart


def test_generate_stock_price_chart(us_ticker_list, ru_ticker_list):
    for ticket in us_ticker_list:
        assert generate_stock_price_chart(ticket, f"data/{ticket}.png") == f"data/{ticket}.png"
        os.remove(f"data/{ticket}.png")

    for ticket in ru_ticker_list:
        assert generate_stock_price_chart(ticket, f"data/{ticket}.png") is None


# Тесты для get_stock_info


def test_get_stock_info(us_ticker_list):
    for ticket in us_ticker_list:
        assert get_stock_info(ticket).startswith(ticket)


# Тесты для get_top_movers


def test_get_top_movers(us_ticker_list):
    top_gainers, top_losers = get_top_movers(us_ticker_list)
    for ticket in us_ticker_list:
        assert ticket in top_gainers['Ticker'].tolist()
        assert ticket in top_losers['Ticker'].tolist()


# Тесты для generate_stock_price_chart_ru


def test_generate_stock_price_chart_ru(us_ticker_list, ru_ticker_list):
    for ticket in us_ticker_list:
        assert generate_stock_price_chart_ru(ticket, f"data/{ticket}.png") is None

    for ticket in ru_ticker_list:
        assert generate_stock_price_chart_ru(ticket, f"data/{ticket}.png") == f"data/{ticket}.png"
        os.remove(f"data/{ticket}.png")


# Тесты для get_stock_info_ru


def test_get_stock_info_ru(ru_ticker_list):
    for ticket in ru_ticker_list:
        assert get_stock_info_ru(ticket).startswith(ticket)
