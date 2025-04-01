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
        return self.solution_dao.get_solution(question_id, solution_id)

    async def create_solution(self, question_id: str, data: SolutionCreate, id: str = None) -> str:
        solution = data.model_dump()

        solution["language"] = solution["language"].value

        # TODO add ai analysis
        solution.update({ "ai_analysis": "" })

        creation_time = datetime.now()
        solution.update({ "created_at": creation_time, "last_modified": creation_time })

        return self.solution_dao.create_solution(question_id, solution, id)
