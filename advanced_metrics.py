
import test_data

def calculate_peg_ratio(stock_data):
    try:
        pe_ratio = stock_data['P/E Ratio']
        earnings_growth = stock_data['earningsGrowth']
        if pe_ratio is None or earnings_growth is None:
            return None
        if earnings_growth in (0, None):
            return None
        return pe_ratio / (earnings_growth * 100)
    except Exception as e:
        return None


def calculate_price_to_book(stock_data):
    try:
        price = stock_data['price']
        book_value = stock_data['bookValue']
        if book_value == 0:
            return None
        return price / book_value
    except Exception as e:
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
        return None

def calculate_free_cash_flow_yield(stock_data):
    try:
        free_cash_flow = stock_data['freeCashFlow']
        market_cap = stock_data['marketCap']
        if free_cash_flow is None or market_cap is None:
            return None
        if market_cap == 0:
            return None
        return free_cash_flow / market_cap
    except Exception as e:
        return None 
    
def calculate_graham_number(stock_data):
    try:
        eps = stock_data['earningsPerShare']
        book_value_per_share = stock_data['bookValue']
        if eps is None or book_value_per_share is None:
            return None
        graham_number = (22.5 * eps * book_value_per_share) ** 0.5
        return graham_number
    except Exception as e:
        return None
    
def calculate_undervaluation_score(stock_data):
    scoring = 0
    try:
        if stock_data['P/E Ratio'] < 20:
            scoring += 20
        if calculate_peg_ratio(stock_data) is not None and calculate_peg_ratio(stock_data) < 1:
            scoring += 25
        if stock_data['price'] is not None and (stock_data['price'] < calculate_graham_number(stock_data)):
            scoring += 20
        if calculate_debt_to_equity(stock_data) is not None and calculate_debt_to_equity(stock_data) < 1:
            scoring += 15
        if calculate_free_cash_flow_yield(stock_data) is not None and calculate_free_cash_flow_yield(stock_data) > 0.05:
            scoring += 15
        return scoring
    except Exception as e:
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
    print("Graham Number:", calculate_graham_number(example_stock))
    print("Undervaluation Score:", calculate_undervaluation_score(example_stock))
    