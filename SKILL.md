---
name: "Lebenslauf Generator"
description: "Generates a professional, ATS-compatible German CV (Lebenslauf) PDF from a JSON configuration file and an HTML template."
---

# Skill: Lebenslauf Generator

**Context:** The user applies for jobs/apprenticeships in Germany (Ausbildung, etc.) and needs a professional, tabular CV (Lebenslauf) that follows German standards. This skill allows an AI agent to generate a perfectly formatted, ready-to-send PDF.

## Folder
The generator is located at:
`/Users/hak/Projects/Others/Geçmiş Projeler/Lebenslauf_Generator/`

## How it Works

This generator relies on a single JSON configuration file containing all CV data.
The output is a `Lebenslauf_{Name}.pdf` file in the generator directory.

---

### Step 1: Create the Config File

If the user asks you to generate or update their CV, prepare the data as a `config.json` file.

**Config File Structure (`--config`)**
```json
{
  "personal": {
    "name": "Full Name",
    "address": "Street, PLZ City",
    "phone": "+49 ...",
    "email": "email@example.com",
    "date_of_birth": "DD.MM.YYYY",
    "place_of_birth": "City",
    "nationality": "Deutsch",
    "photo": "bewerbungsfoto.jpg",
    "linkedin": "linkedin.com/in/...",
    "github": "github.com/..."
  },
  "education": [
    {
      "period": "MM/YYYY – MM/YYYY",
      "degree": "Degree Title",
      "institution": "School/University Name",
      "location": "City",
      "details": ["Detail 1", "Note: X,X"]
    }
  ],
  "experience": [
    {
      "period": "MM/YYYY – heute",
      "title": "Job Title",
      "company": "Company Name",
      "location": "City",
      "tasks": ["Task 1", "Task 2"]
    }
  ],
  "projects": [
    {
      "name": "Project Name",
      "period": "YYYY",
      "technologies": "Tech1, Tech2",
      "description": "Brief description"
    }
  ],
  "skills": {
    "languages": [
      { "name": "Deutsch", "level": "Muttersprache" },
      { "name": "Englisch", "level": "B2" }
    ],
    "technical": [
      { "category": "Programmiersprachen", "items": "Dart, Java, Python" },
      { "category": "Frameworks & Tools", "items": "Flutter, Git" }
    ]
  },
  "other": ["Führerschein Klasse B"],
  "signature": {
    "city": "City",
    "date": "DD. Monat YYYY",
    "image": "unterschrift.jpg",
    "scale": 15
  },
  "settings": {
    "font": {
      "family": "\"Segoe UI\", Arial, Helvetica, sans-serif",
      "size_body": 10,
      "size_section_title": 12,
      "size_name": 16
    },
    "layout": {
      "page_margin_top": "20mm",
      "page_margin_bottom": "15mm",
      "page_margin_left": "25mm",
      "page_margin_right": "20mm",
      "date_column_width": "28%",
      "accent_color": "#1e3a5f",
      "debug_colors": false
    },
    "sections_order": [
      "education",
      "experience",
      "projects",
      "skills",
      "other"
    ]
  }
}
```

**Key Settings Reference:**

| Setting | Default | Description |
|---|---|---|
| `accent_color` | `"#1e3a5f"` | Primary color for headings and dividers |
| `date_column_width` | `"28%"` | Width of the left date column |
| `sections_order` | See above | Controls which sections appear and in what order |
| `debug_colors` | `false` | Renders colored borders on layout blocks for debugging |

---

### Step 2: Execute Generator

Run the generator script via terminal:

```bash
cd "/Users/hak/Projects/Others/Geçmiş Projeler/Lebenslauf_Generator/"
python3 generate_lebenslauf.py --config config.json
```

---

## German CV Rules (CRITICAL)

The AI agent **MUST** follow these rules when generating content:

### Layout Selection (`settings.layout.style`)
- **`"classic"` (1-Column):** Use when applying via online portals (Workday, Stepstone, SAP) or for very conservative industries (banking, law). It guarantees 100% ATS-parsing compatibility.
- **`"modern"` (2-Column):** Use when sending via direct email, handing it in physically, or applying to IT/Tech/Start-ups/Creative roles. It is highly preferred by human readers due to its scannability.

### Section Order (for Berufseinsteiger / Career Starters)
1. Persönliche Daten → 2. Bildungsweg → 3. Berufserfahrung → 4. Projekte → 5. Kenntnisse → 6. Sonstiges → 7. Unterschrift

> **Note:** For experienced professionals, swap Berufserfahrung and Bildungsweg.

### Content Rules
- **Dates:** Use `MM/YYYY – MM/YYYY` or `MM/YYYY – heute` format. Use en-dash (–), not hyphen (-).
- **Antichronological:** Most recent entry first within each section.
- **Language levels:** Use CEFR scale: A1, A2, B1, B2, C1, C2, or "Muttersprache".
- **No narrative text:** Use bullet points, not paragraphs.
- **Driving license:** Write "Führerschein Klasse B" (not B197 or B78).
- **Photo:** Professional headshot, placed top-right, ~3.5 × 4.5 cm.

### Typography Rules
- **Font size:** Body 10–11pt, section titles 12pt, name 16pt.
- **Bold:** Section titles and entry titles only.
- **No ALL CAPS** in names or company names (only section titles use uppercase).
- **Text alignment:** Left-aligned (Linksbündig), never justified.

### Formatting Rules
- **Length:** Maximum 1–2 pages (A4).
- **Margins:** Left 25mm, right 20mm, top 20mm, bottom 15mm.
- **Consistent spacing** between all sections.
- **PDF output** only (never Word, never image).

---

## Constraints & Important Notes

- **Photos:** The template expects `bewerbungsfoto.jpg` or `.png` in the generator directory.
- **Signatures:** Expects `unterschrift.jpg` or `.png`. White backgrounds are blended via CSS `mix-blend-mode: multiply`.
- **Paths:** The resulting PDF is saved in the generator folder as `Lebenslauf_{Name}.pdf`.
- **Dependencies:** Requires `playwright` (`pip install playwright && playwright install chromium`).

## Final Delivery
Inform the user that the PDF has been generated and provide the absolute path to the resulting file.
