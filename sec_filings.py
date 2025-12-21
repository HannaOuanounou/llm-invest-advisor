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
    Parse the 10-K filing and extract the raw text
    """
    # 1. find the main .html or .txt file in filing_path
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

    # 2. read the file
    with open(main_file, "r", encoding="utf-8") as f:
        content = f.read()

    # 3. Parse with BeautifulSoup
    soup = BeautifulSoup(content, "html.parser")

    # 4. Extract text
    for script in soup(["script", "style"]):
        script.decompose()
    text = soup.get_text(separator="\n")
    # 5. return cleaned text
    return text.strip()




import re

def extract_key_sections(text):
    """
    Extrait Items 1, 1A, 7 du 10-K
    """
    sections = {}
    
    pattern = re.compile(r'\bITEM\s+(\d{1,2}[A-Z]?)\.', re.IGNORECASE)
    matches = list(pattern.finditer(text))
    
    if not matches:
        print("Aucun Item trouvé!")
        return sections
    
    positions = []
    for match in matches:
        item_num = match.group(1).upper()
        positions.append((item_num, match.start()))
    
    positions.sort(key=lambda x: x[1])
    
    for i, (item_num, start_pos) in enumerate(positions):
        if i + 1 < len(positions):
            end_pos = positions[i + 1][1]
        else:
            end_pos = len(text)
        
        if item_num in ["1", "1A", "7"]:
            sections[item_num] = text[start_pos:end_pos].strip()
    
    return sections

if __name__ == "__main__":
    path = fetch_10k("AAPL", 1)
    if path:
        print(f"10-K downloaded to: {path}")
        
        for root, dirs, files in os.walk(path):
            for file in files:
                print(f"  - {file}")
    text = parse_10k(path)
    print(f"Text extracted: {len(text)} characters")
    print(text[:500])

    print("\n" + "="*60)
    print("keys sections extracted:")
    print("="*60)
    
    sections = extract_key_sections(text)
    
    for item_num, item_text in sections.items():
        print(f"\nItem {item_num}: {len(item_text):,} characters")
        print(f"Preview: {item_text[:200]}...")