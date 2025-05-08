
import requests
from bs4 import BeautifulSoup
import pandas as pd
from datetime import datetime
import json

# URL for management job search
url = "https://executivesearchbelgie.be/?s=management"

# Set user agent header
headers = {
    "User-Agent": "Mozilla/5.0"
}

# Perform GET request
response = requests.get(url, headers=headers)
soup = BeautifulSoup(response.content, "html.parser")

# Extract article elements
articles = soup.find_all("article")

# Parse job listings
vacatures = []
for article in articles:
    title_tag = article.find("h2", class_="entry-title")
    summary_tag = article.find("div", class_="td-excerpt")
    link_tag = title_tag.find("a") if title_tag else None

    if title_tag and link_tag:
        vacatures.append({
            "title": title_tag.get_text(strip=True),
            "summary": summary_tag.get_text(strip=True) if summary_tag else "",
            "link": link_tag["href"]
        })

# Deduplicate using saved links
sent_path = "executivesearch_sent.json"
try:
    with open(sent_path, "r") as f:
        already_sent = json.load(f)
except FileNotFoundError:
    already_sent = []

# Filter new jobs only
nieuwe_vacatures = [v for v in vacatures if v["link"] not in already_sent]

# Save new sent links
already_sent.extend(v["link"] for v in nieuwe_vacatures)
with open(sent_path, "w") as f:
    json.dump(already_sent, f)

# Save new jobs to CSV
timestamp = datetime.now().strftime("%Y-%m-%d")
csv_path = f"executivesearch_vacatures_{timestamp}.csv"
df = pd.DataFrame(nieuwe_vacatures)
df.to_csv(csv_path, index=False)

# Optional print for GitHub Actions logs
print(f"✅ {len(nieuwe_vacatures)} nieuwe vacatures gevonden op executivesearchbelgie.be")
