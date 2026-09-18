# Backend image for LLM Investment Advisor
FROM python:3.12-slim

WORKDIR /app

RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
    && rm -rf /var/lib/apt/lists/*

COPY backend/requirements.txt /app/backend/requirements.txt
# Install without heavy optional ML deps for the API image by default
RUN pip install --no-cache-dir \
    yfinance python-dotenv pydantic groq \
    "fastapi>=0.110" "uvicorn[standard]>=0.27" \
    sec-edgar-downloader beautifulsoup4 lxml fpdf2 colorama feedparser

COPY backend /app/backend

ENV PYTHONUNBUFFERED=1
ENV PYTHONPATH=/app

EXPOSE 8000

CMD ["uvicorn", "backend.app:app", "--host", "0.0.0.0", "--port", "8000"]
