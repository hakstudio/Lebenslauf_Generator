# Lebenslauf Generator

🌍 [English](README.md) | [Deutsch](README.de.md)

Ein Werkzeug zur automatischen Erstellung eines professionellen, ATS-kompatiblen **tabellarischen Lebenslaufs** für den deutschen Arbeitsmarkt. Das Tool nutzt HTML/CSS-Vorlagen und Playwright für pixelgenaue PDF-Konvertierung.

## Deutsche CV-Standards

Dieser Generator folgt den etablierten deutschen Lebenslauf-Standards:

- **Tabellarisches Format** mit Daten links, Details rechts
- **Antichronologische Reihenfolge** (neueste zuerst) innerhalb jedes Abschnitts
- **Professionelles Bewerbungsfoto** oben rechts (~3,5 × 4,5 cm)
- **Datumsformat:** `MM/YYYY – MM/YYYY` mit Halbgeviertstrich
- **CEFR-Sprachniveaus** (A1–C2, Muttersprache)
- **Ort, Datum, Unterschrift** am Ende (Best Practice)
- **ATS-kompatibel:** Keine Icons, Fortschrittsbalken oder komplexe Grafiken

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
python3 generate_lebenslauf.py --config alt_config.json
```

Eine formatierte PDF-Datei (z. B. `Lebenslauf_Max_Mustermann.pdf`) wird generiert.

## Abschnittsreihenfolge (Standard)

| # | Abschnitt | Beschreibung |
|---|---|---|
| 1 | Persönliche Daten | Name, Adresse, Kontakt, Foto |
| 2 | Bildungsweg | Ausbildung (antichronologisch) |
| 3 | Berufserfahrung | Berufliche Stationen |
| 4 | Projekte | Projekte mit Technologien |
| 5 | Kenntnisse | Sprachen (CEFR) + IT-Kenntnisse |
| 6 | Sonstiges | Führerschein, Zertifikate usw. |
| 7 | Unterschrift | Ort, Datum, Unterschrift |

> Die Abschnittsreihenfolge ist über `settings.sections_order` in der config.json konfigurierbar.

## Abhängigkeiten
- Python 3.8+
- Playwright (`pip install playwright && playwright install chromium`)
