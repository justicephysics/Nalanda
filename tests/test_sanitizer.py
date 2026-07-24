import re
import sys

def sanitize_latex_in_markdown(text):
    """
    DETERMINISTIC MULTI-PASS LATEX SANITIZER
    Cleans all tab corruptions, nested dollar signs, currency collisions, 
    and orphan delimiters before KaTeX or GitHub renders the file.
    """
    if not text:
        return ""

    # Pass 1: Eliminate literal ASCII tabs (\t) and corrupted '\t$ext' / '\t\text' sequences
    text = text.replace('\t', ' ')
    text = re.sub(r'\\?\s*\$?\\?\s*(?:text|ext)\{', r'\\text{', text)

    # Pass 2: Strip nested dollar signs inside subscripts/superscripts
    # Fixes: _{$ \text{Edu} $} or _{$\text{Edu}$} -> _{\text{Edu}}
    text = re.sub(r'(_|\^)\{\s*\$+\s*\\text\{([^}]+)\}\s*\$*\}', r'\1{\\text{\2}}', text)
    text = re.sub(r'(_|\^)\{\s*\$+\s*([a-zA-Z0-9]+)\s*\$*\}', r'\1{\2}', text)

    # Pass 3: Clean display math $$...$$ blocks containing internal single '$' signs
    def de_nest_display_math(match):
        inner = match.group(1).replace('$', '')
        return f"$${inner}$$"
    text = re.sub(r'\$\$(.*?)\$\$', de_nest_display_math, text, flags=re.DOTALL)

    # Pass 4: Fix Rupee & Currency collisions (₹$50\text{Lakh} -> ₹50 Lakh)
    text = re.sub(r'₹\$\s*([\d\.\+]+)\s*\\text\{([^}]+)\}', r'₹\1 \2', text)
    text = re.sub(r'₹\$\s*([\d\.\+]+)', r'₹\1', text)

    # Pass 5: Fix unspaced list item bullet starts (*\text{PI} -> * $\text{PI})
    text = re.sub(r'^(\s*\*\s*)\\text\{', r'\1$\\text{', text, flags=re.MULTILINE)

    # Pass 6: Fix mismatched display math bounds ($\text{...}$$ -> $$\text{...}$$)
    text = re.sub(r'^\$\s*(\\text\{.*?\}|\\[a-zA-Z]+.*?)\s*\$\$$', r'$$\1$$', text, flags=re.MULTILINE)

    # Pass 7: Fix lines starting with \text{} lacking an opening $
    text = re.sub(r'^(\\text\{[^}\n]+\}\s*[\approx\=].*?)\$', r'$\1$', text, flags=re.MULTILINE)

    # Pass 8: Wrap orphan \text{} commands in prose with single $
    text = re.sub(r'(?<!\$)\\text\{([^}]+)\}(?!\$)', r'$\text{\1}$', text)

    # Pass 9: Clean ampersands inside \text{}
    def clean_ampersands(match):
        inner = match.group(1).replace('\\&', 'and').replace('&', 'and')
        return f"\\text{{{inner}}}"
    text = re.sub(r'\\text\{([^}]*)\}', clean_ampersands, text)

    return text


# =====================================================================
# 🧪 TEST SUITE: Every Failing Pattern From Yesterday's Sessions
# =====================================================================
TEST_CASES = [
    {
        "name": "Nested Dollar Subscript",
        "input": r"$S_{$ \text{Civilization} }$",
        "expected": r"$S_{\text{Civilization}}$"
    },
    {
        "name": "Tab Corrupted Equation",
        "input": r"$$\frac{dS_{$	ext{Civilization}$}}{dt} \propto \frac{1}{\eta_{$	ext{Edu}$}}$$".replace("	ext", "\ttext"),
        "expected": r"$$\frac{dS_{\text{Civilization}}}{dt} \propto \frac{1}{\eta_{\text{Edu}}}$$"
    },
    {
        "name": "Limit Corruption",
        "input": r"$$\lim_{t \to \infty} S_{\t$	ext{Civilization}$} = \infty$$".replace("	ext", "\ttext"),
        "expected": r"$$\lim_{t \to \infty} S_{\text{Civilization}} = \infty$$"
    },
    {
        "name": "Integral Subscript Corruption",
        "input": r"$$\int_{\t$	ext{Node}$_{\t$	ext{Low}$}}^{\t$	ext{Node}$_{\t$	ext{High}$}} \Psi_{\t$	ext{Potential}$} \, dN = \t\text{Constant}$$".replace("	ext", "\ttext"),
        "expected": r"$$\int_{\text{Node}_{\text{Low}}}^{\text{Node}_{\text{High}}} \Psi_{\text{Potential}} \, dN = \text{Constant}$$"
    },
    {
        "name": "Rupee Symbol Collision",
        "input": r"₹$1.0\text{Lakh Crore} to ₹$3.5\text{Lakh Crore}",
        "expected": r"₹1.0 Lakh Crore to ₹3.5 Lakh Crore"
    },
    {
        "name": "Bullet List Item Missing Space & Opening Dollar",
        "input": r"*\text{PI} = 0.90$",
        "expected": r"* $\text{PI} = 0.90$"
    },
    {
        "name": "Mismatched Display Math Bounds",
        "input": r"$\text{TI} = (\text{PI} +\text{EI} +\text{SI}) \times (\text{PI} \times\text{EI} \times\text{SI})$$",
        "expected": r"$$\text{TI} = (\text{PI} +\text{EI} +\text{SI}) \times (\text{PI} \times\text{EI} \times\text{SI})$$"
    },
    {
        "name": "Orphan Subscript in Text",
        "input": r"transmission efficiency ($\eta_{$	ext{Edu}$}$)".replace("	ext", "\ttext"),
        "expected": r"transmission efficiency ($\eta_{\text{Edu}}$)"
    }
]

def run_tests():
    print("==================================================")
    print("🚀 RUNNING LOCAL SANITIZER TEST SUITE")
    print("==================================================\n")
    
    passed = 0
    failed = 0

    for idx, test in enumerate(TEST_CASES, 1):
        output = sanitize_latex_in_markdown(test["input"])
        
        # Normalize whitespace for comparison
        clean_out = " ".join(output.split())
        clean_exp = " ".join(test["expected"].split())

        if clean_out == clean_exp:
            print(f"✅ PASS [{idx}/{len(TEST_CASES)}]: {test['name']}")
            passed += 1
        else:
            print(f"❌ FAIL [{idx}/{len(TEST_CASES)}]: {test['name']}")
            print(f"   Input:    {repr(test['input'])}")
            print(f"   Output:   {repr(output)}")
            print(f"   Expected: {repr(test['expected'])}\n")
            failed += 1

    print("\n==================================================")
    print(f"RESULTS: {passed} Passed, {failed} Failed")
    print("==================================================")
    
    if failed > 0:
        sys.exit(1)

if __name__ == "__main__":
    run_tests()
