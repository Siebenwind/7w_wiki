# Session Memory: Nexus Generification (OmniLore Blueprint)

**Datum:** 2026-02-20
**Status:** Abgeschlossen

## Kontext
Ziel war die Entkopplung der Lore Engine von Siebenwind-spezifischen Hardcodierungen, um das Framework generisch nutzbar zu machen ("Nexus"), während Siebenwind als kanonisches Beispiel erhalten bleibt.

## Umsetzung & Änderungen
1. **Config-Erweiterung:** `lore_manifest.json` um ein `lore`-Objekt mit Welt-Definitionen (`world_name`, `directories`) ergänzt.
2. **Setup nexus_config:** Zentrales Modul (`.agent/scripts/nexus_config.py`) geschaffen, um Variablen einheitlich an alle Skripte durchzureichen.
3. **CLI-Entkopplung:** `7w_wiki.py` greift auf das `nexus_config` zu, um CLI-Texte dynamisch zu generieren.
4. **Agenten Prompt-Templating:** Einführung eines `.tpl` Compilers in `compile_skills.py` implementiert und am Skill `Lore-Gelehrter` getestet.
5. **Skript-Taxonomie:** `generate_wiki_indices.py`, `generate_wiki_stats.py`, `register_check.py`, `wiki_sanitizer.py` und `advisor.py` (Kanon-Mission) wurden bereinigt und auf die neuen Variablen (`WIKI_DIR`, `WORLD_NAME`) umgestellt.
6. **Task List & Changelog:** EPIC in die Projekthistorie (v3.1) verschoben und Changelog aktualisiert.

## Validierung
- Vollständige Entkopplung: Orakel, CLI, Skripte arbeiten unbeeinträchtigt.
- Skripte können nun blind für neue Lore-Räume (Directories) arbeiten.
- `audit`, `stats`, `tech --manifest`, `test` und `archive rotate` erfolgreich in der Handover-Phase ausgeführt.

## Offene Punkte
- (Ggf.) Ein Live-Dry-Run mit einer Dummy-Welt zur abschließenden Demo-Sicherheit.
