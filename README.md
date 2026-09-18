# LLM Investment Advisor

Assistant d'analyse boursière : données marché (yfinance), LLM (Groq), filings SEC 10-K, et UI React.

## Structure

```
llm-invest-advisor/
├── backend/                 # Package Python
│   ├── app.py               # API FastAPI (10-K analysis)
│   ├── cli.py               # Interface CLI
│   ├── stock_data.py        # Récupération données yfinance
│   ├── metrics.py           # Ratios / score de sous-évaluation
│   ├── llm_analyzer.py      # Analyse LLM structurée (Pydantic)
│   ├── screener.py          # Screener multi-tickers
│   ├── news_analyzer.py     # Sentiment news (FinBERT)
│   ├── sec_filings.py       # Download / parse / résumé / PDF 10-K
│   └── requirements.txt
├── frontend/                # App React + Vite + MUI
│   └── src/
│       ├── api/             # Client HTTP (axios)
│       ├── components/      # UI (SearchBar, AnalysisResult, …)
│       └── App.tsx
├── .env.example
├── .gitignore
└── README.md
```

## Prérequis

- Python 3.9+
- Node.js 18+
- Clé API Groq : https://console.groq.com

## Installation

```bash
# Backend
python -m venv .venv
source .venv/bin/activate   # Windows: .venv\Scripts\activate
pip install -r backend/requirements.txt
cp .env.example .env        # puis renseigner GROQ_API_KEY

# Frontend
cd frontend
npm install
```

## Lancer

### API (FastAPI)

Depuis la racine du projet :

```bash
uvicorn backend.app:app --reload --port 8000
```

- Docs interactives : http://127.0.0.1:8000/docs
- Endpoint principal : `GET /10K_Analysis/?ticker=AAPL`

### Frontend

```bash
cd frontend
npm run dev
```

Ouvre http://localhost:5173 (proxy vers l'API sur le port 8000).

### CLI

```bash
python -m backend.cli
```

1. Analyser un ticker  
2. Comparer deux tickers  
3. Screener  
4. Quitter  

## Stack

| Techno | Rôle |
|--------|------|
| Python / FastAPI | Backend & API |
| yfinance | Données marché |
| Groq | LLM (analyse + résumé 10-K) |
| Pydantic | Schémas de réponse |
| React / Vite / MUI | Frontend |
| sec-edgar-downloader | Filings SEC |
| FinBERT (optionnel) | Sentiment news |

## Licence

MIT
