import agate

from report_generating_tool.helpers import to_two_decimals

class ExamStats:
    """
    This class is used to generate all the basic statistics for a given
    agate.Table generated from "simplify_agate_table" functions

    Methods
    -------
    mean()
        gets the mean marks of the given agate.Table (out of a 100)

    median()
        gets the median marks of the given agate.Table (out of a 100)

    min()
        gets the minimum marks of the given agate.Table (out of a 100)

    max()
        gets the maximum marks of the given agate.Table (out of a 100)
        
    stdev()
        gets the standard deviation of the given exam results in 
        the agate.Table
    """

    def __init__(self, agateTable):
        """
        Parameters
        ----------
        agateTable : agate.Table
            agate.Table generated from "simplify_agate_table" function
        """

        self._max_marks = agateTable.aggregate(agate.Sum("max_marks")) \
            / agateTable.distinct("username").aggregate(agate.Count())

        # Getting all the marks for all of the students out of a 100
        self._out_of_100_table = agateTable \
            .group_by("username") \
            .aggregate([("outof", agate.Sum("marks"))]) \
            .compute([
                ("outof100", agate.Formula(agate.Number(), 
                    lambda row: (row["outof"] / self._max_marks) * 100))
            ])

        self._mean = to_two_decimals(
            self._out_of_100_table.aggregate(agate.Mean("outof100")))

        self._median = to_two_decimals(
            self._out_of_100_table.aggregate(agate.Median("outof100")))

        self._maximum = to_two_decimals(
            self._out_of_100_table.aggregate(agate.Max("outof100")))

        self._minimum = to_two_decimals(
            self._out_of_100_table.aggregate(agate.Min("outof100")))

        self._standard_deviation = to_two_decimals(
            self._out_of_100_table.aggregate(agate.StDev("outof100")))

    @property
    def mean(self):
        return self._mean

    @property
    def median(self):
        return self._median

    @property
    def max(self):
        return self._maximum

    @property
    def min(self):
        return self._minimum

    @property
    def stdev(self):
        return self._standard_deviation