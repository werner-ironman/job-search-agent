
import requests
from bs4 import BeautifulSoup
import pandas as pd
from datetime import datetime
import json
import smtplib
import os
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

print("🚀 Job search script gestart...")

# === Simulated Internal Job Source ===
internal_jobs = [
    {
        "title": "IT Manager",
        "company": "Tech Solutions",
        "location": "Hasselt",
        "link": "https://www.stepstone.be/job-itmanager-techsolutions"
    },
    {
        "title": "IT Director",
        "company": "Smart Enterprises",
        "location": "Leuven",
        "link": "https://www.vdab.be/job-itdirector-smartenterprises"
    },
    {
        "title": "Interim CIO",
        "company": "VisionTech",
        "location": "Brussel",
        "link": "https://www.indeed.be/job-interimcio-visiontech"
    }
]

# === ExecutiveSearchBelgie.be Scraper ===
def scrape_executivesearch():
    url = "https://executivesearchbelgie.be/?s=management"
    headers = {"User-Agent": "Mozilla/5.0"}
    response = requests.get(url, headers=headers)
    soup = BeautifulSoup(response.content, "html.parser")
    articles = soup.find_all("article")
    results = []
    for article in articles:
        title_tag = article.find("h2", class_="entry-title")
        summary_tag = article.find("div", class_="td-excerpt")
        link_tag = title_tag.find("a") if title_tag else None
        if title_tag and link_tag:
            results.append({
                "title": title_tag.get_text(strip=True),
                "summary": summary_tag.get_text(strip=True) if summary_tag else "",
                "link": link_tag["href"]
            })
    return results

print("🌐 Scraping ExecutiveSearchBelgie.be...")
executive_jobs = scrape_executivesearch()

# === Deduplicate ExecutiveSearch jobs ===
exec_sent_path = "executivesearch_sent.json"
try:
    with open(exec_sent_path, "r") as f:
        already_sent_exec = json.load(f)
except FileNotFoundError:
    already_sent_exec = []

new_exec_jobs = [job for job in executive_jobs if job["link"] not in already_sent_exec]
already_sent_exec.extend(job["link"] for job in new_exec_jobs)
with open(exec_sent_path, "w") as f:
    json.dump(already_sent_exec, f)

# === Deduplicate Internal jobs ===
sent_path = "internal_sent.json"
try:
    with open(sent_path, "r") as f:
        already_sent = json.load(f)
except FileNotFoundError:
    already_sent = []

new_internal_jobs = [job for job in internal_jobs if job["link"] not in already_sent]
already_sent.extend(job["link"] for job in new_internal_jobs)
with open(sent_path, "w") as f:
    json.dump(already_sent, f)

# === Email preparation ===
sender_email = "werner.wekhuizen@gmail.com"
receiver_email = "werner.wekhuizen@gmail.com"
app_password = os.environ.get("GMAIL_APP_PASSWORD")

subject = "Dagelijkse IT Job Update (inclusief ExecutiveSearch)"
body = "Hallo Werner,\n\nHier zijn je nieuwe vacatures van vandaag:\n"

if new_internal_jobs:
    body += "\n📌 Interne bronnen (bv. StepStone, Indeed):\n"
    for job in new_internal_jobs:
        body += f"- {job['title']} bij {job['company']} in {job['location']}\n  Link: {job['link']}\n"

if new_exec_jobs:
    body += "\n📌 ExecutiveSearchBelgie.be:\n"
    for job in new_exec_jobs:
        body += f"- {job['title']}\n  {job['link']}\n"

if not new_internal_jobs and not new_exec_jobs:
    body += "\nVandaag zijn er geen nieuwe vacatures gevonden."

body += "\n\nGroeten,\nJe AI Job Agent 🤖"

# Send email
message = MIMEMultipart()
message["From"] = sender_email
message["To"] = receiver_email
message["Subject"] = subject
message.attach(MIMEText(body, "plain"))

if app_password:
    try:
        print("📤 E-mail wordt verzonden via Gmail SMTP...")
        with smtplib.SMTP_SSL("smtp.gmail.com", 465) as server:
            server.login(sender_email, app_password)
            server.send_message(message)
        print("✅ E-mail succesvol verzonden!")
    except Exception as e:
        print(f"❌ Fout bij verzenden van e-mail: {e}")
else:
    print("⚠️ Geen GMAIL_APP_PASSWORD secret gevonden.")

print("✅ Script volledig voltooid.")
