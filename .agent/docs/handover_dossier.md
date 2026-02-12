# Handover Dossier: Siebenwind-Wiki (v2.3)

**Datum:** 12.02.2026  
**Status:** Infrastruktur modernisiert, Root bereinigt, GitHub-bereit.

## 🏗 Was getan wurde
Wir haben das System auf eine **Markdown-First** Architektur umgestellt. Die Wahrheitshierarchie wurde präzisiert: Der **Lokal-Kanon (#canon)** ist das Gesetz. Das Repository wurde strukturell bereinigt: Prompts, Skripte und Docs befinden sich nun sauber getrennt in `.agent/`.

## 🌍 GitHub & Public Wiki
Das Wiki wird automatisch als Website gehostet (via MkDocs Material). 
- **Setup:** Gehe auf GitHub zu `Settings -> Pages`. Wähle unter `Source` die Option `GitHub Actions`.
- **Tickets:** Nutzer können Lore-Widersprüche über Issues (YAML-Template) melden. Diese landen als strukturierte Daten im Repo.

## 🧠 Das Orakel (RAG System)
Wir haben ein semantic search System implementiert, das auf `jina-embeddings-v3` (8192 Token) basiert und speziell für Mac Silicon optimiert ist.

- **Wichtig:** Jina v3 auf M1/M2 nutzt Flash Attention, was speicherhungrig ist.
- **Config:** Nutze `.agent/skills/oracle/benchmark_hardware.py`, um die optimale Batch-Size zu finden (aktuell: 2).
- **Workflow:** Der **Oberarchivar** nutzt das Orakel für den `Faktencheck`, bevor er neue Inhalte schreibt.
- **Dossier:** Lese `Logs/PROJEKT_DOSSIER_ORACLE.md` für technische Details.

## 📌 Aktueller Fokus
Das Repository verfügt nun über eine **`MASTER_TASK_LIST.md`** im Root. Dies ist dein primärer Leitfaden.

### Nächste Schritte:
1.  **Geografie-Hauptseiten**: Erstelle die Wiki-Seiten für `Brandenstein`, `Falkensee` und `Greifenklipp` im Ordner `/02_Geografie/`.
2.  **Massen-Ingestion**: In `Logs/INVENTUR_QUELLEN.md` stehen noch ~150 Dokumente auf `Pending`. Nutze den modernisierten `/rvw_loop`.
2.  **Massen-Ingestion**: In `Logs/INVENTUR_QUELLEN.md` stehen noch ~150 Dokumente auf `Pending`. Nutze den modernisierten `/rvw_loop`.
3.  **Community**: Prüfe Pull Requests mit dem neuen `/contrib_audit` Workflow.
4.  **Boten-Integration**: 10 fehlende Ausgaben (133-140, 191-193) einpflegen.
5.  **Index-Korrektur**: `Die_Chronik.md` vervollständigen (Boten 176-190 fehlen im Index).

## ⚠️ Bekannte Tücken
- **Jina & MPS:** Falls PyTorch updated, erneut `benchmark_hardware.py` laufen lassen. Flash Attention auf Metal ist volatil.
- **Sandbox:** `setup.sh` muss **außerhalb** der Antigravity-Sandbox laufen (Permissions). Innerhalb der Sandbox funktionieren `build_index` und `search` problemlos mit dem venv.

**Viel Erfolg, Archivar. Möge dein Federkiel niemals trocken werden.**
