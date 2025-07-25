import os
from dotenv import load_dotenv
import requests
import trafilatura
load_dotenv() 

def search_news(query: str, country: str = "in") -> str:
    """
    Searches recent news articles related to a specific query using NewsData.io API.
    """
    api_key = os.getenv("NEWSDATA_API_KEY")  # or load via os.getenv
    url = f"https://newsdata.io/api/1/news?apikey={api_key}&q={query}&country={country}&language=en"

    response = requests.get(url)
    if response.status_code != 200:
        return f"❌ Failed to fetch news: {response.status_code} - {response.text}"

    data = response.json()
    if not data.get("results"):
        return "ℹ️ No relevant news found."

    summaries = []
    for article in data["results"][:5]:  # Limit to top 5
        title = article.get("title", "No Title")
        link = article.get("link", "No Link")
        source = article.get("source_id", "Unknown Source")
        pub_date = article.get("pubDate", "No Date")
        summaries.append(f"📰 **{title}**\n🕒 {pub_date}\n🔗 {link}\n📢 Source: {source}\n")

    return "\n".join(summaries)


def extract_news_content(url: str) -> str:
    downloaded = trafilatura.fetch_url(url)
    if not downloaded:
        return "❌ Couldn’t fetch the article."
    content = trafilatura.extract(downloaded, include_images=False)
    return content[:1500] if content else "⚠️ No readable content found."

