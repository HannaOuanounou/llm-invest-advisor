import yfinance as yf
def getStock(ticker):
    stock = yf.Ticker(ticker)
    mydic=dict()
    mydic['ticker']=ticker
    mydic['name']=stock.info.get('shortName', 'N/A')
    mydic['price']=stock.info.get('regularMarketPrice','N/A')
    mydic['P/E Ratio']=stock.info.get('trailingPE','N/A')
    #mydic['EPS']=stock.info.get('trailingEps','N/A')
    mydic['marketCap']=stock.info.get('marketCap','N/A')
    stock.info.get('sector', 'N/A')    # mydic['open']=stock.info['open']
    # mydic['dayHigh']=stock.info['dayHigh']
    # mydic['dayLow']=stock.info['dayLow']
    mydic['fiftyTwoWeekHigh']=stock.info.get('fiftyTwoWeekHigh','N/A')
    mydic['fiftyTwoWeekLow']=stock.info.get('fiftyTwoWeekLow','N/A')
    mydic['dividendYield']=stock.info.get('dividendYield','N/A')
    #mydic['beta']=stock.info.get('beta','N/A')
    #mydic['averageVolume']=stock.info.get('averageVolume','N/A')    
    mydic['volume']=stock.info.get('volume','N/A')
    return mydic    

if __name__ == "__main__":
    print(getStock("AAPL"))
    print(getStock("MSFT")) 