import markdown
from ..managers.question_manager import QuestionManager
from ..schemas.solution import Solution

class ExportManager:
    question_mamager: QuestionManager

    def __init__(self, question_mamager: QuestionManager):
        self.question_mamager = question_mamager

    async def export_question(self, question_id: str, solution_ids: list[str]):
        question = await self.question_mamager.get_question(question_id)

        solution_htmls = []
        for sln in question.solutions:
            if sln.id in solution_ids:
                sln_html = markdown.markdown(self._format_solution_md(sln))
                solution_htmls.append(sln_html)

    def _format_solution_md(self, solution: Solution):
        md = ""
        md += f"## {solution.summary} - {"Accepted" if solution.accepted else "Denied"}\n"
        md += f"Language: {solution.language.value.capitalize()}\n"
        md += f"Created at: {solution.created_at.strftime("%Y-%m-%d")}\n"
        md += f"Last modified: {solution.last_modified.strftime("%Y-%m-%d")}\n"
        md += f"\n"
        md += f"### Explanation\n"
        md += f"- Time: O({solution.time_complexity})\n- Space: O({solution.space_complexity})\n"
        md += f"{solution.explanation}\n\n"
        md += f"### AI Analysis\n\n"
        md += f"- Time: O({solution.ai_analysis.time_complexity})\n- Space: O({solution.ai_analysis.space_complexity})\n"
        md += f"{solution.ai_analysis.feedback}"
        md += f"```\n{solution.code}\n```\n\n"
        return md
