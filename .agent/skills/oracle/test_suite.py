#!/usr/bin/env python3
# =============================================================================
# Das Orakel – Verifikations-Suite
# Führt definierte Testsuchen aus, um die Qualität des RAG-Systems zu prüfen.
# =============================================================================
import subprocess
import sys
from pathlib import Path

SCRIPT_DIR = Path(__file__).resolve().parent
SEARCH_SCRIPT = SCRIPT_DIR / "search.py"
PYTHON_BIN = sys.executable

TEST_CASES = [
    {
        "name": "Faktencheck (Kanon)",
        "query": "Wer ist Tiamat?",
        "expected": ["Göttin", "Leben", "Schöpfung"],
        "args": ["--top", "3"]
    },
    {
        "name": "Geografie-Suche",
        "query": "Was liegt im Süden von Falandrien?",
        "expected": ["Süden", "Steppe", "Wüste", "Har'ol", "Tarkas"],
        "args": ["--source", "wiki"]
    },
    {
        "name": "Assoziative Suche (Lore)",
        "query": "Der dunkle König",
        "expected": ["Schatten", "Herrscher", "Böse", "Dämon"],
        "args": ["--no-rerank"]
    }
]

def run_test(test):
    print(f"\n🧪 Test: {test['name']}")
    print(f"   Query: \"{test['query']}\"")
    
    cmd = [PYTHON_BIN, str(SEARCH_SCRIPT), test["query"]] + test.get("args", []) + ["--raw"]
    
    try:
        result = subprocess.run(cmd, capture_output=True, text=True, check=True)
        output = result.stdout.lower()
        
        found = []
        missing = []
        for keyword in test["expected"]:
            if keyword.lower() in output:
                found.append(keyword)
            else:
                missing.append(keyword)
        
        # Bewertung
        if found:
            print(f"   ✅ Gefunden: {', '.join(found)}")
        
        if missing:
            print(f"   ⚠️  Vermisst: {', '.join(missing)}")
            
        if not found and missing:
            print("   ❌ KEINE relevanten Keywords gefunden!")
            return False
            
        return True
        
    except subprocess.CalledProcessError as e:
        print(f"   ❌ Fehler bei Ausführung: {e}")
        return False

def main():
    print("╔═══════════════════════════════════════════════════╗")
    print("║   Das Orakel – System-Verifikation               ║")
    print("╚═══════════════════════════════════════════════════╝")
    
    passed = 0
    for test in TEST_CASES:
        if run_test(test):
            passed += 1
            
    print(f"\n📊 Ergebnis: {passed}/{len(TEST_CASES)} Tests erfolgreich.")

if __name__ == "__main__":
    main()
