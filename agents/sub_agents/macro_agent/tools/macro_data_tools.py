import requests
from bs4 import BeautifulSoup
from datetime import datetime

def get_macro_indicators(country: str = "india", limit=25) -> str:
    url = f"https://tradingeconomics.com/{country.lower()}/indicators"
    headers = {"User-Agent": "Mozilla/5.0"}

    response = requests.get(url, headers=headers)
    if response.status_code != 200:
        return f"❌ Failed to fetch page for {country.title()}. Status code: {response.status_code}"

    soup = BeautifulSoup(response.text, "html.parser")
    table = soup.select_one("table.table-hover tbody")

    if not table:
        return f"❌ Could not locate indicator table for {country.title()}."

    rows = table.find_all("tr")
    indicators = []

    for row in rows[:limit]:
        cols = row.find_all("td")
        if len(cols) >= 7:
            indicator = cols[0].get_text(strip=True)
            last = cols[1].get_text(strip=True)
            previous = cols[2].get_text(strip=True)
            highest = cols[3].get_text(strip=True)
            lowest = cols[4].get_text(strip=True)
            unit = cols[5].get_text(strip=True)
            date = cols[6].get_text(strip=True)

            indicators.append(
                f"• **{indicator}** — {last} (Prev: {previous}, High: {highest}, Low: {lowest}, Unit: {unit}, Date: {date})"
            )

    return "\n".join(indicators)


def get_economic_calendar(country: str = "india", limit=20) -> str:
    url = f"https://tradingeconomics.com/{country.lower()}/calendar"
    headers = {"User-Agent": "Mozilla/5.0"}

    response = requests.get(url, headers=headers)
    if response.status_code != 200:
        return f"❌ Failed to fetch calendar page for {country.title()}. Status code: {response.status_code}"

    soup = BeautifulSoup(response.text, "html.parser")
    table = soup.find("table", {"id": "calendar"})
    if not table:
        return f"❌ Calendar table not found for {country.title()}."

    events = []
    for row in table.find_all("tr", recursive=False):
        if not row.has_attr("data-url"):
            continue

        cols = row.find_all("td", recursive=False)
        if len(cols) < 7:
            continue

        time = cols[0].get_text(strip=True)

        country_cell = ""
        nested_table = cols[1].find("table")
        if nested_table:
            tds = nested_table.find_all("td")
            if len(tds) > 1:
                country_cell = tds[1].get_text(strip=True)

        event_name = cols[2].find("a", class_="calendar-event")
        event = event_name.get_text(strip=True) if event_name else cols[2].get_text(strip=True)

        actual = cols[3].get_text(strip=True) or "N/A"
        previous = cols[4].get_text(strip=True) or "N/A"
        consensus = cols[5].get_text(strip=True) or "N/A"
        forecast = cols[6].get_text(strip=True) or "N/A"

        events.append(
            f"• **{event}** at {time} ({country_cell})\n  - Actual: {actual}, Forecast: {forecast}, Consensus: {consensus}, Previous: {previous}"
        )

        if len(events) >= limit:
            break

    return "\n\n".join(events) if events else f"ℹ️ No economic events found for {country.title()}."


def get_financial_news(country: str = "india", limit=10) -> str:
    url = f"https://tradingeconomics.com/ws/stream.ashx?start=0&size={limit}&c={country.lower()}"
    headers = {"User-Agent": "Mozilla/5.0"}

    try:
        response = requests.get(url, headers=headers)
        response.raise_for_status()
        news_data = response.json()

        if not news_data:
            return f"ℹ️ No financial news found for {country.title()}."

        news_items = []
        for item in news_data:
            title = item.get("title", "").strip()
            description = item.get("description", "").strip()
            timestamp = item.get("date", "")
            timestamp = datetime.fromisoformat(timestamp).strftime("%d %b %Y %I:%M %p")

            news_items.append(f"📰 **{title}**\n🕒 {timestamp}\n📝 {description}")

        return "\n\n".join(news_items)

    except Exception as e:
        return f"❌ Failed to fetch news for {country.title()}: {e}"
