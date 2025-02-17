from datetime import datetime, timedelta
from dotenv import load_dotenv
from pathlib import Path
import os
import session
import market
import mathbet
import makebet


def main():
    try:
        #data
        spx_price = 5579.21

        #Login and get token
        env_path = Path('.') / 'info.env'
        load_dotenv(dotenv_path=env_path)
        username = os.getenv('EMAIL')
        password = os.getenv('PASSWORD')
        token = session.kalshiLogin(username, password)

        #get account balance
        account_balance = session.getAccountBalance(token)
        money_risked = account_balance * 0.4
        print("Account balance: " + str(account_balance))
        print()

        #get days ahead - 1
        target_date = market.getTargetDate(0)

        min_close_ts = int(datetime.timestamp(datetime.combine(target_date - timedelta(days=1), datetime.min.time())))
        market_data = market.getMarketData(token, "INX", min_close_ts)

        if market_data:
            current_price = 5571.75  # Replace with the actual current S&P 500 price
            filtered_markets = market.filterMarketsByDate(market_data['markets'], target_date)
            safety_ticker, profit_ticker = market.getMarketTicker(current_price, filtered_markets)
            
            if safety_ticker and profit_ticker:
                safety_yes_ask = market.getYesAskPrice(safety_ticker, filtered_markets)
                profit_yes_ask = market.getYesAskPrice(profit_ticker, filtered_markets)

                print(f"Break-even Ticker: {safety_ticker}, Yes Ask Price: {safety_yes_ask}")
                print(f"Profit Ticker: {profit_ticker}, Yes Ask Price: {profit_yes_ask}")
            else:
                print("No suitable tickers found.")

        try:
            safety_bet_amount, profit_bet_amount, return_rate_safety, return_rate_profit = mathbet.calculateBets(int(money_risked), safety_yes_ask, profit_yes_ask)
        except ValueError as e:
            print(f"Error in calculating bets: {e}")
            return
        #mathbet.mathbetTest(int(money_risked), safety_ticker_ask, profit_ticker_ask)

        confirm = input("y/n: ")
        confirm2 = input("are you sure? y/n ")
        if confirm == "y" and confirm2 == "y":
            print("Trade Placed Sucessfully")
            print("~~~~~~~~~~~~~~~~~~~~~~~~")
            makebet.makeTrade(token, safety_ticker, mathbet.calculateContractsToBuy(safety_bet_amount, safety_yes_ask))
            print("safety projected return: " + str(return_rate_safety))
            makebet.makeTrade(token, profit_ticker, mathbet.calculateContractsToBuy(profit_bet_amount, profit_yes_ask))
            print("profit projected return: " + str(return_rate_profit))
            print("Total profit: " + str(return_rate_profit - safety_bet_amount))
        else:
            print("denied")

    except Exception as e:
        print(f"An unexpected error occurred: {e}")

if __name__ == "__main__":
    main()
