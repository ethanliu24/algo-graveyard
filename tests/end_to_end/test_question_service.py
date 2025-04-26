import pytest

from unittest.mock import patch
from app.exceptions.entity_not_found import EntityNotFoundError
from tests.seed import WEB_SCRAPE_DATA

@pytest.mark.asyncio
async def test_all_crud_question_no_errors(question_service):
    """ Test a standard CRUD operation flow with no errors from the user end """

    data = {"source": "other", "link": "", "difficulty": "easy", "status": "completed", "title": "All CRUD end to end",
            "prompt": "no user errors", "notes": [], "hints": [], "tags": []}
    q = await question_service.create_question(data)
    id = q.id

    q = await question_service.get_question(id)
    assert q.id == id
    assert q.title == "All CRUD end to end"

    q = await question_service.update_question({ "title": "Modified" }, id)
    assert q.title == "Modified"
    q = await question_service.get_question(id)
    assert q.title == "Modified"

    await question_service.delete_question(id)
    with pytest.raises(EntityNotFoundError) as info:
        await question_service.get_question(id)
    assert str(info.value) == "Invalid question ID."

@pytest.mark.asyncio
# @pytest.mark.skip(reason="Doesn't fetch all questions due to pagination. Need to iteratively fetch. Fix later.")
async def test_deleting_all_questions(question_service):
    deleted = []
    page = 1

    while True:
        pagination = (await question_service.get_all_questions(page=page))
        assert len(pagination.data) > 0

        for question in pagination.data:
            deleted.append(await question_service.get_question(question.id))
            await question_service.delete_question(question.id)


        page = pagination.page + 1
        if pagination.page == pagination.pages:
            break

    assert len((await question_service.get_all_questions()).data) == 0
    
    # Insert back to database for other tests
    with patch(
        "app.managers.web_scrape_manager.WebScrapeManager.parse_question",
        return_value=WEB_SCRAPE_DATA[0]
    ):
        for q in deleted:
            data = {"source": q.source.value, "link": q.link, "difficulty": q.difficulty.value,
                    "status": q.status.value, "title": q.title, "prompt": q.prompt, "notes": q.notes,
                    "hints": q.hints, "tags": [t.value for t in q.tags]}
            await question_service.create_question(data, q.id)
