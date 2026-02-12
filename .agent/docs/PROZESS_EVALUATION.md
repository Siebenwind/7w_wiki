---
layout: wiki_page
title: PROZESS EVALUATION
category: Sonstiges
---

# PROZESS EVALUATION

**Epistemischer Status:** #perspektive

**Status:** Analyse der bisherigen Zusammenarbeit und Definition der "Antigravity-Architektur 2.0".
**Datum:** 11.02.2026
**Autor:** Antigravity Agent (Rolle: Oberarchivar)

## 1. Analyse des Status Quo

### Das Problem
Bisher war der Arbeitsfluss zu kleinteilig und reaktiv:
1.  **Schritt A:** Ich lese eine Datei.
2.  **Schritt B:** Ich aktualisiere eine Checkliste (`task.md`), dass ich sie gelesen habe.
3.  **Schritt C:** Der Nutzer muss mich erinnern: "Schreib das Wissen auch auf."
4.  **Schritt D:** Ich erstelle die Wiki-Datei.

**Schwächen:**
*   **Kein "Externes Gedächtnis":** Wissen blieb im Kontext-Fenster (Kurzzeitgedächtnis) statt sofort in `.md`-Dateien (Langzeitgedächtnis) zu landen.
*   **Zu viel Overhead:** Das ständige Aktualisieren der Task-Liste für reine Lese-Vorgänge bläht den Verlauf auf.
*   **Passivität:** Ich habe auf Anweisung gewartet, statt die Rolle des "Oberarchivars" voll auszufüllen, der *selbstständig* entscheidet, dass Wissen gespeichert werden muss.

### Die Ursache
Ich habe die `task.md` als "To-Do-Liste für Aktionen" interpretiert, statt als "Fortschrittsbalken für Ergebnisse". Der Befehl "Research" wurde als "Lesen" interpretiert, nicht als "Dokumentieren".

---

## 2. Der neue "Antigravity-Prozess" (Soll-Zustand)

Um effizienter zu arbeiten, wechseln wir von einem **Task-basierten** zu einem **Artefakt-basierten** Workflow.

### Das Prinzip: "Read-Verify-Write" (RVW-Loop)
Für jeden Punkt auf der Liste (z.B. "Phase 3: Chronik"):

1.  **Ingestion (Lesen):** Ich scanne die lokalen Dateien (z.B. `/Quellen/Zeitung 7w Bote`).
2.  **Verifikation (Web-Skill):** Ich nutze *aktiv* `search_web` (oder `read_url_content`), um zu prüfen, ob `siebenwind.de` aktuellere Infos hat (Kanon-Check).
3.  **Produktion (Schreiben):** Ich erstelle **sofort** die entsprechende Wiki-Datei in `/Siebenwind_Wiki/`.
    *   *Wichtig:* Ich frage nicht um Erlaubnis für jede Datei. Ich erstelle sie.
4.  **Logging:** Ich aktualisiere `task.md` erst, wenn das *Artefakt* (die Wiki-Seite) existiert.

### Warum "Erinnerungen" (= Dateien)?
In einer KI-Umgebung wie dieser sind Dateien mein Gedächtnis.
*   Wenn ich "Konzepte zusammenfasse", erstelle ich ab jetzt ein **Konzept-Papier** im Ordner `00_Fundament` oder `05_Archive`.
*   Ich verlasse mich nicht darauf, dass du mich erinnerst. Die Erstellung der Datei ist der Abschluss des Gedankens.

---

## 3. Evaluation der Prompts

Ich habe deine Prompts (`Archivar`, `Oberarchivar`, `Kickoff`) analysiert.

**Stärken:**
*   Klare Quellen-Hierarchie (Web > Hintergrund > Lore).
*   Gute Definition der "Skills" (die ich durch meine Tools abbilden kann).

**Verbesserungspotenzial für Antigravity:**
*   Die Prompts waren als *Start-Instruktion* gedacht. Da ich bereits laufe, muss ich diese "Identität" nun **internalisieren**.
*   Ich werde die "Skills" aus dem `Kickoff-Prompt` als mentale Makros nutzen:
    *   *Skill Explorer* -> `list_dir` & `view_file`
    *   *Skill Web-Kanon* -> `search_web` (site:siebenwind.de)
    *   *Skill Wiki-Gen* -> `write_to_file` (mit Frontmatter)

---

## 4. Nächste Schritte (Action Plan)

Ich schlage vor, sofort mit **Phase 3: Chronik-Integration** nach dem neuen RVW-Loop zu beginnen.

### Schritt 1: Struktur-Bereinigung
*   Sicherstellen, dass alle bisherigen "Gedanken" (Rassen, Religion) sauber im Wiki liegen (bereits erledigt für Rassen).

### Schritt 2: Die Chronik (Zeitung 7w Bote)
*   **Ziel:** Eine Timeline der Ereignisse erstellen.
*   **Aktion:**
    1.  Ordner `/Quellen/Zeitung 7w Bote` scannen.
    2.  Zeitliche Abfolge extrahieren.
    3.  Abgleich mit `siebenwind.de` (falls möglich via Suche).
    4.  Erstellung `04_Chronik/Zeitleiste_Jahre_X-Y.md`.

### Schritt 3: Geografie & Detail-Wissen
*   Die leeren Ordner (`02_Geografie`) füllen, indem die Regions-Dateien (die ich für die Menschen-Recherche schon gelesen habe: Galadon, Bernstein etc.) in Wiki-Artikel umgewandelt werden.

---

**Frage an den Nutzer:**
Soll ich diesen neuen Prozess direkt auf **Phase 3 (Chronik)** anwenden oder erst die **Geografie (Regionen)** vervollständigen, da ich die Daten gerade "frisch im Kopf" habe?
