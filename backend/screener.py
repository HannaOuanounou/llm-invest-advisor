from backend import metrics
from backend import stock_data

LIST_TICKERS = [
    "AAPL", "MSFT", "GOOGL", "AMZN", "TSLA", "META", "NVDA", "JPM", "V", "JNJ",
    "WMT", "PG", "DIS", "INTC", "CSCO", "PFE", "KO", "PEP", "MCD", "NKE",
]


def screen_stocks(sector, max_pe, min_market_cap, min_dividend):
    try:
        screened_stocks = []

        for ticker in LIST_TICKERS:
            data = stock_data.get_stock(ticker)
            if data is None:
                continue

            data["Graham Number"] = metrics.calculate_graham_number(data)
            data["Undervaluation Score"] = metrics.calculate_undervaluation_score(data)

            # Filtre par secteur
            if sector and data["sector"].lower() != sector.lower():
                continue

            # Filtre par P/E
            if max_pe and data["P/E Ratio"] != "N/A" and data["P/E Ratio"] > max_pe:
                continue
            # Filtre par capitalisation boursière
            if min_market_cap and data["marketCap"] != "N/A" and data["marketCap"] < min_market_cap:
                continue
            # Filtre par rendement du dividende
            if min_dividend and (
                data["dividendYield"] is None
                or data["dividendYield"] == "N/A"
                or data["dividendYield"] < min_dividend
            ):
                continue

            screened_stocks.append(data)

    except Exception:
        print("An error occurred during stock screening.")
        return []

    return sorted(
        screened_stocks,
        key=lambda stock: stock.get("Undervaluation Score") or 0,
        reverse=True,
    )


if __name__ == "__main__":
    print("=== Tech stocks avec P/E < 40 ===")
    results = screen_stocks(sector="Technology", max_pe=40, min_market_cap=None, min_dividend=None)
    print(f"Trouvé {len(results)} stocks")
    for stock in results[:5]:
        print(f"{stock['ticker']}: P/E={stock['P/E Ratio']}")
