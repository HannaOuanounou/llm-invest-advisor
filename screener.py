
import yfinance as yf
import test_data, advanced_metrics

list_tickers = ["AAPL", "MSFT", "GOOGL", "AMZN", "TSLA", "FB", "NVDA", "JPM", "V", "JNJ","WMT", "PG", "DIS", "INTC", "CSCO", "PFE", "KO", "PEP", "MCD", "NKE"]  

def screen_stocks(sector, max_pe, min_market_cap, min_dividend):
    try:
        screened_stocks = []

        for ticker in list_tickers:
            
            data= test_data.getStock(ticker) 
            graham_number=advanced_metrics.calculate_graham_number(data)
            data['Graham Number']=graham_number
            undervaluation_score=advanced_metrics.calculate_undervaluation_score(data)
            data['Undervaluation Score']=undervaluation_score
            if data is None:
                continue
                
            # Filtre par secteur
            if sector and data['sector'].lower() != sector.lower():
                continue
                
            # Filtre par P/E
            if max_pe and data['P/E Ratio'] > max_pe:
                continue
            # Filtre par capitalisation boursière
            if min_market_cap and data['marketCap'] < min_market_cap:
                continue
            # Filtre par rendement du dividende
            if min_dividend and (data['dividendYield'] is None or data['dividendYield'] < min_dividend):
                continue
            
            screened_stocks.append(data)
                
    except Exception:
        print("An error occurred during stock screening.")
        return []   
    sorted_data = sorted(screened_stocks, key=lambda stock: stock.get('Undervaluation Score', 0), reverse=True)
    return sorted_data

if __name__ == "__main__":
    # Test 1: Tech stocks avec P/E < 40
    print("=== Tech stocks avec P/E < 40 ===")
    results = screen_stocks(sector="Technology", max_pe=40, min_market_cap=None, min_dividend=None)
    print(f"Trouvé {len(results)} stocks")
    for stock in results[:5]:  # Top 5
        print(f"{stock['ticker']}: P/E={stock['P/E Ratio']}")