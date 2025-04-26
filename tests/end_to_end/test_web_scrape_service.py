import pytest

from app.schemas.question import Source

Q = {
    "source": "leetcode",
    "link": "https://example.com",
    "difficulty": "easy",
    "status": "completed",
    "title": "Create Question Valid Title",
    "prompt": "",
    "notes": [],
    "hints": [],
    "tags": []
}

@pytest.mark.asyncio
async def test_scrape_invalid_link(web_scrape_service):
    with pytest.raises(ValueError):
        await web_scrape_service.parse_question("invalid", Source.LEETCODE.value)

@pytest.mark.asyncio
async def test_scrape_invalid_source(web_scrape_service):
    with pytest.raises(ValueError):
        # source "OTHER" not supported
        await web_scrape_service.parse_question(Q["link"], Source.OTHER.value)
    with pytest.raises(ValueError):
        await web_scrape_service.parse_question(Q["link"], "abc")
