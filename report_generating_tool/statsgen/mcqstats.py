import agate

from report_generating_tool.statsgen.examstats import ExamStats
from report_generating_tool.helpers import to_two_decimals

class MCQStats(ExamStats):
    """
    This class generates MCQ specific statistics for an agate.Table generated
    from the "simplify_agate_table" function

    Methods
    -------
    get_mcq_avgs()
        gets the average marks for all mcq questions in the exam
    
    max_mcq_mark()
        Get the maximum marks allocated for all of the mcqs
    """

    def __init__(self, agateTable):
        """
        Parameters
        ----------
        agateTable : agate.Table
            agate.Table generated from "simplify_agate_table" function
        """
        # filtering out the table just for mcq questions
        self._init_table = agateTable \
            .where(lambda row: row["question_type"] == "Auto")

        self._max_mcq_mark = self._init_table \
            .select(["max_marks"]) \
            .limit(1)[0]["max_marks"]

        super().__init__(self._init_table)

    def get_mcq_avgs(self):
        """
        gets the average marks for all mcq questions in the exam

        Returns
        -------
        dict
            contains the question id and the average marks for that question
        """
        mcq_avgs_table = self._init_table \
            .group_by("question_id") \
            .aggregate([("Sum of marks", agate.Sum("marks"))]) \
            .compute([
                ("question avg", agate.Formula(agate.Number(), 
                    lambda row: to_two_decimals(row["Sum of marks"]
                    / self._init_table.aggregate(agate.Count("question_id", 
                    row["question_id"]))))
            )])

        individual_avgs = {}

        for row in mcq_avgs_table:
            key = str(row["question_id"])
            value = to_two_decimals(row["question avg"])
            individual_avgs[key] = value 

        return individual_avgs

    @property
    def max_mcq_mark(self):
        return float(self._max_mcq_mark)