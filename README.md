# Lebenslauf Generator (CV Generator)

🌍 [English](README.md) | [Deutsch](README.de.md)

A tool to automatically generate a professional, ATS-compatible **tabellarischer Lebenslauf** (tabular CV) for the German job market. The tool uses HTML/CSS templates and Playwright for pixel-perfect PDF conversion.

## German CV Standards

This generator follows established German CV best practices:

- **Tabular format** with dates on the left, details on the right
- **Reverse-chronological order** (most recent first) within each section
- **Professional photo** placement in the top-right corner (~3.5 × 4.5 cm)
- **Date format:** `MM/YYYY – MM/YYYY` with en-dash
- **CEFR language levels** (A1–C2, Muttersprache)
- **Ort, Datum, Unterschrift** at the bottom (standard practice)
- **ATS-compatible:** No icons, progress bars, or complex graphics

### Sections (Default Order)

| # | Section | Description |
|---|---|---|
| 1 | Persönliche Daten | Name, address, contact, photo |
| 2 | Bildungsweg | Education (reverse-chronological) |
| 3 | Berufserfahrung | Work experience |
| 4 | Projekte | Projects with technologies |
| 5 | Kenntnisse | Languages (CEFR) + Technical skills |
| 6 | Sonstiges | Driving license, certifications, etc. |
| 7 | Unterschrift | City, date, signature |

> The section order is configurable via `settings.sections_order` in config.json.

## Setup & Usage

### 1. Create the Config File
```bash
cp config.example.json config.json
```
Open `config.json` and fill in your actual details. See `config.example.json` for the full structure with all available fields.

### 2. Add Your Photo
Save your professional photo as **`bewerbungsfoto.jpg`** (or `.png`) in this folder.

### 3. Add Your Signature (Optional)
Save your signature as **`unterschrift.jpg`** (or `.png`) in this folder.
- **Pro Feature:** CSS `mix-blend-mode: multiply` automatically makes white backgrounds transparent.

### 4. Generate the PDF
Requires Playwright (`pip install playwright && playwright install chromium`):
```bash
python3 generate_lebenslauf.py
```
Custom config file:
```bash
python3 generate_lebenslauf.py --config alt_config.json
```

A formatted PDF (e.g., `Lebenslauf_Max_Mustermann.pdf`) will be generated.

## Configuration Reference

### Personal Data (`personal`)
| Field | Required | Example |
|---|---|---|
| `name` | ✅ | `"Max Mustermann"` |
| `address` | ✅ | `"Musterstraße 123, 12345 Musterstadt"` |
| `phone` | ✅ | `"+49 152 12345678"` |
| `email` | ✅ | `"max@example.com"` |
| `date_of_birth` | Recommended | `"01.01.1990"` |
| `place_of_birth` | Recommended | `"Musterstadt"` |
| `nationality` | Recommended | `"Deutsch"` |
| `photo` | Recommended | `"bewerbungsfoto.jpg"` |
| `linkedin` | Optional | `"linkedin.com/in/mustermann"` |
| `github` | Optional | `"github.com/mustermann"` |

### Layout Settings (`settings.layout`)
| Setting | Default | Description |
|---|---|---|
| `style` | `"classic"` | Layout style: `"classic"` (1-column, ATS-safe) or `"modern"` (2-column, HR-friendly) |
| `accent_color` | `"#1e3a5f"` | Primary accent color for headings and dividers |
| `date_column_width` | `"28%"` | Width of the left date column |
| `page_margin_*` | `20/15/25/20mm` | Top/Bottom/Left/Right page margins |
| `debug_colors` | `false` | Renders colored borders on each layout block |

### Font Settings (`settings.font`)
| Setting | Default | Description |
|---|---|---|
| `size_body` | `10` | Body text size (pt) |
| `size_section_title` | `12` | Section heading size (pt) |
| `size_name` | `16` | Name size (pt) |

## Dependencies
- Python 3.8+
- Playwright (`pip install playwright && playwright install chromium`)
