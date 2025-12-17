import yfinance as yf

def getStock(ticker: str):
    try:
        ticker = ticker.strip().upper()

        stock = yf.Ticker(ticker)

        info = stock.info or {}
        if not info or info.get("regularMarketPrice") is None:
            return None

        mydic = {
            "ticker": ticker,
            "name": info.get("shortName", "N/A"),
            "price": info.get("regularMarketPrice", "N/A"),
            "P/E Ratio": info.get("trailingPE", "N/A"),
            "marketCap": info.get("marketCap", "N/A"),
            "sector": info.get("sector", "N/A"),
            "fiftyTwoWeekHigh": info.get("fiftyTwoWeekHigh", "N/A"),
            "fiftyTwoWeekLow": info.get("fiftyTwoWeekLow", "N/A"),
            "dividendYield": info.get("dividendYield", "N/A"),
            "volume": info.get("volume", "N/A"),
            "averageVolume": info.get("averageVolume", "N/A"),
            "beta": info.get("beta", "N/A"),
            "bookValue": info.get("bookValue", "N/A"),
            "totalDebt": info.get("totalDebt", "N/A"),
            "totalEquity": info.get("totalStockholdersEquity", "N/A"),
            "freeCashFlow": info.get("freeCashflow", "N/A"),
            "earningsGrowth": info.get("earningsGrowth", "N/A"),
            "debtToEquity": info.get("debtToEquity", "N/A"),
            "currentRatio": info.get("currentRatio", "N/A"),
            "quickRatio": info.get("quickRatio", "N/A"),
            "returnOnAssets": info.get("returnOnAssets", "N/A"),
            "returnOnEquity": info.get("returnOnEquity", "N/A"),
            "grossMargins": info.get("grossMargins", "N/A"),
            "operatingMargins": info.get("operatingMargins", "N/A"),
            "profitMargins": info.get("profitMargins", "N/A"),  
        }

        return mydic

    except Exception:
        return None


if __name__ == "__main__":
    print("AAPL  =>", getStock("AAPL"))
    #print("ZZZZZ =>", getStock("ZZZZZ"))
