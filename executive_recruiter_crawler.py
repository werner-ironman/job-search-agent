
import requests
from bs4 import BeautifulSoup
import pandas as pd
from urllib.parse import urlparse
from datetime import datetime

def get_recruiter_links():
    url = "https://executivesearchbelgie.be/?s=management"
    headers = {"User-Agent": "Mozilla/5.0"}

    print("🌐 Fetching main executive search page...")
    response = requests.get(url, headers=headers)
    soup = BeautifulSoup(response.content, "html.parser")

    articles = soup.find_all("article")
    recruiter_links = []

    for article in articles:
        a_tag = article.find("a")
        if a_tag and "href" in a_tag.attrs:
            href = a_tag["href"]
            parsed = urlparse(href)
            if parsed.netloc and "executivesearchbelgie.be" not in parsed.netloc:
                recruiter_links.append({
                    "recruiter_url": href,
                    "source_title": a_tag.get_text(strip=True)
                })

    return recruiter_links

if __name__ == "__main__":
    print("🚀 Starting executive recruiter crawler...")

    links = get_recruiter_links()

    if links:
        timestamp = datetime.now().strftime("%Y-%m-%d")
        df = pd.DataFrame(links)
        filename = f"recruiter_target_links_{timestamp}.csv"
        df.to_csv(filename, index=False)
        print(f"✅ Found {len(links)} recruiter links. Saved to {filename}")
    else:
        print("⚠️ No recruiter links found.")
