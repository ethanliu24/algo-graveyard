from datetime import datetime
from ..daos.solution_dao import SolutionDAO
from ..schemas.solution import Solution

class QuestionManager(object):
    question_dao: SolutionDAO

    def __init__(self, question_dao: SolutionDAO):
        self.question_dao = question_dao

    async def get_all_solutions(self, question_id: str) -> list[Solution]:
        return self.question_dao.get_all_solutions(question_id)

    async def get_solution(self, question_id: str, solution_id: str) -> Solution:
        return self.question_dao.get_solution(question_id, solution_id)
