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
        spx_price = 5564.21

        #Login and get token
        env_path = Path('.') / 'info.env'
        load_dotenv(dotenv_path=env_path)
        username = os.getenv('EMAIL')
        password = os.getenv('PASSWORD')
        token = session.kalshiLogin(username, password)

        #get account balance
        account_balance = session.getAccountBalance(token)
        money_risked = account_balance * 0.30
        print(account_balance)

        #get days ahead - 1
        target_date = market.getTargetDate(1)
    
        #get date and market data
        min_close_ts = int(datetime.timestamp(datetime.combine(target_date - timedelta(days=1), datetime.min.time())))
        market_data = market.getMarketData(token, "INX", min_close_ts)
    
        #retrieve tickers and ask prices
        safety_ticker, profit_ticker = market.getMarketTicker(spx_price, market_data['markets'])
        safety_ticker_ask = market.getYesAskPrice(safety_ticker, market_data['markets'])
        profit_ticker_ask = market.getYesAskPrice(profit_ticker, market_data['markets'])

        try:
            safety_bet_amount, profit_bet_amount, return_rate_safety, return_rate_profit = mathbet.calculateBets(int(money_risked), safety_ticker_ask, profit_ticker_ask)
        except ValueError as e:
            print(f"Error in calculating bets: {e}")
            return


        # Print calculated values
        print()
        print(target_date)
        print(safety_ticker)
        print(profit_ticker)
   
        print(safety_ticker_ask)
        print(profit_ticker_ask)
        print()
        #mathbet.mathbetTest(int(money_risked), safety_ticker_ask, profit_ticker_ask)

        confirm = input("y/n: ")
        if confirm == "y" and return_rate_profit > safety_bet_amount:
            print("Trade Placed Sucessfully")
            print("~~~~~~~~~~~~~~~~~~~~~~~~")
            makebet.makeTrade(token, safety_ticker, mathbet.calculateContractsToBuy(safety_bet_amount, safety_ticker_ask))
            print("safety projected return: " + str(return_rate_safety))
            makebet.makeTrade(token, profit_ticker, mathbet.calculateContractsToBuy(profit_bet_amount, profit_ticker_ask))
            print("profit projected return: " + str(return_rate_profit))
            print("Total profit: " + str(return_rate_profit - safety_bet_amount))
        else:
            print("denied")

    except Exception as e:
        print(f"An unexpected error occurred: {e}")

if __name__ == "__main__":
    main()
