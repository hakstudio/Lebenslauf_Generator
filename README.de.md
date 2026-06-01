# Lebenslauf Generator

🌍 [English](README.md) | [Deutsch](README.de.md)

Ein Werkzeug zur automatischen Erstellung eines professionellen, ATS-kompatiblen **tabellarischen Lebenslaufs** für den deutschen Arbeitsmarkt. Das Tool nutzt HTML/CSS-Vorlagen und Playwright für pixelgenaue PDF-Konvertierung.

## Deutsche CV-Standards

Dieser Generator folgt den etablierten deutschen Lebenslauf-Standards:

- **Tabellarisches Format** mit Daten links, Details rechts
- **Antichronologische Reihenfolge** (neueste zuerst) innerhalb jedes Abschnitts
- **Professionelles Bewerbungsfoto** oben rechts (~3,5 × 4,5 cm)
- **Kurzprofil** (kurze Zusammenfassung) unter dem Header
- **Datumsformat:** `MM/YYYY – MM/YYYY` mit Halbgeviertstrich
- **Ort, Datum, Unterschrift** am Ende (Best Practice)
- **Auto-Datum:** Das Unterschriftsdatum wird bei jeder Generierung automatisch aktualisiert
- **ATS-kompatibel:** Keine Icons, Fortschrittsbalken oder komplexe Grafiken
- **Einseitig optimiert:** Schriftgrößen und Abstände für kompaktes Layout

## Einrichtung & Verwendung

### 1. Konfigurationsdatei erstellen
```bash
cp config.example.json config.json
```
Öffnen Sie `config.json` und tragen Sie Ihre tatsächlichen Daten ein.

### 2. Bewerbungsfoto hinzufügen
Speichern Sie Ihr professionelles Foto als **`bewerbungsfoto.jpg`** (oder `.png`) in diesem Ordner.

### 3. Unterschrift hinzufügen (Optional)
Speichern Sie Ihre Unterschrift als **`unterschrift.jpg`** (oder `.png`) in diesem Ordner.
- **Tipp:** CSS `mix-blend-mode: multiply` macht weiße Hintergründe automatisch transparent.

### 4. PDF generieren
Voraussetzung: Playwright (`pip install playwright && playwright install chromium`):
```bash
python3 generate_lebenslauf.py
```
Alternative Konfigurationsdatei:
```bash
python3 generate_lebenslauf.py --config config.gastronomie.json
```
HTML-Datei zum Debuggen beibehalten:
```bash
python3 generate_lebenslauf.py --keep-html
```

## Multi-Config-Workflow

Erstellen Sie verschiedene Konfigurationsdateien für verschiedene Berufsfelder:
- `config.json` — IT / Softwareentwicklung
- `config.gastronomie.json` — Gastronomie
- `config.kaufmann.json` — Kaufmann / Wirtschaft

Alle verwenden das gleiche klassische Layout — nur der Inhalt ändert sich.

## Abschnittsreihenfolge (Standard)

| # | Abschnitt | Beschreibung |
|---|---|---|
| 1 | Persönliche Daten | Name, Adresse, Kontakt, Foto |
| 2 | Kurzprofil | 2-3 Sätze Zusammenfassung |
| 3 | Berufserfahrung | Berufliche Stationen |
| 4 | Bildungsweg | Ausbildung (antichronologisch) |
| 5 | Projekte | Projekte mit Technologien |
| 6 | Kenntnisse | Sprachen + IT-Kenntnisse |
| 7 | Sonstiges | Führerschein, Zertifikate usw. |
| 8 | Unterschrift | Ort, Datum, Unterschrift |

> Die Abschnittsreihenfolge ist über `settings.sections_order` in der config.json konfigurierbar.

## CLI-Argumente

| Argument | Standard | Beschreibung |
|---|---|---|
| `--config` | `config.json` | Pfad zur Konfigurationsdatei |
| `--keep-html` | `false` | HTML-Datei nach der PDF-Generierung beibehalten |

## Abhängigkeiten
- Python 3.8+
- Playwright (`pip install playwright && playwright install chromium`)
