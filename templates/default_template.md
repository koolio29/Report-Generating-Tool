# {{ data.unit_code }} Exam Feedback

## Overall Exam Performance

Below shows the basic statistics for the exam.

{{ data.exam_stat_table }}

The graph below shows the distrubution of marks of the exam.

<img src="{{ data.distribution_graph }}" width="550" height="375">

## Question Breakdown

### Automarked (MCQ) Questions

<img src="{{ data.mcq_graph }}" width="550" height="375">

### Manually Marked Questions

<img src="{{ data.essay_graph }}" width="550" height="375">

### General Question Feedback
{% for question in data.essay_feedback %}
* __Q{{question["question_id"]}}__ mean = {{question["mean_out_of_100"]}} ({{question["mean"]}} out of {{question["outof"]}}; min = {{question["min"]}}; max = {{question["max"]}}):
<!-- Enter feedback for question {{question["question_id"]}} -->
{% endfor %}