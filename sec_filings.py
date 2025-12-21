from sec_edgar_downloader import Downloader
import os
from bs4 import BeautifulSoup

def fetch_10k(ticker, num_filings=1):
    """
    Fetch the latest 10-K filings for a given ticker symbol.
    """
    try:
        dl = Downloader("LLMInvestAdvisor", "h.ouanounou@gmail.com")
        dl.get("10-K", ticker, limit=num_filings)
        filing_path = f"sec-edgar-filings/{ticker}/10-K/"
        return filing_path
    except Exception as e:
        print(f"Error fetching 10-K filings for {ticker}: {e}")
        return []
    

def parse_10k(filing_path):
    """
    Parse le fichier 10-K et extrait le texte brut
    """
    # TODO: 
    # 1. Trouver le fichier .html ou .txt principal dans filing_path
    main_file = None
    for root, dirs, files in os.walk(filing_path):
        for file in files:
            if file.endswith(".html") or file.endswith(".txt"):
                main_file = os.path.join(root, file)
                break
        if main_file:
            break

    if not main_file:
        print(f"Aucun fichier .html ou .txt trouvé dans {filing_path}")
        return ""

    # 2. Lire le fichier
    with open(main_file, "r", encoding="utf-8") as f:
        content = f.read()

    # 3. Parser avec BeautifulSoup
    soup = BeautifulSoup(content, "html.parser")
   
    # 4. Extraire le texte (enlever scripts, styles)
    for script in soup(["script", "style"]):
        script.decompose()
    text = soup.get_text(separator="\n")
    # 5. Return le texte propre
    return text.strip()

if __name__ == "__main__":
    path = fetch_10k("AAPL", 1)
    if path:
        print(f"10-K downloaded to: {path}")
        # Liste les fichiers téléchargés
        for root, dirs, files in os.walk(path):
            for file in files:
                print(f"  - {file}")
    text = parse_10k(path)
    print(f"Texte extrait: {len(text)} caractères")
    print(text[:500])  # Affiche les 500 premiers caractères