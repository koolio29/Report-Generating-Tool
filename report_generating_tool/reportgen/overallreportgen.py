from report_generating_tool.statsgen import OverallStats
from report_generating_tool.statsgen import MCQStats
from report_generating_tool.statsgen import EssayStats

from report_generating_tool.graphgen import BarGraphGenerator

from report_generating_tool.reportgen.markdowngenerator import MarkDownGenerator

from report_generating_tool.helpers import get_exam_agate_table
from report_generating_tool.helpers import simplify_agate_table
from report_generating_tool.helpers import get_max_value_from_dict
from report_generating_tool.helpers import get_file_encoding
from report_generating_tool.helpers import get_md_stats_table

class OverallReportGenerator:
    """
    This class generates an overall feedback report for the exam containing 
    basic statistics.

    Methods
    -------
    generate_report(course_id, csv_path, save_path)
        Generates the report to a given path using a given csv dataset
    """
    
    def __init__(self, template_dir, template_name):
        """
        Parameters
        ----------
        template_dir : str
            Path to the directory containing the template
        
        template_name : str
            Name of the template to use
        """
        self._template_dir = template_dir
        self._template_name = template_name

    def generate_report(self, course_id, csv_path, save_path):
        """
        Generates the lecturer specific report

        Parameters
        ----------
        course_id : str
            course id
        
        csv_path : str
            Path to the csv dataset

        save_path : str
            Path to to save the generated report
        """
        file_encoding = get_file_encoding(csv_path)

        exam_table = get_exam_agate_table(csv_path, 
                                            file_encoding=file_encoding)
        simplified_table = simplify_agate_table(exam_table)

        overall_stats = OverallStats(simplified_table)
        mcq_stats = MCQStats(simplified_table)
        essay_stats = EssayStats(simplified_table)

        overall_graph = BarGraphGenerator(save_path, "exam_distribution")
        overall_graph.generate_graph(
            data_dict = overall_stats.get_marks_distribution(),
            title = f"{course_id} Exam Distribution",
            max_y = get_max_value_from_dict(
                        overall_stats.get_marks_distribution()
                    )
        )

        mcq_graph = BarGraphGenerator(save_path, "mcq_averages")
        mcq_graph.generate_graph(
            data_dict = mcq_stats.get_mcq_avgs(),
            title = "Automated Question Averages",
            max_y = mcq_stats.max_mcq_mark
        )

        essay_graph = BarGraphGenerator(save_path, "essay_averages")
        essay_graph.generate_graph(
            data_dict = essay_stats.get_essay_avgs(),
            title = "Manually Marked Question Averages",
            max_y = essay_stats.max_essay_mark
        )

        data = {
            "unit_code" : course_id,
            "exam_stat_table" : get_md_stats_table(overall_stats, mcq_stats, 
                                                                essay_stats),
            "distribution_graph" : overall_graph.graph_name,
            "mcq_graph" : mcq_graph.graph_name,
            "essay_graph" : essay_graph.graph_name,
            "essay_feedback" : essay_stats.get_individual_essay_stats()
        }

        md_generator = MarkDownGenerator(
            save_path = save_path,
            template_dst = self._template_dir,
            template_name = self._template_name,
            md_name = f"{course_id}.md",
            data = data
        )
        
        md_generator.generate_file()