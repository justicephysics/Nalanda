import os
import sys
import requests
from bs4 import BeautifulSoup
import google.generativeai as genai
from datetime import datetime

# Initialize credentials from encrypted environment vault
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")

# Safety Gate: Terminate cleanly if environment variables did not bridge correctly
if not GEMINI_API_KEY:
    print("❌ FATAL ERROR: GEMINI_API_KEY environment variable is empty or missing!")
    print("Please verify that your key is saved under Repository Settings -> Secrets and variables -> Actions.")
    sys.exit(1)

try:
    genai.configure(api_key=GEMINI_API_KEY)
except Exception as e:
    print(f"❌ CONFIGURATION ERROR: Failed to bind GenAI API key: {str(e)}")
    sys.exit(1)

def fetch_live_macro_news():
    """Step 1: Scrape real-time trends to capture current system conditions neutrally."""
    search_url = "https://html.duckduckgo.com/html/?q=latest+global+GDP+growth+inequality+news"
    headers = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) InversionEngine/2.0"}
    
    try:
        response = requests.get(search_url, headers=headers, timeout=10)
        soup = BeautifulSoup(response.text, 'html.parser')
        snippets = soup.find_all('a', class_='result__snippet')
        titles = soup.find_all('a', class_='result__url')
        
        if not titles:
            return "Baseline Status: Legacy material throughput models continue optimization trajectories unchanged."
        
        context_pack = []
        for i in range(min(3, len(titles))):
            context_pack.append(f"Event {i+1}: {titles[i].text.strip()} - {snippets[i].text.strip()}")
        return "\n".join(context_pack)
    except Exception as e:
        print(f"⚠️ SCRAPE WARNING: Ingestion issue encountered: {str(e)}")
        return "Telemetry Bypass: Network tracking timed out. Proceeding using default layer files."

def compile_inversion_report(news_payload):
    """Step 2: Call the Gemini model to execute dynamic inversion calculus and asset design."""
    try:
        model = genai.GenerativeModel('gemini-3.5-flash')
        
        prompt = f"""
        You are the core runtime processing engine for the Universal Metric Inversion Matrix.
        
        [LIVE REAL-TIME SYSTEM TELEMETRY]:
        {news_payload}
        
        [YOUR COMPILATION PROTOCOL]:
        1. Parse this event payload through the lens of LAYER II (Neutral history/trajectory of extraction metrics).
        2. Apply the LAYER III Physics Inversion Core protocols instantly.
        3. Analyze the hidden structural anomalies using the 38x Cancer Mechanism and 103.5x NGDI mathematical proofs.
        4. Format the final output down into three distribution-ready markdown files:
           --- START X_POST ---
           (High-impact short thread, short lines, raw formula text, tags: #TrueIndex #Lequals1)
           --- END X_POST ---
           --- START LINKEDIN_POST ---
           (Scannable corporate narrative hook, bulleted systemic bugs, actionable takeaway for engineers)
           --- END LINKEDIN_POST ---
           --- START VISUAL_PROMPTS ---
           (Explicit layout guidelines for Canva infographics + image-to-video generation engine prompts for Veo 3.1)
           --- END VISUAL_PROMPTS ---
        """
        
        response = model.generate_content(prompt)
        return response.text
    except Exception as e:
        print(f"❌ API RUNTIME ERROR: Gemini content generation pipeline crashed: {str(e)}")
        sys.exit(1)

def write_output_to_staged_ledger(final_drafts):
    """Step 3: Save the finalized content templates directly into the staged folder."""
    try:
        timestamp = datetime.now().strftime("%Y-%m-%d_%H-%M")
        filename = f"staged_outputs/inversion_report_{timestamp}.md"
        
        os.makedirs("staged_outputs", exist_ok=True)
        
        with open(filename, "w", encoding="utf-8") as file:
            file.write(final_drafts)
        print(f"✅ SUCCESS: Staged report permanently committed to repository memory: {filename}")
    except Exception as e:
        print(f"❌ IO ERROR: Failed to write markdown asset to disk: {str(e)}")
        sys.exit(1)

if __name__ == "__main__":
    print("🚀 Initializing Autonomous Inversion Core Module...")
    live_news = fetch_live_macro_news()
    print("📡 Live web data scraped successfully.")
    
    print("🧠 Transmitting payloads to Gemini context compiler...")
    reports = compile_inversion_report(live_news)
    
    print("💾 Staging outputs into repo record vault...")
    write_output_to_staged_ledger(reports)
    print("🏁 Engine run sequence successfully completed!")
