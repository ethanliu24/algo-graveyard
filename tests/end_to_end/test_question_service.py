import pytest

from app.exceptions.entity_not_found import EntityNotFoundError
from app.schemas.question import QuestionCreate

@pytest.mark.asyncio
async def test_all_crud_question_no_errors(question_service):
    """ Test a standard CRUD operation flow with no errors from the user end """

    data = {"source": "other", "link": "", "difficulty": "easy", "status": "completed", "title": "All CRUD end to end",
            "prompt": "no user errors", "notes": [], "hints": [], "tags": []}
    q = await question_service.create_question(QuestionCreate(**data))
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
async def test_deleting_all_questions(question_service):
    questions = (await question_service.get_all_questions()).data
    assert len(questions) > 0

    deleted = []
    for question in questions:
        deleted.append(await question_service.get_question(question.id))
        await question_service.delete_question(question.id)

    assert len((await question_service.get_all_questions()).data) == 0

    # Insert back to database for other tests
    for q in deleted:
        data = {"source": q.source, "link": q.link, "difficulty": q.difficulty, "status": q.status,
                "title": q.title, "prompt": q.prompt, "notes": q.notes, "hints": q.hints, "tags": q.tags}
        await question_service.create_question(QuestionCreate(**data), q.id)
