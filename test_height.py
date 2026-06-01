import asyncio
from playwright.async_api import async_playwright

async def run():
    async with async_playwright() as p:
        browser = await p.chromium.launch()
        page = await browser.new_page()
        await page.set_viewport_size({"width": 794, "height": 1122})
        await page.emulate_media(media="print")
        await page.goto("file:///Users/hak/Projects/Others/CV/temp_config.json.html", wait_until="networkidle")
        
        height = await page.evaluate("""() => {
            const wrapper = document.createElement('div');
            while (document.body.firstChild) {
                wrapper.appendChild(document.body.firstChild);
            }
            document.body.appendChild(wrapper);
            return wrapper.scrollHeight;
        }""")
        print(f"Content Height: {height} (Max Printable is ~1015)")
        await browser.close()

asyncio.run(run())
