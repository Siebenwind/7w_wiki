status: RESEARCHING
priority: 1
source_files: ["/System/Sandbox/test_source.md", "/System/Sandbox/test_source_2.md", "Siebenwind_Wiki/02_Geografie/Region_Galadon.md"]
detected_by: Archivar (Simulation)
---

# Konfliktbeschreibung
>>> TESTDATEN START >>>
Drei-Wege-Widerspruch zur Gründung von Falkensee:
1.  **Kanon:** Gründung 12 n.H.
2.  **Test-Quelle 1 (`test_source.md`):** Zerstörung 5 n.H. (Logischer Fehler: Zerstörung vor Gründung).
3.  **Test-Quelle 2 (`test_source_2.md`):** "Aufblühen" 8 n.H. (Widerspricht Kanon-Datum).
<<< TESTDATEN ENDE <<<

# Orakel-Befunde (Vom Historiker auszufüllen)
- **Befund 1 (Kanon):** Dokument `Region_Galadon` (#canon) setzt das Gründungsdatum explizit auf 12 n.H. (Amtliche Festlegung).
- **Befund 2 (Überlieferung):** `test_source_2` (#überlieferung) berichtet von Besiedlung bereits 8 n.H. Dies könnte eine informelle Siedlungsphase vor der offiziellen Stadtgründung beschreiben.
- **Befund 3 (Perspektive):** `test_source` (#perspektive) behauptet eine Zerstörung 5 n.H. Dies widerspricht sowohl dem Kanon als auch der Überlieferung und ist chronologisch unplausibel (Kausalitätsbruch).

# Lösung (DRAFT)
1. **Priorisierung:** Kanon (12 n.H.) bleibt das offizielle Datum.
2. **Integration:** Die Info aus `test_source_2` wird als "Frühe Gerüchte/Siedlungsspuren" unter `#überlieferung` aufgenommen.
3. **Korrektur:** Die Behauptung aus `test_source` wird als "unzuverlässige Chronik" verworfen.
4. **Wiki-Aktion:** Erstelle `Falkensee_Timeline.tmp` in `/System/Sandbox/` mit diesen korrigierten Daten.

# Gutachten & Empfehlungen
## 🧠 Der Historiker (Lore Opinion)
"Aus analytischer Sicht bietet die Information aus `test_source_2` (8 n.H.) eine wunderbare Gelegenheit für **narrative Tiefe**. Wenn wir 12 n.H. als *juristische* Gründung beibehalten, aber 8 n.H. als Beginn einer *wilden Besiedlung* (Pioniere, Einsiedler) deklarieren, bleibt der Kanon gewahrt, während die Welt lebendiger wirkt. Die 5 n.H. Story muss jedoch als purer Aberglaube markiert werden, da sie die Kausalität bricht."

## 🏛️ Der Oberarchivar (Ops Recommendation)
"Ich empfehle die Umsetzung des 'Soft-Retcon' (Siedlungsspuren 8 n.H.). Technisch gesehen sollten wir das Tag `#überlieferung` nutzen, um die Distanz zum `#canon` zu wahren. Dies verhindert 'Lore-Bleeding' und hält das System konsistent. Die 5 n.H.-Quelle sollte im Ingestion-Log als 'Discarded/Inconsistent' markiert werden."

# Status: RESOLVED
*Der Konflikt wurde durch die Etablierung von **[[Finsterwangen]]** als Nachfolger der Hauptstadt **[[Jassavia]]** gelöst. Die "Siedlungsspuren" 8 n.H. beziehen sich auf erste Wiederbesiedlungs-Versuche der Ruinen, während die offizielle Neugründung später erfolgte. Die Zerstörungs-Daten (5 n.H.) wurden als Fehlinformation/Aberglaube eingestuft, da Jassavia bereits im Dritten Zeitalter fiel.*
