import asyncio
from playwright.async_api import async_playwright

async def run():
    async with async_playwright() as p:
        browser = await p.chromium.launch()
        page = await browser.new_page()
        await page.set_viewport_size({"width": 794, "height": 1122})
        await page.emulate_media(media="print")
        await page.goto("file:///Users/hak/Projects/Others/CV/temp_config.json.html", wait_until="networkidle")
        
        zoomLevel = await page.evaluate("""() => {
            let zoomLevel = 1.0;
            const max_printable_height = 1015;
            const wrapper = document.createElement('div');
            while (document.body.firstChild) {
                wrapper.appendChild(document.body.firstChild);
            }
            document.body.appendChild(wrapper);
            
            while ((wrapper.scrollHeight * zoomLevel) > max_printable_height && zoomLevel >= 0.65) {
                zoomLevel -= 0.01;
                document.body.style.zoom = zoomLevel;
            }
            return zoomLevel;
        }""")
        print(f"Final Zoom Level: {zoomLevel}")
        await browser.close()

asyncio.run(run())
