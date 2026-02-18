# Maintainer-Standpunkt (Menschlicher Leitpunkt)

Status: Aktiv (v1, 2026-02-18)

## Zweck

Diese Seite ist der verbindliche menschliche Leitpunkt fuer Agentenarbeit.
Sie reduziert permanentes Nachsteuern, indem Prioritaeten, No-Gos und Eskalationsregeln klar festgehalten werden.

## 1) Nicht verhandelbar

- Sprache fuer oeffentliche Inhalte: Deutsch (DE only).
- Leserfokus: Zielbild 85% Leserperspektive, 15% Technikperspektive.
- Kanonschutz: Keine Halluzinationen; Unsicherheiten als `[UNGEKLAERT]` markieren.
- Transparente KI: KI-Nutzung ist offen kommuniziert, Ergebnisse sind auditiert und kuratiert.
- Runtime Authority: Operative Ausfuehrung nur ueber `./7w_wiki.py`.
- Link-Hygiene: Keine absoluten `file://` Pfade, WikiLink-Regeln einhalten.
- Banner/Kanonanker: Visuelle Motive muessen die verlinkte Geschichte inhaltlich korrekt abbilden.

## 2) Prioritaeten-Reihenfolge

1. Kanonische Integritaet und Leserverstaendlichkeit (Inhalt vor Effekt).
2. Qualitaetsbetrieb (Ingestion, Bewertung, Bewahrung, Forschung) mit nachvollziehbaren Checks.
3. Zuverlaessige Technik (Oracle, Tests, Build, Dispatch) ohne Betriebsblindheit.
4. Design-/UX-Verfeinerung inklusive Banner-Rotation, solange 1-3 stabil bleiben.

## 3) Stil und Positionierung

- Zielgruppe: Primaer Leser und Lore-Interessierte, sekundär technisch Interessierte.
- Tonalitaet: Serioes, archivalisch, praezise, ohne Marketing-Sprech.
- Visuelle Leitlinie: Archivum Argentum (Silberstift/Graphit, reduzierte Linien, Roetel nur als Akzent).
- Motivgrenze: Keine Figuren als dominantes Banner-Hauptmotiv; Umgebung, Hinweise und Storybezug priorisieren.
- KI-Transparenz: Verfahren sichtbar machen (Ingestion, Bewertung, Bewahrung, Forschung + Quality Checks).

## 4) No-Gos

- Keine Mechanik-/Gear-Bildsprache, ausser explizit fuer Dwarschim/Uhrmacher-Kontext.
- Kein visuelles Rauschen ohne Informationsgewinn auf Landing/README.
- Keine Vermischung von Praesentation und Betriebsdetails im ersten Leserzugriff.
- Keine stillen Governance-Aenderungen ohne Changelog + Dispatch-Hinweis.
- Keine "Bridge-Placeholder" als Dauerloesung fuer defekte Verweise.

## 5) Eskalation und Entscheidungsrecht

- Entscheidungen mit Maintainer-Veto:
  - Kanonaenderungen mit inhaltlicher Tragweite.
  - Endfreigabe von Corporate-Design-Aenderungen und Hero-Bannern.
  - Aenderungen an Governance-Regeln, Test-Gates und Prioritaetslogik.
- Entscheidungen mit Agenten-Autonomie:
  - Redaktionelle Klarstellungen ohne Kanonverschiebung.
  - Struktur-/Link-Reparaturen innerhalb bestehender Regeln.
  - Technische Wartung, sofern keine Leitungsregel beruehrt wird.
- Eskalation bei Unsicherheit:
  - Dispatch an `ALL` oder gezielt an den zustaendigen Fachagenten mit konkreter Entscheidungsfrage.
  - Bei unklarer Tragweite: erst stoppen, dann Entscheidung einholen.

## 6) Aenderungsprotokoll

- Jede Anpassung dieser Seite wird im Changelog vermerkt.
- Diese Seite hat Vorrang vor weichen Stilpraeferenzen in Einzelprompts.
- `./7w_wiki.py leitpunkt check` muss immer gruen sein (Strukturkonsistenz).
- `./7w_wiki.py leitpunkt check --strict` ist **kein** Daily-Blocker:
  nur verpflichtend bei Governance-Release, formaler Handover-Freigabe oder Policy-Freeze.
