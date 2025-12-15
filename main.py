import click
import llm_analyzer
# @click.command()
# @click.argument('option', prompt='Choose an option', type=click.Choice(['Analyse a ticker', 'Compare two tickers', 'Quit'], case_sensitive=False))
# def greet(option):
#     if option == 'Analyse a ticker':
       
#         ticker = click.prompt('Enter the ticker symbol', type=str)
#         analysis = llm_analyzer.analyze_stock(ticker)
#         click.echo(f'Analysis for {ticker}:\n{analysis}')
#     elif option == 'Compare two tickers':
#         ticker1 = click.prompt('Enter the first ticker symbol', type=str)
#         ticker2 = click.prompt('Enter the second ticker symbol', type=str)
#     else:
#         click.echo('Exiting the program. Goodbye!')
   
if __name__ == '__main__':
    while True:
        print("\n=== LLM Investment Advisor ===")
        print("1. Analyser une action")
        print("2. Comparer deux actions")
        print("3. Quitter")
        
        choice = input("Ton choix : ")
        
        if choice == "1":
            # Demande ticker
            print('Enter the ticker symbol:')
            ticker = input().strip().upper()
            # Appelle analyze_stock
            analysis=llm_analyzer.analyze_stock(ticker)
            # Print résultat
            print(f'Analysis for {ticker}:\n{analysis}')
        elif choice == "2":
            # Demande 2 tickers
            print('Enter the first ticker symbol:')
            ticker1 = input().strip().upper()
            print('Enter the second ticker symbol:')
            ticker2 = input().strip().upper()
            # Appelle analyze_stock pour chacun
            analysis1=llm_analyzer.analyze_stock(ticker1)
            analysis2=llm_analyzer.analyze_stock(ticker2)
            # Print les 2 résultats
            print(f'Analysis for {ticker1}:\n{analysis1}')
            print(f'Analysis for {ticker2}:\n{analysis2}')

        elif choice == "3":
            # Quitte
            break
        else:
            print(" invalid choice. Please try again.")