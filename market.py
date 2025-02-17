import requests
from datetime import date, timedelta, datetime
from dotenv import load_dotenv
from pathlib import Path
import os
import session

def getMarketData(token, series_ticker, min_close_ts=None):
    url = f"https://trading-api.kalshi.com/trade-api/v2/markets?series_ticker={series_ticker}"
    headers = {
        "accept": "application/json",
        "Authorization": f"Bearer {token}"
    }

    params = {}
    if min_close_ts:
        params["min_close_ts"] = min_close_ts

    response = requests.get(url, headers=headers, params=params)

    if response.status_code == 200:
        return response.json()
    else:
        print(f"Error: {response.status_code}")
        print(response.text)
        return None

def getTargetDate(days_ahead):
    return date.today() + timedelta(days=days_ahead)

def filterMarketsByDate(markets, target_date):
    target_date_str = target_date.strftime("%y%b%d").upper()
    return [market for market in markets if target_date_str in market['ticker']]

def getMarketTicker(current_price, markets):
    break_even_ticker = None
    profit_ticker = None
    closest_diff = float('inf')

    for market in markets:
        ticker = market['ticker']
        floor_strike = market.get('floor_strike', None)
        cap_strike = market.get('cap_strike', None)

        if floor_strike and cap_strike:
            if floor_strike <= current_price <= cap_strike:
                break_even_ticker = ticker
            else:
                # Calculate the absolute difference from the current price to the range
                diff = min(abs(current_price - floor_strike), abs(current_price - cap_strike))
                if diff < closest_diff:
                    closest_diff = diff
                    profit_ticker = ticker

    return break_even_ticker, profit_ticker

def getYesAskPrice(ticker, markets):
    for market in markets:
        if market['ticker'] == ticker:
            return market.get('yes_ask', None)
    return None

def main():
    env_path = Path('.') / 'info.env'
    load_dotenv(dotenv_path=env_path)
    username = os.getenv('EMAIL')
    password = os.getenv('PASSWORD')
    token = session.kalshiLogin(username, password)

    target_date = getTargetDate(0)

    min_close_ts = int(datetime.timestamp(datetime.combine(target_date - timedelta(days=1), datetime.min.time())))
    market_data = getMarketData(token, "INX", min_close_ts)

    if market_data:
        current_price = 5590.23  # Replace with the actual current S&P 500 price
        filtered_markets = filterMarketsByDate(market_data['markets'], target_date)
        break_even_ticker, profit_ticker = getMarketTicker(current_price, filtered_markets)
        
        if break_even_ticker and profit_ticker:
            break_even_yes_ask = getYesAskPrice(break_even_ticker, filtered_markets)
            profit_yes_ask = getYesAskPrice(profit_ticker, filtered_markets)

            print(f"Break-even Ticker: {break_even_ticker}, Yes Ask Price: {break_even_yes_ask}")
            print(f"Profit Ticker: {profit_ticker}, Yes Ask Price: {profit_yes_ask}")
        else:
            print("No suitable tickers found.")

if __name__ == "__main__":
    main()
