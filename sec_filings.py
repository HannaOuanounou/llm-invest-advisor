from sec_edgar_downloader import Downloader
import os
from bs4 import BeautifulSoup
from fpdf import FPDF
from datetime import datetime

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


from groq import Groq
from dotenv import load_dotenv

load_dotenv()

# Client Groq dédié au 10-K
groq_client = Groq(api_key=os.getenv("GROQ_API_KEY"))
def summarize_section(item_name, item_text):
    """
    Résume une section du 10-K avec Groq
    Args:
        item_name: "1", "1A", ou "7"
        item_text: text of the section
    Returns:
        str: summary in english
    """
    # Specific prompts by section
    prompts = {
        "1": "Summarize in 300 words: principal activity, key products/services, and business model.",
        "1A": "List the 10 most critical risks (format: - Risk X: short description).",
        "7": "Summarize in 300 words: recent financial performance, current strategy, and outlook."
    }

    prompt = prompts.get(item_name, "Summarize this section in 300 words.")
    
    try:
        # Limit the text to 15k characters (avoid token limit)
        text_chunk = item_text[:15000]
        
        response = groq_client.chat.completions.create(
            model="llama-3.3-70b-versatile",
            messages=[
                {
                    "role": "system",
                    "content": "You are an expert financial analyst. Respond in english, be factual and concise."
                },
                {
                    "role": "user",
                    "content": f"{prompt}\n\nSECTION DU 10-K:\n{text_chunk}"
                }
            ],
            temperature=0.3,
            max_tokens=1000
        )
        
        summary = response.choices[0].message.content.strip()
        return summary
    
    except Exception as e:
        print(f"Erreur Groq Item {item_name}: {e}")
        return f"[Error during summary of section {item_name}]"
    

def generate_pdf(ticker, summaries, output_dir="reports"):

    # create report directory if not exists
    os.makedirs(output_dir, exist_ok=True)

    # Create PDF
    pdf = FPDF()
    pdf.add_page()

    # Title
    pdf.set_font("Arial", "B", 20)
    pdf.cell(0, 10, f"Analyse 10-K: {ticker}", ln=True, align="C")
    pdf.set_font("Arial", "", 10)
    pdf.cell(0, 10, f"Date: {datetime.now().strftime('%d/%m/%Y')}", ln=True, align="C")
    pdf.ln(10)
    
    # Sections
    sections_titles = {
        "1": "1. PRINCIPAL ACTIVITY",
        "1A": "2. PRINCIPAL RISKS",
        "7": "3. FINANCIAL PERFORMANCE AND STRATEGY",
    }
    
    for item_num in ["1", "1A", "7"]:
        if item_num in summaries:
            # Titre de section
            pdf.set_font("Arial", "B", 14)
            pdf.cell(0, 10, sections_titles[item_num], ln=True)
            pdf.ln(2)
            
            # Content
            pdf.set_font("Arial", "", 10)
            # Encoding en latin-1 (fpdf limitation)
            text = summaries[item_num].encode('latin-1', 'replace').decode('latin-1')
            pdf.multi_cell(0, 5, text)
            pdf.ln(5)
    
    # Document saving
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

    print(" Génération summaries + PDF...")
    summaries = {}
    for item_num in ["1", "1A", "7"]:
        if item_num in sections:
            summaries[item_num] = summarize_section(item_num, sections[item_num])
    
    pdf_path = generate_pdf(ticker, summaries)
    
    print("\n" + "="*60)
    print("ANALYSE over!")
    print(f" PDF generate: {pdf_path}")
    print("="*60)