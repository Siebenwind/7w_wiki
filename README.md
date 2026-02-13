# ⚔️ Siebenwind Lore Engine 2.0

![Project Status](https://img.shields.io/badge/Status-Aktiv-vibrantgreen?style=for-the-badge)
![CLI](https://img.shields.io/badge/Interface-Unified_CLI-orange?style=for-the-badge)
![Intelligence](https://img.shields.io/badge/AI-Agnostic_Connectable-purple?style=for-the-badge)

Das zentrale Intelligenz-Framework für die Welt von Siebenwind. Dieses Projekt ist nicht nur ein Wiki, sondern eine **standardisierte Lore-Engine**, die 20 Jahre Rollenspielgeschichte durch KI-gestützte Architektur vereint.

---

## 🏛️ Projekt-Dokumentation

| Dokument | Fokus |
| :--- | :--- |
| 📜 **[Changelog](CHANGELOG.md)** | **Evolution & Meilensteine.** |
| ✅ **[Master Task List](MASTER_TASK_LIST.md)** | **Zukunft & Strategischer Fokus.** |
| 📊 **[Wiki Statistiken](Siebenwind_Wiki/10_Archiv/Wiki_Statistiken.md)** | **Lore-Dichte & KPI-Dashboard.** |

---

## 🚀 Unified CLI: Die Schnittstelle `7w.py`

Wir haben alle Intelligenz-Tools in einer zentralen Schnittstelle gebündelt. Dies erlaubt eine nahtlose Integration mit externen Anwendungen (wie dem **Gemini CLI**) oder Shell-Automatisierungen.

### 📚 Nutzung
```bash
# Semantische Lore-Suche (Das Orakel)
./7w.py search "Wer war Benedict Rabenfels?"

# Wiki-Statistiken generieren
./7w.py stats

# Konsistenz-Audit ausführen
./7w.py audit

# Index-Wartung
./7w.py index --status
```

---

## 🏗️ Architektur & Portabilität

Das Projekt folgt einer **AI-Agnostischen Philosophie**. Während es für den *Oberarchivar* (Google Antigravity) optimiert ist, nutzt es strikte Markdown-Standards und entkoppelte Python-Tools, um mit jedem modernen LLM-Framework kompatibel zu sein.

### Verzeichnis-Struktur (Standardized)
- **`/Siebenwind_Wiki/`**: Das funktionale Herz – 100% Markdown-Wiki.
- **`/.agent/`**: Das "Gehirn" – Enthält Workflows, Skills und Prompts.
- **`/7w.py`**: Der Unified Entry-Point für Agenten und User.
- **`/docs/`**: Virtuelle Referenzen (Symlinks) für das MkDocs-Hosting, um Konflikte zwischen Repo-Struktur und Web-Präsentation zu vermeiden.

---

## 🧠 Intelligence Integration

Dieses Repository ist darauf ausgelegt, als **Wissens-Plugin** für KI-Agenten zu fungieren. Durch virtuelle Verweise und standardisierte Metadata (YAML) im Wiki kann das System:
1.  **Semantisch navigieren** (Orakel).
2.  **Epistemisch validieren** (Wahrheitshierarchie #canon bis #perspektive).
3.  **Proaktiv reparieren** (Audit & Repair).

---

## 💻 Deployment & Vorschau

Lokal via MkDocs Material:
```bash
pip install mkdocs-material
mkdocs serve
```

---
> [!IMPORTANT]
> **Für Agenten & Entwickler:** Dieses Projekt nutzt ein virtuelles Verweissystem (`docs/`), um Dokumentations-Stubs von funktionalen Dateien zu trennen. Bearbeite immer die Master-Dateien im Root oder Wiki-Ordner.

*© 2026 Siebenwind Chronisten-Gilde | Engineered for Intelligence*

