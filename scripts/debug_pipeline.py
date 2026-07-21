import os
import sys
import json
import requests
from bs4 import BeautifulSoup
from datetime import datetime

# Initialize Debug Log Buffer
log_entries = []

def log_step(step_num, step_name, status, details=""):
    symbol = "✅ [PASS]" if status == "PASS" else "❌ [FAIL]"
    entry = f"STEP {step_num:02d} | {symbol} | {step_name}\nDetails: {details}\n" + "-"*60
    print(entry)
    log_entries.append(entry)

print("="*60)
print("🔍 NALANDA SYSTEM DIAGNOSTIC RUNNER")
print("="*60)

# ---------------------------------------------------------
# STEP 1: Python Environment & Installed Modules
# ---------------------------------------------------------
try:
    import google.generativeai as genai
    log_step(1, "Python Modules Import", "PASS", "google-generativeai, requests, bs4 successfully imported.")
except Exception as e:
    log_step(1, "Python Modules Import", "FAIL", f"Missing dependency: {str(e)}")

# ---------------------------------------------------------
# STEP 2: Environment Variables Verification
# ---------------------------------------------------------
gemini_key = os.getenv("GEMINI_API_KEY")
topic = os.getenv("INPUT_TOPIC") or "Systemic Ruin of Education and Commodity Extraction"
fmt = os.getenv("INPUT_FORMAT") or "Common Man"

if gemini_key:
    masked_key = gemini_key[:4] + "..." + gemini_key[-4:] if len(gemini_key) > 8 else "***"
    log_step(2, "GEMINI_API_KEY Environment Variable", "PASS", f"Key present: {masked_key} | Topic: '{topic}' | Format: '{fmt}'")
else:
    log_step(2, "GEMINI_API_KEY Environment Variable", "FAIL", "GEMINI_API_KEY is missing or empty in environment secrets!")

# ---------------------------------------------------------
# STEP 3: Directory Structure Check
# ---------------------------------------------------------
dirs_to_check = [
    "src/verticals/local",
    "src/verticals/universal",
    "staged_outputs"
]
missing_dirs = []
for d in dirs_to_check:
    if not os.path.exists(d):
        missing_dirs.append(d)

if not missing_dirs:
    log_step(3, "Directory Structure Verification", "PASS", f"All required directories exist: {dirs_to_check}")
else:
    log_step(3, "Directory Structure Verification", "FAIL", f"Missing directories: {missing_dirs}")

# ---------------------------------------------------------
# STEP 4: Education Matrix Markdown Files Check
# ---------------------------------------------------------
local_file = "src/verticals/local/education_matrix.md"
univ_file = "src/verticals/universal/education_matrix.md"

local_exists = os.path.exists(local_file)
univ_exists = os.path.exists(univ_file)

if local_exists and univ_exists:
    local_size = os.path.getsize(local_file)
    univ_size = os.path.getsize(univ_file)
    log_step(4, "Education Matrix Files Verification", "PASS", 
             f"Local matrix ({local_size} bytes) & Universal matrix ({univ_size} bytes) both found.")
else:
    details = f"Local matrix found: {local_exists} ({local_file}) | Universal matrix found: {univ_exists} ({univ_file})"
    log_step(4, "Education Matrix Files Verification", "FAIL", details)

# ---------------------------------------------------------
# STEP 5: Web Scraping Engine Test (DuckDuckGo Telemetry)
# ---------------------------------------------------------
try:
    search_url = "https://html.duckduckgo.com/html/?q=NEET+exam+paper+leak+protests+2026"
    headers = {"User-Agent": "Mozilla/5.0 InversionControlDashboard/3.0"}
    resp = requests.get(search_url, headers=headers, timeout=8)
    if resp.status_code == 200:
        soup = BeautifulSoup(resp.text, 'html.parser')
        snippets = soup.find_all('a', class_='result__snippet')
        log_step(5, "Web Telemetry Scraper Connection", "PASS", f"DuckDuckGo returned 200 OK. Snippets found: {len(snippets)}")
    else:
        log_step(5, "Web Telemetry Scraper Connection", "FAIL", f"HTTP Status Code: {resp.status_code}")
except Exception as e:
    log_step(5, "Web Telemetry Scraper Connection", "FAIL", f"Connection Error: {str(e)}")

# ---------------------------------------------------------
# STEP 6: Gemini API Model Connection Test
# ---------------------------------------------------------
if gemini_key:
    try:
        genai.configure(api_key=gemini_key)
        # Testing API with lightweight model call
        model = genai.GenerativeModel('gemini-1.5-flash')
        response = model.generate_content("Ping test. Respond with 'PONG'.")
        if response and response.text:
            log_step(6, "Gemini API Model Connection", "PASS", f"Model Response: {response.text.strip()}")
        else:
            log_step(6, "Gemini API Model Connection", "FAIL", "API responded but output text was empty.")
    except Exception as e:
        log_step(6, "Gemini API Model Connection", "FAIL", f"Gemini API Error: {str(e)}")
else:
    log_step(6, "Gemini API Model Connection", "FAIL", "Skipped because GEMINI_API_KEY is missing.")

# ---------------------------------------------------------
# STEP 7: Registry Database File (`registry.json`) Check
# ---------------------------------------------------------
reg_file = "registry.json"
if os.path.exists(reg_file):
    try:
        with open(reg_file, "r", encoding="utf-8") as f:
            data = json.load(f)
        reports_count = len(data.get("reports", []))
        log_step(7, "registry.json Validation", "PASS", f"registry.json is valid JSON. Existing reports count: {reports_count}")
    except Exception as e:
        log_step(7, "registry.json Validation", "FAIL", f"JSON parsing error: {str(e)}")
else:
    log_step(7, "registry.json Validation", "FAIL", "registry.json does not exist in root directory!")

# ---------------------------------------------------------
# Save Results to debug_log.txt
# ---------------------------------------------------------
log_content = "\n".join(log_entries)
with open("debug_log.txt", "w", encoding="utf-8") as f:
    f.write(f"NALANDA DIAGNOSTIC REPORT - {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
    f.write("="*60 + "\n")
    f.write(log_content)

print("\n📄 Diagnostic report saved to 'debug_log.txt'.")
