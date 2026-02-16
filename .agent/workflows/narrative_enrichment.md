---
description: Narrative Enrichment Workflow (Roman-Qualität)
---
# Narrative Enrichment Workflow

## Interop-Status
- runtime_commands:
  - `7w_wiki.py historian <query>`
  - `7w_wiki.py search <query> --source all`
  - `7w_wiki.py score <file>`
- method_only:
  - `/narrative_enrichment`

**Ziel:** Aufwertung von Stubs und faktischen Artikeln zu lebendigen, atmosphärischen Beschreibungen ("Roman-Qualität").
**Zielgruppe:** Charaktere mit mehrfacher Erwähnung oder besonderer Relevanz (keine One-Hit-Wonder).

## 1. Identifikation
- Prüfe die Relevanz: Wird die Person in mindestens **2 verschiedenen Quellen** (z.B. Boten-Ausgaben) erwähnt?
- Prüfe den Status: Ist der aktuelle Artikel ein "Datenwüste" (nur Listen, Werte)?

## 2. Quellen-Analyse (Deep Read)
Suche in allen verfügbaren Quellen nach:
- **Kontext:** Wo taucht die Person auf? (Taverne, Schlachtfeld, Hofball)
- **Handlung:** Was tut sie aktiv? (Kämpft, verhandelt, flieht)
- **Beziehungen:** Wen kennt sie? Wie steht sie zu anderen?

## 3. Narrative Anreicherung (The 'Novel' Touch)
Ergänze den Artikel um folgende Dimensionen (ohne Fakten zu erfinden - interpretiere die vorhandenen!):
- **Atmosphäre:** Beschreibe die Szene. ("...im verrauchten Hinterzimmer des 'Humpen'...")
- **Motivation:** *Warum* handelt die Person so? (Pflichtgefühl, Gier, Angst?)
- **Auftreten:** Wie wirkt sie auf andere? (Arrogant, unscheinbar, charismatisch?)

## 4. Struktur-Update
- **Einleitung:** Ein narrativer Hook statt trockener Definition.
- **Biografie:** Erzähle die Geschichte chronologisch, aber spannend.
- **Zitate:** Wenn möglich, füge direkte Rede aus den Quellen als Zitatblock ein.

## 5. Review (Self-Correction)
- [ ] Wirkt die Figur lebendig?
- [ ] Sind alle Fakten weiterhin korrekt (keine Halluzination)?
- [ ] Ist der Epistemische Status (`#bote`, `#perspektive`) klar?

---
*Hinweis: "NPC" ist ein verbotener Begriff. Nutze "Charakter", "Person", "Wesen" oder den in-world Titel.*
