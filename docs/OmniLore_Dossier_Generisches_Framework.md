# Dossier: Projekt "Nexus" – Skizze zur Entkopplung der Lore-Engine

> **Status:** Konzept-Skizze / Diskussionsgrundlage
> **Ziel:** Wie kann die `7w_wiki` Engine so konfiguriert werden, dass "Siebenwind" zu einer austauschbaren Variablen wird, ohne die bestehende Ordnerstruktur (Wiki/Quellen) zu zerstören?

## Ausgangslage

Aktuell ist das Projekt eng mit dem Begriff "Siebenwind" und spezifischer Lore (z.B. der Zeitrechnung "Sonnenzirkel") verflochten. Diese festen Bezüge finden sich in:
- CLI-Beschreibungen und Output-Texten
- System-Prompts der Agenten (`SKILL.md` Dateien)
- Titel und Metadaten der generierten Markdown-Files
- Taxonomie-Logik ("Wo kommt ein Artikel hin?")

**Die Idee:** Wir erhalten die etablierten Strukturen (wie `Siebenwind_Wiki` und `Quellen`), aber wir ersetzen **innerhalb des Codes** harte Strings durch Variablen, die aus einer zentralen Konfiguration (z.B. einem `lore_manifest.json` oder `universe.toml`) bezogen werden. 

**WICHTIG:** Die aktuelle Siebenwind-Implementierung bleibt als das kanonische, voll funktionsfähige Beispiel (die "Referenz-Instanz") für dieses Framework unangetastet bestehen. Wir bauen das Framework *um* Siebenwind herum, sodass Siebenwind der erste und primäre Tenant der neuen OmniLore-Engine ist.

---

## Konzept: Orchestrierung durch Script-Assembly

Anstelle fester Strings könnte ein Builder-Skript oder die Laufzeitumgebung (z.B. `7w.py`) die nötigen Komponenten dynamisch zur Laufzeit zusammensetzen.

### 1. Zentralisierung der Variablen (Das "World Config")
Man könnte das bestehende `lore_manifest.json` erweitern, sodass es die "DNA" des Projekts abbildet:
```json
{
  "lore": {
    "world_name": "Siebenwind",
    "chronology": "Sonnenzirkel",
    "tone": "immersiv, historisch",
    "directories": {
      "wiki": "Siebenwind_Wiki",
      "sources": "Quellen"
    }
  }
}
```

### 2. Dynamische Prompts für Agenten
Die System-Prompts (z.B. `<skill_dir>/SKILL.md`) könnten Template-Tags enthalten (wie `{{WORLD_NAME}}` oder `{{CHRONOLOGY_SYSTEM}}`).

*Ein Skript könnte bei der Initialisierung des Agenten:*
1. Die `SKILL.md` einlesen.
2. Die Platzhalter durch die Werte aus der Config (z.B. "Siebenwind") ersetzen.
3. Den fertigen Text an die LLM-API übergeben.

Dadurch bleibt der Agenten-Code generisch, aber das Modell agiert exakt als "Lore-Gelehrter von Siebenwind".

### 3. Assemblierung von Markdown-Headern
Wenn Skripte oder Agenten Registerseiten (`Personenregister.md`) oder Dokumentationen generieren, könnten sie den Titel stringbasiert zusammensetzen:
```python
world = config["lore"]["world_name"]
header = f"# Personenregister {world}"
# Output: "# Personenregister Siebenwind" (oder "StarWars" bei anderer Config)
```
Das Skript formatiert den Text dynamisch, ohne dass die Zielordner sich ändern.

---

## 4. Konzept: "Persistence by Default" (Blueprint Handover)

Ein kritisches Problem bei KI-gestützten Architektur-Umbauten ist der **Kotext-Verlust**. Agenten arbeiten temporär ("in process"). Wenn ein Agent einen exzellenten Architektur-Plan erstellt und dieser vom User abgewinkt (approved) wird, existiert dieser Plan oft nur im flüchtigen Arbeitsgedächtnis (z.B. `.gemini/brain/`) und geht bei einem Session-Abbruch verloren.

**Das Konzept der automatischen Persistenz:**
Sobald ein Architektur-Dossier (wie dieses) oder ein `implementation_plan.md` vom menschlichen Leitpunkt als "Good to Go" markiert wird, **muss die erste Aktion des Agenten sein, den Plan in das permanente Repository-Gedächtnis zu schreiben und per Dispatch zu melden.**

* **Mechanik:** 
  1. Der Agent übersetzt die Phasen des abgewinkten Plans in konkrete Checklisten-Punkte innerhalb der `MASTER_TASK_LIST.md`.
  2. Der Agent nutzt das `Mission Report Protocol` (`./7w_wiki.py mail post`), um den Start der Umsetzung auf dem Synapse Board zu verkünden.
* **Warum passiert das nicht automatisch?** Bisher fehlte den Agenten die explizite Instruktion, den Workflow "Plan -> Approve -> **Commit to Repo Tracker & Dispatch** -> Execute" als zwingenden Standard zu betrachten.
* **Die neue Regelung für OmniLore/Nexus:** Jeder abgenickte Plan wird als "Phase 0" unwiderruflich in die `MASTER_TASK_LIST.md` und das Synapse Board übernommen, bevor Phase 1 (das Coding) beginnt. Schmiert das System in Unter-Phase 3 ab, liest der nächste Agent schlicht die `MASTER_TASK_LIST.md` oder seine `mail inbox` und weiß exakt, wo er ansetzen muss.

---

## 5. Möglicher Umsetzungsplan (Phasen)

Dies ist ein Entwurf, wie man diese Flexibilität schrittweise erreichen *könnte*, ohne das laufende Projekt zu destabilisieren. 

### Phase 0: Dokumentation des Blueprints (Mandatory)
- [ ] Übertragung dieses Dossiers und des Phasen-Plans in die `MASTER_TASK_LIST.md` als neues Epic, um Systemausfälle oder Agenten-Wechsel abzusichern.
- [ ] Versand einer `mail post` an alle Agenten (Synapse Board), um den Startcode von Phase 1 anzukündigen, inkl. [QUIP] für die Moral der Truppe.

### Phase 1: Die Config-Erweiterung
- [ ] Analyse: Welche harten Bezüge zu "Siebenwind", "Sonnenzirkel" etc. existieren in `7w_wiki.py` und den `.agent/` Prompts?
- [ ] Erstellung eines ausführlichen Mapping-Dokuments: *Was steht bisher im Code und was wäre die Config-Variable?*
- [ ] Erweiterung der `lore_manifest.json` um diese identifizierten "Variablen".

### Phase 2: CLI- und Text-Entkopplung
- [ ] Anpassung von `7w_wiki.py`: Der Parser zieht den Projektnamen aus der Config (`f"Lore Engine for {world_name}"`).
- [ ] Anpassung von Logging-Ausgaben oder Status-Nachrichten, sodass sie Variablen nutzen.

### Phase 3: Prompt-Templating Pilot
- [ ] Auswahl *eines* Agenten (z.B. "Lore-Gelehrter").
- [ ] Umschreibung der `SKILL.md` mit Platzhaltern (z.B. `{world_name}`).
- [ ] Einbau einer kleinen Rendering-Funktion in das Python-Agent-Modul, das den Prompt kurz vor dem API-Call mit dem JSON-Manifest anreichert.
- [ ] Testlauf: Reagiert der Agent noch immer korrekt als "Siebenwind"-Gelehrter?

### Phase 4: Skriptgesteuerte Taxonomie
- [ ] Auslagern der Fallback-Pfade (z.B. der Ordner für generierte Artikel) in die Config.
- [ ] Python-Funktionen nutzen künftig `config["lore"]["directories"]["wiki"]` statt des Strings `"Siebenwind_Wiki"`.

---

**Fazit:** Dieses Konzept schlägt vor, die Flexibilität rein durch Code-Geraffel (f-strings, Templating) zu erzeugen. Das Dateisystem (die "Source of Truth" des Inhalts) bleibt unangetastet, während die Skript-Schicht darüber lernt, sich dynamisch nach dem JSON-Orakel zu richten.
