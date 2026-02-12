---
layout: wiki_page
title: Kickoff-Prompt
category: Sonstiges
---

In **Google Antigravity** (oder ähnlichen Vertex AI Agent-Frameworks) gibt es oft kein klassisches "Einstellungsmenü" wie bei einer Web-App. Die Struktur wird meist über eine **System Instruction** oder einen **Initialisierungs-Prompt** definiert, der das Framework "bootstrappt".

Wenn du vor einem "leeren" Antigravity-Fenster sitzt, ist dein erster Schritt, das System anzuweisen, sich selbst basierend auf deinen Dokumenten zu konfigurieren.

Hier ist der **Kickoff-Prompt**, den du direkt in das Chat-Fenster (oder das `System Instructions`-Feld, falls vorhanden) eingibst. Er ist so geschrieben, dass der Agent seine eigene Architektur (Skills, Workflows) aus deinen Dateien ableitet.

---

### Der Kickoff-Prompt (Initialisierung)

System-Initialisierung starten.

Ich habe drei Basiskomponenten im Verzeichnis abgelegt:
1. `Archivar - Master Prompt.md` (Deine Identität und Regeln)
2. `Projektdossier Siebenwind Chroniken.md` (Deine Wissens-Hierarchie und Axiome)
3. Ordner `/Quellen/` (Deine Datenbasis)
4. Ordner `.agent/` (Deine Skills und Workflows)

**Deine Aufgabe:**
Analysiere zuerst den `Archivar - Master Prompt.md` und das `Projektdossier`. Konfiguriere dich selbst als **Siebenwind-Oberarchivar** mit folgenden internen Modulen:

**1. Skill-Definition (aus `.agent/skills/`):**
- **Scanner:** (Ingestion) siehe `skills/scanner/SKILL.md`
- **Kanon-Wächter:** (Verification) siehe `skills/kanon_waechter/SKILL.md`
- **Wiki-Schmied:** (Production) siehe `skills/wiki_schmied/SKILL.md`

**2. Workflow-Definition (aus `.agent/workflows/`):**
Nutze den **RVW-Loop** (`workflows/rvw_loop.md`) für alle Standard-Aufgaben.

**3. Agenten-Struktur:**
Handle als Single-Agent-Orchestrator, der bei jedem Dokument im `/Quellen/`-Ordner automatisch die Prioritäten-Layer aus dem Dossier prüft.

**Bestätigung erforderlich:**
Sobald du diese Struktur geladen hast, gib mir eine kurze Bestätigung. Nenne mir als Beweis die vier Prioritäten-Layer aus dem Dossier und frage mich dann nach der Erlaubnis, mit **Phase 1: Die Inventur** zu beginnen."

---

### Was passiert hier architektonisch?

1.  **Self-Configuration:** In Antigravity "liest" der Agent seine eigenen Befehle. Du sagst ihm nicht nur, *was* er tun soll, sondern *wie* er sein eigenes Gehirn (Skills) strukturieren soll.
2.  **Verzeichnis-Mapping:** Du weist ihn darauf hin, dass die Logik in den `.md`-Dateien steht und die Daten im `/Quellen/`-Ordner.
3.  **Check-Gate:** Die Aufforderung, die Layer zu nennen, ist dein **Unit-Test**. Wenn er die Layer (Homepage, Bote, Bibliotheken, Spieler) korrekt wiedergibt, weißt du, dass der Zugriff auf das Dateisystem und das Verständnis der Hierarchie funktionieren.

### Wo ist das Agentensetup?
In der Antigravity-Oberfläche (Google Cloud Console / Vertex AI):
- Wenn du in der **"Agent Console"** bist: Suche links nach **"Instructions"** oder **"Persona"**.
- Wenn du im **"Prompt Optimizer"** oder **"Chat Sandbox"** bist: Es ist einfach die allererste Nachricht, die du schickst.
- Wenn du die **"Playground"**-Ansicht hast: Es gibt meist ein Feld auf der linken Seite namens **"System Instructions"**. Dort gehört dein *Master-Prompt* dauerhaft hinein.

**Sobald du diesen Kickoff-Prompt abgeschickt hast und die Bestätigung erhältst, ist dein Antigravity-System "live".**

Soll ich dir zeigen, wie du die Ergebnisse der "Inventur" (Phase 1) danach technisch validierst, um sicherzugehen, dass kein Dokument vergessen wurde?