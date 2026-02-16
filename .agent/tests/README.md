# .agent/tests

Standardisierte Test-Suiten fuer den Runtime-Einstieg `./7w_wiki.py test`.

## Struktur

- `suites/*.json`: deklarative Testfaelle
- `TEST_CASES.md`: konzeptionelle, historische Testideen (nicht direkt vom Runner genutzt)

## Suite-Format

```json
{
  "suite": "clean-client-state",
  "description": "Read-first smoke",
  "cases": [
    {
      "id": "help",
      "name": "CLI help",
      "cmd": ["./7w_wiki.py", "--help"],
      "expect_exit": 0,
      "expect_stdout": ["mail", "advisor"]
    }
  ]
}
```

### Unterstuetzte Felder je Case

- `id`: stabile Kennung
- `name`: lesbarer Titel
- `cmd`: Kommando als Tokenliste (muss mit `./7w_wiki.py` starten)
- `link_check_files`: Liste von Markdown-Dateien fuer lokalen Link-Existenzcheck (Alternative zu `cmd`)
- `expect_exit`: erwarteter Exitcode (Default `0`)
- `expect_stdout`: Liste erwarteter Substrings in stdout
- `expect_stderr`: Liste erwarteter Substrings in stderr
- `forbid_stdout`: Liste verbotener Substrings in stdout
- `forbid_stderr`: Liste verbotener Substrings in stderr
- `min_duration_sec`: optionale Untergrenze fuer Laufzeit (Benchmark-Guard)
- `max_duration_sec`: optionale Obergrenze fuer Laufzeit (Timeout-/Regressions-Guard)
- `skip_if_context_missing`: Context-Keys, bei deren Fehlen der Case als `SKIP` markiert wird

Der Runner schreibt pro Case die gemessene Laufzeit (`Laufzeit (s)`) in den Report.

## Kontext-Token

Aktuell unterstuetzt:

- `{{first_open_message_id}}`: erste Message-ID aus `mail inbox --status OPEN`

## Kommunikation bei FAIL

Empfohlen:

```bash
./7w_wiki.py test --suite <name> --post-failures --from-agent Test-Waechter --to-agent ALL --priority HIGH
```

Fixes erfolgen erst nach Dispatch- oder Task-Referenz.

## RAG-Relevanz Smoke

Fuer retrieval-orientierte Rauchtests steht die Suite `rag-relevance-smoke` bereit:

```bash
./7w_wiki.py test --suite rag-relevance-smoke
```
