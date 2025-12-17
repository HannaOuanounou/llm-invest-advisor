
import test_data

def calculate_peg_ratio(stock_data):
    try:
        pe_ratio = stock_data['P/E Ratio']
        earnings_growth = stock_data['earningsGrowth']
        if earnings_growth in (0, None):
            return None
        return pe_ratio / (earnings_growth * 100)
    except Exception as e:
        print(f"Error calculating PEG ratio: {e}")
        return None


def calculate_price_to_book(stock_data):
    try:
        price = stock_data['price']
        book_value = stock_data['bookValue']
        if book_value == 0:
            return None
        return price / book_value
    except Exception as e:
        print(f"Error calculating price-to-book ratio: {e}")
        return None


def calculate_debt_to_equity(stock_data):
    try:
        total_debt = stock_data['totalDebt']
        total_equity = stock_data['totalEquity']
        if total_debt == 'N/A' or total_equity == 'N/A':
            return None
            
        if total_equity == 0:
            return None
            
        return total_debt / total_equity
    except Exception as e:
        print(f"Error calculating debt-to-equity ratio: {e}")
        return None

def calculate_free_cash_flow_yield(stock_data):
    try:
        free_cash_flow = stock_data['freeCashFlow']
        market_cap = stock_data['marketCap']
        if market_cap == 0:
            return None
        return free_cash_flow / market_cap
    except Exception as e:
        print(f"Error calculating free cash flow yield: {e}")
        return None 
    

if __name__ == "__main__":
    # Example stock data for testing
    ticker = "AAPL"
    example_stock = test_data.getStock(ticker)
    if example_stock is None:
        print(f"Could not retrieve data for ticker {ticker}")
    else:
        print(f"Calculating advanced metrics for {ticker}:")
    print("PEG Ratio:", calculate_peg_ratio(example_stock))
    print("Price-to-Book Ratio:", calculate_price_to_book(example_stock))
    print("Debt-to-Equity Ratio:", calculate_debt_to_equity(example_stock))
    print("Free Cash Flow Yield:", calculate_free_cash_flow_yield(example_stock))