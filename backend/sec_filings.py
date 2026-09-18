"""SEC 10-K download, parse, summarize, and PDF report generation."""

import os
import re
from datetime import datetime

from bs4 import BeautifulSoup
from colorama import Fore, Style
from dotenv import load_dotenv
from fpdf import FPDF, XPos, YPos
from groq import Groq
from sec_edgar_downloader import Downloader

load_dotenv()

_GROQ_API_KEY = os.getenv("GROQ_API_KEY")
# Free/developer tier default after Aug 2026 Llama deprecation (see Groq docs).
GROQ_MODEL = os.getenv("GROQ_MODEL", "openai/gpt-oss-20b")
groq_client = Groq(api_key=_GROQ_API_KEY) if _GROQ_API_KEY else None


def display_10k_sections(sections, max_chars=2000):
    """Affiche proprement les sections principales d'un 10-K dans la console."""
    section_titles = {
        "1": "1. PRINCIPAL ACTIVITY",
        "1A": "2. PRINCIPAL RISKS",
        "7": "3. FINANCIAL PERFORMANCE AND STRATEGY",
    }

    for item_num in ["1", "1A", "7"]:
        if item_num in sections:
            title = section_titles.get(item_num, f"Item {item_num}")
            print(Fore.GREEN + "=" * 60 + Style.RESET_ALL)
            print(Fore.CYAN + title + Style.RESET_ALL)
            print(Fore.GREEN + "-" * 60 + Style.RESET_ALL)

            text = sections[item_num]
            print(text[:max_chars])

            if len(text) > max_chars:
                print(
                    Fore.YELLOW
                    + f"... (affichage limité à {max_chars} caractères)"
                    + Style.RESET_ALL
                )

            print("\n")


def fetch_10k(ticker, num_filings=1):
    """Fetch the latest 10-K filings for a given ticker symbol."""
    try:
        dl = Downloader("LLMInvestAdvisor", "h.ouanounou@gmail.com")
        dl.get("10-K", ticker, limit=num_filings)
        filing_path = f"sec-edgar-filings/{ticker}/10-K/"
        return filing_path
    except Exception as e:
        print(f"Error fetching 10-K filings for {ticker}: {e}")
        return []


def parse_10k(filing_path):
    """Parse the 10-K filing and extract the raw text."""
    main_file = None
    for root, _dirs, files in os.walk(filing_path):
        for file in files:
            if file.endswith(".html") or file.endswith(".txt"):
                main_file = os.path.join(root, file)
                break
        if main_file:
            break

    if not main_file:
        print(f"Aucun fichier .html ou .txt trouvé dans {filing_path}")
        return ""

    with open(main_file, "r", encoding="utf-8") as f:
        soup = BeautifulSoup(f, "lxml")

    print(soup.title)
    for script in soup(["script", "style"]):
        script.decompose()
    text = soup.get_text(separator="\n")
    return text.strip()


def extract_key_sections(text):
    """Extrait Items 1, 1A, 7 du 10-K."""
    sections = {}

    pattern = re.compile(r"\bITEM\s+(\d{1,2}[A-Z]?)\.", re.IGNORECASE)
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


def summarize_section(item_name, item_text):
    """Résume une section du 10-K avec Groq."""
    prompts = {
        "1": "Read and Summarize this first item: principal activity, key products/services, and business model.",
        "1A": "List the 10 most critical risks (format: - Risk X: short description).",
        "7": "Read and Summarize this item: recent financial performance, current strategy, and outlook.",
    }

    prompt = prompts.get(item_name, "Summarize this section in 300 words.")

    if groq_client is None:
        return f"[Error: GROQ_API_KEY not configured for section {item_name}]"

    try:
        text_chunk = item_text[:15000]

        response = groq_client.chat.completions.create(
            model=GROQ_MODEL,
            messages=[
                {
                    "role": "system",
                    "content": "You are an expert financial analyst. Respond in english, be factual and concise.",
                },
                {
                    "role": "user",
                    "content": f"{prompt}\n\nSECTION DU 10-K:\n{text_chunk}",
                },
            ],
            temperature=0.3,
            max_tokens=1000,
        )

        return response.choices[0].message.content.strip()

    except Exception as e:
        reason = str(e).strip() or type(e).__name__
        if len(reason) > 200:
            reason = reason[:197] + "..."
        print(f"Erreur Groq Item {item_name}: {e}")
        return (
            f"[Error during summary of section {item_name}: {reason}. "
            f"Check GROQ_API_KEY / GROQ_MODEL (current: {GROQ_MODEL})]"
        )


def clean_title(title):
    """Supprime les ** ou autres caractères spéciaux."""
    return re.sub(r"\*+", "", title).strip()


def generate_pdf(ticker, summaries, output_dir="reports"):
    os.makedirs(output_dir, exist_ok=True)

    pdf = FPDF()
    pdf.add_page()

    pdf.set_font("Helvetica", "B", 20)
    pdf.cell(0, 10, f"Analyse 10-K: {ticker}", new_x=XPos.LMARGIN, new_y=YPos.NEXT, align="C")
    pdf.set_font("Helvetica", "", 10)
    pdf.cell(
        0,
        10,
        f"Date: {datetime.now().strftime('%d/%m/%Y')}",
        new_x=XPos.LMARGIN,
        new_y=YPos.NEXT,
        align="C",
    )
    pdf.ln(10)

    sections_titles = {
        "1": "1. PRINCIPAL ACTIVITY",
        "1A": "2. PRINCIPAL RISKS",
        "7": "3. FINANCIAL PERFORMANCE AND STRATEGY",
        "Competition": "4. COMPETITION",
    }

    for item_num in ["1", "1A", "7", "Competition"]:
        if item_num in summaries:
            title = clean_title(sections_titles.get(item_num, f"Item {item_num}"))

            pdf.set_font("Helvetica", "B", 14)
            pdf.cell(0, 10, title, new_x=XPos.LMARGIN, new_y=YPos.NEXT)
            pdf.ln(2)

            pdf.set_font("Helvetica", "", 10)
            text = summaries[item_num].encode("latin-1", "replace").decode("latin-1")
            pdf.multi_cell(0, 5, text)
            pdf.ln(5)

    filename = f"{ticker}_10K_Analysis_{datetime.now().strftime('%Y%m%d')}.pdf"
    filepath = os.path.join(output_dir, filename)
    pdf.output(filepath)

    return filepath


if __name__ == "__main__":
    ticker = "AAPL"

    print("Download 10-K...")
    path = fetch_10k(ticker, 1)

    print(" Extract text")
    text = parse_10k(path)

    print(" Extract key sections ")
    sections = extract_key_sections(text)
    display_10k_sections(sections)

    print(" Génération summaries + PDF...")
    summaries = {}
    for item_num in ["1", "1A", "7"]:
        if item_num in sections:
            summaries[item_num] = summarize_section(item_num, sections[item_num])

    pdf_path = generate_pdf(ticker, summaries)

    print("\n" + "=" * 60)
    print("ANALYSE over!")
    print(f" PDF generate: {pdf_path}")
    print("=" * 60)
