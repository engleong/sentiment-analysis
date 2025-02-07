import requests
from datetime import datetime, timedelta
from transformers import pipeline

finbert = pipeline("text-classification", model="ProsusAI/finbert")

# --- Configuration ---

# Replace with your actual NewsAPI API key
NEWS_API_KEY = "0cd13d0cd3444de69d1fcd3e0e33c2c4"

# URL for fetching news (using 'everything' to allow date filtering)
NEWS_API_URL = "https://newsapi.org/v2/everything"

def check_news(start_date, end_date, keywords):
    """
    Fetches news articles from a specific date and scans for keywords and sentiment.
    """
    params = {
        "apiKey": NEWS_API_KEY,
        "language": "en",
        "q": " OR ".join(keywords),  # Search for any of the keywords
        "from": start_date,        # Start date for the query
        "to": end_date,          # End date for the query (same day)
        "sortBy": "relevancy",      # Get the most relevant news
        "pageSize": 20              # Number of articles per request
    }
    news_items = []  # List to store news items

    try:
        response = requests.get(NEWS_API_URL, params=params)
        data = response.json()

        if data.get("status") != "ok":
            print("Error fetching news:", data.get("message"))
            return

        articles = data.get("articles", [])
        for article in articles:
            title = article.get("title", "")
            description = article.get("description", "")
            content = f"{title} {description}"

            # Perform sentiment analysis
            # sentiment = sid.polarity_scores(content)
            # compound_score = sentiment.get("compound", 0)
            result = finbert(content)
            print(f'result={result}')
            sentiment = result[0]['label']
            score = result[0]['score']

            # Append the news item to the list
            if (sentiment == 'positive' or sentiment == 'negative'):
                news_items.append({
                    "title": title,
                    "description": description,
                    "sentiment": sentiment,
                    "score": score
                })

    except Exception as e:
        print("An error occurred:", e)
    
    return news_items

def main():
    # Default to today's date unless a different date is specified
    START_DATE = "2025-02-06"  # Change this to your desired date (YYYY-MM-DD)
    END_DATE = "2025-02-06"  # Change this to your desired date (YYYY-MM-DD)

    # Keywords to monitor (modify this list as needed)
    KEYWORDS = ["SPX", "QQQ", "Fed", "Nasdaq", "Dow"]

    print(f"Checking news for {START_DATE} - {END_DATE} - {KEYWORDS}...")
    news_items = check_news(START_DATE, END_DATE, KEYWORDS)

    for item in news_items:
        print(f"Title: {item['title']}")
        print(f"Description: {item['description']}")
        print(f"Sentiment Label: {item['label']}")
        print(f"Sentiment Score: {item['score']}\n")

if __name__ == "__main__":
    main()

