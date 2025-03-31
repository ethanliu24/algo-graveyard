import pytest

from app.schemas.question import QuestionCreate

@pytest.mark.asyncio
async def test_deleting_everything(question_service):
    questions = await question_service.get_all_questions()
    assert len(questions) > 0

    for question in questions:
        print(question.id)
        await question_service.delete_question(question.id)

    assert len(await question_service.get_all_questions()) == 0

    # Insert back to database for other tests
    for q in questions:
        data = {"source": q.source, "link": q.link, "status": q.status, "title": q.title,
                "prompt": q.prompt, "test_cases": q.test_cases, "notes": q.notes, "hints": q.hints,
                "tags": q.tags}
        await question_service.create_question(QuestionCreate(**data))
