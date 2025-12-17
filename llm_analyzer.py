import os
import json
from dotenv import load_dotenv
from groq import Groq
from pydantic import BaseModel, ValidationError
from typing import Literal, Optional
import advanced_metrics
import test_data

# Load environment variables from .env file
load_dotenv()
GROQ_API_KEY = os.getenv("GROQ_API_KEY")

client = Groq(api_key=GROQ_API_KEY) if GROQ_API_KEY else Groq()


class StockVerdict(BaseModel):
    decision: Literal["ACHETER", "TENIR", "EVITER"]
    justification: str


class StockAnalysis(BaseModel):
    resume: str
    points_forts: list[str]
    risques: list[str]
    verdict: StockVerdict


def analyze_stock(ticker: str) -> Optional[StockAnalysis]:
    # 1) Stock data
    stock_data = test_data.getStock(ticker)

    if stock_data is None:
        return None
    # Enrich with advanced metrics
    stock_data['PEG Ratio'] = advanced_metrics.calculate_peg_ratio(stock_data) or 'N/A'
    stock_data['Price to Book'] = advanced_metrics.calculate_price_to_book(stock_data) or 'N/A'
    stock_data['Debt to Equity'] = advanced_metrics.calculate_debt_to_equity(stock_data) or 'N/A'
    stock_data['Free Cash Flow Yield'] = advanced_metrics.calculate_free_cash_flow_yield(stock_data) or 'N/A'

    # 2) Appel Groq 
    try:
        response = client.chat.completions.create(
            model="openai/gpt-oss-20b",
            messages=[
                {
                    "role": "system",
                    "content": (
                        "Tu es un analyste financier. "
                        "Retourne UNIQUEMENT un JSON conforme au schéma. "
                        "Si une info manque, mets null. Sois concis et pertinent."
                    ),
                },
                {
                    "role": "user",
                    "content": (
                        "Analyse ce stock et fournis une réponse structurée.\n\n"
                        f"DONNÉES:\n{json.dumps(stock_data, ensure_ascii=False)}\n\n"
                        "Contraintes:\n"
                        "- resume: 2-3 phrases\n"
                        "- points_forts: 3-4 bullets\n"
                        "- risques: 3-4 bullets\n"
                        "- justification: courte\n"
                    ),
                },
            ],
            response_format={
                "type": "json_schema",
                "json_schema": {
                    "name": "stock_analysis",
                    "schema": StockAnalysis.model_json_schema(),
                },
            },
        )

        content = (response.choices[0].message.content or "").strip()
        if not content:
            return None
        # invalid JSON => None
        try:
            payload = json.loads(content)
        except json.JSONDecodeError:
            return None

        # 5) Validation Pydantic
        try:
            return StockAnalysis.model_validate(payload)
        except ValidationError:
            return None

    except Exception:
        # timeout / rate limit / erreur API / etc.
        return None


if __name__ == "__main__":
    print("=== TEST AAPL ===")
    aapl = analyze_stock("AAPL")
    print(aapl.model_dump() if aapl else None)

    print("\n=== TEST ZZZZZ ===")
    zzzzz = analyze_stock("ZZZZZ")
    print(zzzzz)
