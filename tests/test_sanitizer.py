import re
import sys

def sanitize_latex_in_markdown(text):
    """
    DETERMINISTIC MULTI-PASS LATEX SANITIZER
    Achieves 100% pass rate across all 10 historical corruption patterns.
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

    # 3. FIX FOR ISSUE 2: Convert math-mode percentages ($99.92\%$ or $99.92\%$) to plain Markdown (99.92%)
    text = re.sub(r'\$\s*([\d\.]+)\s*\\?%\s*\$', r'\1%', text)

    # 4. FIX FOR ISSUE 1: Convert escaped currency dollars before numbers inside math blocks (\$42 -> 42)
    text = re.sub(r'\\\$\s*(\d+)', r'\1', text)

    # 5. Clean stray dollar signs right after \text{...} but before _, ^, or }
    text = re.sub(r'(\\text\{[^}]+\})\$([_\^}])', r'\1\2', text)

    # 6. Clean stray dollar signs BEFORE \text{...} inside subscripts/superscripts
    text = re.sub(r'(_|\^)\{\s*\$+\s*(\\text\{[^}]+\})\s*\}', r'\1{\2}', text)
    text = re.sub(r'(_|\^)\{\s*\$+\s*(\\text\{[^}]+\})\s*\$+\s*\}', r'\1{\2}', text)

    # 7. Fix Mismatched Display Math Bounds ($\text{...}$$ -> $$\text{...}$$)
    text = re.sub(r'^\$(\s*\\text\{.*?)\$\$$', r'$$\1$$', text, flags=re.MULTILINE)

    # 8. Fix Rupee currency symbol collisions (₹$1.0\text{Lakh Crore} -> ₹1.0 Lakh Crore)
    text = re.sub(r'₹\$\s*([\d\.\+]+)\s*\\text\{([^}]+)\}', r'₹\1 \2', text)
    text = re.sub(r'₹\$\s*([\d\.\+]+)', r'₹\1', text)

    # 9. Fix list item bullets missing space & opening dollar (*\text{PI} -> * $\text{PI})
    text = re.sub(r'^(\s*\*)\s*\\text\{', r'\1 $\\text{', text, flags=re.MULTILINE)

    # 10. Clean ampersands inside \text{}
    def clean_ampersands(match):
        inner = match.group(1).replace('\\&', 'and').replace('&', 'and')
        return f"\\text{{{inner}}}"
    text = re.sub(r'\\text\{([^}]*)\}', clean_ampersands, text)

    return text


# =====================================================================
# 🧪 TEST SUITE: Every Failing Pattern From Historical Sessions
# =====================================================================
TEST_CASES = [
    {
        "name": "Nested Dollar Subscript",
        "input": r"$S_{$ \text{Civilization} }$",
        "expected": r"$S_{\text{Civilization}}$"
    },
    {
        "name": "Tab Corrupted Equation",
        "input": r"$$\frac{dS_{$\ttext{Civilization}$}}{dt} \propto \frac{1}{\eta_{$\ttext{Edu}$}}$$".replace("	ext", "\ttext"),
        "expected": r"$$\frac{dS_{\text{Civilization}}}{dt} \propto \frac{1}{\eta_{\text{Edu}}}$$"
    },
    {
        "name": "Limit Corruption",
        "input": r"$$\lim_{t \to \infty} S_{\t$\ttext{Civilization}$} = \infty$$".replace("	ext", "\ttext"),
        "expected": r"$$\lim_{t \to \infty} S_{\text{Civilization}} = \infty$$"
    },
    {
        "name": "Integral Subscript Corruption",
        "input": r"$$\int_{\t$\ttext{Node}$_{\t$\ttext{Low}$}}^{\t$\ttext{Node}$_{\t$\ttext{High}$}} \Psi_{\t$\ttext{Potential}$} \, dN = \t\text{Constant}$$".replace("	ext", "\ttext"),
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
        "input": r"transmission efficiency ($\eta_{$\ttext{Edu}$}$)".replace("	ext", "\ttext"),
        "expected": r"transmission efficiency ($\eta_{\text{Edu}}$)"
    },
    {
        "name": "Inner Currency Dollar in Math Range",
        "input": r"($12\text{B}\text{--}\$42\text{B USD}$)",
        "expected": r"($12\text{B}\text{--}42\text{B USD}$)"
    },
    {
        "name": "Math Mode Percentage Simplification",
        "input": r"$99.92\%$",
        "expected": r"99.92%"
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
