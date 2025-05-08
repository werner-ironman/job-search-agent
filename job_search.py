
import pandas as pd
from datetime import datetime

# Simulated job search results (replace with real scraper logic later)
job_data = [
    {
        "Title": "IT Manager België",
        "Company": "Bedrijf A",
        "Location": "Antwerpen",
        "Link": "https://www.stepstone.be/job-a"
    },
    {
        "Title": "ICT Team Lead",
        "Company": "Bedrijf B",
        "Location": "Brussel",
        "Link": "https://www.stepstone.be/job-b"
    },
    {
        "Title": "Head of IT Operations",
        "Company": "Bedrijf C",
        "Location": "Gent",
        "Link": "https://www.stepstone.be/job-c"
    }
]

# Create DataFrame and save to CSV
df = pd.DataFrame(job_data)
timestamp = datetime.now().strftime("%Y-%m-%d")
df.to_csv(f"job_search_results_{timestamp}.csv", index=False)

print(f"Saved job search results to job_search_results_{timestamp}.csv")
