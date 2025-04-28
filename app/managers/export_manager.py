import markdown
from ..managers.question_manager import QuestionManager
from ..schemas.question import Question
from ..schemas.solution import Solution

class ExportManager:
    question_mamager: QuestionManager

    def __init__(self, question_mamager: QuestionManager):
        self.question_mamager = question_mamager

    async def export_question(self, question_id: str, solution_ids: list[str]):
        question = await self.question_mamager.get_question(question_id)

        html = ""
        html += markdown.markdown(self._format_question_md(question))

        solution_htmls = []
        for sln in question.solutions:
            if sln.id in solution_ids:
                sln_html = markdown.markdown(self._format_solution_md(sln))
                solution_htmls.append(sln_html)

    def _format_question_md(self, question: Question) -> str:
        md = ""
        md += f"# {question.title} - {question.status.value.capitalize()}\n"
        md += f"Difficulty: {question.difficulty.value.capitalize()}\n"
        md += f"{question.source.value.capitalize()}: [{question.link}]({question.link})\n"
        md += f"Created at: {question.created_at.strftime("%Y-%m-%d")}\n"
        md += f"Created at: {question.created_at.strftime("%Y-%m-%d")}\n"
        md += f"\n"
        md += f"{question.prompt}\n\n"
        md += f"### Notes\n"
        md += f"{"\n".join([f"- {note}" for note in question.notes])}\n\n"
        md += f"### Hints\n"
        md += f"{"\n".join([f"- {hint}" for hint in question.hints])}\n\n"
        md += f"### Tags\n"
        md += f"{", ".join([tag.value for tag in question.tags])}\n\n"
        return md

    def _format_solution_md(self, solution: Solution) -> str:
        md = ""
        md += f"## {solution.summary} - {"Accepted" if solution.accepted else "Denied"}\n"
        md += f"Created at: {solution.created_at.strftime("%Y-%m-%d")}\n"
        md += f"Last modified: {solution.last_modified.strftime("%Y-%m-%d")}\n"
        md += f"Language: {solution.language.value.capitalize()}\n"
        md += f"\n"
        md += f"### Explanation\n"
        md += f"- Time: O({solution.time_complexity})\n- Space: O({solution.space_complexity})\n"
        md += f"{solution.explanation}\n\n"
        md += f"### AI Analysis\n\n"
        md += f"- Time: O({solution.ai_analysis.time_complexity})\n- Space: O({solution.ai_analysis.space_complexity})\n"
        md += f"{solution.ai_analysis.feedback}"
        md += f"```\n{solution.code}\n```\n\n"
        return md
