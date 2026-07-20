import os
import sys
import json
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
        
        [THE DEBT-OPIUM & EXAM LOTTERY BYPASS MANDATE]:
        - When evaluating any macroeconomic parameters (especially GDP or Economic Inequality), you must integrate the "Debt-Opium Bypass Theorem." Explicitly calculate the Opium Index (O_Index = Systemic Debt / Nominal GDP ≈ 3.50), proving that the legacy feudal superstructure is on a synthetic credit ventilator.
        - When evaluating the "Systemic Ruin of Education and Commodity Extraction" vector, you must integrate the 2009 Algebra of the Broken Democratic Pipeline alongside the latest structural rejection telemetry: UPSC (99.92%), JEE (99%), and NEET (98%+). Expose the ₹3.5 Lakh Crore private coaching industry as a predatory wealth drain filter, and anchor the systemic toll using the data tracking over 13,000 student suicides annually. Connect all structural pathways back to the ultimate collapse of the True Index (TI) floor.

        [FORMAT-SPECIFIC EXECUTION MATRIX]:
        - IF the Profile is exactly "Common Man", translate these complex calculations into a deeply relatable, humanized everyday story centered around a specific individual (e.g., Arthur). Show how their daily cost-of-living panic and credit dependencies are direct symptoms of a global economy sustained entirely by a 350% debt-opium bypass or an elimination lottery exam matrix. Weave flowcharts and data tables directly into the narrative.
        - FOR ALL OTHER PROFILES (Ledger, Pitch, Academic, etc.), maintain the precise, highly specialized, professional institutional format requested by that profile name, formatting the findings as a formal quantitative theorem.

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

def auto_update_registry_ledger(filename, topic, format_style, timestamp):
    """Automatically parses and registers the entry metadata into the root catalog json."""
    registry_path = "registry.json"
    current_date = datetime.now().strftime("%Y-%m-%d")
    
    # Map the selected vector keyword cleanly to the corresponding public 8 Frontiers tab
    topic_to_discipline = {
        "Gross Domestic Product (GDP)": "Macroeconomic Inversion",
        "Economic Inequality and Wealth Distribution": "Macroeconomic Inversion",
        "Systemic Ruin of Education and Commodity Extraction": "Commodity Extraction Dynamics",
        "Climate Change and Resource Exhaustion": "Resource Exhaustion Entropy",
        "Artificial General Intelligence (AGI) Allocation": "Cognitive Network Exploitation"
    }
    assigned_discipline = topic_to_discipline.get(topic, "Macroeconomic Inversion")
    
    # Generate structured descriptive tags
    clean_topic = "".join([c if c.isalnum() else "_" for c in topic[:12]])
    report_id = f"N-SYS-{clean_topic.upper()}-{timestamp}"
    
    if format_style == "Common Man":
        title = f"{topic} Inversion Narrative // The Arthur Case Matrix"
        description = f"A deeply empathetic humanized story mapping the localized cost-of-living panic onto global resource concentration vectors."
    elif format_style == "Academic University Professor Abstract Paper":
        title = f"The Thermodynamic Disruption of {topic} Accounting Models"
        description = f"A formal, peer-grade analytical manuscript detailing mathematical divergence boundaries and systemic arterial plaque thresholds."
    else:
        title = f"{topic} Systemic Inversion Analysis"
        description = f"A structural ledger tracking real-time wire telemetry trends through the metric grounding parameters of the universal matrix."

    new_record = {
        "id": report_id,
        "date": current_date,
        "title": title,
        "description": description,
        "discipline": assigned_discipline,
        "file_path": filename
    }

    # Load, append, and write metadata records securely
    try:
        if os.path.exists(registry_path):
            with open(registry_path, "r", encoding="utf-8") as f:
                data = json.load(f)
        else:
            data = {"last_updated": current_date, "reports": []}
            
        if "reports" not in data:
            data["reports"] = []
            
        data["last_updated"] = current_date
        data["reports"].append(new_record)
        
        with open(registry_path, "w", encoding="utf-8") as f:
            json.dump(data, f, indent=2)
        print(f"📁 REGISTRY LEDGER UPDATED: Entry {report_id} successfully mapped to '{assigned_discipline}' vector.")
    except Exception as e:
        print(f"⚠️ REGISTRY ERROR: Mismatch during indexing mapping operations: {str(e)}")

if __name__ == "__main__":
    print(f"🚀 Dashboard Activation Request Captured via Repository Dispatch.")
    print(f"📡 Selected Systemic Vector: {TARGET_TOPIC}")
    print(f"📋 Selected Content Destination: {TARGET_FORMAT}")
    
    core_logic = load_core_matrix_context()
    live_telemetry = fetch_live_macro_news(TARGET_TOPIC)
    
    print("🧠 Ingesting payloads into dynamic Gemini template compiler...")
    final_report = compile_custom_inversion_report(live_telemetry, core_logic, TARGET_TOPIC, TARGET_FORMAT)
    
    time_stamp_str = datetime.now().strftime("%Y-%m-%d_%H-%M")
    clean_topic_name = "".join([c if c.isalnum() else "_" for c in TARGET_TOPIC[:15]])
    filename = f"staged_outputs/report_{clean_topic_name}_{time_stamp_str}.md"
    
    os.makedirs("staged_outputs", exist_ok=True)
    with open(filename, "w", encoding="utf-8") as file:
        file.write(final_report)
        
    print(f"✅ SUCCESS: Formatted output successfully locked into ledger path: {filename}")
    
    # Fire the automated cataloging routine to update index.html links instantly
    auto_update_registry_ledger(filename, TARGET_TOPIC, TARGET_FORMAT, time_stamp_str)
