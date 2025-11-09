import pandas as pd
import yfinance as yf
import moexalgo as moex
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
from datetime import datetime, timedelta
from bot.utils import load_tickers, load_from_cache, save_to_cache


def generate_stock_price_chart(ticker, file_path):
    data = yf.download(ticker, period='1d', interval='1m')

    if data.empty:
        return None

    plt.figure(figsize=(10, 5))
    plt.plot(data.index, data['Close'], color='blue')
    plt.title(f'Цена {ticker} за последний день')
    plt.xlabel('Время')
    plt.ylabel('Цена, $')

    plt.gca().xaxis.set_major_formatter(mdates.DateFormatter('%H'))
    plt.gca().xaxis.set_major_locator(mdates.MinuteLocator(byminute=[0]))

    plt.grid()
    plt.tight_layout()

    plt.savefig(file_path)
    plt.close()

    return file_path


def get_stock_info(ticker):
    result = []
    data = yf.download(ticker, period='2d', interval='1d', auto_adjust=True, progress=False)
    last_day_data = data.iloc[-1]
    open_price = last_day_data['Open'].item()
    close_price = last_day_data['Close'].item()
    price_change = close_price - open_price
    percent_change = (price_change / open_price) * 100
    result.append(f"{ticker} {close_price:.2f}$")
    if price_change < 0:
        result.append(f"📉 {percent_change:.2f}% ({abs(price_change):.2f}$)")
    else:
        result.append(f"📈 +{percent_change:.2f}% ({price_change:.2f}$)")

    return "\n".join(result)


def get_top_movers(tickers):
    results = []

    for ticker in tickers:
        data = yf.download(ticker, period='2d', interval='1d', auto_adjust=True, progress=False)

        if data.empty:
            print(f"Нет данных для {ticker}")
            continue

        last_day_data = data.iloc[-1]

        open_price = last_day_data['Open'].item()
        close_price = last_day_data['Close'].item()
        price_change = close_price - open_price
        percent_change = (price_change / open_price) * 100

        results.append({
            'Ticker': ticker,
            'Open': open_price,
            'Close': close_price,
            'Price Change': price_change,
            'Percent Change': percent_change
        })

    df_results = pd.DataFrame(results)

    top_gainers = df_results.nlargest(3, 'Percent Change')
    top_losers = df_results.nsmallest(3, 'Percent Change')

    return top_gainers, top_losers


def format_top_movers(gainers, losers):
    result = []
    result.append("Лидеры роста:")
    result.append(" ")

    for index, row in gainers.iterrows():
        result.append(f"{row['Ticker']} {row['Close']:.2f}$")
        if row['Price Change'] < 0:
            result.append(f"📉 {row['Percent Change']:.2f}% ({abs(row['Price Change']):.2f}$)")
        else:
            result.append(f"📈 +{row['Percent Change']:.2f}% ({row['Price Change']:.2f}$)")
        result.append(" ")

    result.append("Лидеры снижения:")
    result.append(" ")

    for index, row in losers.iterrows():
        result.append(f"{row['Ticker']} {row['Close']:.2f}$")
        if row['Price Change'] < 0:
            result.append(f"📉 {row['Percent Change']:.2f}% ({abs(row['Price Change']):.2f}$)")
        else:
            result.append(f"📈 +{row['Percent Change']:.2f}% ({row['Price Change']:.2f}$)")
        result.append(" ")

    return "\n".join(result)


def get_and_format_top_movers():
    cached_result = load_from_cache()
    if cached_result is not None:
        return cached_result
    tickers = load_tickers()
    top_gainers, top_losers = get_top_movers(tickers)
    result = format_top_movers(top_gainers, top_losers)

    save_to_cache(result)

    return result


def generate_stock_price_chart_ru(ticker, file_path):
    try:
        data = moex.Ticker(ticker).candles(
            start=(datetime.now() - timedelta(days=1)),
            end=datetime.now()
        )

        if data.empty:
            return None

        plt.figure(figsize=(10, 5))
        plt.plot(data['end'], data['close'], color='blue')
        plt.title(f'Цена {ticker} за последний день')
        plt.xlabel('Время')
        plt.ylabel('Цена, ₽')

        plt.gca().xaxis.set_major_formatter(mdates.DateFormatter('%H'))
        plt.gca().xaxis.set_major_locator(mdates.MinuteLocator(byminute=[0]))

        plt.grid()
        plt.tight_layout()

        plt.savefig(file_path)
        plt.close()

        return file_path
    except LookupError:
        return None


def get_stock_info_ru(ticker):
    result = []
    data = moex.Ticker(ticker).candles(
        start=(datetime.now() - timedelta(days=1)),
        end=datetime.now()
    )
    earliest_row = data.loc[data['end'].idxmin()]
    latest_row = data.loc[data['end'].idxmax()]
    open_price = earliest_row['open']
    close_price = latest_row['close']
    price_change = close_price - open_price
    percent_change = (price_change / open_price) * 100
    result.append(f"{ticker} {close_price:.2f}₽")
    if price_change < 0:
        result.append(f"📉 {percent_change:.2f}% ({abs(price_change):.2f}₽)")
    else:
        result.append(f"📈 +{percent_change:.2f}% ({price_change:.2f}₽)")

    return "\n".join(result)
