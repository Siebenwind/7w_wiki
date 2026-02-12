# Handover Dossier: Siebenwind-Wiki (v2.3)

**Datum:** 12.02.2026  
**Status:** Infrastruktur modernisiert, Root bereinigt, GitHub-bereit.

## 🏗 Was getan wurde
Wir haben das System auf eine **Markdown-First** Architektur umgestellt. Die Wahrheitshierarchie wurde präzisiert: Der **Lokal-Kanon (#canon)** ist das Gesetz. Das Repository wurde strukturell bereinigt: Prompts, Skripte und Docs befinden sich nun sauber getrennt in `.agent/`.

## 🌍 GitHub & Public Wiki
Das Wiki wird automatisch als Website gehostet (via MkDocs Material). 
- **Setup:** Gehe auf GitHub zu `Settings -> Pages`. Wähle unter `Source` die Option `GitHub Actions`.
- **Tickets:** Nutzer können Lore-Widersprüche über Issues (YAML-Template) melden. Diese landen als strukturierte Daten im Repo.

## 📌 Aktueller Fokus
Das Repository verfügt nun über eine **`MASTER_TASK_LIST.md`** im Root. Dies ist dein primärer Leitfaden.

### Nächste Schritte:
1.  **Geografie-Hauptseiten**: Erstelle die Wiki-Seiten für `Brandenstein`, `Falkensee` und `Greifenklipp` im Ordner `/02_Geografie/`.
2.  **Massen-Ingestion**: In `Logs/INVENTUR_QUELLEN.md` stehen noch ~150 Dokumente auf `Pending`. Nutze den modernisierten `/rvw_loop`.
3.  **Community**: Prüfe Pull Requests mit dem neuen `/contrib_audit` Workflow.

**Viel Erfolg, Archivar. Möge dein Federkiel niemals trocken werden.**
