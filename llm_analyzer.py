
import os
from dotenv import load_dotenv
from groq import Groq
from pydantic import BaseModel
from typing import Literal
import json
import test_data

# Load environment variables from .env file
load_dotenv()
GROQ_API_KEY = os.getenv('GROQ_API_KEY')    

client=Groq()


class StockVerdict(BaseModel):
    decision: Literal["ACHETER", "TENIR", "EVITER"]
    justification: str


class StockAnalysis(BaseModel):
    resume: str
    points_forts: list[str]
    risques: list[str]
    verdict: StockVerdict


def analyze_stock(ticker: str) -> StockAnalysis:
    stock_data = test_data.getStock(ticker)

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

    content = response.choices[0].message.content or "{}"
    return StockAnalysis.model_validate(json.loads(content))


if __name__ == "__main__":
    

    analysis = analyze_stock("AAPL")
    print(json.dumps(analysis.model_dump(), indent=2, ensure_ascii=False))