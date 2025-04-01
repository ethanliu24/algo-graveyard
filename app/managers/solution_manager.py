from datetime import datetime
from ..daos.solution_dao import SolutionDAO
from ..schemas.solution import Solution, SolutionCreate

class SolutionManager(object):
    solution_dao: SolutionDAO

    def __init__(self, solution_dao: SolutionDAO):
        self.solution_dao = solution_dao

    async def get_all_solutions(self, question_id: str) -> list[Solution]:
        return self.solution_dao.get_all_solutions(question_id)

    async def get_solution(self, question_id: str, solution_id: str) -> Solution:
        res = self.solution_dao.get_solution(question_id, solution_id)
        if not res:
            raise ValueError(f"Invalid solution ID for question {question_id}")
        return res

    async def create_solution(self, question_id: str, data: SolutionCreate, id: str = None) -> str:
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

        return self.solution_dao.create_solution(question_id, solution, id)

    async def update_solution(self, question_id: str, solution_id: str, data: dict) -> Solution:
        solution = await self.get_solution(question_id, solution_id)
        solution_data = solution.model_dump()
        data.update({ "last_modified": datetime.now() })
        solution_data.update(data)
        res = Solution(**solution_data) # validate data
        self.solution_dao.update_solution(question_id, solution_id, data)
        return res

    async def delete_solution(self, question_id: str, solution_id: str):
        self.solution_dao.delete_solution(question_id, solution_id)
