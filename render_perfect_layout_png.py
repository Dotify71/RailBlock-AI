import asyncio
from playwright.async_api import async_playwright
import os

async def render_perfect_slide():
    os.system("python3 fix_layout_and_text.py")

    async with async_playwright() as p:
        browser = await p.chromium.launch()
        page = await browser.new_page(viewport={"width": 1840, "height": 820}, device_scale_factor=2)
        
        file_url = "file://" + os.path.abspath("slide3_perfect_layout.html")
        await page.goto(file_url)
        await page.wait_for_timeout(1000)
        
        element = await page.query_selector(".main-content")
        out_path = "slide3_content_bw_perfect_8k.png"
        
        if element:
            await element.screenshot(path=out_path)
            print(f"Rendered Perfect B&W content 8K image: {out_path}")
        else:
            await page.screenshot(path=out_path)
            print(f"Rendered full page: {out_path}")

        await browser.close()

    # Copy to brain artifacts
    artifacts_dir = "/Users/dushyantacharya/.gemini/antigravity/brain/3e27fecf-19d5-4c17-9432-ffa2ce99e25f"
    if os.path.exists(artifacts_dir):
        os.system(f"cp {out_path} {artifacts_dir}/")
        print("Copied slide3_content_bw_perfect_8k.png to brain artifacts directory!")

if __name__ == "__main__":
    asyncio.run(render_perfect_slide())
