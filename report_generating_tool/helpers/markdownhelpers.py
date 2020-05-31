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