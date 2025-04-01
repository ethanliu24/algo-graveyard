from typing import Any
from ..schemas.solution import Solution

class SolutionDAO:
    db: Any
    question_collection: str
    solution_collection: str

    def __init__(self, client, question_collection: str, solution_collection: str):
        self.db = client
        self.question_collection = question_collection
        self.solution_collection = solution_collection

    def get_all_solutions(self, question_id: str) -> list[Solution] | None:
        q_ref = self._question_exists(question_id)
        if not q_ref:
            return None

        sol_refs = q_ref.collection(self.solution_collection).stream()
        return [Solution(**(sol.to_dict())) for sol in sol_refs]

    def get_solution(self, question_id: str, solution_id: str) -> Solution | None:
        q_ref = self._question_exists(question_id)
        if not q_ref:
            return None
        doc = q_ref.collection(self.solution_collection).document(solution_id).get()
        return None if not doc.exists else Solution(**(doc.to_dict()))

    def create_solution(self, question_id: str, data: dict, id: str = None) -> Solution | None:
        q_ref = self._question_exists(question_id)
        if not q_ref:
            return None

        collection_ref = q_ref.collection(self.solution_collection)
        doc_ref = collection_ref.document(id) if id else collection_ref.document()

        data.update({ "id": doc_ref.id })
        doc_ref.set(data)
        return Solution(**data)

    def update_solution(self, question_id: str, solution_id: str, data: dict) -> Solution | None:
        q_ref = self._question_exists(question_id)
        if not q_ref:
            return None

        doc_ref = q_ref.collection(self.solution_collection).document(solution_id)
        doc_ref.update(data)
        return Solution(**doc_ref.get().to_dict())

    def delete_solution(self, question_id: str, solution_id: str) -> bool:
        q_ref = self._question_exists(question_id)
        if not q_ref:
            return False

        s_ref = q_ref.collection(self.solution_collection).document(solution_id)

        res = s_ref.get().exists
        s_ref.delete()
        return res

    def _question_exists(self, question_id):
        """ Checks if question exists or not. Return a doc ref of question if it exists, None ow. """
        q_ref = self.db.collection(self.question_collection).document(question_id)
        return q_ref if q_ref.get().exists else None