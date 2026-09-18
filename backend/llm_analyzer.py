import os
import json
from dotenv import load_dotenv
from groq import Groq
from pydantic import BaseModel, ValidationError
from typing import Literal, Optional

from backend import metrics
from backend import stock_data


# Load environment variables from .env file
load_dotenv()
GROQ_API_KEY = os.getenv("GROQ_API_KEY")

client = Groq(api_key=GROQ_API_KEY) if GROQ_API_KEY else None


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
    data = stock_data.get_stock(ticker)

    if data is None:
        return None
    # Enrich with advanced metrics
    data["PEG Ratio"] = metrics.calculate_peg_ratio(data) or "N/A"
    data["Price to Book"] = metrics.calculate_price_to_book(data) or "N/A"
    data["Debt to Equity"] = metrics.calculate_debt_to_equity(data) or "N/A"
    data["Free Cash Flow Yield"] = metrics.calculate_free_cash_flow_yield(data) or "N/A"

    # 2) Appel Groq
    if client is None:
        return None

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
                        f"DONNÉES:\n{json.dumps(data, ensure_ascii=False)}\n\n"
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
