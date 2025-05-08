
import pandas as pd
import json
import smtplib
import os
from datetime import datetime
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

print("🚀 Job search script gestart...")

# Simulated scraped job postings
scraped_jobs = [
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

# Load sent jobs
sent_jobs_path = "sent_jobs.json"
try:
    with open(sent_jobs_path, "r") as f:
        sent_jobs = json.load(f)
except FileNotFoundError:
    sent_jobs = []

# Filter new jobs
new_jobs = [job for job in scraped_jobs if job["link"] not in sent_jobs]
print(f"🆕 {len(new_jobs)} nieuwe vacatures gevonden.")

# Update sent jobs list
sent_jobs.extend(job["link"] for job in new_jobs)
with open(sent_jobs_path, "w") as f:
    json.dump(sent_jobs, f)

# Save to CSV
timestamp = datetime.now().strftime("%Y-%m-%d")
df = pd.DataFrame(new_jobs)
df.to_csv(f"job_search_results_{timestamp}.csv", index=False)

# Email setup
sender_email = "werner.wekhuizen@gmail.com"
receiver_email = "werner.wekhuizen@gmail.com"
app_password = os.environ.get("GMAIL_APP_PASSWORD")

# Create email content
subject = "Nieuwe IT Vacatures - Dagelijkse Update"
body = "Hallo Werner,\n\nHier zijn je nieuwe relevante vacatures van vandaag:\n\n"

for job in new_jobs:
    body += f"- {job['title']} bij {job['company']} in {job['location']}\n  Link: {job['link']}\n\n"

if not new_jobs:
    body += "Vandaag zijn er geen nieuwe vacatures gevonden die aan je criteria voldoen."

body += "\nGroeten,\nJe AI Job Agent 🤖"

# Build and send email
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

print("✅ Script voltooid.")
