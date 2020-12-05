import agate

from report_generating_tool.statsgen.examstats import ExamStats

class OverallStats(ExamStats):
    """
    This class generates overall marks distribution for a given 
    agate.Table generated from the "simplify_agate_table" function

    Methods
    -------
    get_marks_distributions()
        Gets a dictionary containing the amount of students who fit the 
        given marks range.
    """

    def __init__(self, agateTable):
        """
        Parameters
        ----------
        agateTable : agate.Table
            agate.Table generated from "simplify_agate_table" function
        """
        super().__init__(agateTable)

    def get_marks_distribution(self):
        """
        Gets a dictionary containing the amount of students who fit the 
        given marks range.

        The marks ranges are <30, 30-40s, 50s, 60s, 70s and ≥80

        Returns
        -------
        dict
            dict containing the numbers of students in the defined mark ranges
        """
        return {
            "<30" : self._out_of_100_table.where(
                lambda row: row["outof100"] < 30).aggregate(agate.Count()),

            "30-40s" : self._out_of_100_table.where(
                lambda row: row["outof100"] >= 30 and row["outof100"] < 50) \
                    .aggregate(agate.Count()),

            "50s" :  self._out_of_100_table.where(
                lambda row: row["outof100"] >= 50 and row["outof100"] < 60) \
                    .aggregate(agate.Count()),

            "60s" :  self._out_of_100_table.where(
                lambda row: row["outof100"] >= 60 and row["outof100"] < 70) \
                    .aggregate(agate.Count()),

            "70s" :  self._out_of_100_table.where(
                lambda row: row["outof100"] >= 70 and row["outof100"] < 80) \
                    .aggregate(agate.Count()),

            "≥80" :  self._out_of_100_table.where(
                lambda row: row["outof100"] >= 80).aggregate(agate.Count())
        }