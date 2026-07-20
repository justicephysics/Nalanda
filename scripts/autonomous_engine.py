import os
import sys
import requests
from bs4 import BeautifulSoup
import google.generativeai as genai
from datetime import datetime

GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")
TARGET_TOPIC = os.getenv("INPUT_TOPIC") or "Gross Domestic Product (GDP)"
TARGET_FORMAT = os.getenv("INPUT_FORMAT") or "LinkedIn Professional Article Format"

if not GEMINI_API_KEY:
    print("❌ FATAL ERROR: GEMINI_API_KEY missing from system secret registers.")
    sys.exit(1)

genai.configure(api_key=GEMINI_API_KEY)

def load_core_matrix_context():
    """Ingests the structural mathematical axioms from the universal matrix ledger."""
    matrix_path = "src/universal_matrix.md"
    if not os.path.exists(matrix_path):
        print("⚠️ Matrix reference folder empty.")
        return ""
    with open(matrix_path, "r", encoding="utf-8") as file:
        return file.read()

def fetch_live_macro_news(topic_string):
    """Scrapes live real-time wire telemetry matched to the selected domain vector."""
    search_query = f"latest global {topic_string} trends analysis news 2026"
    search_url = f"https://html.duckduckgo.com/html/?q={search_query.replace(' ', '+')}"
    headers = {"User-Agent": "Mozilla/5.0 InversionControlDashboard/3.0"}
    
    try:
        response = requests.get(search_url, headers=headers, timeout=10)
        soup = BeautifulSoup(response.text, 'html.parser')
        snippets = soup.find_all('a', class_='result__snippet')
        titles = soup.find_all('a', class_='result__url')
        
        if not titles:
            return f"Baseline Status: Tracking layout limits for {topic_string}."
        
        context_pack = []
        for i in range(min(3, len(titles))):
            context_pack.append(f"Telemetry {i+1}: {titles[i].text.strip()} - {snippets[i].text.strip()}")
        return "\n".join(context_pack)
    except Exception as e:
        return f"Telemetry Bypass: Search engine tracking timeout for {topic_string}."

def compile_custom_inversion_report(news_payload, core_context, topic, format_style):
    """Compiles the targeted execution document using absolute structural constraints."""
    try:
        model = genai.GenerativeModel('gemini-3.5-flash')
        
        prompt = f"""
        [CRITICAL SYSTEM BOUNDARY & EXECUTION CONSTRAINTS]:
        - You act EXCLUSIVELY as a raw, programmatic ledger compilation machine. You do NOT function as a standard AI conversational assistant.
        - Absolutely ZERO conversational prefaces, friendly introductions, or postscripts are permitted.
        - Absolutely ZERO disclaimers regarding "mainstream consensus" or unconventionality are allowed.
        - Begin printing the requested production document IMMEDIATELY from the very first character of your output.
        
        [STRICT TYPOGRAPHY & VISUAL CLEANLINESS RULES]:
        - Absolutely ZERO long repeating strings of equals signs (====), dashes (----), or underscores (____) are allowed.
        - For structural steps or processing logs, use precise third-level Markdown headers (###) and wrap system step identifiers cleanly inside monospace tracking blocks.
          Example Format: ### `[SYSTEM_EXECUTION_STEP_01]` SECTION TITLE
        - For layout section breaks, use standard triple-dash horizontal rules (`---`) restricted to exactly three characters.

        [NATIVE VISUALIZATION & DIAGRAMMING MANDATE]:
        - You MUST integrate native Markdown visual components directly within the content steps.
        - Embed at least ONE comprehensive, native **Mermaid.js flowchart** (using ```mermaid ... ``` blocks) that visually charts out the extraction architecture, the debt ventilator pipelines, or structural barriers.
        - Embed detailed, highly clean **Markdown structural data matrices / comparison grids** to visually plot numeric variances side-by-side.

        [CORE UNIVERSAL GROUNDING LOGIC]:
        {core_context}
        
        [LIVE COMPILATION VARIABLES]:
        - Targeted Systemic Vector Query: {topic}
        - Required Presentation Layout Profile: {format_style}
        
        [REAL-TIME WIRE TELEMETRY]:
        {news_payload}
        
        [THE DEBT-OPIUM BYPASS MANDATE]:
        - When evaluating any macroeconomic parameters (especially GDP or Economic Inequality), you must integrate the "Debt-Opium Bypass Theorem."
        - Explicitly state and calculate the Opium Index: O_Index = Systemic Debt / Nominal GDP ≈ 3.50 (representing a system leveraged at 350% of its reported economic output).
        - Mathematically and textually demonstrate that because natural circulation is choked by high structural cholesterol (L_Gini ≈ 0.92, 38× capture ratio, and collapsed True Index levels), the legacy Fortune 500 / feudal architecture is on a synthetic ventilator. It is forced to inject continuous credit liquidity through this artificial debt bypass to prevent immediate systemic organ failure and total cascade collapse.
        
        [THE DEBT-OPIUM & EXAM LOTTERY BYPASS MANDATE]:
        - When evaluating the "Education & Commodity Extraction" vector, you must integrate the 2009 Algebra of the Broken Democratic Pipeline alongside the latest search engine telemetry.
        - Explicitly incorporate the Extreme Rejection Coefficients: UPSC (99.85%), JEE (99%), and NEET (98%+), proving the system focuses on elimination rather than education.
        - Frame the ₹3.5 Lakh Crore coaching ecosystem as a predatory financial extraction channel draining ancestral household wealth.
        - Ground the pathology textually and mathematically using the tragic data of over 13,000 student suicides annually, the 12,500+ examination-failure deaths (averaging >5 per day), and the clinical spread of youth hypertension and psychological batch segregation. Connect this directly to the ultimate collapse of the True Index (TI) floor.
        
        [FORMAT-SPECIFIC EXECUTION MATRIX]:
        - IF the Profile is exactly "Common Man", translate these complex calculations into a deeply relatable, humanized everyday story centered around a specific individual (e.g., Arthur). Show how their daily cost-of-living panic and credit dependencies are direct symptoms of a global economy sustained entirely by a 350% debt-opium bypass. Seamlessly weave your flowcharts and data tables directly into the narrative.
        - FOR ALL OTHER PROFILES (Ledger, Pitch, Academic, etc.), maintain the precise, highly specialized, professional institutional format requested by that profile name, formatting the Debt-Opium Bypass as a formal quantitative theorem.

        [YOUR COMPILATION DIRECTIONS]:
        1. Evaluate the real-time wire telemetry specifically regarding the selected vector domain: {topic}.
        2. Seamlessly execute and present the mathematical proofs detailed in your core universal grounding logic (The 38× Disparity Mechanism, the 103.5× NGDI execution, the True Index formulas, and the 350% Opium Bypass Index). Run the numbers transparently based on the telemetry.
        3. Produce ONE highly detailed, comprehensive, production-grade master document formatted EXCLUSIVELY to fit the requested profile layout: {format_style}.
        4. At the absolute bottom of the document, generate your explicit blocks for the CANVA INFOGRAPHIC BLUEPRINT and the VEO 3.1 CINEMATIC TEXT SCRIPT PROMPT.
        """
        
        response = model.generate_content(prompt)
        return response.text
    except Exception as e:
        print(f"❌ COMPILER ERROR: {str(e)}")
        sys.exit(1)

if __name__ == "__main__":
    print(f"🚀 Dashboard Activation Request Captured via Repository Dispatch.")
    print(f"📡 Selected Systemic Vector: {TARGET_TOPIC}")
    print(f"📋 Selected Content Destination: {TARGET_FORMAT}")
    
    core_logic = load_core_matrix_context()
    live_telemetry = fetch_live_macro_news(TARGET_TOPIC)
    
    print("🧠 Ingesting payloads into dynamic Gemini template compiler...")
    final_report = compile_custom_inversion_report(live_telemetry, core_logic, TARGET_TOPIC, TARGET_FORMAT)
    
    timestamp = datetime.now().strftime("%Y-%m-%d_%H-%M")
    clean_topic_name = "".join([c if c.isalnum() else "_" for c in TARGET_TOPIC[:15]])
    filename = f"staged_outputs/report_{clean_topic_name}_{timestamp}.md"
    
    os.makedirs("staged_outputs", exist_ok=True)
    with open(filename, "w", encoding="utf-8") as file:
        file.write(final_report)
        
    print(f"✅ SUCCESS: Formatted output successfully locked into ledger path: {filename}")
