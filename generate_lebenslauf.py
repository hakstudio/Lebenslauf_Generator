"""
Lebenslauf (CV) PDF Generator
Generates a professional, ATS-compatible German CV from config.json + template.html.
Uses Playwright headless Chromium for pixel-perfect PDF rendering.
"""

import json
import os
import asyncio
import argparse
from playwright.async_api import async_playwright

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
TEMPLATE_PATH = os.path.join(BASE_DIR, "template.html")


def load_config(config_path):
    """Load and parse the JSON configuration file."""
    with open(config_path, "r", encoding="utf-8") as f:
        return json.load(f)


# ============================================================
# HTML BUILDERS — Each section gets its own builder function
# ============================================================

def build_contact_block(personal):
    """Build the contact info grid in the header."""
    items = []

    # Row 1: Address
    if personal.get("address"):
        items.append(("Adresse", personal["address"]))

    # Row 2: Phone + Email
    if personal.get("phone"):
        items.append(("Telefon", personal["phone"]))
    if personal.get("email"):
        items.append(("E-Mail", personal["email"]))

    # Row 3: Date of birth + Place of birth
    if personal.get("date_of_birth"):
        items.append(("Geburtsdatum", personal["date_of_birth"]))
    if personal.get("place_of_birth"):
        items.append(("Geburtsort", personal["place_of_birth"]))

    # Row 4: Nationality
    if personal.get("nationality"):
        items.append(("Staatsangehörigkeit", personal["nationality"]))

    # Row 5: Optional links (LinkedIn, GitHub)
    if personal.get("linkedin"):
        items.append(("LinkedIn", personal["linkedin"]))
    if personal.get("github"):
        items.append(("GitHub", personal["github"]))

    html = ""
    for label, value in items:
        html += f'''<div class="cv-contact-item">
                <span class="cv-contact-label">{label}</span>
                <span class="cv-contact-value">{value}</span>
            </div>\n'''
    return html


def build_photo_block(personal):
    """Build the photo element if a photo file exists."""
    photo_file = personal.get("photo", "bewerbungsfoto.jpg")
    photo_path = os.path.join(BASE_DIR, photo_file)

    if os.path.exists(photo_path):
        return f'''<div class="cv-photo-container">
            <img src="file://{photo_path}" class="cv-photo" alt="Bewerbungsfoto" />
        </div>'''
    return ""


def build_education_section(education_list):
    """Build the Bildungsweg section."""
    if not education_list:
        return ""

    html = '<div class="cv-section">\n'
    html += '    <div class="cv-section-title">Bildungsweg</div>\n'
    html += '    <table class="cv-entry-table">\n'

    for entry in education_list:
        html += "        <tr>\n"
        html += f'            <td class="cv-date-col">{entry.get("period", "")}</td>\n'
        html += '            <td class="cv-detail-col">\n'
        html += f'                <div class="cv-entry-title">{entry.get("degree", "")}</div>\n'

        # Institution + Location on same line
        institution = entry.get("institution", "")
        location = entry.get("location", "")
        subtitle = f"{institution}, {location}" if location else institution
        html += f'                <div class="cv-entry-subtitle">{subtitle}</div>\n'

        # Detail bullet points (grade, focus area, etc.)
        details = entry.get("details", [])
        if details:
            html += '                <ul class="cv-detail-list">\n'
            for detail in details:
                html += f"                    <li>{detail}</li>\n"
            html += "                </ul>\n"

        html += "            </td>\n"
        html += "        </tr>\n"

    html += "    </table>\n"
    html += "</div>\n"
    return html


def build_experience_section(experience_list):
    """Build the Berufserfahrung section."""
    if not experience_list:
        return ""

    html = '<div class="cv-section">\n'
    html += '    <div class="cv-section-title">Berufserfahrung</div>\n'
    html += '    <table class="cv-entry-table">\n'

    for entry in experience_list:
        html += "        <tr>\n"
        html += f'            <td class="cv-date-col">{entry.get("period", "")}</td>\n'
        html += '            <td class="cv-detail-col">\n'
        html += f'                <div class="cv-entry-title">{entry.get("title", "")}</div>\n'

        company = entry.get("company", "")
        location = entry.get("location", "")
        subtitle = f"{company}, {location}" if location else company
        html += f'                <div class="cv-entry-subtitle">{subtitle}</div>\n'

        tasks = entry.get("tasks", [])
        if tasks:
            html += '                <ul class="cv-task-list">\n'
            for task in tasks:
                html += f"                    <li>{task}</li>\n"
            html += "                </ul>\n"

        html += "            </td>\n"
        html += "        </tr>\n"

    html += "    </table>\n"
    html += "</div>\n"
    return html


def build_projects_section(projects_list):
    """Build the Projekte section."""
    if not projects_list:
        return ""

    html = '<div class="cv-section">\n'
    html += '    <div class="cv-section-title">Projekte</div>\n'
    html += '    <table class="cv-entry-table">\n'

    for project in projects_list:
        html += "        <tr>\n"
        html += f'            <td class="cv-date-col">{project.get("period", "")}</td>\n'
        html += '            <td class="cv-detail-col">\n'

        # Project name + technologies on same line
        name = project.get("name", "")
        tech = project.get("technologies", "")
        tech_html = f' <span class="cv-project-tech">({tech})</span>' if tech else ""
        html += f'                <div><span class="cv-project-name">{name}</span>{tech_html}</div>\n'

        desc = project.get("description", "")
        if desc:
            html += f'                <div class="cv-project-desc">{desc}</div>\n'

        html += "            </td>\n"
        html += "        </tr>\n"

    html += "    </table>\n"
    html += "</div>\n"
    return html


def build_skills_section(skills):
    """Build the Kenntnisse section (languages + technical skills)."""
    if not skills:
        return ""

    html = '<div class="cv-section">\n'
    html += '    <div class="cv-section-title">Kenntnisse</div>\n'
    html += '    <table class="cv-skills-table">\n'

    # Languages
    languages = skills.get("languages", [])
    if languages:
        lang_html = ""
        for lang in languages:
            level = f' ({lang["level"]})' if lang.get("level") else ""
            lang_html += f'<div class="cv-lang-entry"><span class="cv-lang-name">{lang["name"]}</span><span class="cv-lang-level">{level}</span></div>\n'

        html += "        <tr>\n"
        html += '            <td class="cv-skills-label">Sprachen</td>\n'
        html += f'            <td class="cv-skills-value">{lang_html}</td>\n'
        html += "        </tr>\n"

    # Technical skills (grouped by category)
    technical = skills.get("technical", [])
    for tech in technical:
        category = tech.get("category", "")
        items = tech.get("items", "")
        html += "        <tr>\n"
        html += f'            <td class="cv-skills-label">{category}</td>\n'
        html += f'            <td class="cv-skills-value">{items}</td>\n'
        html += "        </tr>\n"

    html += "    </table>\n"
    html += "</div>\n"
    return html


def build_other_section(other_list):
    """Build the Sonstiges section."""
    if not other_list:
        return ""

    html = '<div class="cv-section">\n'
    html += '    <div class="cv-section-title">Sonstiges</div>\n'
    html += '    <ul class="cv-other-list">\n'
    for item in other_list:
        html += f"        <li>{item}</li>\n"
    html += "    </ul>\n"
    html += "</div>\n"
    return html


def build_signature_block(signature, settings):
    """Build the Ort, Datum, Unterschrift block."""
    if not signature:
        return ""

    city = signature.get("city", "")
    date = signature.get("date", "")
    sig_scale = signature.get("scale", 100)

    html = '<div class="cv-signature">\n'

    # City, Date line
    if city and date:
        html += f'    <div class="cv-signature-location-date">{city}, {date}</div>\n'
    elif date:
        html += f'    <div class="cv-signature-location-date">{date}</div>\n'

    # Signature image
    sig_image = signature.get("image", "")
    if sig_image:
        sig_path = os.path.join(BASE_DIR, sig_image)
        if os.path.exists(sig_path):
            sig_style = f"zoom: {sig_scale / 100.0}; mix-blend-mode: multiply;"
            html += f'    <img src="file://{sig_path}" class="cv-signature-img" style="{sig_style}" />\n'
        else:
            # Spacer if no signature image exists
            html += '    <div style="height: 12mm;"></div>\n'
    else:
        html += '    <div style="height: 12mm;"></div>\n'

    html += "</div>\n"
    return html


# ============================================================
# SECTION ORDER MAPPING
# ============================================================

# Maps section key names to their builder functions and config keys
SECTION_BUILDERS = {
    "education": lambda config: build_education_section(config.get("education", [])),
    "experience": lambda config: build_experience_section(config.get("experience", [])),
    "projects": lambda config: build_projects_section(config.get("projects", [])),
    "skills": lambda config: build_skills_section(config.get("skills", {})),
    "other": lambda config: build_other_section(config.get("other", [])),
}


def build_all_sections(config, section_order):
    """Build CV sections based on the provided list of section keys."""
    sections_html = ""
    for section_key in section_order:
        builder = SECTION_BUILDERS.get(section_key)
        if builder:
            sections_html += builder(config)

    return sections_html


# ============================================================
# HTML GENERATION
# ============================================================

def generate_html(config, output_html_path):
    """Load the template, replace all placeholders, and write the final HTML."""
    settings = config.get("settings", {})
    layout = settings.get("layout", {})
    
    style = layout.get("style", "classic")
    template_name = "template_modern.html" if style == "modern" else "template_classic.html"
    template_path = os.path.join(BASE_DIR, template_name)
    
    if not os.path.exists(template_path):
        raise FileNotFoundError(f"Template {template_name} nicht gefunden!")

    with open(template_path, "r", encoding="utf-8") as f:
        html = f.read()

    personal = config.get("personal", {})
    settings = config.get("settings", {})
    font_conf = settings.get("font", {})
    layout = settings.get("layout", {})
    signature = config.get("signature", {})

    # ---- Font settings ----
    html = html.replace("{{ FONT_FAMILY }}", font_conf.get("family", '"Segoe UI", Arial, sans-serif'))
    html = html.replace("{{ FONT_SIZE_BODY }}", str(font_conf.get("size_body", 10)))
    html = html.replace("{{ FONT_SIZE_SECTION }}", str(font_conf.get("size_section_title", 12)))
    html = html.replace("{{ FONT_SIZE_NAME }}", str(font_conf.get("size_name", 16)))

    # ---- Layout settings ----
    html = html.replace("{{ PAGE_MARGIN_TOP }}", layout.get("page_margin_top", "20mm"))
    html = html.replace("{{ PAGE_MARGIN_BOTTOM }}", layout.get("page_margin_bottom", "15mm"))
    html = html.replace("{{ PAGE_MARGIN_LEFT }}", layout.get("page_margin_left", "25mm"))
    html = html.replace("{{ PAGE_MARGIN_RIGHT }}", layout.get("page_margin_right", "20mm"))
    html = html.replace("{{ DATE_COLUMN_WIDTH }}", layout.get("date_column_width", "28%"))
    html = html.replace("{{ ACCENT_COLOR }}", layout.get("accent_color", "#1e3a5f"))

    # Photo dimensions (default: passport-style 35mm x 45mm)
    html = html.replace("{{ PHOTO_WIDTH }}", layout.get("photo_width", "35mm"))
    html = html.replace("{{ PHOTO_HEIGHT }}", layout.get("photo_height", "45mm"))

    # ---- Header: Name ----
    html = html.replace("{{ NAME }}", personal.get("name", ""))

    # ---- Header: Contact grid ----
    html = html.replace("{{ CONTACT_BLOCK }}", build_contact_block(personal))

    # ---- Header: Photo ----
    html = html.replace("{{ PHOTO_BLOCK }}", build_photo_block(personal))

    # ---- Sections (dynamic, ordered) ----
    main_order = settings.get("sections_order", ["education", "experience", "projects"])
    sidebar_order = settings.get("sidebar_sections_order", ["skills", "other"])

    if style == "classic":
        # In classic layout, everything goes into the main column sequentially
        combined_order = main_order + sidebar_order
        html = html.replace("{{ SECTIONS_HTML }}", build_all_sections(config, combined_order))
        html = html.replace("{{ SIDEBAR_SECTIONS_HTML }}", "") # Unused in classic
    else:
        # In modern layout, split them
        html = html.replace("{{ SECTIONS_HTML }}", build_all_sections(config, main_order))
        html = html.replace("{{ SIDEBAR_SECTIONS_HTML }}", build_all_sections(config, sidebar_order))

    # ---- Signature block ----
    html = html.replace("{{ SIGNATURE_BLOCK }}", build_signature_block(signature, settings))

    # ---- Debug mode ----
    debug_css = ""
    if layout.get("debug_colors", False):
        debug_css = """
        .cv-header { background-color: rgba(255, 0, 0, 0.1) !important; border: 1px solid red; }
        .cv-section { background-color: rgba(0, 255, 0, 0.1) !important; border: 1px solid green; }
        .cv-signature { background-color: rgba(0, 0, 255, 0.1) !important; border: 1px solid blue; }
        .cv-photo { border: 2px solid red !important; }
        """
    html = html.replace("{{ DEBUG_CSS }}", debug_css)

    # Write the final HTML
    with open(output_html_path, "w", encoding="utf-8") as f:
        f.write(html)

    return output_html_path


# ============================================================
# PDF GENERATION (Playwright)
# ============================================================

async def generate_pdf(html_path, output_pdf_path, force_single_page=False):
    """Render the HTML to a pixel-perfect A4 PDF using headless Chromium."""
    async with async_playwright() as p:
        browser = await p.chromium.launch()
        page = await browser.new_page()

        # Set A4-equivalent viewport for consistent rendering
        await page.set_viewport_size({"width": 794, "height": 1122})
        await page.emulate_media(media="print")
        await page.goto(f"file://{html_path}", wait_until="networkidle")

        if force_single_page:
            # Inject Javascript loop to actively reduce zoom until the document height shrinks to 1 page
            await page.evaluate("""() => {
                let zoomLevel = 1.0;
                // A4 height is 1122px. Margins: top 15mm, bottom 15mm = 30mm (~113px).
                // 1122 - 113 = 1009px absolute physical maximum body height. 
                const max_printable_height = 1000;
                while (document.documentElement.scrollHeight > max_printable_height && zoomLevel > 0.85) {
                    zoomLevel -= 0.02;
                    document.body.style.zoom = zoomLevel;
                }
            }""")

        # Generate PDF with zero margins (margins are handled in CSS @page)
        await page.pdf(
            path=output_pdf_path,
            width="210mm",
            height="297mm",
            print_background=True,
            margin={"top": "0", "right": "0", "bottom": "0", "left": "0"},
        )
        await browser.close()

    # Clean up temporary HTML file
    if os.path.exists(html_path):
        os.remove(html_path)

    print(f"✅ Lebenslauf PDF erfolgreich generiert: {output_pdf_path}")


# ============================================================
# MAIN
# ============================================================

def main():
    parser = argparse.ArgumentParser(
        description="Generiere einen professionellen Lebenslauf als PDF"
    )
    parser.add_argument(
        "--config",
        default="config.json",
        help="Pfad zur config.json Datei (Standard: config.json)",
    )
    args = parser.parse_args()

    config_path = os.path.abspath(args.config)

    if not os.path.exists(config_path):
        print(f"❌ Config-Datei nicht gefunden: {config_path}")
        print("   Erstelle eine config.json aus config.example.json:")
        print("   cp config.example.json config.json")
        return

    try:
        config = load_config(config_path)

        # Generate output filename from sender name
        name = config.get("personal", {}).get("name", "Bewerber")
        safe_name = (
            name.replace(" ", "_")
            .replace("ö", "oe")
            .replace("ü", "ue")
            .replace("ä", "ae")
            .replace("ß", "ss")
        )

        output_pdf = os.path.join(BASE_DIR, f"Lebenslauf_{safe_name}.pdf")
        temp_html = os.path.join(
            BASE_DIR, f"temp_{os.path.basename(config_path)}.html"
        )

        # Step 1: Generate HTML from template + config
        html_file = generate_html(config, temp_html)

        # Step 2: Convert HTML to PDF via Playwright
        force_single_page = config.get("settings", {}).get("force_single_page", False)
        asyncio.run(generate_pdf(html_file, output_pdf, force_single_page))

    except json.JSONDecodeError as e:
        print(f"❌ JSON-Fehler in {config_path}: {e}")
    except Exception as e:
        print(f"❌ Fehler bei der Generierung: {e}")
        raise


if __name__ == "__main__":
    main()
