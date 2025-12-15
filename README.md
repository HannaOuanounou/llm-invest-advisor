#  LLM Investment Advisor

An AI-powered stock analysis assistant that provides structured investment recommendations based on real-time financial data.

##  Overview

This project fetches live stock market data via yfinance and uses a Large Language Model (Groq API) to generate detailed analyses including strengths, risks, and investment verdicts.

##  Features

- Real-time stock data retrieval
- AI-powered structured analysis
- Side-by-side stock comparison
- Clean CLI interface
- JSON-validated responses using Pydantic

##  Installation

### Prerequisites
- Python 3.9+
- Groq API key (free tier available)

### Setup
```bash
# Clone the repository
git clone <your-repo-url>
cd llm-invest-advisor

# Install dependencies
pip install yfinance groq python-dotenv pydantic
```

##  Configuration

1. Create a `.env` file in the project root:
```env
GROQ_API_KEY=your_groq_api_key_here
```

2. Get your free API key at: https://console.groq.com

##  Usage

Run the main program:
```bash
python main.py
```

### Menu Options

1. **Analyze a stock** - Get detailed analysis for a single ticker
2. **Compare two stocks** - Side-by-side comparison of two tickers
3. **Quit** - Exit the program

### Example
```
Enter the ticker symbol: AAPL
```

##  Tech Stack

| Technology | Purpose |
|-----------|---------|
| **Python 3.9+** | Core language |
| **yfinance** | Stock market data retrieval |
| **Groq API** | LLM for analysis (openai/gpt-oss-20b) |
| **Pydantic** | Data validation & structuring |
| **python-dotenv** | Environment variable management |

## Project Structure
```
llm-invest-advisor/
├── main.py              # CLI interface
├── llm_analyzer.py      # LLM integration & analysis logic
├── test_data.py         # Stock data retrieval
├── .env                 # API keys (not committed)
├── .gitignore          
└── README.md
```

##  Contributing

This is a personal learning project. Feel free to fork and adapt.

##  License

MIT