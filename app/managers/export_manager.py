import markdown
from io import BytesIO
from weasyprint import HTML, CSS
from ..schemas.question import Question
from ..schemas.solution import Solution

class ExportManager:
    async def export_question(self, question: Question, solution_ids: list[str]) -> BytesIO:
        html = ""
        html += markdown.markdown(self._format_question_md(question))
        html += "# Solutions"

        for sln in question.solutions:
            if sln.id in solution_ids:
                sln_html = markdown.markdown(self._format_solution_md(sln))
                html += sln_html

        html = html.replace("```", "")

        pdf = BytesIO()
        HTML(string=html).write_pdf(pdf, stylesheets=[CSS("app/templates/export.css")])
        pdf.seek(0)
        return pdf

    def _format_question_md(self, question: Question) -> str:
        md = ""
        md += f"# {question.title} - {question.status.value.capitalize()}\n"
        md += f"Difficulty: {question.difficulty.value.capitalize()}\n\n"
        md += f"{question.source.value.capitalize()}: [{question.link}]({question.link})\n\n"
        md += f"Created at: {question.created_at.strftime("%Y-%m-%d")}\n\n"
        md += f"Created at: {question.created_at.strftime("%Y-%m-%d")}\n\n"
        md += f"### Description:\n"
        md += f"{question.prompt}\n\n"

        if question.notes:
            md += f"### Notes\n"
            md += f"{"\n".join([f"- {note}" for note in question.notes])}\n\n"

        if question.hints:
            md += f"### Hints\n"
            md += f"{"\n".join([f"- {hint}" for hint in question.hints])}\n\n"

        if question.tags:
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
        md += f"- Time: O({solution.ai_analysis.time_complexity})\n- Space: O({solution.ai_analysis.space_complexity})\n\n"
        md += f"{solution.ai_analysis.feedback}\n\n"
        md += f"```{solution.code}```\n\n"
        return md
