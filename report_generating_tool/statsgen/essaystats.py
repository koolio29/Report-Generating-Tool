import agate

from report_generating_tool.statsgen.examstats import ExamStats
from report_generating_tool.helpers import to_two_decimals

class EssayStats(ExamStats):
    """
    This class generates essay specific statistics for an agate.Table generated
    from the "simplify_agate_table" function

    Methods
    -------
    get_essay_avgs()
        gets the average marks for all essay questions in the exam

    get_individual_essay_stats()
        gets all the basic stats for all of the question in the exam
    
    max_mcq_mark()
        Get the maximum marks allocated for all of the essays
    """

    def __init__(self, agateTable):
        """
        Parameters
        ----------
        agateTable : agate.Table
            agate.Table generated from "simplify_agate_table" function
        """
        # filtering out the table just for essay questions
        self._init_table = agateTable \
            .where(lambda row: row["question_type"] == "Manual")

        self._max_essay_mark = self._init_table \
            .select(["max_marks"]) \
            .limit(1)[0]["max_marks"]

        super().__init__(self._init_table)

    def get_essay_avgs(self):
        """
        gets the average marks for all essay questions in the exam

        Returns
        -------
        dict
            contains the question id and the average marks for that question
        """
        essay_avgs_table = self._init_table \
            .group_by("question_id") \
            .aggregate([("Sum of marks", agate.Sum("marks"))]) \
            .compute([
                ("question avg",  agate.Formula(agate.Number(), 
                    lambda row: to_two_decimals(row["Sum of marks"] 
                    / self._init_table.aggregate(agate.Count("question_id", 
                    row["question_id"])) ) )
            )])

        individual_avgs = {}

        for row in essay_avgs_table:
            key = str(row["question_id"])
            value = to_two_decimals(row["question avg"])
            individual_avgs[key] = value 

        return individual_avgs

    def get_individual_essay_stats(self):
        """
        gets all the basic stats for all of the question in the exam

        Returns
        -------
        list
            A list containing a dict per essay question with basic stats
        """
        essay_stats = self._init_table \
            .select(["question_id", "max_marks", "marks"]) \
            .group_by("question_id") \
            .aggregate([
                ("min", agate.Min("marks")),
                ("max", agate.Max("marks")),
                ("sum of marks", agate.Sum("marks")),
                ("sum of max marks", agate.Sum("max_marks"))
            ]) \
            .compute([
                ("mean", agate.Formula(agate.Number(), 
                    lambda row: to_two_decimals(row["sum of marks"] 
                    / self._init_table.aggregate(agate.Count("question_id", 
                    row["question_id"])))))
            ]) \
            .compute([
                ("max_marks", agate.Formula(agate.Number(), 
                lambda row: row["sum of max marks"] 
                / self._init_table.aggregate(agate.Count("question_id", 
                row["question_id"]))))
            ]) \
            .order_by("question_id")

        stats = []

        for row in essay_stats:
            stats.append({
                "question_id" : int(row["question_id"]),
                "mean" : to_two_decimals(row["mean"]),
                "outof" : to_two_decimals(row["max_marks"]),
                "mean_out_of_100" : to_two_decimals((row["mean"] \
                                                    / row["max_marks"]) * 100),
                "min" : to_two_decimals(row["min"]),
                "max" : to_two_decimals(row["max"]),
            })

        return stats
    
    @property
    def max_essay_mark(self):
        return float(self._max_essay_mark)