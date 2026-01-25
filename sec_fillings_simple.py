# sec_filings_simple.py
from sec_edgar_downloader import Downloader
import os
from bs4 import BeautifulSoup
from datetime import datetime
from fpdf import FPDF, XPos, YPos
import re
from colorama import Fore, Style

# ---------------------------
# Fonctions d'affichage console
# ---------------------------
def display_10k_sections(sections, max_chars=2000):
    """
    Affiche proprement les sections principales d'un 10-K dans la console.

    Args:
        sections (dict): dictionnaire Item -> texte
        max_chars (int): nombre maximum de caractères à afficher par section
    """
    section_titles = {
        "1": "1. PRINCIPAL ACTIVITY",
        "1A": "2. PRINCIPAL RISKS",
        "7": "3. FINANCIAL PERFORMANCE AND STRATEGY",
        "Competition": "4. COMPETITION"
    }

    for item_num in ["1", "1A", "7", "Competition"]:
        if item_num in sections:
            title = section_titles.get(item_num, f"Item {item_num}")
            print(Fore.GREEN + "="*60 + Style.RESET_ALL)
            print(Fore.CYAN + title + Style.RESET_ALL)
            print(Fore.GREEN + "-"*60 + Style.RESET_ALL)
            
            text = sections[item_num]
            print(text[:max_chars])
            
            if len(text) > max_chars:
                print(Fore.YELLOW + f"... (affichage limité à {max_chars} caractères)" + Style.RESET_ALL)
            
            print("\n")  # ligne vide entre sections

# ---------------------------
# Fonctions récupération 10-K
# ---------------------------
def fetch_10k(ticker, num_filings=1):
    """
    Récupère les derniers 10-K pour un ticker donné.
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
    main_file = None
    for root, dirs, files in os.walk(filing_path):
        for file in files:
            if file.endswith(".html") or file.endswith(".txt"):
                main_file = os.path.join(root, file)
                break
        if main_file:
            break

    if not main_file:
        print(f"Aucun fichier trouvé dans {filing_path}")
        return ""

    with open(main_file, "r", encoding="utf-8", errors="replace") as f:
        raw_html = f.read()

        raw_html = re.sub(r"<SEC-HEADER>.*?</SEC-HEADER>", "", raw_html, flags=re.DOTALL)

        soup = BeautifulSoup(raw_html, "lxml")

        for tag in soup.find_all(lambda t: t.name and t.name.startswith("ix:")):
            tag.decompose()

        for tag in soup(["script", "style", "noscript", "header", "footer", "nav", "meta", "link"]):
            tag.decompose()

        # Texte brut
        text = soup.get_text(separator="\n", strip=True)
        text = re.sub(r"\n{2,}", "\n\n", text)

        print(text[:2000])

    return text.strip()

# ---------------------------
# Extraction des sections
# ---------------------------
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
        end_pos = positions[i + 1][1] if i + 1 < len(positions) else len(text)
        if item_num in ["1", "1A", "7"]:
            sections[item_num] = text[start_pos:end_pos].strip()
    
    return sections

def extract_competition_section(text):
    business = extract_key_sections(text).get("1", "")
    keywords = ["competition", "competitor", "competitive", "market share", "rival"]

    lines = []
    for line in business.split("\n"):
        if any(k in line.lower() for k in keywords):
            if len(line.strip()) > 50:
                lines.append(line.strip())

    return "\n".join(lines[:25]) if lines else "[No competition section found]"

# ---------------------------
# Génération PDF
# ---------------------------
def clean_title(title):
    """Supprime les ** ou autres caractères spéciaux"""
    return re.sub(r"\*+", "", title).strip()

def generate_pdf(ticker, sections, output_dir="reports"):
    os.makedirs(output_dir, exist_ok=True)
    pdf = FPDF()
    pdf.add_page()

    # Titre
    pdf.set_font("Helvetica", "B", 20)
    pdf.cell(0, 10, f"Analyse 10-K: {ticker}", new_x=XPos.LMARGIN, new_y=YPos.NEXT, align="C")
    pdf.set_font("Helvetica", "", 10)
    pdf.cell(0, 10, f"Date: {datetime.now().strftime('%d/%m/%Y')}", new_x=XPos.LMARGIN, new_y=YPos.NEXT, align="C")
    pdf.ln(10)

    sections_titles = {
        "1": "1. PRINCIPAL ACTIVITY",
        "1A": "2. PRINCIPAL RISKS",
        "7": "3. FINANCIAL PERFORMANCE AND STRATEGY",
        "Competition": "4. COMPETITION"
    }

    for item_num in ["1", "1A", "7", "Competition"]:
        if item_num in sections:
            title = clean_title(sections_titles.get(item_num, f"Item {item_num}"))
            pdf.set_font("Helvetica", "B", 14)
            pdf.cell(0, 10, title, new_x=XPos.LMARGIN, new_y=YPos.NEXT)
            pdf.ln(2)

            pdf.set_font("Helvetica", "", 10)
            text = sections[item_num].encode('latin-1', 'replace').decode('latin-1')
            pdf.multi_cell(0, 5, text)
            pdf.ln(5)

    filename = f"{ticker}_10K_Analysis_{datetime.now().strftime('%Y%m%d')}.pdf"
    filepath = os.path.join(output_dir, filename)
    pdf.output(filepath)
    return filepath

# ---------------------------
# Main
# ---------------------------
if __name__ == "__main__":
    ticker = "AAPL"
    
    print("Download 10-K...")
    path = fetch_10k(ticker, 1)
    
    print(" Extract text")
    text = parse_10k(path)

    print(" Extract key sections ")
    sections = extract_key_sections(text)

    # Ajouter section compétition
    sections["Competition"] = extract_competition_section(text)

    # Affichage console
    display_10k_sections(sections, max_chars=2000)

    # Génération PDF
    print(" Génération PDF...")
    pdf_path = generate_pdf(ticker, sections)
    
    print("\n" + "="*60)
    print("ANALYSE over!")
    print(f" PDF generate: {pdf_path}")
    print("="*60)
