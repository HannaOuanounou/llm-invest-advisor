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
│   ├── news_analyzer.py     # Sentiment news (FinBERT, optionnel)
│   ├── sec_filings.py       # Download / parse / résumé / PDF 10-K
│   ├── requirements.txt     # Dépendances core (léger)
│   └── requirements-news.txt # Extras FinBERT (torch + transformers)
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

> **Branche requise :** `main` a encore l’ancienne arborescence (fichiers Python à la racine, **pas** de dossier `backend/`).  
> Installez uniquement depuis `cursor/restructure-project-c005` (ou après merge de la [PR #1](https://github.com/HannaOuanounou/llm-invest-advisor/pull/1)).

```bash
# 1) Se placer sur la branche restructurée
git fetch origin
git checkout cursor/restructure-project-c005
git pull origin cursor/restructure-project-c005

# 2) Vérifier que vous êtes à la racine du repo et que backend/ existe
pwd                                          # doit finir par .../llm-invest-advisor
ls backend/requirements.txt                  # doit afficher le fichier (sinon mauvaise branche / mauvais dossier)

# 3) Backend (core uniquement — sans torch / transformers)
python3 -m venv .venv
source .venv/bin/activate                    # Windows: .venv\Scripts\activate
pip install -r backend/requirements.txt
cp .env.example .env                         # puis renseigner GROQ_API_KEY

# Optionnel : analyseur news FinBERT (très volumineux — plusieurs Go)
# pip install -r backend/requirements-news.txt

# 4) Frontend
cd frontend
npm install
```

Par défaut, installez uniquement `backend/requirements.txt`. Les extras news (`torch`, `transformers`) sont dans `backend/requirements-news.txt` et prennent beaucoup d’espace disque.

Si `pip install -r backend/requirements.txt` échoue avec `No such file or directory`, vous êtes encore sur `main` (ou hors du dossier du projet) : refaire les étapes 1–2.

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

Ouvre http://localhost:5173 (API sur le port 8000).

### CLI

```bash
python -m backend.cli
```

1. Analyser un ticker  
2. Comparer deux tickers  
3. Screener  
4. Quitter  

## Déploiement (Docker)

1. Crée un `.env` avec `GROQ_API_KEY=...` (optionnel : `GROQ_MODEL=openai/gpt-oss-20b`)
2. Lance :

```bash
docker compose up --build -d
```

- Frontend : http://localhost:8080  
- API : http://localhost:8000  
- Docs : http://localhost:8000/docs  

Variable optionnelle : `FRONTEND_ORIGIN=https://ton-domaine` pour le CORS en prod.
Variable frontend build : `VITE_API_BASE_URL` (URL publique de l’API).

## Stack

| Techno | Rôle |
|--------|------|
| Python / FastAPI | Backend & API |
| yfinance | Données marché |
| Groq | LLM (analyse + résumé 10-K ; modèle via `GROQ_MODEL`, défaut `openai/gpt-oss-20b`) |
| Pydantic | Schémas de réponse |
| React / Vite / MUI | Frontend |
| sec-edgar-downloader | Filings SEC |
| FinBERT (optionnel) | Sentiment news |

## Licence

MIT
