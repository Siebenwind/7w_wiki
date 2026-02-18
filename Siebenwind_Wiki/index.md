---
layout: wiki_page
title: Siebenwind Wiki
category: Index
---

<div class="hero-wrapper">
  <p class="hero-kicker">Das Archiv</p>
  <h1 class="hero-title">Siebenwind Wiki</h1>
  <p class="hero-subtitle">Willkommen im zentralen Wissensspeicher der Welt Siebenwind. Hier finden sich alle kanonischen Informationen, von den Göttern bis zur Geografie.</p>
</div>

## Abteilungen

<div class="portal-grid">
  <a href="00_Fundament/" class="portal-card"><h3>Fundament</h3><p>Register, Völker & Magie.</p></a>
  <a href="01_Pantheon/" class="portal-card"><h3>Pantheon</h3><p>Götter & Religion.</p></a>
  <a href="02_Geografie/" class="portal-card"><h3>Geografie</h3><p>Atlas & Orte.</p></a>
  <a href="03_Gesellschaft/" class="portal-card"><h3>Gesellschaft</h3><p>Stände & Politik.</p></a>
  <a href="04_Chronik/" class="portal-card"><h3>Chronik</h3><p>Geschichte & Boten.</p></a>
  <a href="07_Persoenlichkeiten/" class="portal-card"><h3>Personen</h3><p>Who is Who.</p></a>
  <a href="09_Bibliothek/" class="portal-card"><h3>Bibliothek</h3><p>Werke & Schriften.</p></a>
  <a href="10_Archiv/" class="portal-card"><h3>Archiv</h3><p>Verwaltung & Stats.</p></a>
</div>

## Projekt Status

<p align="center">
  <a href="https://github.com/Siebenwind/7w_wiki" target="_blank">
    <img src="https://img.shields.io/badge/Status-Aktiv-vibrantgreen?style=for-the-badge&logo=github" alt="Project Status">
  </a>
  <a href="../CHANGELOG.md">
    <img src="https://img.shields.io/badge/Version-Reconstruction_v2.1-orange?style=for-the-badge" alt="Version">
  </a>
</p>

### System-Architektur

```mermaid
graph TD
    A["🗂️ Rohdaten"] -->|Ingestion| B("🤖 Lore Extraktion")
    B -->|Validation| C{"⚖️ Konsistenz-Audit"}
    C -->|Kanon| D["📚 Wiki-Archiv"]
    D -->|Semantic Search| F["👁️ Das Orakel"]
```

*Stand: 2026 | LeCorbeau & Siebenwind*
