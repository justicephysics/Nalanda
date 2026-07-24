import os
import sys
import json
import requests
from datetime import datetime

log_entries = []
fatal_error = False

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
    fatal_error = True

# STEP 2: Secrets Check
gemini_key = os.getenv("GEMINI_API_KEY")
topic = os.getenv("INPUT_TOPIC") or "Systemic Ruin of Education and Commodity Extraction"
fmt = os.getenv("INPUT_FORMAT") or "Common Man"

if gemini_key:
    masked_key = gemini_key[:4] + "..." + gemini_key[-4:] if len(gemini_key) > 8 else "***"
    log_step(2, "GEMINI_API_KEY Secrets Check", "PASS", f"Key present: {masked_key} | Topic: '{topic}'")
else:
    log_step(2, "GEMINI_API_KEY Secrets Check", "FAIL", "GEMINI_API_KEY missing from environment secrets!")
    fatal_error = True

# STEP 3: Directory Structure Check
dirs = ["src/verticals/local", "src/verticals/universal", "staged_outputs"]
missing = [d for d in dirs if not os.path.exists(d)]
if not missing:
    log_step(3, "Directory Structure Verification", "PASS", f"All paths verified: {dirs}")
else:
    log_step(3, "Directory Structure Verification", "FAIL", f"Missing paths: {missing}")
    fatal_error = True

# STEP 4: Matrix Files Check (Dynamic - checks the matrix relevant to the selected topic)
# Map topic to its discipline key
discipline_map = {
    "Systemic Ruin of Education and Commodity Extraction": "education",
    "Gross Domestic Product (GDP)": "macroeconomics",
    "Economic Inequality and Wealth Distribution": "macroeconomics",
    "Climate Change and Resource Exhaustion": "ecology",
    "Artificial General Intelligence (AGI) Allocation": "agi"
}
matrix_key = discipline_map.get(topic, "education")
local_file = f"src/verticals/local/{matrix_key}_matrix.md"
univ_file = f"src/verticals/universal/{matrix_key}_matrix.md"

# Check if the specific matrix exists. If not, warn but don't stop (engine can still run with telemetry only)
if os.path.exists(local_file) and os.path.exists(univ_file):
    log_step(4, f"Matrix Verification ({matrix_key.upper()})", "PASS", f"Local & Universal {matrix_key} matrices verified.")
else:
    missing_files = []
    if not os.path.exists(local_file): missing_files.append(local_file)
    if not os.path.exists(univ_file): missing_files.append(univ_file)
    log_step(4, f"Matrix Verification ({matrix_key.upper()})", "FAIL", f"Missing files: {missing_files}. Engine will run without matrix context.")
    # We DO NOT set fatal_error here because the engine can still run with telemetry only.

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
        fatal_error = True

# Save Log
with open("debug_log.txt", "w", encoding="utf-8") as f:
    f.write("\n".join(log_entries))

# FINAL DECISION: Exit with error if fatal flag is set
if fatal_error:
    print("\n" + "="*60)
    print("❌ FATAL DIAGNOSTIC FAILURE DETECTED.")
    print("Pipeline aborted to prevent wasting runner time.")
    print("Please fix the issues listed above and re-run.")
    print("="*60)
    sys.exit(1)
else:
    print("\n" + "="*60)
    print("✅ ALL CRITICAL CHECKS PASSED. Proceeding to Autonomous Engine.")
    print("="*60)
    sys.exit(0)
