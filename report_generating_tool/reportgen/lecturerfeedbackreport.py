import agate

from report_generating_tool.statsgen import OverallStats
from report_generating_tool.statsgen import MCQStats
from report_generating_tool.statsgen import EssayStats

from report_generating_tool.itemanalysis import agateplugin

from report_generating_tool.reportgen.markdowngenerator import MarkDownGenerator

from report_generating_tool.helpers import get_exam_agate_table
from report_generating_tool.helpers import simplify_agate_table
from report_generating_tool.helpers import get_file_encoding
from report_generating_tool.helpers import get_md_stats_table
from report_generating_tool.helpers import get_md_difficulty_table
from report_generating_tool.helpers import get_md_discrimination_table
from report_generating_tool.helpers import get_md_to_be_reviewed_table

class LecturerReportGenerator:
    # TODO: Docs
    def __init__(self, template_dir, template_name):
        self._template_dir = template_dir
        self._template_name = template_name

    def generate_report(self, course_id, csv_path, save_path):
        # TODO: Docs
        file_encoding = get_file_encoding(csv_path)

        exam_table = get_exam_agate_table(csv_path, 
                                            file_encoding=file_encoding)
        simplified_table = simplify_agate_table(exam_table)

        overall_stats = OverallStats(simplified_table)
        mcq_stats = MCQStats(simplified_table)
        essay_stats = EssayStats(simplified_table)

        difficulties = simplified_table.difficulty()
        discriminations = simplified_table.discrimination()

        data = {
            "unit_code" : course_id,
            "exam_stat_table" : get_md_stats_table(overall_stats, mcq_stats, 
                                                                essay_stats),
            "essay_feedback" : essay_stats.get_individual_essay_stats(),
            "mcq_difficulty_table" : get_md_difficulty_table(difficulties),
            "mcq_discrimination_table" : get_md_discrimination_table(
                discriminations
            ),
            "mcq_to_be_reviewed" : get_md_to_be_reviewed_table(
                difficulties, discriminations
            )
        }

        md_generator = MarkDownGenerator(
            save_path = save_path,
            template_dst = self._template_dir,
            template_name = self._template_name,
            md_name = f"{course_id}-lecturer_report.md",
            data = data
        )

        md_generator.generate_file()

