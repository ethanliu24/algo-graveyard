import pytest

from app.schemas.question import QuestionCreate
from app.schemas.solution import SolutionCreate

@pytest.mark.asyncio
async def test_all_crud_solution_no_errors(question_service, solution_service):
    """ Test a standard CRUD operation flow with no errors from the user end """
    q_data = {"source": "other", "link": "", "status": "completed", "title": "All CRUD end to end",
            "prompt": "no user errors", "test_cases": [], "notes": [], "hints": [], "tags": []}
    s_data = {"summary": "Created", "explanation": "created in test_create_solution_basic",
              "language": "python", "time_complexity": "n!", "space_complexity": "n!", "code": ""}

    q = await question_service.create_question(QuestionCreate(**q_data))
    q_id = q.id
    s = await solution_service.create_solution(q_id, SolutionCreate(**s_data))
    s_id = s.id

    s = await solution_service.get_solution(q_id, s_id)
    assert s.summary == "Created"

    s = await solution_service.update_solution(q_id, s_id, { "summary": "Updated" })
    assert s.summary == "Updated"
    s = await solution_service.get_solution(q_id, s_id)
    assert s.summary == "Updated"

    assert await solution_service.delete_solution(q_id, s_id) is None
