import os
import sys
import json
import time
import requests
from bs4 import BeautifulSoup
import google.generativeai as genai
from datetime import datetime
import re

def sanitize_latex_in_markdown(markdown_text):
    """
    Self-healing LaTeX sanitizer for Python backend:
    1. Fixes ASCII tab-corrupted \text commands (\t	ext{ -> \text{)
    2. Fixes ASCII tab-corrupted \text commands (\t$	ext{ -> \text{)
    3. Strips nested dollars in subscripts: _{$...$} -> _{\text{...}}
    3. Replaces & with 'and' inside \text{}
    """
    if not markdown_text:
        return ""
    
    text = markdown_text

    # 1. Repair tab/space corrupted \text commands
    text = re.sub(r'\\?[\t\s]*ext\{', r'\\text{', text)

    # 2. Strip nested dollars from subscripts
    text = re.sub(r'(_|\^)\{\s*\$+', r'\1{', text)
    text = re.sub(r'\$+\s*\}', '}', text)

    # 3. Strip inner dollars from \text{$...$}
    text = re.sub(r'\\text\{\s*\$([^$]+)\$\s*\}', r'\\text{\1}', text)

    # 4. Clean ampersands inside \text{}
    def clean_text_block(match):
        inner = match.group(1)
        inner = inner.replace('$', '')
        inner = inner.replace('\\&', 'and').replace('&', 'and')
        return f"\\text{{{inner}}}"

    text = re.sub(r'\\text\{([^}]*)\}', clean_text_block, text)

    # 5. Fix orphan \text{} in prose
    text = re.sub(r'(?<!\$)\\text\{([^}]+)\}(?!\$)', r'$\text{\1}$', text)

    return text

GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")
TARGET_TOPIC = os.getenv("INPUT_TOPIC") or "Systemic Ruin of Education and Commodity Extraction"
TARGET_FORMAT = os.getenv("INPUT_FORMAT") or "Common Man"

if not GEMINI_API_KEY:
    print("❌ FATAL ERROR: GEMINI_API_KEY missing from system secret registers.")
    sys.exit(1)

genai.configure(api_key=GEMINI_API_KEY)

def get_vector_key(topic_string):
    topic_map = {
        "Systemic Ruin of Education and Commodity Extraction": "education",
        "Gross Domestic Product (GDP)": "macroeconomics",
        "Economic Inequality and Wealth Distribution": "inequality",
        "Climate Change and Resource Exhaustion": "ecology",
        "Artificial General Intelligence (AGI) Allocation": "agi"
    }
    return topic_map.get(topic_string, "education")

def load_vertical_matrix_context(topic_string):
    vector_key = get_vector_key(topic_string)
    local_path = f"src/verticals/local/{vector_key}_matrix.md"
    universal_path = f"src/verticals/universal/{vector_key}_matrix.md"
    
    context_payload = ""
    if os.path.exists(local_path):
        with open(local_path, "r", encoding="utf-8") as f:
            context_payload += f"\n--- LOCAL EMPIRICAL MATRIX ({vector_key.upper()}) ---\n" + f.read()
            print(f"✅ Loaded Local Matrix: {local_path}")

    if os.path.exists(universal_path):
        with open(universal_path, "r", encoding="utf-8") as f:
            context_payload += f"\n--- UNIVERSAL PHYSICS MATRIX ({vector_key.upper()}) ---\n" + f.read()
            print(f"✅ Loaded Universal Matrix: {universal_path}")
            
    return context_payload

def fetch_live_macro_news(topic_string):
    search_query = f"latest {topic_string} paper leak protests news 2026"
    search_url = f"https://html.duckduckgo.com/html/?q={search_query.replace(' ', '+')}"
    headers = {"User-Agent": "Mozilla/5.0 InversionControlDashboard/3.0"}
    
    try:
        response = requests.get(search_url, headers=headers, timeout=8)
        if response.status_code == 200:
            soup = BeautifulSoup(response.text, 'html.parser')
            snippets = soup.find_all('a', class_='result__snippet')
            titles = soup.find_all('a', class_='result__url')
            
            if titles:
                context_pack = []
                for i in range(min(4, len(titles))):
                    context_pack.append(f"Telemetry {i+1}: {titles[i].text.strip()} - {snippets[i].text.strip()}")
                return "\n".join(context_pack)
    except Exception as e:
        print(f"⚠️ Telemetry fetch skipped: {str(e)}")
        
    return f"Live Telemetry Baseline: Active tracking engaged for vector '{topic_string}' matching 2026 state variables."

def dump_prompt_audit_file(prompt_text):
    try:
        with open("prompt.md", "w", encoding="utf-8") as f:
            f.write(prompt_text)
            
        os.makedirs("staged_outputs", exist_ok=True)
        with open("staged_outputs/latest_prompt.md", "w", encoding="utf-8") as f:
            f.write(prompt_text)
            
        print("📝 PROMPT AUDIT DUMP SUCCESS: Prompt written to 'prompt.md' and 'staged_outputs/latest_prompt.md'.")
    except Exception as e:
        print(f"⚠️ PROMPT AUDIT DUMP FAILED: {str(e)}")

def compile_custom_inversion_report(news_payload, matrix_context, topic, format_style):
    models_to_try = ['gemini-3.6-flash', 'gemini-3.5-flash-lite', 'gemini-3.1-pro']
    
    prompt = f"""
    [STRICT LATEX & GRAPHICS CONSTRAINTS - ZERO-ERROR ENFORCEMENT]:
    1. NO NESTED DOLLAR SIGNS: Never place a '$' inside an existing math block or inside subscripts/superscripts.
       - WRONG: $S_{{\\text{{Civilization}}}}$ with internal dollar signs
       - CORRECT: $S_{{\\text{{Civilization}}}}$ or $$\\frac{{dS_{{\\text{{Civilization}}}}}}{{dt}}$$
    2. CLEAN SUB-SCRIPTS: Write clean subscripts like $S_{{\\text{{Civilization}}}}$ or $\\eta_{{\\text{{Edu}}}}$ without internal '$' signs.
    3. NO AMPERSANDS IN \\text{{}}: Inside \\text{{}} blocks, NEVER use '&' or '\\&'. Always spell out the word 'and'.
    4. NO ORPHAN \\text{{}} IN PROSE: Every \\text{{}} command MUST be enclosed inside math delimiters ($...$ or $$...$$).
    5. INLINE MATH IN LISTS: Inside bulleted or numbered lists, use ONLY compact inline math ($...$) on the exact same line as the bullet text.
    6. BLOCKQUOTES FOR SLOGANS: Format all slogans, quotes, and street demands as standard Markdown Blockquotes (e.g., > "Education is Not a Commodity").
    7. MERMAID DIAGRAMS: Enclose all flowcharts inside ```mermaid ... ``` code blocks.
    
    [CRITICAL SYSTEM BOUNDARY & EXECUTION CONSTRAINTS]:
    - You act EXCLUSIVELY as a raw, programmatic ledger compilation machine.
    - Absolutely ZERO conversational prefaces, friendly introductions, or postscripts are permitted.
    - Begin printing the requested production document IMMEDIATELY from the very first character of your output.

    [CORE MATRIX CONTEXT (LOCAL + UNIVERSAL DUAL SYNTHESIS)]:
    {matrix_context}
    
    [LIVE COMPILATION VARIABLES]:
    - Targeted Systemic Vector Query: {topic}
    - Required Presentation Layout Profile: {format_style}
    
    [REAL-TIME WIRE TELEMETRY]:
    {news_payload}

    [YOUR COMPILATION DIRECTIONS]:
    1. Synthesize BOTH the Local Empirical Matrix and Universal Physics Matrix provided in the context.
    2. Produce ONE highly detailed, comprehensive, production-grade master document formatted EXCLUSIVELY to fit the requested profile layout: {format_style}.
    3. Include Mermaid.js flowcharts and Markdown data comparison tables.
    """

    dump_prompt_audit_file(prompt)

    for model_name in models_to_try:
        for attempt in range(3):
            try:
                print(f"🧠 Attempting compilation using '{model_name}' (Attempt {attempt+1}/3)...")
                model = genai.GenerativeModel(model_name)
                response = model.generate_content(prompt)
                if response and response.text:
                    return response.text
            except Exception as e:
                err_str = str(e)
                if "429" in err_str or "quota" in err_str.lower():
                    print(f"⏳ Rate limit encountered. Pausing 15 seconds before retry...")
                    time.sleep(15)
                else:
                    print(f"⚠️ Model {model_name} failed: {err_str[:100]}... Trying next option.")
                    break

    print("❌ FATAL COMPILER ERROR: All model attempts exhausted due to API limits or availability.")
    sys.exit(1)

def auto_update_registry_ledger(filename, topic, format_style, timestamp):
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
    description = f"Dual-synthesis (Local + Universal) master document evaluated under real-time telemetry."

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
        print(f"📁 REGISTRY LEDGER UPDATED: Entry {report_id} mapped to '{assigned_discipline}'.")
    except Exception as e:
        print(f"⚠️ REGISTRY ERROR: {str(e)}")

if __name__ == "__main__":
    print(f"🚀 Dynamic Modular Execution Triggered.")
    print(f"📡 Selected Vector: {TARGET_TOPIC}")
    print(f"📋 Selected Profile: {TARGET_FORMAT}")
    
    matrix_context = load_vertical_matrix_context(TARGET_TOPIC)
    live_telemetry = fetch_live_macro_news(TARGET_TOPIC)
    
    final_report = compile_custom_inversion_report(live_telemetry, matrix_context, TARGET_TOPIC, TARGET_FORMAT)
    
    # Run Self-Heal Sanitizer
    final_report = sanitize_latex_in_markdown(final_report)
    
    time_stamp_str = datetime.now().strftime("%Y-%m-%d_%H-%M")
    clean_topic_name = "".join([c if c.isalnum() else "_" for c in TARGET_TOPIC[:15]])
    filename = f"staged_outputs/report_{clean_topic_name}_{time_stamp_str}.md"
    
    os.makedirs("staged_outputs", exist_ok=True)
    with open(filename, "w", encoding="utf-8") as file:
        file.write(final_report)
        
    print(f"✅ SUCCESS: Formatted output locked into ledger path: {filename}")
    auto_update_registry_ledger(filename, TARGET_TOPIC, TARGET_FORMAT, time_stamp_str)
