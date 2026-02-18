---
source: https://www.siebenwind.de/serverversion-1-12-5/
title: Serverversion 1.12.5
date: 2011-04-04
type: News
epistemic: "#news"
status: archiviert
post_id: 5817
kategorien:
  - Siebenwindnews
---

# Serverversion 1.12.5

_Beobachterprotokoll des Netz-Waechters. Quelle: offizielle Siebenwind-News._

## Meldungskern

Moin, da nun wieder ein wenig Zeit ins Land verstrichen ist, wollen wir eine neue Severversion einspielen. Welche folgendes für Spieler interessante beinhaltet: Neues Callsystem Bausystem Urkundenumwandlungssystem(zum Bausystem gehörend) !abwesend stoppt auch hungern. Erweiterung Tarnnamen: Neben dem bisherigen System ist auch ein weiteres System implementiert. Dort wird der Tarnname ausschliesslich im verkleideten Zustand angezeigt. Gewechselt […]

## Volltext (bereinigt)

Moin,

da nun wieder ein wenig Zeit ins Land verstrichen ist, wollen wir eine neue Severversion einspielen. Welche folgendes für Spieler interessante beinhaltet:

Neues Callsystem

Bausystem

Urkundenumwandlungssystem(zum Bausystem gehörend)

!abwesend stoppt auch hungern.

Erweiterung Tarnnamen: Neben dem bisherigen System ist auch ein weiteres System implementiert. Dort wird der Tarnname ausschliesslich im verkleideten Zustand angezeigt. Gewechselt wird zwischen den Systemen mit dem Befehl !tarnfunktion

Die Fähre zwischen Brandenstein und Vänskap fährt nun deutlich häufiger

Merkname zum selbstständigen merken von Namen.

!merken Merkname

Es gibt unterschiedliche Merknamen für normalen Status, Verkleidet und Incognito. Chars, die unbekannt herumlaufen, kann man nicht benennen.

!vergessen kann man Merknamen vergessen.

!vergessenincognito kann ein Magier den Merknamen aus der Liste aller anderen Chars löschen. Wenn er mehrmals hintereinander als die selbe Person auftritt, sollte er wiedererkannt werden, wenn er die Rolle wechselt, darf natürlich nicht der alte Merkname auftauchen.

Beim Anpflanzsystem muss man nicht erst einen Patch abwarten, bevor man ernten kann

Die Rohstoffe einmal hergestellter oder identifizierter Items werden ab jetzt in der Gegenstandsbeschreibung mit angezeigt

!keinemote stellt die Autoemote bei einem NSC ab. Player können es bei eigenen NPCs einsetzen, und Hüter darum bitten es in Gattern etc. auszuführen.

Änderung im Sättigungsystem

Loot Preisanpassung

Bausystem:

Vorab: Regeln für das neue System:

Gegenstände, die zur Diebstahlsicherung außerhalb normaler Reichweiten platziert werden, werden von der 30% Regelung ausgenommen, und dürften mit Support gestohlen werden.

Gegenstände, die in Durchgängen platziert und fixiert werden, dürfen durch Support gelöst werden, und bei übertriebenen Fällen von Blockaden durch Besitzer fixierte Gegenstände, wird dies geahndet als Non-Rp. Gleiches gilt für Gegenstände, die an ungeeigneten Stellen platziert werden.

Nach dem platzieren von Teppichen, Vorhängen und anderen Gegenständen ohne weitere Funktionen, wird darum gebeten zu Callen bzgl Aufnahme der Gegenstände in die Static.

Hinweis: Sätmliche bauliche Aktionen werden geloggt.

Funktionsweise:

Jede Besitzerregion kann mehrere Besitzer mit bestimmten Rechtelevel besitzen, Level gehen von 0 bis 2.

!besitzerregion gibt Informationen über Koordinaten und Name aus

!besitzerhinzufuegen + Parameter 0 oder 1 für den Rechtelevel, dabei muss sich der Char in der Region aufhalten. Level 2 kann nur Hüter setzen.

!bewegbar 0/1/2 Einschränkungen: Umbenannte Items können nicht gelöst werden. Rechtelevel 0 erlaubt nur fixieren aber nicht lösen.(Parameter: 0 oder 2: Unbewegbar, 1: Bewegbar)

!xrel,!yrel,!zrel erlaubt verschieben innerhalb der Region

!versetzen öffnet das kleine Verschiebemenü bei Klick auf einen Gegenstand und erlaubt versetzen innerhalb der Region

!rauswerfen ermöglicht sämtliche ausgeloggten Spieler eines Hauses an eine Koordinate vor der Tür zu setzen, entpsrechendes muss zuvor in den Skripten eingetragen sein.

!schlosskopie erlaubt kopieren von Schlössern ab Rechtestufe 2, dabei wird Schlosstyp und vorhandene Urkunde geprüft, nur geöffnete Schlösser lassen sich verändern, sowie Player muss direkt daneben stehen.

Einbau von neuen Schlössern ist möglich durch Doppelklick innerhalb der Region auf eine Schlossurkunde. Möglich ab Rechtelevel 2 und der Einschränkung, das man sich direkt neben dem Schloss befinden muss, das nicht verschlossen sein darf.(altes Schloss geht unwiderruflich verloren)

Urkundenumwandlungssystem : Per Doppelklick können vorher definierte Tile in einem Menü gesetzt werden

!urkunde erlaubt einzelne Items zurückzuwandeln in ihre Urkundenform

!tuerautoschliessen zum Einstellen des autoamtischen Zufallens bei aufgeschlossenen Türen

!besitzerloeschen + name Entfernt einen Eintrag aus der Besitzerliste

Anmerkung:

Es fehlen noch Urkunden und Regionen. Es sind nicht alle eingetragen. Zum Beantragen von Regionen bitte ein Ticket an die Technik mit den Koodinaten des Wohnungs/Unterkunft/Hauses. Urkunden bitte im Forum sammeln. Wir haben einige Urkunden, welche hauptsächlich außerhalb von Besitzerregionen genutzt werden, ausgelassen.

Neues Callsystem:

Zitat:

Liebe Mitspieler,

mit der nächsten Serverversion wird es ein neues Callsystem geben, dass das alte (liebevoll von uns genannte „80-Zeichenwunder“) ablösen soll. Vorab möchte ich mich bei allen Mitarbeitern des Projektteams bedanken: Quirian und Brami bei der Hilfe des Konzeptes. Arbo für die Umsetzung des Systems und Nyuchan für den grafischen Einsatz. Aber auch den Mitarbeitern, die sich an der Internen Diskussion beteiligt haben.

Nun aber zu dem zu den Möglichkeiten des Callsystems:

Ein „ich hänge Fest“ Button

Die Serverinfo, wo man Datum, Wetter und vieles mehr abrufen kann

Unterschiedliche Callarten (Allgemeiner Call, Technikfehler, Designcall, Beschwerde) mit Zusatzinformationen

Man kann eigene Calls verwalten und sehen

Ein Call kann nun mehr als 80 Zeichen enthalten

Privantworten auf Calls erhält man beim Einloggen

Wie Calle ich mit dem neuen Callsystem?

Zitat:

Ein paar Gedankenstöße wie man richtig mit dem neuen System umgehen sollte:

In welchen Bereich gehört mein Hilfegesuch?

–> Allgemeiner Call (alles was Regelfragen/Supporthilfe/Etwas verschieben/Restliche Calls betrifft)

–> Technikfehler (Falsch gesetzte Teleporter/Fehlspawn)

–> Designcall (alles was falsch gesetzte Items betrifft/Einrichtungscall)

–> Beschwerde (Wie gehabt)

Kann ich mein Hilfegesuch schnell und möglichst genau erklären?

–> Nein dann ein Ticket schreiben

–> Ja, dann ein Call schreiben

Hat sich mein Call vielleicht erledigt?

–> Wenn ja, dann diesen selbst löschen

Ist mein Call offenbar noch nicht bearbeitet, was soll ich tun?

–> Falsch wäre es noch einmal zu Callen, da dann ein neuer Call erstellt wird! Also in jedem Fall nur einmal callen!

Mit freundlichem Gruß

Nitramtin

Neue Sättigungsberechnung

Die Sättigung eines Items ist abhängig vom eigenen Hunger und der Qualität der Verarbeitung. Ein einfacher Apfel von frei zugänglichen Bäumen ist bei höherer Sättigung weniger effektiv als ein weiterverarbeitetes Produkt.

frei verfügbare Feldfrüchte sind bis 20% Sättigung effektiv

angepflanze Feldfrüchte sind bis 40% Sättigung effektiv

einfache verarbeitete Nahrung bis Skill 10 ist bis 50% Sättigung effektiv

verarbeitete Nahrung im Gesellenbereich(11-15) ist bis 65% Sättigung effektiv

meisterhafte Nahrung (16-19) ist bis 80% Sättigung effektiv

Stufe 20 Nahrung und Hobbitrassenspeisen sind bis 100% effektiv

Einspielung im Laufe des Tages.

so long…

Enialis

Siehe auch: [[Die_Chronik]]
