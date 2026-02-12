---
layout: wiki_page
title: WORKFLOW ANTIGRAVITY
category: Sonstiges
---

# WORKFLOW ANTIGRAVITY

**Epistemischer Status:** #perspektive

**Status:** Aktiv (Revision 12.02.2026)
**Rolle:** Siebenwind Oberarchivar
**Ziel:** Autonome, artefakt-basierte Wissens-Konsolidierung.

## 1. Definierte Skills (Mental Macros)

Diese Skills sind abstrakte Fähigkeiten, die durch konkrete Tool-Calls abgebildet werden.

### Skill: `Scanner` (Ingestion)
*   **Trigger:** Neue Phase oder unbekanntes Thema.
*   **Aktion:** Liest Verzeichnisinhalte (`list_dir`) und relevante Dateien (`view_file`).
*   **Ziel:** Aufbau von temporärem Kontext-Wissen.

### Skill: `Kanon-Wächter` (Verification)
*   **Trigger:** Bevor Wissen festgeschrieben wird.
*   **Aktion:** Prüft Fakten gegen `siebenwind.de` (`search_web` site:siebenwind.de).
*   **Ziel:** Widersprüche zwischen alten Daten und neuem Web-Kanon auflösen.

### Skill: `Wiki-Schmied` (Production)
*   **Trigger:** Wissen ist verifiziert.
*   **Aktion:** Erstellt `.md` Dateien im Wiki-Ordner (`write_to_file`).
*   **Format:**
    ```markdown
    ---
    layout: wiki_page
    title: [Titel]
    category: [Kategorie]
    status: [Kanon/Legende]
    ---
    # [Titel]
    ...
    ```

## 2. Der "RVW-Loop" (Workflow)

Dies ist der Standard-Prozess für jede Wissens-Einheit (Region, Rasse, Ereignis).

1.  **READ (Lesen):**
    *   Lese Quelldatei (z.B. `Region Galadon`).
    *   Extrahiere Entitäten (z.B. "Fürstentum Herder").

2.  **VERIFY (Verifizieren):**
    *   *Check:* Gibt es dazu neuere Infos auf der Homepage?
    *   *Entscheidung:* Web-Infos überschreiben lokale Infos.

3.  **WRITE (Schreiben):**
    *   Erstelle `Siebenwind_Wiki/[Kategorie]/[Name].md`.
    *   Verlinke verwandte Themen (`[[Link]]`).

4.  **FORGET (Abschließen):**
    *   Markiere Task als erledigt.
    *   Lösche temporäres Wissen aus dem Fokus (indem der Task gewechselt wird).

---

## 3. Temporäres Wissen (Cache) - Status: PENDING

Folgende Konzepte befinden sich aktuell im Kontext ("Kopf") des Agenten und müssen in Artefakte ("Papier") überführt werden:

### Aus `Region Galadon.html`:
*   [ ] **Grenzland Falkenstein:** Handelstor zum Süden, Markgraf Salman di Seregatto.
*   [ ] **Fürstentum Herder:** Militärisch, Kornkammer, Fürst Vanagard.
*   [ ] **Herzogtum Bernstein:** Königsland, Hauptstadt Draconis.
*   [ ] **Fürstentum Malthust:** Bergbau, verarmt, neuer Fürst Kasimier.
*   [ ] **Fürstentum Ossian:** Seehandel, Schiffbau, Fürstin Asodayr.
*   [ ] **Fürstentum Tiefenwald:** Waldelfen-Bezug, Holz, Edwin von Tiefenwald.
*   [ ] **Baronie Kadamark:** Holz, Handwerk, Baron Siegfried.
*   [ ] **Baronie Kettel:** Tradition, Textil (Librasulus), Baron Kelfor.
*   [ ] **Baronie Ravel:** Orkenland, Sumpf, Baronin Luvaril.
*   [ ] **Grafschaft Ersont:** Militär, Garnisonen, Graf Gernod.
*   [ ] **Grafschaft Lichtenfeld:** Schafe, Auenelfen, Graf Feestar.
*   [ ] **Grafschaft Rothschild:** Werften, Fluss Drac, Graf Patrick.
*   [ ] **Herzogtum Sae:** Wissen, Magie, Herzog Bellodor.
*   [ ] **Herzogtum Savaro:** Landwirtschaft, Seilerei, Herzogin Almut.
*   [ ] **Baronie Gerdenwald:** Halblinge, Hügelau, Baron Friedward.
*   [ ] **Grafschaft Papin:** Dreist, seehandel, Graf (unbekannt im Textfile?).
*   [ ] **Baronie Wallenburg:** Edelsteine, Reichtum, Baronin Yeroma.
*   [ ] **Baronie Morthum:** Bergbau, Krankheiten (Necris), Baron Vitallus.
*   [ ] **Grenzland Khalandra:** Barbaren, Orks, Norden.
*   [ ] **Grenzland Morgenthau:** Wall, wenig besiedelt.

### Aus `Das Adelssystem.md`:
*   [ ] **System:** Unterscheidung Hochadel vs. Blutsadel vs. Dienstadel.

### Aus `Die Kirche der Viere.md`:
*   [ ] **Struktur:** Orden, Rolle im Alltag.
