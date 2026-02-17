---
description: Generiere aktuelle Statistiken für das Siebenwind Wiki
---

Dieser Workflow generiert den **leserorientierten Kompass** des Wikis und den zugehörigen technischen Fortschrittskontext.

## Interop-Status
- runtime_commands:
  - `7w_wiki.py stats`
  - `7w_wiki.py audit`
  - `7w_wiki.py test --suite reader-stats-contract`
- method_only:
  - `/stats`

## Zielbild
- Leser sehen auf einen Blick: Weltumfang, Aktivitaet, Entdeckungs-Hubs, Qualitaet/Vertrauen.
- Maintainer sehen transparent: Werkstattstatus (Audit/Test), aber getrennt vom Lesefluss.

## Ausfuehrung
1. Fuehre den Statistik-Befehl aus:
// turbo
```bash
./7w_wiki.py stats
```

2. Pruefe die Zielartefakte:
- [Wiki_Statistiken.md](../../Siebenwind_Wiki/10_Archiv/Wiki_Statistiken.md) (Leseransicht)
- [INGESTION_TRACKING_REGISTER.md](../../Logs/INGESTION_TRACKING_REGISTER.md) (Technikdetail)
- [STATS_SNAPSHOT_latest.json](../../Logs/Archive/STATS_SNAPSHOT_latest.json) (maschinenlesbare Schnittstelle)

3. **Reader-Contract (Pflichtsektionen in Wiki_Statistiken.md):**
- `## 🌍 Welt Heute`
- `## 🔄 Was sich bewegt`
- `## 🏆 Entdecke die Welt`
- `## ✅ Qualitaet & Vertrauen`
- `## 🛠️ Werkstattstatus (Transparenz)`
- `## 📍 Fortschritt Live Verfolgen`

4. **Progress-Quellen sichtbar halten:**
- `MASTER_TASK_LIST.md`
- `CHANGELOG.md`
- `Logs/Archive/Audit_*.txt`
- `Logs/Archive/TEST_*.md`

5. Optionaler Guard-Run:
```bash
./7w_wiki.py test --suite reader-stats-contract
./7w_wiki.py audit
```

## Regel
`Wiki_Statistiken.md` ist ein **Reader-Asset**. Tiefere Operativdaten bleiben in Logs/Boards und werden nur verdichtet eingebettet.
