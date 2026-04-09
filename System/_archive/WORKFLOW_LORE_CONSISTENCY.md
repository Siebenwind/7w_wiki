---
uuid: b0ea0ccf-e7bd-4ef1-b14e-a37220884c25
status: ACTIVE
updated_at: 2026-03-08T16:00:00Z
epistemic: "#meta"
---

# WORKFLOW_LORE_CONSISTENCY

> Archived note: This guide predates the current precedence and drift model.
> Active lore-operating truth now lives in:
> - `System/Synapse_Board/SY_DRIFT_PAGES_CONTRACT.md`
> - `System/Synapse_Board/SY_INTEROP.md`
> - `docs/architecture.md`

Verbindlicher Arbeitsleitfaden fuer Lore-Konsistenzpruefungen und Wiki-Integration.

## 1. Mindestablauf (Konsistenzpruefung)
1. Konflikt identifizieren (Quelle, Stelle, Wirkung).
2. Primarquellenabgleich im Wiki/Quellenarchiv.
3. Einstufung nach `CORE_LORE_SCORE_GUIDE`.
4. Bei ungelosten Widerspruechen: Ticket im `System/Synapse_Board/`.
5. Ergebnis in `Logs/Konsistenzbericht_2026.md` protokollieren.

## 2. Truth Hierarchy & Escalation
1. **Lokal-Kanon (#canon):** Ordner `/Hintergrund/`. Axiomatische Weltgesetze (Absolute Wahrheit).
2. **Lokale Quelle (#bote, #überlieferung, #perspektive):** Das spezifische Dokument.
3. **Wiki-Standard:** Siehe [wiki_style_guide.md](../../.agent/workflows/wiki_style_guide.md) fuer Ranking & Regeln.
4. **Web-Kanon (`siebenwind.de`):** Verifizierung und Lueckenfuellung.
5. **User Enquiry:** Letzte Instanz via Synapse Board.

**Escalation Logic:**
- Verify Local -> Verify Web -> Log as `[UNGEKLÄRT]` if inconclusive -> Ask User as last resort.

## 3. Consistency Checks
1. **Axiom Check**: Widerspricht die Geschichte dem Goetter-Kanon oder Magie-Axiomen?
2. **Oracle Check**: `.agent/skills/oracle/` nutzen, um Konflikte mit anderen Quellen zu finden.
3. **Time Check**: `Time Keeper` Skill zur Datumspruefung nutzen.
4. **Uncertainty Logging**: Unbewiesene Behauptungen mit `[UNGEKLÄRT]` markieren und in `Konsistenzbericht_2026.md` loggen.

## 4. Bi-directional Linking
- **In der Quelle**: Jede erwaehnte Entitaet (Person, Ort, Ereignis) zum Wiki-Artikel verlinken.
- **Im Wiki**: Abschnitt `## Überlieferungen` am Ende des Wiki-Artikels ergaenzen und zur Quelle zurueckverlinken.

## 5. Git-Konventionen
- **Batch Commits**: Nach Verarbeitung eines Batches (z.B. 10 Geschichten) wird ein Git-Commit erstellt.
- **Commit Message Pattern**: `Batch-Processing: [Count] sources integrated. [Conflict Count] conflicts listed in /Logs.`
