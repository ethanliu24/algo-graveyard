from datetime import datetime
from ..daos.solution_dao import SolutionDAO
from ..exceptions.entity_not_found import EntityNotFoundError
from ..schemas.solution import Solution, SolutionCreate

class SolutionManager(object):
    solution_dao: SolutionDAO

    def __init__(self, solution_dao: SolutionDAO):
        self.solution_dao = solution_dao

    async def get_all_solutions(self, question_id: str) -> list[Solution]:
        res = self.solution_dao.get_all_solutions(question_id)
        if res is None:
            raise EntityNotFoundError("Invalid question ID")
        return res

    async def get_solution(self, question_id: str, solution_id: str) -> Solution:
        res = self.solution_dao.get_solution(question_id, solution_id)
        if not res:
            raise EntityNotFoundError()
        return res

    async def create_solution(self, question_id: str, data: SolutionCreate, id: str = None) -> Solution:
        solution = data.model_dump()

        solution["language"] = solution["language"].value

        # TODO add ai analysis
        solution.update({"ai_analysis": {
            "time_complexity": "",
            "space_complexity": "",
            "feedback": ""
        }})

        creation_time = datetime.now()
        solution.update({ "created_at": creation_time, "last_modified": creation_time })

        res = self.solution_dao.create_solution(question_id, solution, id)
        if not res:
            raise EntityNotFoundError("Invalid question ID")
        return res

    async def update_solution(self, question_id: str, solution_id: str, data: dict) -> Solution:
        solution = await self.get_solution(question_id, solution_id)
        solution_data = solution.model_dump()
        data.update({ "last_modified": datetime.now() })
        solution_data.update(data)
        _ = Solution(**solution_data) # validate data
        res = self.solution_dao.update_solution(question_id, solution_id, data)
        if not res:
            raise EntityNotFoundError("Invalid solution ID")
        return res

    async def delete_solution(self, question_id: str, solution_id: str) -> None:
        if not self.solution_dao.delete_solution(question_id, solution_id):
            raise EntityNotFoundError()
