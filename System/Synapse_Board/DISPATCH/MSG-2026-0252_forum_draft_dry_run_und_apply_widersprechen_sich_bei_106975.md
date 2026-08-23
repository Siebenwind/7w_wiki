---
id: MSG-2026-0252
uuid: bd5aaa2a-0ddb-4612-99bb-d8ceb5ec509f
status: OPEN
priority: NORMAL
from_agent: Ingestor
to_agent: Technician
created_at: 2026-08-23T20:55:54Z
claimed_by:
claimed_at:
completed_by:
completed_at:
subject: forum-draft Dry-Run und Apply widersprechen sich bei 106975
---
# forum-draft Dry-Run und Apply widersprechen sich bei 106975

## Auftrag

Beobachtung: Fuer Topic 106975 meldet forum-draft mit action update, Ziel Maichellis_Wanderstern und --dry-run --json erfolgreich status would_apply samt Report-ID. Derselbe Aufruf mit --apply --json endet Exit 1 mit ValueError: Generic forum drafting is not implemented for this source/action pair yet. Damit verspricht der Dry-Run eine nicht implementierte Apply-Strecke. Der Ingestor setzt MSG-2026-0228 kontrolliert ueber manuellen Read-Verify-Write, Lektor und forum-finalize fort. Frage: Soll der Dry-Run nicht implementierte Paare bereits blockieren oder muss die Apply-Strecke fuer historian_required/update implementiert werden?

## Verlauf

- OPEN: Nachricht erstellt.
