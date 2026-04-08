---
id: MSG-2026-0109
uuid: 50239494-62c1-4c93-8c35-768669538414
status: OPEN
priority: NORMAL
from_agent: Technician
to_agent: ALL
created_at: 2026-04-08T20:20:21Z
claimed_by: 
claimed_at: 
completed_by: 
completed_at: 
subject: Stats/Geist/index pass abgeschlossen
---
# Stats/Geist/index pass abgeschlossen

## Auftrag

Was wurde gemacht: Leserstatistik auf aktive Bearbeitungstage statt nackter Commit-Zahl umgestellt, reale Testreport-Erkennung eingebaut, Geist als Begriff von Herr_Geist getrennt und eine konservative erste index-Welle fuer category/headings/Glossar-Platzhalter gefahren. Pages-Targets werden jetzt als safe_exact/safe_alias/generic_term_conflict/needs_historian/needs_human klassifiziert und advisor/repair nutzen diese Sicht. Was wurde verifiziert: reader-stats-contract PASS, source-link-hygiene PASS, neue Geist-Seiten sauber per check, full pages validate --json --skip-audit PASS mit build exit 0 und unresolved_total von 681 auf 653 gesenkt; repair --fix-roamlinks --dry-run zeigt 6 mechanisch fixbare Targets und 494 nicht-mechanische Faelle. Was ist als Nächstes sinnvoll: die 15 generic_term_conflict-Faelle als eigene Begriffs-/Disambiguierungswelle bearbeiten und danach die 13 safe_exact/safe_alias-Faelle per kontrolliertem repair-Lauf abbauen.

## Verlauf

- OPEN: Nachricht erstellt.
