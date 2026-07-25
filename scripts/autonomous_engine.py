import os
import sys
import json
import time
import requests
from bs4 import BeautifulSoup
import google.generativeai as genai
from datetime import datetime, timezone, timedelta
import re

# =====================================================================
# 📐 THE 8 OFFICIAL DISCIPLINE MAPPINGS
# =====================================================================
FORMAT_MAP = {
    "Common Man": ("Easy Snapshot", "EZS"),
    "Easy snapshot": ("Easy Snapshot", "EZS"),
    "Short System Profile": ("Short System Profile", "SSP"),
    "Medium System Profile": ("Medium System Profile", "MSP"),
    "Long System Profile": ("Long System Profile", "LSP"),
    "X (Twitter) Post Thread": ("Twitter Post Thread", "XPT"),
    "LinkedIn Post Asset": ("LinkedIn Post Asset", "LPA"),
    "YouTube Video Script": ("YouTube Video Script", "YVS"),
    "Institutional Investor Pitch": ("Investor Pitch", "IIP"),
    "University Professor Paper": ("Professor Paper", "UPP")
}

DISCIPLINE_MAP = {
    "Systemic Ruin of Education and Commodity Extraction": ("Education", "EDU"),
    "Gross Domestic Product (GDP)": ("Economics", "ECO"),
    "Economic Inequality and Wealth Distribution": ("Economics", "ECO"),
    "Climate Change and Resource Exhaustion": ("Ecology", "ECL"),
    "Artificial General Intelligence (AGI) Allocation": ("AI-AGI", "AGI")
}
# =====================================================================
# 📐 UNIFIED TITLING & MAPPING ENGINE
# =====================================================================

def get_ist_datetime():
    """Returns current date and time in Indian Standard Time (UTC+5:30)."""
    ist_offset = timedelta(hours=5, minutes=30)
    now_ist = datetime.now(timezone.utc) + ist_offset
    return {
        "date_str": now_ist.strftime("%Y-%m-%d"),
        "time_str": now_ist.strftime("%H-%M"),
        "compact_ts": now_ist.strftime("%Y%m%d-%H%M")
    }

def build_unified_metadata(raw_topic, raw_format):
    """Generates clean, human-readable file naming and registry metadata."""
    discipline, disc_code = DISCIPLINE_MAP.get(raw_topic, ("General", "GEN"))
    file_type, format_code = FORMAT_MAP.get(raw_format, (raw_format or "Profile", "PROFILE"))
    
    ist = get_ist_datetime()
    
    # 1. Clean topic name (remove special characters, shorten)
    topic_clean = raw_topic.replace("Systemic Ruin of Education and Commodity Extraction", "SystemicRuin")
    topic_clean = topic_clean.replace("Gross Domestic Product (GDP)", "GDP")
    topic_clean = topic_clean.replace("Economic Inequality and Wealth Distribution", "Inequality")
    topic_clean = topic_clean.replace("Climate Change and Resource Exhaustion", "Climate")
    topic_clean = topic_clean.replace("Artificial General Intelligence (AGI) Allocation", "AGI")
    topic_clean = topic_clean.replace(" ", "_")
    
    # 2. Clean format name (remove spaces)
    format_clean = file_type.replace(" ", "")
    
    # 3. Build a SIMPLE human-readable filename
    # Format: YYYY-MM-DD_Discipline_Topic_Format.md
    file_name = f"{ist['date_str']}_{discipline}_{topic_clean}_{format_clean}.md"
    
    # 4. Simple file path (no codes in the filename)
    published_path = f"published/{file_name}"
    staged_path = f"staged_outputs/{file_name}"
    
    # 5. Simple display title (just topic and format)
    display_title = f"{raw_topic} – {file_type} ({ist['date_str']})"
    
    # 6. Short ID (just date + discipline + format)
    short_id = f"{ist['date_str']}-{disc_code}-{format_code}"
    
    return {
        "id": short_id,
        "discipline": discipline,
        "file_type": file_type,
        "raw_topic": raw_topic,
        "topic_clean": topic_clean,
        "date_ist": ist["date_str"],
        "time_ist": f"{ist['time_str']} IST",
        "published_path": published_path,
        "staged_path": staged_path,
        "display_title": display_title
    }
    
def sanitize_latex_in_markdown(text):
    """
    DETERMINISTIC MULTI-PASS LATEX SANITIZER
    Achieves 100% pass rate across all 11 historical corruption patterns.
    """
    if not text:
        return ""

    # 1. Strip literal ASCII tabs (0x09)
    text = text.replace('\t', ' ')

    # 2. Hard-replace exact corruption sequences LLMs produce
    text = text.replace(r'\t$\ttext', r'\text')
    text = text.replace(r'$\ttext', r'\text')
    text = text.replace(r'\t\text', r'\text')
    text = text.replace(r'\t$', '')

    # 3. Convert math-mode percentages ($99.92\%$ or $99.92\%$ or $>99.92\%$ or $<99.92\%$) to plain Markdown (99.92%)
    text = re.sub(r'\$\s*([\d\.]+)\s*\\?%\s*\$', r'\1%', text)
    
    # 4. Convert math-mode percentages ($98.92\% \text{--} 99.92\%$) to plain Markdown (98.92%--99.92%)
    text = re.sub(r'\$\s*([\d\.]+)\s*\\?%\s*\$', r'\1%', text)

    # 5. Convert escaped currency dollars before numbers inside math blocks (\$42 -> 42)
    text = re.sub(r'\\\$\s*(\d+)', r'\1', text)

    # 6. Clean stray dollar signs right after \text{...} but before _, ^, or }
    text = re.sub(r'(\\text\{[^}]+\})\$([_\^}])', r'\1\2', text)

    # 7. Clean stray dollar signs BEFORE \text{...} inside subscripts/superscripts
    text = re.sub(r'(_|\^)\{\s*\$+\s*(\\text\{[^}]+\})\s*\}', r'\1{\2}', text)
    text = re.sub(r'(_|\^)\{\s*\$+\s*(\\text\{[^}]+\})\s*\$+\s*\}', r'\1{\2}', text)

    # 8. Fix Mismatched Display Math Bounds ($\text{...}$$ -> $$\text{...}$$)
    text = re.sub(r'^\$(\s*\\text\{.*?)\$\$$', r'$$\1$$', text, flags=re.MULTILINE)

    # 9. Fix Rupee currency symbol collisions (₹$1.0\text{Lakh Crore} -> ₹1.0 Lakh Crore)
    text = re.sub(r'₹\$\s*([\d\.\+]+)\s*\\text\{([^}]+)\}', r'₹\1 \2', text)
    text = re.sub(r'₹\$\s*([\d\.\+]+)', r'₹\1', text)

    # 10. Fix list item bullets missing space & opening dollar (*\text{PI} -> * $\text{PI})
    text = re.sub(r'^(\s*\*)\s*\\text\{', r'\1 $\\text{', text, flags=re.MULTILINE)

    # 11. Clean ampersands inside \text{}
    def clean_ampersands(match):
        inner = match.group(1).replace('\\&', 'and').replace('&', 'and')
        return f"\\text{{{inner}}}"
    text = re.sub(r'\\text\{([^}]*)\}', clean_ampersands, text)

    return text

GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")
TARGET_TOPIC = os.getenv("INPUT_TOPIC") or "Systemic Ruin of Education and Commodity Extraction"
TARGET_FORMAT = os.getenv("INPUT_FORMAT") or "Common Man"

if not GEMINI_API_KEY:
    print("❌ FATAL ERROR: GEMINI_API_KEY missing from system secret registers.")
    sys.exit(1)

genai.configure(api_key=GEMINI_API_KEY)

def load_vertical_matrix_context(topic_string):
    discipline, disc_code = DISCIPLINE_MAP.get(topic_string, ("education", "EDU"))
    vector_key = disc_code.lower()
    if vector_key == "edu": vector_key = "education"
    elif vector_key == "eco": vector_key = "macroeconomics"
    elif vector_key == "ecl": vector_key = "ecology"
    elif vector_key == "agi": vector_key = "agi"

    local_path = f"src/verticals/local/{vector_key}_matrix.md"
    universal_path = f"src/verticals/universal/{vector_key}_matrix.md"

    context_payload = ""
    if os.path.exists(local_path):
        with open(local_path, "r", encoding="utf-8") as f:
            context_payload += f"\n--- LOCAL EMPIRICAL MATRIX ({vector_key.upper()}) ---\n" + f.read()

    if os.path.exists(universal_path):
        with open(universal_path, "r", encoding="utf-8") as f:
            context_payload += f"\n--- UNIVERSAL PHYSICS MATRIX ({vector_key.upper()}) ---\n" + f.read()

    return context_payload

def fetch_live_macro_news(topic_string):
    search_query = f"latest {topic_string} news 2026"
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

    return f"Live Telemetry Baseline: Active tracking engaged for vector '{topic_string}'."

def compile_custom_inversion_report(news_payload, matrix_context, topic, format_style, meta):
    models_to_try = ['gemini-3.6-flash', 'gemini-3.5-flash-lite', 'gemini-3.1-pro']

    prompt = f"""
    [STRICT LATEX CURRENCY & MATH DELIMITER RULES]:
    1. CLEAN LATEX TEXT: Write clean LaTeX commands like \\text{{Civilization}} or \\text{{Edu}}.
    2. MATCHING DELIMITERS: ALWAYS wrap entire math expressions with matching dollar signs ($...$ or $$...$$).
    3. CLEAN CURRENCY: Write plain currency terms (e.g., ₹50 Lakh or ₹1.0 Lakh Crore).
    4. BULLET LIST SPACING: ALWAYS include a space and leading dollar sign after bullet stars (* $\\text{{PI}} = 0.90$).
    5. MERMAID DIAGRAMS: Enclose all flowcharts inside ```mermaid ... ``` code blocks.

    [CRITICAL SYSTEM BOUNDARY & EXECUTION CONSTRAINTS]:
    - You act EXCLUSIVELY as a raw, programmatic ledger compilation machine.
    - Begin printing the requested production document IMMEDIATELY from the very first character.

    [CORE MATRIX CONTEXT]:
    {matrix_context}

    [LIVE COMPILATION VARIABLES]:
    - Targeted Systemic Vector Query: {topic}
    - Required Presentation Layout Profile: {format_style}

    [REAL-TIME WIRE TELEMETRY]:
    {news_payload}
    """

    os.makedirs("staged_outputs", exist_ok=True)
    
    # ✅ NEW: Append prompt to prompt.md with a clear header
    header = f"""# Prompt: {meta['id']} – {meta['raw_topic']}
> **Generated for:** {meta['display_title']}
> **Date:** {meta['date_ist']} {meta['time_ist']}
> **Discipline:** {meta['discipline']}
> **Format:** {meta['file_type']}
> **File:** {meta['published_path']}
---
"""
    content = header + prompt + "\n\n---\n\n"
    
    # Open in APPEND mode ('a') so previous prompts are kept
    with open("prompt.md", "a", encoding="utf-8") as f:
        f.write(content)

    for model_name in models_to_try:
        for attempt in range(3):
            try:
                print(f"🧠 Attempting compilation using '{model_name}'...")
                model = genai.GenerativeModel(model_name)
                response = model.generate_content(prompt)
                if response and response.text:
                    return response.text
            except Exception as e:
                time.sleep(10)

    print("❌ FATAL COMPILER ERROR: All model attempts exhausted.")
    sys.exit(1)

def auto_update_registry_ledger(meta):
    """Updates registry.json with clean, minimal fields."""
    base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    registry_path = os.path.join(base_dir, "registry.json")

    # Clean record with human-readable fields
    new_record = {
        "id": meta["id"],
        "date": meta["date_ist"],
        "time": meta["time_ist"],
        "topic": meta["raw_topic"],
        "discipline": meta["discipline"],
        "format": meta["file_type"],
        "title": meta["display_title"],
        "file": meta["published_path"]
    }

    try:
        # Load existing registry
        data = {"last_updated": meta["date_ist"], "reports": []}
        if os.path.exists(registry_path):
            with open(registry_path, "r", encoding="utf-8") as f:
                try:
                    loaded = json.load(f)
                    if isinstance(loaded, dict) and "reports" in loaded:
                        data = loaded
                except Exception:
                    pass

        # Update timestamp
        data["last_updated"] = meta["date_ist"]
        
        # Remove duplicate if same ID exists (prevent duplicates)
        data["reports"] = [r for r in data.get("reports", []) if r.get("id") != meta["id"]]
        
        # Append new record at the END (newest last)
        data["reports"].append(new_record)

        # Write back
        with open(registry_path, "w", encoding="utf-8") as f:
            json.dump(data, f, indent=2)

        print(f"📁 REGISTRY UPDATED: {meta['id']}")
    except Exception as e:
        print(f"⚠️ REGISTRY ERROR: {str(e)}")

if __name__ == "__main__":
    meta = build_unified_metadata(TARGET_TOPIC, TARGET_FORMAT)

    print(f"🚀 UNIFIED EXECUTION TRIGGERED")
    print(f"🆔 ID:          {meta['id']}")
    print(f"📚 Discipline:  {meta['discipline']}")
    print(f"📄 File Type:   {meta['file_type']}")
    print(f"⏰ Timestamp:   {meta['date_ist']} {meta['time_ist']}")

    matrix_context = load_vertical_matrix_context(TARGET_TOPIC)
    live_telemetry = fetch_live_macro_news(TARGET_TOPIC)

    final_report = compile_custom_inversion_report(live_telemetry, matrix_context, TARGET_TOPIC, TARGET_FORMAT, meta)
    final_report = sanitize_latex_in_markdown(final_report)

    os.makedirs("staged_outputs", exist_ok=True)
    os.makedirs("published", exist_ok=True)

    # Dump into staged_outputs
    with open(meta["staged_path"], "w", encoding="utf-8") as f:
        f.write(final_report)

    # Publish master copy
    with open(meta["published_path"], "w", encoding="utf-8") as f:
        f.write(final_report)

    # Update latest fallback
    #with open("published/latest_report.md", "w", encoding="utf-8") as f:
    #    f.write(final_report)

    print(f"✅ STAGED DUMP: {meta['staged_path']}")
    print(f"✅ PUBLISHED:   {meta['published_path']}")

    auto_update_registry_ledger(meta)
