from playwright.async_api import async_playwright, Error
from typing import Any
from ..schemas.question import Source

class WebScrapeManager:
    timeout: int

    def __init__(self, timeout: int = 1000):
        self.timeout = timeout

    async def parse_question(self, link: str, src: str) -> dict:
        async with async_playwright() as pw:
            try:
                browser = await pw.chromium.launch(headless=True)
                context = await browser.new_context(
                    user_agent="Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/115.0.0.0 Safari/537.36",
                    viewport={"width": 1280, "height": 800},
                    java_script_enabled=True,
                    locale="en-CA"
                )
                page = await context.new_page()
                response = await page.goto(link)
                if not (response.status >= 200 and response.status < 300):
                    raise ValueError("Invalid link, parsing failed.")

                if src == Source.LEETCODE.value:
                    data = await self._parse_leetcode(page)
                else:
                    data = None
            except Error as e:
                raise ValueError(str(e))
            finally:
                await browser.close()

        if data is None:
            raise ValueError("Parsing unsupported for source: " + src)
        return data

    async def _parse_leetcode(self, page: Any) -> dict:
        await page.wait_for_selector("#__next", timeout=self.timeout)

        title = (await page.title()).strip().removesuffix("- LeetCode")
        prompt = (await page.locator('[data-track-load="description_content"]').all_inner_texts())[0]
        difficulty = (await page.locator('div[class*="text-difficulty-"]').inner_text(timeout=self.timeout)).lower()
        tags = [t.lower() for t in (await page.locator(".no-underline.hover\\:text-current.text-caption").all_inner_texts())]
        hints = (await page.locator(".text-body.elfjS").all_inner_texts())

        return {
            "title": title,
            "prompt": prompt,
            "difficulty": difficulty,
            "hints": hints,
            "tags": tags,
        }
