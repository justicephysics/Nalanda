import os
import sys
import json
import requests
from bs4 import BeautifulSoup
import google.generativeai as genai
from datetime import datetime

GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")
TARGET_TOPIC = os.getenv("INPUT_TOPIC") or "Systemic Ruin of Education and Commodity Extraction"
TARGET_FORMAT = os.getenv("INPUT_FORMAT") or "Common Man"

if not GEMINI_API_KEY:
    print("❌ FATAL ERROR: GEMINI_API_KEY missing from system secret registers.")
    sys.exit(1)

genai.configure(api_key=GEMINI_API_KEY)

def get_vector_key(topic_string):
    """Maps the topic string from dashboard.html to its vertical file key."""
    topic_map = {
        "Systemic Ruin of Education and Commodity Extraction": "education",
        "Gross Domestic Product (GDP)": "macroeconomics",
        "Economic Inequality and Wealth Distribution": "inequality",
        "Climate Change and Resource Exhaustion": "ecology",
        "Artificial General Intelligence (AGI) Allocation": "agi"
    }
    return topic_map.get(topic_string, "education")

def load_vertical_matrix_context(topic_string):
    """
    Loads BOTH the Local Empirical Matrix and Universal Physics Matrix 
    for the selected vertical from src/verticals/local/ and src/verticals/universal/.
    """
    vector_key = get_vector_key(topic_string)
    
    local_path = f"src/verticals/local/{vector_key}_matrix.md"
    universal_path = f"src/verticals/universal/{vector_key}_matrix.md"
    
    context_payload = ""
    
    if os.path.exists(local_path):
        with open(local_path, "r", encoding="utf-8") as f:
            context_payload += f"\n--- LOCAL EMPIRICAL MATRIX ({vector_key.upper()}) ---\n" + f.read()
            print(f"✅ Loaded Local Matrix: {local_path}")
    else:
        print(f"⚠️ Local matrix missing at {local_path}")

    if os.path.exists(universal_path):
        with open(universal_path, "r", encoding="utf-8") as f:
            context_payload += f"\n--- UNIVERSAL PHYSICS MATRIX ({vector_key.upper()}) ---\n" + f.read()
            print(f"✅ Loaded Universal Matrix: {universal_path}")
    else:
        print(f"⚠️ Universal matrix missing at {universal_path}")
        
    return context_payload

def fetch_live_macro_news(topic_string):
    """Scrapes live real-time wire telemetry matched to the selected domain vector."""
    search_query = f"latest {topic_string} paper leak protests news 2026"
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
        for i in range(min(4, len(titles))):
            context_pack.append(f"Telemetry {i+1}: {titles[i].text.strip()} - {snippets[i].text.strip()}")
        return "\n".join(context_pack)
    except Exception as e:
        return f"Telemetry Bypass: Search engine tracking timeout for {topic_string}."

def compile_custom_inversion_report(news_payload, matrix_context, topic, format_style):
    """Compiles the targeted execution document using absolute structural constraints."""
    try:
        model = genai.GenerativeModel('gemini-2.5-flash')
        
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
        - Embed at least ONE comprehensive, native **Mermaid.js flowchart** (using ```mermaid ... ``` blocks) that visually charts out the extraction architecture or structural barriers.
        - Embed detailed, highly clean **Markdown structural data matrices / comparison grids** to visually plot numeric variances side-by-side.

        [CORE MATRIX CONTEXT (LOCAL + UNIVERSAL DUAL SYNTHESIS)]:
        {matrix_context}
        
        [LIVE COMPILATION VARIABLES]:
        - Targeted Systemic Vector Query: {topic}
        - Required Presentation Layout Profile: {format_style}
        
        [REAL-TIME WIRE TELEMETRY]:
        {news_payload}

        [FORMAT-SPECIFIC EXECUTION MATRIX]:
        - IF the Profile is "Common Man", translate these calculations into a deeply relatable, humanized everyday story centered around a student or family navigating the education system. Weave flowcharts and data tables directly into the narrative.
        - FOR ALL OTHER PROFILES (Ledger, Pitch, Academic, etc.), maintain the precise, highly specialized, professional institutional format requested by that profile name, formatting the findings as a formal quantitative theorem.

        [YOUR COMPILATION DIRECTIONS]:
        1. Evaluate the real-time wire telemetry specifically regarding the selected vector domain: {topic}.
        2. Synthesize BOTH the Local Empirical Matrix and Universal Physics Matrix provided in the context.
        3. Produce ONE highly detailed, comprehensive, production-grade master document formatted EXCLUSIVELY to fit the requested profile layout: {format_style}.
        4. At the absolute bottom of the document, generate your explicit blocks for the CANVA INFOGRAPHIC BLUEPRINT and the VEO 3.1 CINEMATIC TEXT SCRIPT PROMPT.
        """
        
        response = model.generate_content(prompt)
        return response.text
    except Exception as e:
        print(f"❌ COMPILER ERROR: {str(e)}")
        sys.exit(1)

def auto_update_registry_ledger(filename, topic, format_style, timestamp):
    """Automatically parses and registers the entry metadata into root registry.json."""
    registry_path = "registry.json"
    current_date = datetime.now().strftime("%Y-%m-%d")
    
    topic_to_discipline = {
        "Systemic Ruin of Education and Commodity Extraction": "Commodity Extraction Dynamics",
        "Gross Domestic Product (GDP)": "Macroeconomic Inversion",
        "Economic Inequality and Wealth Distribution": "Macroeconomic Inversion",
        "Climate Change and Resource Exhaustion": "Resource Exhaustion Entropy",
        "Artificial General Intelligence (AGI) Allocation": "Cognitive Network Exploitation"
    }
    assigned_discipline = topic_to_discipline.get(topic, "Commodity Extraction Dynamics")
    
    clean_topic = "".join([c if c.isalnum() else "_" for c in topic[:12]])
    report_id = f"N-SYS-{clean_topic.upper()}-{timestamp}"
    
    title = f"{topic} Inversion Analysis // {format_style}"
    description = f"Dual-synthesis (Local + Universal) structural master document evaluated under real-time wire telemetry."

    new_record = {
        "id": report_id,
        "date": current_date,
        "title": title,
        "description": description,
        "discipline": assigned_discipline,
        "file_path": filename
    }

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
    print(f"🚀 Dynamic Modular Execution Triggered.")
    print(f"📡 Selected Systemic Vector: {TARGET_TOPIC}")
    print(f"📋 Selected Target Profile: {TARGET_FORMAT}")
    
    matrix_context = load_vertical_matrix_context(TARGET_TOPIC)
    live_telemetry = fetch_live_macro_news(TARGET_TOPIC)
    
    print("🧠 Ingesting payloads into dynamic Gemini template compiler...")
    final_report = compile_custom_inversion_report(live_telemetry, matrix_context, TARGET_TOPIC, TARGET_FORMAT)
    
    time_stamp_str = datetime.now().strftime("%Y-%m-%d_%H-%M")
    clean_topic_name = "".join([c if c.isalnum() else "_" for c in TARGET_TOPIC[:15]])
    filename = f"staged_outputs/report_{clean_topic_name}_{time_stamp_str}.md"
    
    os.makedirs("staged_outputs", exist_ok=True)
    with open(filename, "w", encoding="utf-8") as file:
        file.write(final_report)
        
    print(f"✅ SUCCESS: Formatted output successfully locked into ledger path: {filename}")
    auto_update_registry_ledger(filename, TARGET_TOPIC, TARGET_FORMAT, time_stamp_str)
