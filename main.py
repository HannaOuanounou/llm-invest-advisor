import llm_analyzer

if __name__ == "__main__":
    while True:
        print("\n=== LLM Investment Advisor ===")
        print("1. Analyze a stock")
        print("2. Compare two stocks")
        print("3. Quit")

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
            break
        else:
            print("Invalid choice. Please try again.")
