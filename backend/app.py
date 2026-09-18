from typing import Dict

from fastapi import FastAPI, Query
from fastapi.middleware.cors import CORSMiddleware

from backend.sec_filings import (
    extract_key_sections,
    fetch_10k,
    generate_pdf,
    parse_10k,
    summarize_section,
)

app = FastAPI(title="LLM Investment Advisor", version="0.1.0")

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


@app.get("/health")
async def health() -> Dict:
    return {"status": "ok"}


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
