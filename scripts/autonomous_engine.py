import os
import sys
import requests
from bs4 import BeautifulSoup
import google.generativeai as genai
from datetime import datetime

GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")
# Capture the dynamic dropdown variables forwarded from the website dashboard UI
TARGET_TOPIC = os.getenv("INPUT_TOPIC", "Gross Domestic Product (GDP)")
TARGET_FORMAT = os.getenv("INPUT_FORMAT", "LinkedIn Professional Article Format")

if not GEMINI_API_KEY:
    print("❌ FATAL ERROR: GEMINI_API_KEY missing from system secret registers.")
    sys.exit(1)

genai.configure(api_key=GEMINI_API_KEY)

def load_core_matrix_context():
    """Shakes hands with the universal core blueprint architecture inside the separate folder."""
    matrix_path = "src/universal_matrix.md"
    if not os.path.exists(matrix_path):
        print("⚠️ Matrix reference folder empty. Initializing fallback variables.")
        return "TI = (PI+EI+SI)*(PI*EI*SI) with 0.70 cliff. NGDI = 103.5. 38x disparity mechanism."
    
    with open(matrix_path, "r", encoding="utf-8") as file:
        return file.read()

def fetch_live_macro_news(topic_string):
    """Step 1: Scrape live real-time news explicitly matched to your selected dropdown vector."""
    # Build clean query URL string based directly on your choice
    search_query = f"latest global {topic_string} trends analysis news 2026"
    search_url = f"https://html.duckduckgo.com/html/?q={search_query.replace(' ', '+')}"
    headers = {"User-Agent": "Mozilla/5.0 InversionControlDashboard/3.0"}
    
    try:
        response = requests.get(search_url, headers=headers, timeout=10)
        soup = BeautifulSoup(response.text, 'html.parser')
        snippets = soup.find_all('a', class_='result__snippet')
        titles = soup.find_all('a', class_='result__url')
        
        if not titles:
            return f"Baseline Status: Standard extraction models continue tracking layout limits for {topic_string}."
        
        context_pack = []
        for i in range(min(3, len(titles))):
            context_pack.append(f"Telemetry {i+1}: {titles[i].text.strip()} - {snippets[i].text.strip()}")
        return "\n".join(context_pack)
    except Exception as e:
        return f"Telemetry Bypass: Search engine tracking timeout for {topic_string}."

def compile_custom_inversion_report(news_payload, core_context, topic, format_style):
    """Step 2: Force Gemini to output a deeply targeted execution text matching the exact selected format."""
    try:
        model = genai.GenerativeModel('gemini-3.5-flash')
        
        prompt = f"""
        You are the core processing engine for the Universal Metric Inversion Matrix.
        
        [CORE UNIVERSAL GROUNDING LOGIC]:
        {core_context}
        
        [LIVE COMPILATION VARIABLES]:
        - Targeted Systemic Vector Query: {topic}
        - Required Presentation Layout Profile: {format_style}
        
        [REAL-TIME WIRE TELEMETRY]:
        {news_payload}
        
        [YOUR STRICT COMPILATION DIRECTIONS]:
        1. Evaluate this live news telemetry specifically regarding the selected vector: {topic}.
        2. Apply the exact mathematical proofs from your core universal grounding logic (The True Index formula, the 38x Cancer Mechanism parameters, and the 103.5x NGDI index).
        3. Do NOT invent new equations. Apply your universal structural laws directly to audit the current news.
        4. Produce ONE comprehensive, high-fidelity production document formatted EXCIUSIVELY to fit the requested profile layout: {format_style}.
        5. At the absolute bottom of the report, ALWAYS generate an explicit block containing:
           - A custom visual infographic blueprint layout configuration for CANVA.
           - An explicit cinematic text visual script prompt ready to be pasted directly into the VEO 3.1 video engine in your Google AI Pro account.
        """
        
        response = model.generate_content(prompt)
        return response.text
    except Exception as e:
        print(f"❌ COMPILER ERROR: {str(e)}")
        sys.exit(1)

if __name__ == "__main__":
    print(f"🚀 Dashboard Activation Request Captured.")
    print(f"📡 Selected Systemic Vector: {TARGET_TOPIC}")
    print(f"📋 Selected Content Destination: {TARGET_FORMAT}")
    
    core_logic = load_core_matrix_context()
    live_telemetry = fetch_live_macro_news(TARGET_TOPIC)
    
    print("🧠 Ingesting payloads into dynamic Gemini template compiler...")
    final_report = compile_custom_inversion_report(live_telemetry, core_logic, TARGET_TOPIC, TARGET_FORMAT)
    
    # Clean file saving sequence
    timestamp = datetime.now().strftime("%Y-%m-%d_%H-%M")
    clean_topic_name = "".join([c if c.isalnum() else "_" for c in TARGET_TOPIC[:15]])
    filename = f"staged_outputs/report_{clean_topic_name}_{timestamp}.md"
    
    os.makedirs("staged_outputs", exist_ok=True)
    with open(filename, "w", encoding="utf-8") as file:
        file.write(final_report)
        
    print(f"✅ SUCCESS: Formatted output successfully locked into ledger path: {filename}")
