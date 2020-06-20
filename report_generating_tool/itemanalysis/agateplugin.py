import agate

def __filter_questions(self, should_filter):
    """
    Filter Essay questions out of the table

    Parameters
    ----------
    should_filter : Boolean
        If True, attempts to filter out essay questions

    Returns
    -------
    agate.Table
        An agate Table
    """
    return  self.where(lambda row: row["question_type"] == "Auto") \
        if should_filter else self

def difficulty(self, filter=True, in_percentage=True):
    """
    Calculates the difficulty for each item (question) given in the test

    Parameters
    ----------
    filter : Boolean, optional
        If True, it will try to filter out the agate table to get rid of essay
        questions

    in_percentage : Boolean, optional
        If True, the difficulty for the items will be returned as a percentage

    Returns
    -------
    dict 
        A dictionary containing the item number and its difficulty as a value
    """
    temp_table = __filter_questions(self, True)

    temp_table = temp_table \
        .group_by("question_id") \
        .aggregate([
            ("sum_marks", agate.Sum("marks")),
            ("sum_max_marks", agate.Sum("max_marks"))
        ]) \
        .compute([
            ("difficulty", agate.Formula(agate.Number(), 
                lambda row: row["sum_marks"] / row["sum_max_marks"]))
        ])

    difficulty_dict = {}

    for r in temp_table:
        difficulty_dict[int(r["question_id"])] = float(r["difficulty"]) * 100 \
            if in_percentage else float(r["difficulty"])

    return difficulty_dict

def discrimination(self):
    pass

def standardDeviation(self):
    pass

def standardError(self):
    pass

agate.Table.difficulty = difficulty
agate.Table.discrimination = discrimination
agate.Table.standardDeviation = standardDeviation
agate.Table.standardError = standardError