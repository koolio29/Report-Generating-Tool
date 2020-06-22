from report_generating_tool.helpers import to_two_decimals

def __get_difficulty_ranges(data):
    # TODO: Docs
    range_dict = {"<30" : 0, "30-80" : 0, "≥80" : 0}

    for key in data.keys():
        difficulty = to_two_decimals(data[key])

        if difficulty < 30:
            range_dict["<30"] += 1
        elif difficulty >= 30 and difficulty <= 80:
            range_dict["30-80"] += 1
        else:
            range_dict["≥80"] += 1
    
    return range_dict

def __get_discrimination_ranges(data):
    # TODO: Docs
    range_dict = {"<0.1" : 0, "0.1-0.39" : 0, "0.4-0.9" : 0, "1" : 0}

    for key in data.keys():
        discrimination = to_two_decimals(data[key])

        if discrimination < 0.1:
             range_dict["<0.1"] += 1
        elif discrimination >= 0.1 and discrimination <= 0.39:
            range_dict["0.1-0.39"] += 1
        elif discrimination >= 0.4 and discrimination <=0.9:
            range_dict["0.4-0.9"] += 1
        else:
            range_dict["1"] += 1
    
    return range_dict

def get_md_stats_table(overall_stats, mcq_stats, essay_stats):
    """
    Generates a markdown table string containing the exam statistics

    Parameters
    ----------
    overall_stats : OverallStats
        OverallStats instance to be used

    mcq_stats : MCQStats
        MCQstats instance to be used

    essay_stats : EssayStats
        EssayStats instance to be used

    Returns:
    --------
    str
        A string which contains a markdown table which includes exam statitics
    """

    return f"""
|        | All                    | MCQs               | Essays               |
|--------|------------------------|--------------------|----------------------|  
| Mean   | {overall_stats.mean}   | {mcq_stats.mean}   | {essay_stats.mean}   |  
| Median | {overall_stats.median} | {mcq_stats.median} | {essay_stats.median} |  
| Stdev  | {overall_stats.stdev}  | {mcq_stats.stdev}  | {essay_stats.stdev}  |  
| Min    | {overall_stats.min}    | {mcq_stats.min}    | {essay_stats.min}    |  
| Max    | {overall_stats.max}    | {mcq_stats.max}    | {essay_stats.max}    |
"""

def get_md_difficulty_table(difficulty_dict):
    # TODO: Docs
    range_dict = __get_difficulty_ranges(difficulty_dict)
    return f"""
| Number of Questions   | Difficulty Level | Percentage of Students Correct   |
|---------------------- |------------------|----------------------------------|
| {range_dict["<30"]}   | Hard             | Less than 30%                    |
| {range_dict["30-80"]}| Medium           | Between 30% to 80%               |
| {range_dict["≥80"]}   | Easy             | Greater than 80%                 |
"""

def get_md_discrimination_table(discrimination_dict):
    # TODO: Docs
    range_dict = __get_discrimination_ranges(discrimination_dict)
    return f"""
| Number of Questions      | Discrimination Types                           |
|--------------------------|------------------------------------------------|
| {range_dict["<0.1"]}     | Negative Discrimination (between -1.0 an 0.0)  |
| {range_dict["0.1-0.39"]} | Bottom threshold (between 0.10 and 0.39)       |
| {range_dict["0.4-0.9"]}  | Great discriminators (between 0.40 and 0.90)   |
| {range_dict["1"]}        | Perfectly discriminating (equal to 1.0)        |
"""

def get_md_to_be_reviewed_table(difficulty_dict, discrimination_dict):
    questions = difficulty_dict.keys()

    flagged_questions = []

    for question in questions:
        ques_diff = difficulty_dict[question]
        ques_disc = discrimination_dict[question]

        if (ques_disc < 0.1) or (ques_diff < 30 and ques_diff >= 80):
            flagged_questions.append(question)

    md_str = """
| Question Number | Difficulty | Discrimination |
|-----------------|------------|----------------|
"""

    for q in flagged_questions:
        row = f"|{q}|{difficulty_dict[q]}|{discrimination_dict[q]}|\n"
        md_str += row

    return md_str