# Dispatch und Agentenkommunikation

Agent-zu-Agent Kommunikation laeuft ueber `mail` und den Statusfluss `OPEN -> CLAIMED -> DONE`.

`TASK` ist der Standard für einen Auftrag mit Folgeaktion. `INFO` dokumentiert eine reine Mitteilung und wird unmittelbar als abgeschlossen geführt. `./7w_wiki.py mail inbox --kind TASK --status OPEN --json` zeigt die Arbeitswarteschlange. Bestehende Nachrichten werden einzeln mit Nachweis über `mail classify` eingeordnet; unklare oder noch offene Folgeaktionen bleiben Aufträge.

## Standardablauf

```bash
./7w_wiki.py mail inbox --status OPEN
./7w_wiki.py mail read <MSG-ID>
./7w_wiki.py mail claim <MSG-ID> --agent <name>
./7w_wiki.py mail done <MSG-ID> --agent <name> --note "<abschluss>"
```

## Defect-Flow im Testbetrieb

Bei Test-FAIL zuerst Nachricht erzeugen, dann Fix:

```bash
./7w_wiki.py test --suite <name> --post-failures --from-agent Test-Waechter --to-agent ALL --priority HIGH
```

## Betriebsregeln

1. Keine stillen Fixes ohne Claim oder referenzierte Aufgabe.
2. Nach jedem Fix Re-Test und Abschlussnotiz mit Message-ID.
3. Advisor und Start-Workflow sollen offene Queue regelmaessig beachten.

## Kanonische Quelle

- `System/Synapse_Board/SY_DISPATCH.md`
