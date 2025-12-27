import requests
import json
import time
import csv
import os
from datetime import datetime
from google.colab import drive

# ---------------------------------------------------------
# 1. CLEAN CONNECTION & PATH FINDER
# ---------------------------------------------------------
print("🔌 establishing fresh connection to Google Drive...")
drive.mount('/content/drive', force_remount=True)

# Find the correct path (Handling the "My Drive" vs "MyDrive" bug)
base_path = "/content/drive"
if os.path.exists(f"{base_path}/MyDrive"):
    FOLDER_PATH = f"{base_path}/MyDrive/JobBot"
else:
    FOLDER_PATH = f"{base_path}/My Drive/JobBot"

print(f"📂 Targeting Folder: {FOLDER_PATH}")

# Create folder immediately
if not os.path.exists(FOLDER_PATH):
    os.makedirs(FOLDER_PATH)
    print("✅ JobBot folder created!")

# ---------------------------------------------------------
# 2. FILE CREATION (The "Hard Reset")
# ---------------------------------------------------------
CSV_FILE = f"{FOLDER_PATH}/to_apply_list.csv"
HISTORY_FILE = f"{FOLDER_PATH}/job_history.json"

# Force create the CSV header
with open(CSV_FILE, 'w', encoding='utf-8') as f:
    f.write("Date Found,Role,Company,Location,URL,Status,Source\n")

# Force create the History file
with open(HISTORY_FILE, 'w') as f:
    f.write("[]")

print("✅ Files created successfully.")
print("👀 GO CHECK YOUR GOOGLE DRIVE NOW -> You should see 'JobBot' folder.")
print("waiting 10 seconds for sync...")
time.sleep(10)

# ---------------------------------------------------------
# 3. THE BOT LOGIC (Paste Keys Below!)
# ---------------------------------------------------------
# ⚠️ PASTE KEYS HERE
ADZUNA_APP_ID = "PASTE_YOUR_ID_HERE"
ADZUNA_APP_KEY = "PASTE_YOUR_KEY_HERE"
DISCORD_WEBHOOK_URL = "PASTE_YOUR_WEBHOOK_URL_HERE"
MAX_JOBS_TO_SEND = 40

# ... (Rest of logic is pre-loaded) ...

def is_clearance_job(title, url, company):
    blob = (title + " " + company).lower()
    if "clearancejobs" in url: return True
    terms = ["security clearance", "secret clearance", "ts/sci", "polygraph", "top secret"]
    return any(t in blob for t in terms)

def is_valid_role(title):
    title = title.lower()
    avoid = ["senior", "sr.", "lead", "manager", "director", "head of", "principal", "iii"]
    return not any(bad in title for bad in avoid)

def append_to_csv(job_data):
    with open(CSV_FILE, 'a', newline='', encoding='utf-8') as f:
        writer = csv.writer(f)
        writer.writerow([
            datetime.now().strftime("%Y-%m-%d"),
            job_data['title'],
            job_data['company'],
            job_data['location'],
            job_data['url'],
            "Not Applied",
            "Adzuna"
        ])

def search_adzuna(keywords, location):
    base_url = "http://api.adzuna.com/v1/api/jobs/us/search/1"
    params = {
        'app_id': ADZUNA_APP_ID, 'app_key': ADZUNA_APP_KEY,
        'results_per_page': 50, 'what': keywords,
        'what_exclude': 'clearance secret polygraph', 'where': location,
        'content-type': 'application/json'
    }
    try: return requests.get(base_url, params=params).json().get('results', [])
    except: return []

# EXECUTION
searches = [
    {"q": "System Administrator", "l": "Denver, Colorado"},
    {"q": "IT Analyst", "l": "Denver, Colorado"},
    {"q": "NOC Technician", "l": "Denver, Colorado"},
    {"q": "Junior System Administrator", "l": "United States"}
]

history = []
found_count = 0

print("🔎 Scanning job boards...")
for s in searches:
    if found_count >= MAX_JOBS_TO_SEND: break
    for job in search_adzuna(s['q'], s['l']):
        title = job.get('title', 'Unknown')
        url = job.get('redirect_url')
        company = job.get('company', {}).get('display_name', 'Unknown')
        loc = job.get('location', {}).get('display_name', 'Unknown')

        if is_valid_role(title) and not is_clearance_job(title, url, company):
            if url not in history:
                # Alert Discord
                requests.post(DISCORD_WEBHOOK_URL, json={
                    "content": "🎯 **Job Target**",
                    "embeds": [{"title": title, "description": f"**{company}** - {loc}", "url": url, "color": 3447003}]
                })
                # Save to CSV
                history.append(url)
                append_to_csv({'title':title, 'company':company, 'location':loc, 'url':url})
                found_count += 1
                time.sleep(1)
                if found_count >= MAX_JOBS_TO_SEND: break

# Save History
with open(HISTORY_FILE, 'w') as f:
    json.dump(history, f)
print(f"✅ Finished. Sent {found_count} alerts. Check Drive!")
