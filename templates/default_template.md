# {{ data.unit_code }} Exam Feedback

## Overall Exam Performance

Below shows the basic statistics for the exam.

|                    | ALL                    | MCQs                          | Essays                            |  
|--------------------|------------------------|-------------------------------|-----------------------------------|  
| Mean               | {{ data.exam_mean }}   | {{ data.mcq_overall_mean }}   | {{ data.essay_overall_mean }}     |  
| Median             | {{ data.exam_median }} | {{ data.mcq_overall_median }} | {{ data.essay_overall_median }}   |  
| Standard Deviation | {{ data.exam_stdev }}  | {{ data.mcq_overall_stdev }}  | {{ data.essay_overall_stdev }}    |  
| Minimum            | {{ data.exam_min }}    | {{ data.mcq_overall_min }}    | {{ data.essay_overall_min }}      |  
| Maximum            | {{ data.exam_max }}    | {{ data.mcq_overall_max }}    | {{ data.essay_overall_max }}      |

The graph below shows the distrubution of marks of the exam.

<img src="{{ data.exam_distr_graph }}" width="550" height="375">

## Question Breakdown

### Automarked (MCQ) Questions

<img src="{{ data.mcq_avgs }}" width="550" height="375">

### Manually Marked Questions

<img src="{{ data.essay_avgs }}" width="550" height="375">