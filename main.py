import llm_analyzer
import screener


if __name__ == "__main__":
    while True:
        print("\n=== LLM Investment Advisor ===")
        print("1. Analyze a stock")
        print("2. Compare two stocks")
        print("3. Screen stocks")
        print("4. Quit")

        choice = input("Your choice: ").strip()

        if choice == "1":
            print("Enter the ticker symbol:")
            ticker = input().strip().upper()

            analysis = llm_analyzer.analyze_stock(ticker)

            if analysis is None:
                print(" Error: Invalid ticker or API issue")
                continue  # back to menu without crashing

            print(f"\nANALYSIS FOR {ticker}:\n")
            print(f"SUMMARY: {analysis.resume}\n")

            print("STRENGTHS:")
            for pf in analysis.points_forts:
                print(f"- {pf}")

            print("\nRISKS:")
            for r in analysis.risques:
                print(f"- {r}")

            print(f"\nVERDICT: {analysis.verdict.decision}")
            print(f"Justification: {analysis.verdict.justification}")

        elif choice == "2":
            print("Enter the first ticker symbol:")
            ticker1 = input().strip().upper()

            print("Enter the second ticker symbol:")
            ticker2 = input().strip().upper()

            analysis1 = llm_analyzer.analyze_stock(ticker1)
            if analysis1 is None:
                print(f" Error: Invalid ticker or API issue ({ticker1})")
            else:
                print(f"\nANALYSIS FOR {ticker1}:\n")
                print(f"SUMMARY: {analysis1.resume}\n")

                print("STRENGTHS:")
                for pf in analysis1.points_forts:
                    print(f"- {pf}")

                print("\nRISKS:")
                for r in analysis1.risques:
                    print(f"- {r}")

                print(f"\nVERDICT: {analysis1.verdict.decision}")
                print(f"Justification: {analysis1.verdict.justification}")

            analysis2 = llm_analyzer.analyze_stock(ticker2)
            if analysis2 is None:
                print(f"\n Error: Invalid ticker or API issue ({ticker2})")
                continue  # back to menu without crashing
            else:
                print(f"\nANALYSIS FOR {ticker2}:\n")
                print(f"SUMMARY: {analysis2.resume}\n")

                print("STRENGTHS:")
                for pf in analysis2.points_forts:
                    print(f"- {pf}")

                print("\nRISKS:")
                for r in analysis2.risques:
                    print(f"- {r}")

                print(f"\nVERDICT: {analysis2.verdict.decision}")
                print(f"Justification: {analysis2.verdict.justification}")

        elif choice == "3":

            # Screen stocks by criteria
            print("Enter the sector (or leave blank):")
            sector = input().strip() or None

            print("Enter the maximum P/E ratio (or leave blank):")
            max_pe = input().strip()
            max_pe = float(max_pe) if max_pe else None

            print("Enter the minimal market cap in milliards (or leave blank):")
            min_market_cap = input().strip()
            min_market_cap = (float(min_market_cap) * 1e9) if min_market_cap else None
            print("Enter the minimum dividend yield (or leave blank):")
            min_dividend = input().strip()
            min_dividend = (float(min_dividend) / 100) if min_dividend else None
            results = screener.screen_stocks(
                sector,
                max_pe,
                (min_market_cap) if min_market_cap else None,
                (min_dividend) if min_dividend else None
            )
            print(f"Found {len(results)} stocks")
            for stock in results[:5]:  # Top 5
                print(f"{stock['ticker']}: P/E={stock['P/E Ratio']}")
        elif choice == "4":
            break
        else:
            print("Invalid choice. Please try again.")
