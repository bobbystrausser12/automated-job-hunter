#Automated Job Market Intelligence Tool

## 🚀Project Overview 
The tool is a Python based automation pipeline that aggregates and filters for specific IT infrastructure roles. This tool can bridge the gap from high volume job boards to real time notification systems so you can react to new postings in under one second.

## 🛠️Technology Stack 
- Language: Python 3.10+ 
- APIs: Adzuna Job Search API 
- Integration: Discord Webhook (JSON payloads) 
- Data handling: pandas, requests, csv (Google drive integration)

## ⚙️Key Features 
### 1. Smart Filtering: 
- Logic gates: automatically exclude roles that say "senior", "manager", and "clearance required" to find junior/associate level positions.
- Keyword targeting: search for jobs with keywords "system administrator", "noc technician", and "linux support".

### 2. Deduplication engine: 
- maintain a json based history file so the same job will never be alerted again.

### 3. Persistence layer: 
- automatically generate and update a csv tracking file (to_apply_list.csv) for managing your application lifecycle.

### 4. Real Time Alerting: 
- send discord webhook embeds with rich text immediately after finding a job.

## 📦How It Works 
1. Extract: query the adzuna api for jobs in certain geographic areas (ie. denver co).

2. Transform: take raw json data, parse it, remove jobs that don't meet your requirements (eg. remove TS/SCI or Principal jobs), etc.

3. Load: valid jobs get sent to you through discord, also add them to your persistent csv log.

## 🔧Setup 
In order to run this locally, you'll need to set up the following environment variables:
```python
ADZUNA_APP_ID = "YOUR_ID"
ADZUNA_APP_KEY = "YOUR_KEY"
DISCORD_WEBHOOK_URL = "YOUR_WEBHOOK"
