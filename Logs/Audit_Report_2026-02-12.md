# Audit-Report: Konsistenz & Vollständigkeit
**Datum:** 12.02.2026  
**Durchgeführt von:** Antigravity (Audit-Workflow)  
**Scope:** Gesamtes Wiki — Quellen-Abgleich, Register-Kreuzprüfung, Index-Validierung

---

## 1. Zusammenfassung

| Prüfbereich | Ergebnis | Offene Aktionen |
|:---|:---|:---|
| Konsistenzbericht | 5 ✅ fixiert, 4 ⚠️ offen | 4 |
| Personenregister | 255 Einträge, 4 Duplikate, 19 verwaiste Profile | 23 |
| Boten-Archiv | 66 von 71 Boten integriert, Index veraltet | 8 |
| Geografie | 45 Artikel, alle Hauptorte vorhanden | 0 |
| Gesellschaft | 35 Artikel, inkl. verschobener Dateien | 0 |
| Git-Repository | Bereinigt, 12 MB, GitHub-ready | 0 |

**Gesamtbewertung:** Das Wiki ist inhaltlich umfangreich und die Erzähllogik innerhalb der Boten 120-190 ist konsistent. Die Hauptprobleme liegen in der **Register-Hygiene** (Duplikate, verwaiste Profile) und der **Index-Pflege** (Die_Chronik veraltet). Es existieren keine kritischen Lore-Widersprüche.

---

## 2. Quellen-Kreuzreferenz: Boten vs. Wiki

### 2.1 Boten-Lücken: 7 fehlende Ausgaben

Die Dateien im Wiki-Verzeichnis `04_Chronik/` weisen eine Lücke auf:

| Lücke | Status Quellen-Ordner | Wiki-Status |
|:---|:---|:---|
| Bote 133 | ✅ `.md` + `.html` vorhanden | ❌ Nicht integriert |
| Bote 134 | ✅ `.md` + `.html` vorhanden | ❌ Nicht integriert |
| Bote 135 | ✅ `.md` + `.html` vorhanden | ❌ Nicht integriert |
| Bote 137 | ✅ `.md` + `.html` vorhanden | ❌ Nicht integriert |
| Bote 138 | ✅ `.md` + `.html` vorhanden | ❌ Nicht integriert |
| Bote 139 | ✅ `.md` + `.html` vorhanden | ❌ Nicht integriert |
| Bote 140 | ✅ `.md` + `.html` vorhanden | ❌ Nicht integriert |

**Befund:** Die Quellen existieren vollständig — die Lücke ist ein Integrationsfehler, kein Datenverlust. Die 7 Boten müssen über den RVW-Loop verarbeitet werden.

### 2.2 Die_Chronik Index vs. Dateisystem

`Die_Chronik.md` listet Boten 120–175 im Archiv. Tatsächlich existieren Dateien bis Bote 190.

```diff
  Archiv-Index:     120 ────────────────────── 175
  Dateisystem:      120 ────────────────────────────── 190
                                                ^^^^^^^ 15 Boten fehlen im Index
```

---

## 3. Register-Kreuzprüfung

### 3.1 Duplikate im Personenregister

Vier Personen erscheinen doppelt, jeweils mit leicht abweichenden Beschreibungen:

| Person | Eintrag A | Eintrag B | Bewertung |
|:---|:---|:---|:---|
| `Waldemar_Delarie` | Z.100: Gardehauptmann (#canon) | Z.129: Gardewaibel/Regierungsrat (#bote) | **Zusammenführen** — beide korrekt, beschreiben Karriereverlauf |
| `Paule_Bitterling` | Z.84: Fischer/Turniersieger | Z.251: Turniersieger | **Z.251 entfernen** — Z.84 ist informationsreicher |
| `Altumion_Eisenbruch` | Z.25: Inselrichter (Dwarshim) | Z.247: Inselrichter (Zwerg) | **Z.247 entfernen** — "Dwarshim" ist die korrekte Ortsbezeichnung |
| `Arman` | Z.27: Ordensmitglied/"Hexer" | Z.257: Legendenfigur/Märtyrer | **Prüfen** — möglicherweise zwei verschiedene Aspekte derselben Person |

> [!IMPORTANT]
> Die Duplikate entstanden durch das in Issue `[REGISTER] Datenverlust durch fehlerhaftes Append-Muster` dokumentierte Problem: Batch 120-123 wurde nach der Wiederherstellung verlorener Einträge erneut verarbeitet, ohne auf existierende Einträge zu prüfen.

### 3.2 Verwaiste Profile (kein Register-Eintrag)

19 Profildateien in `07_Persoenlichkeiten/` existieren, sind aber **nicht** im Personenregister verzeichnet:

| Profil | Vermutete Quelle |
|:---|:---|
| `Caiomme` | Unklar |
| `Calin_Drakar` | Unklar |
| `Eichstamm_B` | Unklar |
| `Feanthil_(Arinth)` | Unklar |
| `Feestar_von_Lichtenfeld` | Kanon / Geografie |
| `Fraomar_Arkad'Grembargh` | Bote 150 (Namensformat-Abweichung im Register: `Fraomar_Arkad_Grembargh`) |
| `Iycheas_Vrahn` | Unklar |
| `Jalina` | Unklar |
| `Jassyria_el_Vanjath` | Unklar |
| `Katharina_von_Tiefenwald` | Kanon / Geografie |
| `L.H.` | Unklar |
| `Laurelin` | Bote 124/128 (im Register als Rollenname erwähnt, nicht als Person) |
| `Lazalantin` | Unklar |
| `Luther_Dueff` | Unklar |
| `Lyam_Anarjion` | Unklar |
| `M._Pfahl` | Unklar |
| `Merden` | Unklar |
| `Randur_Kantrin` | Unklar |
| `Sarthas_Glaser` | Unklar |

> [!WARNING]
> 13 Profile mit Quelle "Unklar" deuten auf eine ältere Ingestion-Session hin, deren Herkunft nicht mehr nachverfolgt werden kann. Diese sollten gegen die Quellen geprüft werden, bevor sie ins Register aufgenommen werden.

---

## 4. Struktur-Analyse

### 4.1 Gelöste Probleme (diese Session)

| Issue | Aktion | Status |
|:---|:---|:---|
| Fehlende Orts-Stubs (Brandenstein, Falkensee, Greifenklipp) | Alle existieren in `02_Geografie/` | ✅ |
| Stale Root-Verzeichnisse (`02_Organisationen/`, `03_Pantheon/`) | Dateien nach `Siebenwind_Wiki/` verschoben, Ordner gelöscht | ✅ |
| Temp-Daten im Root (`Inbox/`) | Gelöscht und gitignored | ✅ |
| Git-Bloat (4.4 GB venv + Modelle) | `.gitignore` erstellt, History gepurgt → 12 MB | ✅ |
| README.md GitHub-Format | YAML-Frontmatter und #perspektive entfernt | ✅ |

### 4.2 Offene Punkte

| # | Priorität | Issue | Empfohlene Aktion |
|:---|:---|:---|:---|
| 1 | 🔴 Hoch | 7 Boten nicht integriert (133-135, 137-140) | RVW-Loop starten |
| 2 | 🟡 Mittel | Die_Chronik Index veraltet (176-190 fehlen) | Index ergänzen |
| 3 | 🟡 Mittel | 4 Register-Duplikate | Zusammenführen/Entfernen |
| 4 | 🟡 Mittel | 19 verwaiste Profile | Quellen prüfen, dann registrieren |
| 5 | 🟢 Niedrig | Boten-Archiv-Sortierung in Die_Chronik | Formatierung verbessern |

---

## 5. Prozess-Empfehlungen

Basierend auf den identifizierten Mustern:

### 5.1 Register-Validierung vor Schreibvorgängen
Das Append-Problem und die Duplikate zeigen, dass der Schreibprozess eine **Pre-Write-Validierung** benötigt:
- Vor jeder Profil-Erstellung: Prüfen ob Datei existiert
- Vor jedem Register-Append: Prüfen ob Name bereits im Register steht

### 5.2 Index-Synchronisation
Die `Die_Chronik.md` wird nicht automatisch aktualisiert, wenn neue Boten verarbeitet werden. Der RVW-Loop sollte einen **Post-Write Index-Update-Schritt** enthalten.

### 5.3 Quellen-Tracking bei Ingestion
Profile mit "unklarer Quelle" sind ein Zeichen für fehlende Provenienz-Dokumentation. Jedes Profil sollte im YAML-Frontmatter eine `quelle:` Angabe tragen.

---
*Nächster Audit geplant: Nach Integration der 7 fehlenden Boten.*
