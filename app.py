from fastapi.middleware.cors import CORSMiddleware
from fastapi import FastAPI, Query
from sec_filings import fetch_10k, parse_10k, extract_key_sections,summarize_section,generate_pdf
from typing import Dict

app = FastAPI()

# Autoriser React (localhost:5173)
origins = [
    "http://localhost:5173",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/10K_Analysis/")
async def get_10k_analysis(ticker: str = Query(..., description="Ticker symbol")) -> Dict:
    filing_path = fetch_10k(ticker)
    text = parse_10k(filing_path)
    sections = extract_key_sections(text)
    summaries = {}
    for item_num in ["1", "1A", "7"]:
        if item_num in sections:
            summaries[item_num] = summarize_section(item_num, sections[item_num])
    pdf_path = generate_pdf(ticker, summaries)
    
    return {"ticker": ticker, "summaries": summaries, "pdf_path": pdf_path}
