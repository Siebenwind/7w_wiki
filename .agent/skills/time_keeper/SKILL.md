---
layout: wiki_page
name: Time Keeper
description: Utilities for handling the Siebenwind "Sonnenzirkel" time system (Calendar, Seasons, Dates).
---

# Time Keeper – Sonnenzirkel Kalender

**Epistemischer Status:** #perspektive

This skill provides utilities to work with the customized "Sonnenzirkel" calendar of Siebenwind.
Use this whenever you need to:
1.  Check which Season (Morsan, Vitama, Astrael, Bellum) a month belongs to.
2.  Convert an approximate Earth month (e.g., "August") to a Siebenwind month.
3.  Validate if a date (Day + Month) is valid within the 28-day standard month.
4.  List the order of months.

# Commands

The script is located at `.agent/skills/time_keeper/scripts/sonnenzirkel.py`.

### 1. Check Season
**Goal:** Find out if "Sekar" is in Winter or Summer.
```bash
python3 .agent/skills/time_keeper/scripts/sonnenzirkel.py season [MonthName]
```
*Example:* `python3 .agent/skills/time_keeper/scripts/sonnenzirkel.py season Sekar` -> "Morsan"

### 2. Convert Earth Month
**Goal:** Translate "December" (12) to Siebenwind.
```bash
python3 .agent/skills/time_keeper/scripts/sonnenzirkel.py convert [MonthIndex]
```
*Example:* `python3 .agent/skills/time_keeper/scripts/sonnenzirkel.py convert 12` -> "Sekar"

### 3. Validate Date
**Goal:** Check if "30. Sekar" is a valid date (Standard months have 28 days).
```bash
python3 .agent/skills/time_keeper/scripts/sonnenzirkel.py validate [Day] [MonthName]
```
*Example:* `python3 .agent/skills/time_keeper/scripts/sonnenzirkel.py validate 30 Sekar` -> "INVALID: Day out of range"

### 4. List All
**Goal:** See the full calendar structure.
```bash
python3 .agent/skills/time_keeper/scripts/sonnenzirkel.py list
```
