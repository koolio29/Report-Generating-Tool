import csv

from report_generating_tool.helpers import get_exam_agate_table
from report_generating_tool.helpers import simplify_agate_table
from report_generating_tool.helpers import to_two_decimals

from report_generating_tool.itemanalysis import agateplugin

class LecturerFeedbackCsvGenerator:
    """
    This class is used to generate csv files which contains data, such as
    difiiculty, discrimination, etc.., of questions found in a given dataset.

    Methods
    -------
    generate_csv()
        Generates a csv file
    """

    def __init__(self, csv_path, filename, save_path):
        """
        Parameters
        ----------
        csv_path : str
            Path to the input csv file

        filename : str
            Name of the csv file which will be generated

        save_path : str
            Path to save the csv file
        """
        self._working_table = simplify_agate_table(get_exam_agate_table(csv_path))
        self._abs_path = f"{save_path}/{filename}"

    def _get_question_numbers(self):
        """
        Returns all the question numbers in an exam.

        Returns
        -------
        Tuple
            A tuple containing all the question number of the agate.Table

        """
        return self._working_table.group_by("question_id").keys()

    def generate_csv(self):
        """
        Generates a csv file for the lecturer

        The csv file generated contains the following header:
        question number,difficulty,discrimination,standard deviation,standard error

        The statistics are calculated using the agate plugin
        """
        difficulties = self._working_table.difficulty()
        discriminations = self._working_table.discrimination()
        stdevs = self._working_table.standardDeviation()
        stderrs = self._working_table.standardError()

        with open(self._abs_path, "w") as file:
            headers = ["question number", "difficulty", "discrimination", 
                                    "standard deviation", "standard error"]

            file_writer = csv.writer(file, delimiter=',')
            file_writer.writerow(headers)

            all_questions = self._get_question_numbers()

            for question in all_questions:
                row = [
                    question,
                    difficulties.get(question, ""),
                    discriminations.get(question, ""),
                    stdevs.get(question, ""),
                    stderrs.get(question, "")
                ]

                file_writer.writerow(row)



