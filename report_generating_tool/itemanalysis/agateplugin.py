import math

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

def difficulty(self, filter_items=True, in_percentage=True):
    """
    Calculates the difficulty for each item (question) given in the test.  This
    can be only done on MCQ questions.

    Parameters
    ----------
    filter_items : Boolean, optional
        If True, it will try to filter out the agate table to get rid of essay
        questions

    in_percentage : Boolean, optional
        If True, the difficulty for the items will be returned as a percentage

    Returns
    -------
    dict 
        A dictionary containing the item number and its difficulty as a value
    """
    temp_table = __filter_questions(self, filter_items)

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

def discrimination(self, filter_items=True):
    """
    Calculates discrimination for all items in the exam. This can be only done
    on MCQ questions.

    Parameters
    ----------
    filter_items : Boolean, optional
        If True, it will try to filter out the agate table to get rid of essay
        questions

    Returns
    -------
    dict 
        A dictionary containing the item number and its discrimination value
    """
    working_table = __filter_questions(self, filter_items)

    # Step 1: order students total marks in ascending order
    step_one_table = working_table \
        .group_by("username") \
        .aggregate([
            ("total_marks", agate.Sum("marks"))
        ]) \
        .order_by("total_marks")

    # Step 2: extract the upper and lower 27% of students
    total_students = step_one_table.aggregate(agate.Count("username"))
    student_limit = (27 * total_students) // 100

    lower_table = step_one_table.limit(student_limit)
    upper_table = step_one_table \
        .order_by("total_marks", reverse=True) \
        .limit(student_limit)

    lower_students = []
    upper_students = []

    for row in lower_table:
        lower_students.append(str(row["username"]))

    for row in upper_table:
        upper_students.append(str(row["username"]))

    lower_table = working_table \
        .where(lambda row: row["username"] in lower_students)
    upper_table = working_table \
        .where(lambda row: row["username"] in upper_students)

    # Step 3: get item difficulty for upper and lower 27% of students
    lower_difficulty = difficulty(lower_table, filter_items=False, 
                                                        in_percentage=False)
    upper_difficulty = difficulty(upper_table, filter_items=False, 
                                                        in_percentage=False)

    # Step 4: subtract lower difficulty from upper difficulty
    discrimination_dict = {}

    for k in lower_difficulty.keys():
        discrimination_dict[k] = upper_difficulty[k] - lower_difficulty[k]

    return discrimination_dict

def standardDeviation(self):
    """
    Calculates standard deviation for all of the items in the exam

    Returns
    -------
    dict
        A dictionary containing the question numbers and its standard deviation
    """
    working_table = self \
        .group_by("question_id") \
        .aggregate([
            ("stdev", agate.StDev("marks"))
        ])

    stdev_dict = {}

    for row in working_table:
        stdev_dict[str(row["question_id"])] = float(row["stdev"])

    return stdev_dict

def standardError(self):
    working_table = self \
        .group_by("question_id") \
        .aggregate([
            ("stdev", agate.StDev("marks")),
            ("question_count", agate.Count())
        ]) \
        .compute([
            ("stderr", agate.Formula(agate.Number(),
                lambda row: float(row["stdev"]) 
                / math.sqrt(float(row["question_count"]))))
        ])

    stderr_dict = {}

    for row in working_table:
        stderr_dict[str(row["question_id"])] = float(row["stderr"])

    return stderr_dict

agate.Table.difficulty = difficulty
agate.Table.discrimination = discrimination
agate.Table.standardDeviation = standardDeviation
agate.Table.standardError = standardError