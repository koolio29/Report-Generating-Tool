# {{ data.unit_code }} - Exam Performance Feedback

## Overview

Below shows the basic statistics for the exam.

{{ data.exam_stat_table }}

## Automarked (MCQ) Questions

### Difficulty

The table below shows the summary of the MCQs difficulty.

{{ data.mcq_difficulty_table }}

### Discrimination

The table below shows a summary of discriminations for MCQ questions.

{{ data.mcq_discrimination_table}}

### Questions to be reviewed

Table below shows the MCQ questions which may need to be reviewed.

{{ data.mcq_to_be_reviewed }}

## Comments on Manually Marked (Essay) Questions
{% for question in data.essay_feedback %}
* __Question {{ question["question_id"] }}:-__ Average Marks = ({{question["mean"]}}/{{question["outof"]}})
<!-- Enter comment for question {{question["question_id"]}} -->
{% endfor %}