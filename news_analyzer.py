import yfinance as yf
import feedparser
from transformers import AutoTokenizer, AutoModelForSequenceClassification
import torch
tokenizer = AutoTokenizer.from_pretrained("ProsusAI/finbert")
model = AutoModelForSequenceClassification.from_pretrained("ProsusAI/finbert")



def fetch_stock_news(ticker, max_results=5):
    try:
        url = f"https://news.google.com/rss/search?q={ticker}+stock"
        feed = feedparser.parse(url)
        news_items = []
        for entry in feed.entries[:max_results]:
            news_items.append({
                "title": entry.title,
                "link": entry.link,
                "published": entry.published
            })
        return news_items
    except Exception:
        return []

def analyze_news_sentiment(news_items):
    
    sentiments = []
    count_positive = 0
    count_negative = 0
    count_neutral = 0

    
    
    for item in news_items:
        inputs = tokenizer(item['title'], return_tensors="pt", padding=True, truncation=True)
        with torch.no_grad():
            logits = model(**inputs).logits
        sentiment = logits.argmax().item()
        if sentiment == 0:
            sentiment = "negative"
            count_negative += 1
        elif sentiment == 1:
            sentiment = "neutral"
            count_neutral += 1
        else:
            sentiment = "positive"
            count_positive += 1 
        sentiments.append({
            "title": item['title'],
            "link": item['link'],
            "published": item['published'],
            "sentiment": sentiment
        })
    return sentiments, (count_positive - count_negative) / (count_positive + count_negative + count_neutral) if (count_positive + count_negative + count_neutral) > 0 else 0

if __name__ == "__main__":
    news = fetch_stock_news("AAPL")
    for item in news:
        print(f"Title: {item['title']}")
        print(f"Link: {item['link']}")
        print(f"Published: {item['published']}")
        print()
    sentiments, score = analyze_news_sentiment(news)
    print(f"\nGlobal Sentiment Score: {score:.2f}")