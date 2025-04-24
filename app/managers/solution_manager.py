from datetime import datetime, timezone
from ..daos.solution_dao import SolutionDAO
from ..exceptions.entity_not_found import EntityNotFoundError
from ..schemas.solution import Solution, SolutionCreate
from ..managers.ai_analysis_manager import AiAnalysisManager

class SolutionManager(object):
    solution_dao: SolutionDAO
    ai_analysis_service: AiAnalysisManager

    def __init__(self, solution_dao: SolutionDAO, ai_analysis_service: AiAnalysisManager):
        self.solution_dao = solution_dao
        self.ai_analysis_service = ai_analysis_service

    async def get_all_solutions(self, question_id: str) -> list[Solution]:
        res = self.solution_dao.get_all_solutions(question_id)
        if res is None:
            raise EntityNotFoundError("Invalid question ID.")
        return res

    async def get_solution(self, question_id: str, solution_id: str) -> Solution:
        res = self.solution_dao.get_solution(question_id, solution_id)
        if not res:
            raise EntityNotFoundError()
        return res

    async def create_solution(self, question_id: str, data: SolutionCreate, id: str = None) -> Solution:
        solution = data.model_dump()

        solution["language"] = solution["language"].value

        solution.update({"ai_analysis": self.ai_analysis_service.get_feedback(
            solution["question_title"],
            solution["question_prompt"],
            solution["language"],
            solution["code"]
        ).model_dump()})

        del solution["question_title"]
        del solution["question_prompt"]

        creation_time = datetime.now(timezone.utc)
        solution.update({ "created_at": creation_time, "last_modified": creation_time })

        res = self.solution_dao.create_solution(question_id, solution, id)
        if not res:
            raise EntityNotFoundError("Invalid question ID.")
        return res

    async def update_solution(self, question_id: str, solution_id: str, data: dict) -> Solution:
        solution = await self.get_solution(question_id, solution_id)
        solution_data = solution.model_dump()

        # update ai analysis if code is modified
        if "code" in data and data["code"] != solution_data["code"]:
            edited_code = data["code"]
            language = data.get("language", solution_data["language"])

            if "question_title" not in data or "question_prompt" not in data:
                raise ValueError("Question title and prompt must be provided")

            data.update({ "ai_analysis": self.ai_analysis_service.get_feedback(
                data["question_title"],
                data["question_prompt"],
                language,
                edited_code
            ).model_dump()})

        data.pop("question_prompt", None)
        data.pop("question_title", None)

        data.update({ "last_modified": datetime.now() })
        solution_data.update(data)
        _ = Solution(**solution_data) # validate data
        res = self.solution_dao.update_solution(question_id, solution_id, data)
        if not res:
            raise EntityNotFoundError("Invalid solution ID.")
        return res

    async def delete_solution(self, question_id: str, solution_id: str) -> None:
        if not self.solution_dao.delete_solution(question_id, solution_id):
            raise EntityNotFoundError()
