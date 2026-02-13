# Spezifikation: Siebenwind Synapsen-System (v2.0)

**Version:** 2.0 (Active Agent Collaboration)
**Status:** Aktiv
**Ziel:** Autonome Eskalationspipeline für Lore-Konflikte.

## 1. Verzeichnisstruktur
Das System operiert im Verzeichnis `/System/Synapse_Board/`. Jedes Lore-Problem wird als individuelles Ticket (`Conflict_[ID].md`) behandelt.

## 2. Agenten-Logik
- **Archivar (Ingestion):** Identifiziert Widersprüche. Erstellt Tickets mit Status `NEEDS_REVIEW`.
- **Historiker (QA):** Überwacht das Board. Analysiert Tickets mittels Orakel (RAG). **Muss Lore-Gutachten abgeben.**
- **Oberarchivar (Ops):** Überwacht den Prozess. Muss Verfahrensempfehlung abgeben.
- **Entscheidungsinstanz (User):** Wird bei Status `AWAITING_USER` konsultiert. Seine Entscheidungen manifestieren sich als **Intervention (Rank 0)**.

## 3. Ticket-Lebenszyklus
1. `NEEDS_REVIEW`: Neu erstellt durch Archivar.
2. `RESEARCHING`: Historiker arbeitet am Fall.
3. `AUTO_RESOLVED`: Historiker konnte den Konflikt basierend auf der Truth Hierarchy (Kanon > Bote) lösen.
4. `AWAITING_USER`: Widerspruch innerhalb derselben Hierarchieebene (z.B. Kanon vs. Kanon).
5. `HUMAN_RESOLVED`: Lösung durch User-Entscheid.

## 4. Skills & Triggers
- `trigger_conflict_alert`: Erstellt Ticket und gibt Warnung aus.## 4. Epistemische Hierarchie der Entscheidung (User-Logic)
Manuelle Interventionen durch den User werden intern wie folgt gewichtet:
- **Rang 0 (`#user_canon`):** Direkte Meisterentscheidung. Steht über dem offiziellen Kanon (`#canon`).
- **Rang 0.5 (`#user_speculation`):** Vermutung des Meisters. Wird als "wahrscheinlich" markiert, ist aber kein Gesetz.
- **Status: Unknown:** Wenn der Meister es nicht weiß, verbleibt das Ticket als ` Lore-Gap` im Backlog oder wird für spätere Forschung markiert.
- **Anzeige:** Im Wiki-Artikel werden solche Stellen intern mit `[Intervention: Rank 0]` oder `[Speculation: Rank 0.5]` markiert.
- **Lore Score Interaction:** Erfolgreiche Konfliktlösungen durch den User ermöglichen dem Historiker ein finales Audit, um den `lore_trust` zu erhöhen (User-Entscheidung allein boostet den Score nicht automatisch).
- **Transparenz:** Das Ticket dokumentiert den Grad der Gewissheit.
- `resolve_with_oracle`: Nutze RAG zur Faktenprüfung.
- `human_intervention`: Eskalation an das Chat-Interface.
- `/decide` Workflow: Erlaubt dem User die schnelle Abarbeitung offener Tickets.
