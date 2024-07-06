import math

def calculateFees(num_contracts, contract_price):
    return math.ceil(0.035 * num_contracts * contract_price * (1 - contract_price))

def calculateBets(total_budget, ask_price_break_even, ask_price_profit):
    # Convert ask prices from cents to dollars
    ask_price_break_even /= 100
    ask_price_profit /= 100

    # Calculate return rates
    return_rate_break_even = 1 / ask_price_break_even
    return_rate_profit = 1 / ask_price_profit

    # Calculate the minimum amount for the break-even bet
    x = total_budget / return_rate_break_even

    # Allocate remaining funds to the profit bet
    y = total_budget - x

    # Ensure the profit condition holds
    if y * return_rate_profit <= x:
        raise ValueError("Profit condition not met. Adjust your ask prices or budget.")

    return x, y, return_rate_break_even, return_rate_profit

def calculateContractsToBuy(budget, ask_price):
    # Calculate the number of contracts to buy
    if ask_price > 0:
        count = budget * 100 // ask_price
        return int(count)
    else:
        raise ValueError("Invalid ask price")

def main():
    # Example parameters
    total_budget = 100.0  # Total budget in dollars
    ask_price_break_even = 50.0  # Ask price for the break-even bet in cents
    ask_price_profit = 34.0  # Ask price for the profit bet in cents

    try:
        x, y, return_rate_break_even, return_rate_profit = calculateBets(total_budget, ask_price_break_even, ask_price_profit)
        print()
        print(f"Break-even bet amount: ${x:.2f}")
        print(f"Profit bet amount: ${y:.2f}")
        print(f"Return rate for break-even bet: {return_rate_break_even:.2f}")
        print(f"Return rate for profit bet: {return_rate_profit:.2f}")
        print()

        # Calculate returns
        return_break_even = x * return_rate_break_even
        return_profit = y * return_rate_profit

        print(f"Total return for break-even bet: ${return_break_even:.2f}")
        print(f"Total return for profit bet: ${return_profit:.2f}")

        # Calculate profit
        profit = return_profit - total_budget

        print(f"Total profit if the profit bet wins: ${profit:.2f}")
        print()

        break_even_count = calculateContractsToBuy(x, ask_price_break_even)
        profit_count = calculateContractsToBuy(y, ask_price_profit)
        
        print(f"Break-even contracts to buy: {break_even_count}")
        print(f"Profit contracts to buy: {profit_count}")

        # Calculate fees for break-even and profit contracts
        break_even_fees = calculateFees(break_even_count, ask_price_break_even / 100)
        profit_fees = calculateFees(profit_count, ask_price_profit / 100)
        print()
        
        print(f"Fees for break-even contracts: ${break_even_fees:.2f}")
        print(f"Fees for profit contracts: ${profit_fees:.2f}")

        # Calculate profit minus fees
        total_fees = break_even_fees + profit_fees
        profit_minus_fees = profit - total_fees

        print(f"Total profit minus fees: ${profit_minus_fees:.2f}")

    except ValueError as e:
        print(e)

if __name__ == "__main__":
    main()
