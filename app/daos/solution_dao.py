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

    def get_all_solutions(self, question_id: str) -> list[Solution]:
        sol_refs = self.db \
            .collection(self.question_collection) \
            .document(question_id) \
            .collection(self.solution_collection) \
            .stream()

        return [Solution(**(sol.to_dict())) for sol in sol_refs]

    def get_solution(self, question_id: str, solution_id: str) -> Solution:
        doc = self.db \
            .collection(self.question_collection) \
            .document(question_id) \
            .collection(self.solution_collection) \
            .document(solution_id) \
            .get()
        return None if not doc.exists else Solution(**(doc.to_dict()))

    def create_solution(self, question_id: str, data: dict, id: str = None) -> Solution:
        collection_ref = self.db \
            .collection(self.question_collection) \
            .document(question_id) \
            .collection(self.solution_collection)
        doc_ref = collection_ref.document(id) if id else collection_ref.document()

        data.update({ "id": doc_ref.id })
        doc_ref.set(data)
        return Solution(**data)

    def update_solution(self, question_id: str, solution_id: str, data: dict) -> None:
        self.db \
            .collection(self.question_collection) \
            .document(question_id) \
            .collection(self.solution_collection) \
            .document(solution_id) \
            .update(data)

    def delete_solution(self, question_id: str, solution_id: str) -> None:
        doc_ref = self.db \
            .collection(self.question_collection) \
            .document(question_id) \
            .collection(self.solution_collection) \
            .document(solution_id) \

        res = doc_ref.get().exists
        doc_ref.delete()
        return res
