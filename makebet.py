from time import time
from dotenv import load_dotenv
from pathlib import Path
import os
import requests
import session
import mathbet
    
def makeTrade(token, market_ticker, count):
        url = "https://trading-api.kalshi.com/trade-api/v2/portfolio/orders"
        payload = {
            "action": "buy",
            "client_order_id": f"{int(time.time())}",  # Use current timestamp as a unique ID
            "count": count,
            "side": "yes",
            "ticker": market_ticker,
            "type": "market"
        }

        headers = {
            "accept": "application/json",
            "content-type": "application/json",
            "Authorization": f"Bearer {token}"
        }

        response = requests.post(url, json=payload, headers=headers)

        if response.status_code == 200:
            print(f"Trade successful: {response.json()}")
            return response.json()
        else:
            print(f"Trade failed: {response.status_code} {response.text}")
            return None
    
def main():
    env_path = Path('.') / 'info.env'
    load_dotenv(dotenv_path=env_path)
    username = os.getenv('EMAIL')
    password = os.getenv('PASSWORD')
    token = session.kalshiLogin(username, password)
    print(session.getAccountBalance(token))

    x, y, breakeven_return, profit_return = mathbet.calculateBets()
    makeTrade(token, "SafetyTicker", mathbet.calculateContractsToBuy())

if __name__ == "__main__":
    main()