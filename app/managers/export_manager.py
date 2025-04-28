from ..managers.question_manager import QuestionManager

class ExportManager:
    question_mamager: QuestionManager

    def __init__(self, question_mamager: QuestionManager):
        self.question_mamager = question_mamager

    async def export_question(self, question_id: str, solution_ids: list[str]):
        for i in solution_ids:
            pass
