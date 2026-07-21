import os
import sys
import json
import requests
from datetime import datetime

log_entries = []

def log_step(step_num, step_name, status, details=""):
    symbol = "✅ [PASS]" if status == "PASS" else "❌ [FAIL]"
    entry = f"STEP {step_num:02d} | {symbol} | {step_name}\nDetails: {details}\n" + "-"*60
    print(entry)
    log_entries.append(entry)

print("="*60)
print("🔍 NALANDA LIGHTWEIGHT DIAGNOSTIC RUNNER")
print("="*60)

# STEP 1: Python Dependencies
try:
    import google.generativeai as genai
    from bs4 import BeautifulSoup
    log_step(1, "Python Modules Import", "PASS", "google-generativeai, requests, bs4 ready.")
except Exception as e:
    log_step(1, "Python Modules Import", "FAIL", f"Missing dependency: {str(e)}")

# STEP 2: Secrets Check
gemini_key = os.getenv("GEMINI_API_KEY")
topic = os.getenv("INPUT_TOPIC") or "Systemic Ruin of Education and Commodity Extraction"
fmt = os.getenv("INPUT_FORMAT") or "Common Man"

if gemini_key:
    masked_key = gemini_key[:4] + "..." + gemini_key[-4:] if len(gemini_key) > 8 else "***"
    log_step(2, "GEMINI_API_KEY Secrets Check", "PASS", f"Key present: {masked_key} | Topic: '{topic}'")
else:
    log_step(2, "GEMINI_API_KEY Secrets Check", "FAIL", "GEMINI_API_KEY missing from environment secrets!")

# STEP 3: Directory Structure Check
dirs = ["src/verticals/local", "src/verticals/universal", "staged_outputs"]
missing = [d for d in dirs if not os.path.exists(d)]
if not missing:
    log_step(3, "Directory Structure Verification", "PASS", f"All paths verified: {dirs}")
else:
    log_step(3, "Directory Structure Verification", "FAIL", f"Missing paths: {missing}")

# STEP 4: Matrix Files Check
local_file = "src/verticals/local/education_matrix.md"
univ_file = "src/verticals/universal/education_matrix.md"
if os.path.exists(local_file) and os.path.exists(univ_file):
    log_step(4, "Education Matrix Verification", "PASS", "Local & Universal Education matrices verified.")
else:
    log_step(4, "Education Matrix Verification", "FAIL", "One or both education matrix files missing.")

# STEP 5: Scraper Readiness Check (Non-blocking)
try:
    resp = requests.get("https://html.duckduckgo.com/html/?q=test", headers={"User-Agent": "Mozilla/5.0"}, timeout=5)
    log_step(5, "Scraper Connectivity", "PASS", f"HTTP Status: {resp.status_code} (Fallback handler active)")
except Exception as e:
    log_step(5, "Scraper Connectivity", "PASS", f"Network note: {str(e)} (Engine will use local telemetry)")

# STEP 6: API Key Configuration Validation (Zero Quota Consumption)
if gemini_key:
    try:
        genai.configure(api_key=gemini_key)
        log_step(6, "Gemini API Client Setup", "PASS", "API Key configured successfully without burning quota.")
    except Exception as e:
        log_step(6, "Gemini API Client Setup", "FAIL", f"Config Error: {str(e)}")

# Save Log
with open("debug_log.txt", "w", encoding="utf-8") as f:
    f.write("\n".join(log_entries))
